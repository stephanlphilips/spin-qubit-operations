from pulse_templates.utility.template_wrapper import template_wrapper 
from pulse_templates.utility.oper import add_block, add_ramp

from pulse_lib.segments.utility.looping import loop_obj
from dataclasses import dataclass, field
from typing import Union
import copy


@dataclass
class single_qubit_gate_spec:
    '''
    Args:
        qubit_name : name of the virtual qubit channel
        f_qubit : frequency at which you want to drive the qubit
        t_pulse : time of the pulse
        MW_power : voltage to apply on the I and Q channels
        phase : phase of the current MW
        permanent_phase_shift : permanent phase shift to introduce after the gate
    '''
    qubit_name : str
    f_qubit : Union[float, loop_obj]
    t_pulse : Union[float, loop_obj]
    MW_power : Union[float, loop_obj]
    phase : Union[float, loop_obj] = 0 
    permanent_phase_shift : Union[float, loop_obj] = 0
    padding : Union[float, int] = 1 #left right padding around the MW pulse in ns
    AM_mod : any = None
    PM_mod : any = None
    phase_corrections : dict = field(default_factory=dict)
    _segment_generator : any = None

    def add(self, segment=None, reset=True, **kwargs):
        '''
        adds itselves to a segment

        Args:
            segment (segment_container) : segement where to add the gate to.
        '''
        if segment is None and self._segment_generator is None:
            raise ValueError('no segment privided')
        if segment is None:
            segment = self._segment_generator.generate_segment()

        cpy = copy.copy(self)
        if len(kwargs) > 0:
            for key, value in kwargs.items():
                if key not in self.__dict__.keys():
                    raise ValueError(f'invalid keyword argument detected for single_qubit_gate_spec, {key}, options are {list(self.__dict__.keys())}')
                setattr(cpy, key, value)

        single_qubit_gate_simple(segment, cpy, reset=reset)

        for qubit_name, permanent_phase_shift in cpy.phase_corrections.items():
            seg_qubit = getattr(segment, qubit_name)
            seg_qubit.add_global_phase(permanent_phase_shift) 

    def __call__(self, angle):
        '''
        fuction that allows for easy mod of the object:

        Args:
            angle (double) : angle to rotate
        '''
        cpy = copy.copy(self)

        if self.t_pulse == 0 or self.MW_power==0:
            cpy.permanent_phase_shift = angle

        cpy.phase += angle
        return cpy

    def copy(self):
        copy = single_qubit_gate_spec(self.qubit_name, copy.deepcopy(f_qubit), copy.deepcopy(t_pulse), copy.deepcopy(MW_power), 
            copy.deepcopy(phase) ,copy.deepcopy(permanent_phase_shift) ,copy.deepcopy(padding))
        copy.AM_mod = self.AM_mod
        copy.PM_mod = self.PM_mod
        copy._segment_generator = self._segment_generator

        return copy

class gate_sequence_spec:
    '''
    concatened set of single_qubit_gate_spec's
    '''
    def __init__(self, gates=[]):
        self.gates = gates
        self._phase = 0
        self._permanent_phase_shift = 0

    def __add__(self, other):
        if isinstance(other, single_qubit_gate_spec):
            self.gates.append(other)
        elif isinstance(other, gate_sequence_spec):
            self.gates += other.gates
        else:
            raise ValueError('invalid input provided.')
        return self

    @property
    def phase(self):
        return self._phase

    @phase.setter
    def phase(self, value):
        for gate in self.gates:
            gate.phase += value
        self._phase += value

    @property
    def permanent_phase_shift(self):
        return self._permanent_phase_shift

    @phase.setter
    def permanent_phase_shift(self, value):
        for gate in self.gates:
            gate.permanent_phase_shift += value
        self._permanent_phase_shift += value


    def add(self, segment=None, reset=True, **kwargs):
        for gate in self.gates:
            gate.add(segment, reset, **kwargs)

    def copy(self):
        copy_set = []
        for gate in self.gates:
            copy_set.append(copy.copy(gate))
        return gate_sequence_spec(copy_set)

    def __call__(self, angle):
        copy_set = copy.copy(self)
        for i in range(len(copy_set.gates)):
            copy_set.gates[i] = copy_set.gates[i](angle)
        return copy_set

    def __repr__(self):
        info = 'sigle qubit gate collection :\n'
        for gate in self.gates:
            info += '\t' + str(gate) + '\n'
        return info

    def __iter__(self):
        self.__nth_iter = 0
        return self

    def __next__(self):
        if self.__nth_iter < len(self.gates):
            self.__nth_iter += 1
            return self.gates[self.__nth_iter-1]
        else:
          raise StopIteration

# @template_wrapper
def single_qubit_gate_simple(segment, gate_object,**kwargs):
    '''
    add a single qubit gate

    Args:
        segment (segment_container) : segment to which to add this stuff
        gate_object (single_qubit_gate_spec) : gate object describing the microwave pulse
        padding (double) : padding that needs to be put around the microwave (value added at each side).
    '''
    if isinstance(gate_object, gate_sequence_spec):
        for gate in gate_object:
            single_qubit_gate_simple(segment, gate, **kwargs)
    else:
        _load_single_qubit_gate(getattr(segment, gate_object.qubit_name), gate_object, **kwargs)
        segment.reset_time()


def _load_single_qubit_gate(segment, gate_object,**kwargs):
    '''
    add a single qubit gate on a segment (NOT SEGMENT_container)

    Args:
        segment (segment) : segment to which to add this stuff
        gate_object (single_qubit_gate_spec) : gate object describing the microwave pulse
        padding (double) : padding that needs to be put around the microwave (value added at each side).
    '''
    if isinstance(gate_object, gate_sequence_spec):
        for gate in gate_object:
            _load_single_qubit_gate(segment, gate, **kwargs)
    else:
        if gate_object.t_pulse != 0 and gate_object.MW_power!=0:
            segment.add_MW_pulse(gate_object.padding, gate_object.t_pulse + gate_object.padding, gate_object.MW_power, gate_object.f_qubit, gate_object.phase ,  gate_object.AM_mod,  gate_object.PM_mod)
            segment.reset_time()
            segment.wait(gate_object.padding)
        segment.add_global_phase(gate_object.permanent_phase_shift)

        if 'reset' in kwargs:
            if kwargs['reset'] == True:
                segment.reset_time()
        else:
            segment.reset_time()

if __name__ == '__main__':
    from pulse_templates.utility.plotting import plot_seg
    from pulse_templates.demo_pulse_lib.virtual_awg import get_demo_lib
    from pulse_lib.segments.utility.looping import linspace
    from pulse_templates.oper.operators import wait
    pulse = get_demo_lib('six')
    seg = pulse.mk_segment()

    gates = ('vP4',)
    base_level = (0,)
    # seg.vP4 += 10
    qubit = 'qubit4_MW'
    t_drive = 1000
    amp = 10
    freq = 200e8
    padding = 10
    Q4_Pi2 = single_qubit_gate_spec(qubit, freq, t_drive, amp, AM_mod='flattop', phase_corrections={'qubit2_MW' : 0.23})

    # # T2* measurement
    single_qubit_gate_simple(seg, Q4_Pi2, reset=False)

    wait(seg, gates, linspace(10,100), base_level)
    # shorthand syntax
    Q4_Pi2.add(seg, reset=True)
    wait(seg, gates, 80, base_level)
    # shorthand syntax
    Q4_Pi2.add(seg, reset=True, MW_power = 200)
    wait(seg, gates, 80, base_level)
    Q4_Pi2.add(seg, reset=True)
    plot_seg(seg)
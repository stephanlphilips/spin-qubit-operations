from pulse_templates.utility.segment_manager import segment_mgr
from dataclasses import dataclass
import inspect
import copy

def unwrap(func):
    while hasattr(func, '__wrapped__'):
        func = func.__wrapped__
    return func

@dataclass
class two_qubit_gate_generic:
    '''
    class describing a generic two qubit gate

    Args:
        shaping_function (func)  : function that has as first input a segment and returns a segment.
        pulse_kwargs (dict)      : arguments for the function that are not the segment.
        phase_corrections (dict) : phase correction that have to be added to the microwave channels afeter execution of the two qubit gate
    '''
    shaping_function : any
    pulse_kwargs : dict
    phase_corrections : dict
    _segment_generator : segment_mgr = None

    def add(self, segment=None, **kwargs):
        if segment is None and self._segment_generator is None:
            raise ValueError('no segment privided')
        if segment is None:
            segment = self._segment_generator.generate_segment()

        all_kwargs  = copy.copy(self.pulse_kwargs)
        valid_kwargs = inspect.getfullargspec(unwrap(self.shaping_function))[0] + ['phase_corrections']
        for key, value in kwargs.items():
            if key not in valid_kwargs:
                raise ValueError(f'Bad keyword detected ({key}) in two qubit descriptor. Accepected keywords are : {valid_kwargs}')
            if key == 'phase_corrections':
                self.phase_corrections = value
            else:
                all_kwargs[key] = value

        self.shaping_function(segment, **all_kwargs)

        for qubit_name, permanent_phase_shift in self.phase_corrections.items():
            seg_qubit = getattr(segment, qubit_name)
            seg_qubit.add_global_phase(permanent_phase_shift)

        segment.reset_time()

        return segment

class gate_collection:
    def __init__(self):
        self.collection  = []
    
    def __add__(self, other):
        if isinstance(other, (tuple, list)):
            for i in other:
                self.collection.append(i)
        else:
            self.collection.append(other)

        return self

    def add(self, segment=None, **kwargs):
        for instruction in self.collection:
            if isinstance(instruction, two_qubit_gate_generic):
                instruction.add(segment, **kwargs)
            else:
                instruction.add(segment)
        return segment


class two_qubit_gate_descriptor:
    def __init__(self, *args):
        self.reference_gates = args

    def __set_name__(self, owner, name):
        self.name = name
        self.private_name = '_' + name

    def __set__(self, obj, gate_specification):
        if isinstance(gate_specification, two_qubit_gate_generic):
            setattr(gate_specification, '_segment_generator', getattr(obj, 'segment_generator'))
            setattr(obj, self.private_name, gate_specification)
        else: 
            raise ValueError('bad two qubit gate descriptor provided, please use the two_qubit_gate_generic class')

    def __get__(self, obj, objtype=None):
        if hasattr(obj, self.private_name):
            return getattr(obj, self.private_name)
        else:
            if len(self.reference_gates) == 0:
                raise ValueError(f'The gate {self.name} is not yet defined, please it in your standard set.')
            
            gates_to_do = gate_collection()
            for gate in self.reference_gates:
                gate_comp = gate.split('_')
                if len(gate_comp) == 1:
                    gates_to_do += getattr(obj, gate)
                else: # single_qubit gate
                    qubit_1 = getattr(obj, '_q1')
                    qubit_2 = getattr(obj, '_q2')
                    gates_to_do += getattr(qubit_1, gate_comp[0])
                    gates_to_do += getattr(qubit_2, gate_comp[1])
            return gates_to_do

class two_qubit_std_set:
    cphase     = two_qubit_gate_descriptor()
    CNOT12     = two_qubit_gate_descriptor('X_I', 'cphase', 'X_I')
    CNOT21     = two_qubit_gate_descriptor('I_X', 'cphase', 'I_X')    
    CROT12     = two_qubit_gate_descriptor()
    zCROT12     = two_qubit_gate_descriptor()
    CROT21     = two_qubit_gate_descriptor()
    zCROT21     = two_qubit_gate_descriptor()    
    SWAP       = two_qubit_gate_descriptor('CNOT21', 'CNOT12', 'CNOT21')
    iSWAP      = two_qubit_gate_descriptor('CNOT21', 'CNOT12', 'CNOT21', 'cphase')
    sqrt_swap  = two_qubit_gate_descriptor()
    sqrt_iswap = two_qubit_gate_descriptor()

    def __init__(self, q1, q2, segment_generator=None):
        self._q1 = q1
        self._q2 = q2
        self.segment_generator = segment_generator


if __name__ == '__main__':
    from pulse_templates.utility.plotting import plot_seg
    from pulse_templates.demo_pulse_lib.virtual_awg import get_demo_lib
    from pulse_templates.oper.operators import wait

    from pulse_templates.coherent_control.single_qubit_gates.single_qubit_gates import single_qubit_gate_spec
    from pulse_templates.coherent_control.single_qubit_gates.standard_set import single_qubit_std_set

    from pulse_templates.coherent_control.two_qubit_gates.cphase import cphase_basic
    from pulse_templates.utility.segment_manager import segment_mgr
    pulse = get_demo_lib('six')
    seg = pulse.mk_segment()
    ss = segment_mgr(pulse)
    gates = ('vP1','vB1', 'vP2')
    base_level = (0,0,0)
    

    # example -- make cphase spec
    cphase12 = two_qubit_gate_generic(cphase_basic, {'gates' : gates, 
                                    'v_exchange_pulse_off' : (0,4,0),
                                    'v_exchange_pulse_on' : (0,8,0),
                                    't_gate' : 100,
                                    't_ramp' : 20},
                 {'qubit1_MW' : 0.23, 'qubit2_MW' : 0.8})

    # make two sinle qubit gates sets
    qubit_1 = single_qubit_std_set(ss)
    qubit_1.X = single_qubit_gate_spec('qubit1_MW', 1e9, 100, MW_power=5)

    qubit_2 = single_qubit_std_set(ss)
    qubit_2.X = single_qubit_gate_spec('qubit2_MW', 1e9, 100, MW_power=5)

    two_qubit_gate_spec = two_qubit_std_set(qubit_1, qubit_2, ss)
    two_qubit_gate_spec.cphase = cphase12

    # composite gate
    two_qubit_gate_spec.CNOT12.add(v_exchange_pulse_on = (0,12,0))

    wait(seg, gates, 250, base_level)
    
    # single gate
    two_qubit_gate_spec.cphase.add(t_gate=200, phase_corrections={'qubit1_MW': 0.25})

    wait(seg, gates, 250, base_level)
    
    # composite gate
    two_qubit_gate_spec.SWAP.add()

    # plot_seg(ss.segments)

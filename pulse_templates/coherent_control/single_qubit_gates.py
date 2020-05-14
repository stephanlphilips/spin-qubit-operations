from pulse_templates.utility.template_wrapper import template_wrapper 
from pulse_templates.utility.oper import add_block, add_ramp

from pulse_lib.segments.utility.looping import loop_obj
from dataclasses import dataclass
from typing import Union
from collections import OrderedDict

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
    AM_mod : any = None
    PM_mod : any = None


# TODO generic one for multiple single qubit gates
@template_wrapper
def single_qubit_gate_simple(segment, gate_object, padding = 1,**kwargs):
    '''
    add a single qubit gate

    Args:
        segment (segment_container) : segment to which to add this stuff
        gate_object (single_qubit_gate_spec) : gate object describing the microwave pulse
        padding (double) : padding that needs to be put around the microwave (value added at each side).
    '''
    _load_single_qubit_gate(getattr(segment, gate_object.qubit_name), gate_object, padding)
    segment.reset_time()


def _load_single_qubit_gate(segment, gate_object, padding = 1,**kwargs):
    '''
    add a single qubit gate on a segment (NOT SEGMENT_container)

    Args:
        segment (segment) : segment to which to add this stuff
        gate_object (single_qubit_gate_spec) : gate object describing the microwave pulse
        padding (double) : padding that needs to be put around the microwave (value added at each side).
    '''
    if gate_object.t_pulse > 0:
        segment.add_MW_pulse(padding, gate_object.t_pulse + padding, gate_object.MW_power, gate_object.f_qubit, gate_object.phase ,  gate_object.AM_mod,  gate_object.PM_mod)
        segment.reset_time()
        segment.wait(padding)
    segment.add_global_phase(gate_object.permanent_phase_shift)
    segment.reset_time()


if __name__ == '__main__':
    from pulse_templates.utility.plotting import plot_seg
    from pulse_templates.demo_pulse_lib.virtual_awg import get_demo_lib
    from pulse_lib.segments.utility.looping import linspace
    from pulse_templates.oper.operators import wait
    pulse = get_demo_lib('quad')
    seg = pulse.mk_segment()

    gates = ('vP4',)
    base_level = (10,)
    # seg.vP4 += 10
    qubit = 'qubit4_MW'
    t_drive = 100
    amp = 10
    freq = 200e8
    padding = 10
    Q4_Pi2 = single_qubit_gate_spec(qubit, freq, t_drive, amp)
    # # T2* measurement
    single_qubit_gate_simple(seg, Q4_Pi2)
    wait(seg, gates, linspace(10,100), base_level)
    # # might be useful to add here extra phase if the qubit freq is not defined.
    single_qubit_gate_simple(seg, Q4_Pi2)
    plot_seg(seg)
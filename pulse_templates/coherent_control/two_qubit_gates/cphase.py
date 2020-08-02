from pulse_templates.utility.template_wrapper import template_wrapper 
from pulse_templates.utility.oper import add_block, add_ramp


@template_wrapper
def cphase_basic(segment, gates, v_exchange_pulse_off, v_exchange_pulse_on, t_gate, t_ramp):
    '''
    basic cphase, with a linear ramp

    Args:
        segment (segment_container) : segment to which to add this stuff
        barrier (str) : barrier to pulse
        v_exchange_pulse (double) : voltage to pulse to
        t_gate (double) : total time of the gate not inclusing the ramps
        t_ramp (double) : ramp time
    '''

    add_ramp(segment, t_ramp, gates, v_exchange_pulse_off, v_exchange_pulse_on)
    add_block(segment, t_gate, gates, v_exchange_pulse_on)
    add_ramp(segment, t_ramp, gates, v_exchange_pulse_on, v_exchange_pulse_off)


if __name__ == '__main__':
    from pulse_templates.utility.plotting import plot_seg
    from pulse_templates.demo_pulse_lib.virtual_awg import get_demo_lib
    from pulse_lib.segments.utility.looping import linspace
    from pulse_templates.oper.operators import wait
    pulse = get_demo_lib('quad')
    seg = pulse.mk_segment()

    gates = ('vP1','vB1', 'vP2')
    base_level = (0,0,0)
    # seg.vP4 += 10
    wait(seg, gates, 100, base_level)
    import numpy as np
    t = linspace(0,50, 50, setvals=np.linspace(0,20,50))
    cphase_basic(seg, gates, (0,4,0), (0,8,0), t, 10)
    plot_seg(seg)   
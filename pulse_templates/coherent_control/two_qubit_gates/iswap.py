from pulse_templates.utility.template_wrapper import template_wrapper 
from pulse_templates.utility.oper import add_block, add_ramp


@template_wrapper
def iswap_basic(segment, gates, barrier_gate,v_exchange_pulse_off, v_exchange_pulse_on, v_ac, f_ac, t_gate, t_ramp, padding = 2):
    '''
    basic cphase, with a linear ramp

    Args:
        segment (segment_container) : segment to which to add this stuff
        gates (tuple<str>) : gates to be pulses for this gate.
        barrier_gate (str) : barrier to pulse (for the ac)
        v_exchange_pulse (double) : voltage to pulse to
        t_gate (double) : total time of the gate not inclusing the ramps
        t_ramp (double) : ramp time
    '''
    add_ramp(segment, t_ramp, gates, v_exchange_pulse_off, v_exchange_pulse_on)
    
    add_block(segment, padding, gates, v_exchange_pulse_on)
    for gate, level in zip(gates, v_exchange_pulse_on):
        getattr(segment, gate).add_block(0, t_gate, level)
    getattr(segment, barrier_gate).add_sin(0, t_gate, v_ac, f_ac)
    segment.reset_time()
    add_block(segment, padding, gates, v_exchange_pulse_on)

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
    iswap_basic(seg, gates, 'vB1' ,(0,4,0), (0,8,0), 2, 1e8, 100, 10)
    plot_seg(seg)   
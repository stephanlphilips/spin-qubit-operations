'''
simple operators for pulses

Pulses
    * add_stage : add stage level to pulse
	* jump : jump from point a to point b
	* wait : wait for a certain time at a point.

'''
from pulse_templates.utility.template_wrapper import template_wrapper 
from pulse_templates.utility.oper import add_block, add_ramp

@template_wrapper
def ramp(segment, gates, t_ramp, p_0, p_1, reset_time=True, **kwargs):
    '''
    ramp from p_0 to p_1 for time t_ramp

    Args:
        segment (segment_container) : segment to which to add this stuff
        gates (tuple<str>) : plunger gate names
        t_ramp (double) : time to ramp from point 0 to point 1
        p_0 (tuple <double>) : point where to start
        p_1 (tuple <double>) : point where to end.
    '''
    add_ramp(segment, t_ramp, gates, p_0, p_1, reset_time)

@template_wrapper
def jump(segment, gates, t_ramp, p_0, p_1, reset_time=True, **kwargs):
    '''
    deperacted, use ramp instead.

    Args:
        segment (segment_container) : segment to which to add this stuff
        gates (tuple<str>) : plunger gate names
        t_ramp (double) : time to ramp from point 0 to point 1
        p_0 (tuple <double>) : point where to start
        p_1 (tuple <double>) : point where to end.
    '''
    add_ramp(segment, t_ramp, gates, p_0, p_1, reset_time)


@template_wrapper
def wait(segment, gates, t_wait, p_0, reset_time=True,**kwargs):
    '''
    wait at p_0 for t_wait

    Args:
        segment (segment_container) : segment to which to add this stuff
        gates (tuple<str>) : plunger gate names
        t_wait (double) : time to wait at p_0
        p_0 (tuple <double>) : point where to wait at
    '''
    add_block(segment, t_wait, gates, p_0, reset_time)


@template_wrapper
def add_stage(segment, gates, p_0, **kwargs):
    '''
    add stage level for the pulse (= default operating point)

    Args:
        segment (segment_container) : segment to which to add this stuff
        gates (tuple<str>) : plunger gate names
        p_0 (tuple <double>) : points for the stage
    '''
    wait(segment, gates, -1, p_0, **kwargs)

def wait_jump_wait(seg, gates, t_wait, t_jump, state_1, state_2, debug=False):
    wait(seg, gates, t_wait, state_1, debug=debug)
    ramp(seg, gates, t_jump, state_1, state_2)
    wait(seg, gates, t_wait, state_2)


def ramp_through_anticorssing(gates_to_jump, jump, center_position, gates):
    start = list(center_position)
    stop = list(center_position)

    for gate_idx in range(len(gates_to_jump)):
        start[gates.index(gates_to_jump[gate_idx])] += -jump[gate_idx]
        stop[gates.index(gates_to_jump[gate_idx])] += jump[gate_idx]

    return tuple(start), tuple(stop)


if __name__ == '__main__':
    from pulse_templates.utility.plotting import plot_seg
    from pulse_templates.demo_pulse_lib.virtual_awg import get_demo_lib
    
    pulse = get_demo_lib('quad')
    seg = pulse.mk_segment()

    gates = ('vP1', 'vP2')
    
    p_0 = (0, 0)
    p_1 = (5, 0)
    seg.P1  += 1
    seg.vP1 += 5 

    jump(seg, gates, 1000, p_0, p_1)
    wait(seg, gates, 2000, p_1)
    
    plot_seg(seg)
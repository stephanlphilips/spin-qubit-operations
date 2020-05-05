'''
simple operators for pulses

Pulses
	* jump : jump from point a to point b
	* wait : wait for a certain time at a point.

'''
from pulse_templates.utility.template_wrapper import template_wrapper 
from pulse_templates.utility.oper import add_block, add_ramp

@template_wrapper
def jump(segment, gates, t_ramp, p_0, p_1, **kwargs):
    '''
    wait at p_0

    Args:
        segment (segment_container) : segment to which to add this stuff
        gates (tuple<str>) : plunger gate names
        t_ramp (double) : time to ramp from point 0 to point 1
        p_0 (tuple <double>) : point where to start
        p_1 (tuple <double>) : point where to end.
    '''
    # wait at this spot..
    add_ramp(segment, t_ramp, gates, p_0, p_1)


@template_wrapper
def wait(segment, gates, t_wait, p_0, **kwargs):
    '''
    wait at p_0

    Args:
        segment (segment_container) : segment to which to add this stuff
        gates (tuple<str>) : plunger gate names
        t_wait (double) : time to wait at p_0
        p_0 (tuple <double>) : point where to wait at
    '''
    # wait at this spot..
    add_block(segment, t_wait, gates, p_0)

if __name__ == '__main__':
    from pulse_templates.utility.plotting import plot_seg
    from pulse_templates.demo_pulse_lib.virtual_awg import get_demo_lib
    
    pulse = get_demo_lib('quad')
    seg = pulse.mk_segment()

    gates = ('P1', 'P2')
    
    p_0 = (-7, -4)
    p_1 = (-5, -4)
    jump(seg, gates, 1000, p_0, p_1)
    wait(seg, gates, 2000, p_1)
    
    plot_seg(seg)
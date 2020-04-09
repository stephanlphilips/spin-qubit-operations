'''
Readout pulse templates for PSB.

Pulses:
    * psb_read : native readout function for readout at the anticrossing
    * psb_read_latched : readout function to use in case you want to make use of latching mechanisms

'''
from pulse_templates.utility.template_wrapper import template_wrapper 

@template_wrapper
def PSB_read(segment, gates, t_ramp, t_read, p_0, p_1, disable_trigger=False):
    '''
    pulse able to perform a psb readout

    Args:
        segment (segment_container) : segment to which to add this stuff
        gates (tuple<str>) : plunger gate names
        t_ramp (double) : time to linearly ramp trought the anticrossing
        t_read (double) : readout time
        p_0 (tuple <double>) : starting point
        p_1 (tuple<double>) : point after the anticrossing, where the readout should happen.
        disable_trigger (bool) : disable triggerig for digitizer, only for debuggig.
    '''

    P1, P2 = gates

    # jump close to (1,1) -- (2,0) wait 100 ns
    getattr(segment, P1).add_block(0, 100, p_0[0])
    getattr(segment, P2).add_block(0, 100, p_0[1])
    segment.reset_time()

    # pulse towards the window and stay for the measurment time
    getattr(segment, P1).add_ramp_ss(0, t_ramp, p_0[0], p_1[0])
    getattr(segment, P2).add_ramp_ss(0, t_ramp, p_0[1], p_1[1])
    segment.reset_time()

    if disable_trigger == False:
        getattr(segment, P1).add_HVI_marker("dig_wait")
        getattr(segment, P1).add_HVI_variable("t_measure", t_read)

    getattr(segment, P1).add_block(0, t_read, p_1[0])
    getattr(segment, P2).add_block(0, t_read, p_1[1])
    segment.reset_time()

@template_wrapper
def PSB_read_latched(segment, gates, t_ramp, t_read, p_0, p_1, p_2, disable_trigger=False):
    '''
    pulse able to perform a psb readout

    Args:
        segment (segment_container) : segment to which to add this stuff
        gates (tuple<str>) : plunger gate names
        t_ramp (double) : time to linearly ramp trought the anticrossing
        t_read (double) : readout time
        p_0 (tuple <double>) : starting point
        p_1 (tuple <double>) : point after the anticrossing
        p_2 (tuple <double>) : effective point where the averaging should happen
        disable_trigger (bool) : disable triggerig for digitizer, only for debuggig.
    '''

    P1, P2 = gates

    # jump close to (1,1) -- (2,0) wait 100 ns
    getattr(segment, P1).add_block(0, 100, p_0[0])
    getattr(segment, P2).add_block(0, 100, p_0[1])
    segment.reset_time()

    # pulse towards the window and stay for the measurment time
    getattr(segment, P1).add_ramp_ss(0, t_ramp, p_0[0], p_1[0])
    getattr(segment, P2).add_ramp_ss(0, t_ramp, p_0[1], p_1[1])
    segment.reset_time()

    getattr(segment, P1).add_ramp_ss(0, 10, p_1[0], p_2[0])
    getattr(segment, P2).add_ramp_ss(0, 10, p_1[1], p_2[1])
    segment.reset_time()

    if disable_trigger == False:
        getattr(segment, P1).add_HVI_marker("dig_wait")
        getattr(segment, P1).add_HVI_variable("t_measure", t_read)

    getattr(segment, P1).add_block(0, t_read, p_2[0])
    getattr(segment, P2).add_block(0, t_read, p_2[1])
    segment.reset_time()

if __name__ == '__main__':
    from pulse_templates.utility.plotting import plot_seg
    from pulse_templates.demo_pulse_lib.virtual_awg import get_demo_lib
    
    pulse = get_demo_lib('quad')
    seg = pulse.mk_segment()

    gates = ('P1', 'P2')
    
    p_0 = (-1,  1)
    p_1 = ( 1, -1)
    PSB_read(seg, gates, 1e3, 5e3, p_0, p_1)
    p_2 = (2, 1)
    PSB_read_latched(seg, gates, 1e3, 5e3, p_0, p_1, p_2)

    plot_seg(seg)
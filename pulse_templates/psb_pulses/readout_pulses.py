'''
Readout pulse templates for PSB.

Pulses:
    * psb_read : native readout function for readout at the anticrossing
    * psb_read_latched : readout function to use in case you want to make use of latching mechanisms

'''
from pulse_templates.utility.template_wrapper import template_wrapper 
from pulse_templates.utility.oper import add_block, add_ramp

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
    # jump close to (1,1) -- (2,0) wait 100 ns
    add_block(segment, 100, gates, p_0)

    # pulse towards the window and stay for the measurment time
    add_ramp(segment, t_ramp, gates, p_0, p_1)

    if disable_trigger == False:
        getattr(segment, gates[0]).add_HVI_marker("dig_wait_1")
        getattr(segment, gates[0]).add_HVI_variable("t_measure", t_read)

    add_block(segment, t_read, gates, p_1)

@template_wrapper
def PSB_read_tc_ctrl(segment, gates, t_ramp, t_read, p_0, p_1, p_2, nth_readout, disable_trigger=False):
    '''
    pulse able to perform a psb readout, the tunnelcoupling is lowered at the end to make the pulse robust against T1 effects.

    Args:
        segment (segment_container) : segment to which to add this stuff
        gates (tuple<str>) : plunger gate names
        t_ramp (double) : time to linearly ramp trought the anticrossing
        t_read (double) : readout time
        p_0 (tuple <double>) : starting point
        p_1 (tuple<double>) : point after the anticrossing, for readout, when the tunnel coupling is on
        p_2 (tuple<double>) : point after the anticrossing, for readout, when the tunnel coupling oig odff
        disable_trigger (bool) : disable triggerig for digitizer, only for debuggig.
    '''
    # jump close to (1,1) -- (2,0) wait 100 ns
    add_block(segment, 100, gates, p_0)

    # pulse towards the window and stay for the measurment time
    add_ramp(segment, t_ramp, gates, p_0, p_1)
    add_ramp(segment, 2, gates, p_1, p_2)


    if disable_trigger == False:
        getattr(segment, gates[0]).add_HVI_marker("dig_wait_{}".format(int(nth_readout)))
        getattr(segment, gates[0]).add_HVI_variable("t_measure", t_read)

    add_block(segment, t_read, gates, p_2)
    add_ramp(segment, 2, gates, p_2, p_1)
    add_ramp(segment, t_ramp, gates, p_1, p_0)

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
    # jump close to (1,1) -- (2,0) wait 100 ns
    add_block(segment, 100, gates, p_0)

    # pulse towards the window and stay for the measurment time
    add_ramp(segment, t_ramp, gates, p_0, p_1)
    add_ramp(segment, 10, gates, p_1, p_2)


    if disable_trigger == False:
        getattr(segment, gates[0]).add_HVI_marker("dig_wait_1")
        getattr(segment, gates[0]).add_HVI_variable("t_measure", t_read)

    add_block(segment, t_read, gates, p_2)

@template_wrapper
def PSB_read_multi(segment, gates, t_ramp, t_read, p_0, p_1, nth_readout=0, disable_trigger=False):
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
    # jump close to (1,1) -- (2,0) wait 100 ns
    add_block(segment, 500, gates, p_0)

    # pulse towards the window and stay for the measurment time
    add_ramp(segment, t_ramp, gates, p_0, p_1)

    if disable_trigger == False:
        getattr(segment, gates[0]).add_HVI_marker("dig_wait_{}".format(int(nth_readout)))
        getattr(segment, gates[0]).add_HVI_variable("t_measure", t_read)

    add_block(segment, t_read, gates, p_1)

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
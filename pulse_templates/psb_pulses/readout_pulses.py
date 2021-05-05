'''
Readout pulse templates for PSB.

Pulses:
    * psb_read : native readout function for readout at the anticrossing
    * psb_read_latched : readout function to use in case you want to make use of latching mechanisms

'''
from pulse_templates.utility.template_wrapper import template_wrapper
from pulse_templates.utility.oper import add_block, add_ramp
from pulse_templates.measurement.measurement import measurement

#@template_wrapper
def PSB_read(segment, gates, t_ramp, meas, p_0, p_1, disable_trigger=False):
    '''
    pulse able to perform a psb readout

    Args:
        segment (segment_container) : segment to which to add this stuff
        gates (tuple<str>) : plunger gate names
        t_ramp (double) : time to linearly ramp trought the anticrossing
        meas (measurement) : measurement
        p_0 (tuple <double>) : starting point
        p_1 (tuple<double>) : point after the anticrossing, where the readout should happen.
        disable_trigger (bool) : disable triggerig for digitizer, only for debuggig.
    '''
    # jump close to (1,1) -- (2,0) wait 100 ns
    add_block(segment, 100, gates, p_0)

    # pulse towards the window and stay for the measurment time
    add_ramp(segment, t_ramp, gates, p_0, p_1)

    t_read = meas.t_measure
    if disable_trigger == False:
        meas.build(segment, reset=False)

    add_block(segment, t_read, gates, p_1)

#@template_wrapper
def PSB_read_tc_ctrl(segment, gates, t_ramp, meas, p_0, p_1, p_2, nth_readout, disable_trigger=False):
    '''
    pulse able to perform a psb readout, the tunnelcoupling is lowered at the end to make the pulse robust against T1 effects.

    Args:
        segment (segment_container) : segment to which to add this stuff
        gates (tuple<str>) : plunger gate names
        t_ramp (double) : time to linearly ramp trought the anticrossing
        meas (measurement) : measurement
        p_0 (tuple <double>) : starting point
        p_1 (tuple<double>) : point after the anticrossing, for readout, when the tunnel coupling is on
        p_2 (tuple<double>) : point after the anticrossing, for readout, when the tunnel coupling oig odff
        disable_trigger (bool) : disable triggerig for digitizer, only for debuggig.
    '''
    # pulse towards the window and stay for the measurment time
    add_ramp(segment, t_ramp, gates, p_0, p_1)
    add_ramp(segment, 10, gates, p_1, p_2)

    t_read = meas.t_measure
    if disable_trigger == False:
        meas.build(segment, reset=False)

    add_block(segment, t_read, gates, p_2)
    add_ramp(segment, 10, gates, p_2, p_1)
    add_ramp(segment, t_ramp, gates, p_1, p_0)

#@template_wrapper
def PSB_read_latched(segment, gates, t_ramp, meas, p_0, p_1, p_2, disable_trigger=False):
    '''
    pulse able to perform a psb readout

    Args:
        segment (segment_container) : segment to which to add this stuff
        gates (tuple<str>) : plunger gate names
        t_ramp (double) : time to linearly ramp trought the anticrossing
        meas (measurement) : measurement
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

    t_read = meas.t_measure
    if disable_trigger == False:
        meas.build(segment, reset=False)

    add_block(segment, t_read, gates, p_2)

#@template_wrapper
def PSB_read_multi(segment, gates, t_ramp, meas, p_0, p_1, nth_readout=0,  unmute=None, disable_trigger=False):
    '''
    pulse able to perform a psb readout

    Args:
        segment (segment_container) : segment to which to add this stuff
        gates (tuple<str>) : plunger gate names
        t_ramp (double) : time to linearly ramp trought the anticrossing
        meas (measurement) : measurement
        p_0 (tuple <double>) : starting point
        p_1 (tuple<double>) : point after the anticrossing, where the readout should happen.
        disable_trigger (bool) : disable triggerig for digitizer, only for debuggig.
    '''
    # pulse towards the window and stay for the measurment time
    add_ramp(segment, t_ramp, gates, p_0, p_1)
    t_read = meas.t_measure
    if unmute is not None:
        segment[unmute].add_marker(0, t_read)

    if disable_trigger == False:
        meas.build(segment, reset=False)
    if disable_trigger == False:
        measurement.build(segment, reset=False)

    add_block(segment, t_read, gates, p_1)
    add_ramp(segment, t_ramp, gates, p_1, p_0)

if __name__ == '__main__':
    from pulse_templates.utility.plotting import plot_seg
    from pulse_templates.demo_pulse_lib.virtual_awg import get_demo_lib

    pulse = get_demo_lib('quad')
    seg = pulse.mk_segment()

    gates = ('P1', 'P2')
    m1 = measurement('SD1_I', 5e3)
    m2 = measurement('SD1_I', 1e3)

    p_0 = (-1,  1)
    p_1 = ( 1, -1)
    PSB_read(seg, gates, 1e3, m1, p_0, p_1)
    p_2 = (2, 1)
    PSB_read_latched(seg, gates, 1e3, m2, p_0, p_1, p_2)

    plot_seg(seg)
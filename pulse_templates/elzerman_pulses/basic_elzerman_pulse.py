'''
basic elzerman pulse (to be used for the classic experiments)
'''
from pulse_templates.utility.template_wrapper import template_wrapper 
from pulse_templates.utility.oper import add_block, add_ramp

@template_wrapper
def elzerman_basic(segment, gates, t_init, t_ramp, t_load, t_read,
        p_0, p_1 , p_2, p_3, p_4, disable_trigger=False):
    '''
    pulse able to perform a psb readout

    Args:
        segment (segment_container) : segment to which to add this stuff
        gates (tuple<str>) : plunger gate names
        t_init (double) : initialisation time to eject electron
        t_ramp (double) : time to ramp
        t_load (double) : time to wait at the load stage
        t_read (double) : readout time
        p_0 (tuple <double>) : init point
        p_1 (tuple <double>) : ramp start from N=0 to N=1
        p_2 (tuple <double>) : ramp end from N=0 to N=1
        p_3 (tuple <double>) : operating point
        p_4 (tuple <double>) : point where to readout
        disable_trigger (bool) : disable triggerig for digitizer, only for debuggig.
    '''
    # init
    add_block(segment, t_init, gates, p_0)

    # pulse towards the window and stay for the measurment time
    add_ramp(segment, t_ramp, gates, p_1, p_2)
    add_block(segment, t_load, gates, p_3)

    if disable_trigger == False:
        getattr(segment, gates[0]).add_HVI_marker("dig_wait")
        getattr(segment, gates[0]).add_HVI_variable("t_measure", t_read)

    add_block(segment, t_read, gates, p_4)


if __name__ == '__main__':
    from pulse_templates.utility.plotting import plot_seg
    from pulse_templates.demo_pulse_lib.virtual_awg import get_demo_lib
    
    pulse = get_demo_lib('quad')
    seg = pulse.mk_segment()

    gates = ('vP4',)
    
    t_init = 10e3
    t_ramp = 10e3
    t_load = 100
    t_read = 30e3
    p_0 = (-10,)
    p_1 = (-1,)
    p_2 = (1,)
    p_3 = (20,)
    p_4 = (0,)

    elzerman_basic(seg, gates, t_init, t_ramp, t_load, t_read, p_0, p_1, p_2, p_3, p_4)
    plot_seg(seg)
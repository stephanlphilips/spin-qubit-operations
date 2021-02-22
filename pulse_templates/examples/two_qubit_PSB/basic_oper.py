from pulse_templates.oper.operators import wait, ramp, add_stage, ramp_through_anticorssing
from pulse_templates.psb_pulses.readout_pulses import PSB_read_multi, PSB_read_tc_ctrl

from pulse_templates.utility.plotting import plot_seg
from pulse_templates.examples.two_qubit_PSB.var import variables

import pulse_lib.segments.utility.looping as lp
import qcodes as qc

def do_EMPTY(debug = False):
    gates, ST_anti_12, ST_anti_12_close, ST_anti_12_tc_high_, _30, _30_load, _40, _31 = variables()

    pulse = qc.Station.default.pulse 
    EMPTY = pulse.mk_segment() 

    if debug:
        print(round(EMPTY.total_time.flat[0]/1e3), 'us -- 31' )

    start, stop = ramp_through_anticorssing(['vP1', 'vP2'], [1,-1], ST_anti_12_tc_high_, gates)
    ramp(EMPTY, gates, 1e3, _31, start, debug=debug)
    ramp(EMPTY, gates, 1e3, start, stop)
    ramp(EMPTY, gates, 1e3, stop, _40)

    if debug:
        print(round(EMPTY.total_time.flat[0]/1e3), 'us -- 40' )

    ramp(EMPTY, gates, 1e3, _40, _30_load)
    ramp(EMPTY, gates, 1e3, _30_load, _30)
    wait(EMPTY, gates, 1e3, _30)

    if debug: 
        print(round(EMPTY.total_time.flat[0]/1e3), 'us -- 30' )


    return EMPTY

def do_LOAD(pulse_deep = False, debug = False):
    gates, ST_anti_12, ST_anti_12_close, ST_anti_12_tc_high_, _30, _30_load, _40, _31 = variables()

    pulse = qc.Station.default.pulse
    LOAD =  pulse.mk_segment()

    if debug:
        print(round(LOAD.total_time.flat[0]/1e3), 'us -- 30' )

    start = list(_30_load)
    stop = list(_30_load)

    start[1]-=0.5
    stop[1] +=0.5

    start = tuple(start)
    stop = tuple(stop)

    wait(LOAD, gates, 1e3, _30, debug=debug)
    ramp(LOAD, gates, 2e3, _30, _30_load)
    ramp(LOAD, gates, 5e3,start, stop)
    ramp(LOAD, gates, 1e3, stop, _40)

    if debug:
        print(round(LOAD.total_time.flat[0]/1e3), 'us -- 40' )

    start, stop = ramp_through_anticorssing(['vP1', 'vP2'], [-2,2], ST_anti_12_tc_high_, gates)
    ramp(LOAD, gates, 1e3, _40, start)
    ramp(LOAD, gates, 5e3, start, stop)
    ramp(LOAD, gates, 2e3, stop, _31)
    wait(LOAD, gates, 1e3, _31)

    if debug:
        print(round(LOAD.total_time.flat[0]/1e3), 'us -- 31' )

    return LOAD

def do_READ(ramp = 100, t_meas=2e3, scan_range = 0, nth_readout=1, debug=False):
    gates, ST_anti_12, ST_anti_12_close, ST_anti_12_tc_high_, _30, _30_load, _40, _31 = variables()

    pulse = qc.Station.default.pulse
    READ = pulse.mk_segment()

    if debug:
        wait(LOAD, gates, 100, _31, debug=debug)

    PSB_read_multi(READ, gates, ramp, t_meas, _31, ST_anti_12, nth_readout, disable_trigger=debug)

    return READ

def do_MANIP(disble_SD=False):
    gates, ST_anti_12, ST_anti_12_close, ST_anti_12_tc_high_, _30, _30_load, _40, _31 = variables()

    pulse = qc.Station.default.pulse
    MANIP = pulse.mk_segment()
    
    if disble_SD:
        MANIP.M2 += 1200

    return MANIP

if __name__ == '__main__':
    from pulse_templates.utility.plotting import plot_seg
    from pulse_templates.demo_pulse_lib.virtual_awg import get_demo_lib
    
    station = qc.Station()
    pulse = get_demo_lib('quad')

    station.pulse = pulse
    seg = do_READ()

    plot_seg(seg)
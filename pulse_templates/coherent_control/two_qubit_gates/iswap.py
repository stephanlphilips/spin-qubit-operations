from pulse_templates.utility.template_wrapper import template_wrapper
from pulse_templates.utility.oper import add_block, add_ramp, add_pulse_template
from pulse_templates.coherent_control.two_qubit_gates.cphase import calculate_cphase_properties,t_ramp_

from pulse_lib.segments.utility.looping import loop_obj
from pulse_lib.segments.utility.loops_to_numpy import loops_to_numpy

import numpy as np

import matplotlib.pyplot as plt
def integrate_array(array):
    integral = np.zeros(array.shape)
    for i in range(1,array.size):
        integral[i] = integral[i-1] + array[i]
    return integral

def iswap_function(duration, sample_rate, amplitude, t_ramp=None, t_pulse=None, phase=None, J_max=None, J_to_voltage_relation=None, f_res_to_J_relation=None):
    sample_rate = sample_rate * 10
    n_points = int(round(duration*sample_rate*1e-9))
    J_valued_data = np.zeros([n_points])
    n_points_ramp = int(round(t_ramp*sample_rate*1e-9))

    J_valued_data[0:n_points_ramp] = (0.5-0.5*np.cos(np.arange(n_points_ramp)*np.pi/t_ramp/sample_rate*1e9))*J_max
    dc_stop = int(round((t_ramp + t_pulse ) * sample_rate * 1e-9))
    J_valued_data[n_points_ramp:dc_stop] = J_max
    offset = dc_stop - t_ramp - t_pulse
    
    J_valued_data[dc_stop:n_points] = (0.5-0.5*np.cos(np.arange(n_points-dc_stop)/sample_rate*1e9*np.pi/t_ramp+np.pi))*J_max
    
    # plt.plot(J_valued_data)
    # plt.show()
    envelope = J_to_voltage_relation(J_valued_data)*amplitude

    frequencies = f_res_to_J_relation(J_valued_data)

    # format as a phase modulation to be phase coherent.
    PM = np.sin(integrate_array(frequencies*2*np.pi*1/sample_rate)+phase)/2+.5
    PM[np.where(PM<0.4)] = 0

    return J_to_voltage_relation((J_valued_data*PM)[::10])*amplitude


def iswap_cal_function(duration, sample_rate, amplitude, t_ramp=None,
    t_pulse=None, J_eff=None, J_drive=None, f_drive=None, J_to_voltage_relation=None):
    n_points = int(round(duration * sample_rate * 1e-9))
    J_valued_data = np.zeros([n_points])
    n_points_ramp = int(round(t_ramp * sample_rate * 1e-9))

    J_valued_data[0:n_points_ramp] = (0.5-0.5*np.cos(np.arange(n_points_ramp)*np.pi/t_ramp))*J_eff
    dc_stop = int(round((t_ramp + t_pulse )/ sample_rate * 1e9))
    
    drive_signal = 0.5+0.5*np.cos(np.arange(dc_stop-n_points_ramp)*2*np.pi*f_drive/sample_rate+np.pi)
    drive_signal[np.where(drive_signal>0.6)] = 1

    J_valued_data[n_points_ramp:dc_stop] = J_eff - J_drive*drive_signal
    offset = dc_stop - t_ramp - t_pulse
    
    J_valued_data[dc_stop:n_points] = (0.5-0.5*np.cos(np.arange(n_points-dc_stop)/sample_rate*1e9*np.pi/t_ramp+np.pi))*J_eff
    
    envelope = J_to_voltage_relation(J_valued_data)*amplitude

    return envelope

@loops_to_numpy
def calculate_cphase_properties_iswap_cal(angle:np.ndarray, 
    J_target:np.ndarray, f_excitation:np.ndarray)-> np.ndarray:
    t_ramp:np.ndarray = t_ramp_(J_target, f_excitation)*1e9
    t_pulse:np.ndarray = 4/J_target/2*1e9*angle/np.pi/2 #since drive is with

    duration = t_ramp*2 + t_pulse
    print(type(angle), type(J_target), type(f_excitation))
    return duration, t_ramp, t_pulse

def iswap_cal(segment, gates, J_value, f_excitation, angle, J_to_voltage_relation, padding = 5):
    add_block(segment, padding, gates, tuple([0]*len(gates)))

    duration, t_ramp, t_pulse = calculate_cphase_properties_iswap_cal(angle, J_value, f_excitation)

    for gate, v_to_J in zip(gates, J_to_voltage_relation):
        ch = getattr(segment, gate)
        ch.add_custom_pulse(0, duration, 1.0,
                            iswap_cal_function, t_ramp=t_ramp, t_pulse=t_pulse, J_eff=J_value, J_drive=J_value,
                            f_drive=f_excitation, J_to_voltage_relation=v_to_J)
    segment.reset_time()

    add_block(segment, padding, gates, tuple([0]*len(gates)))

def iswap(segment, gates, iswap_angle, phase, J_max, delta_B, J_to_voltage_relation, f_res_to_J_relation, padding = 5):
    add_block(segment, padding, gates, tuple([0]*len(gates)))

    duration, t_ramp, t_pulse, J_max = calculate_cphase_properties(iswap_angle*4, J_max, delta_B)

    for gate, v_to_J in zip(gates, J_to_voltage_relation):
        ch = getattr(segment, gate)
        ch.add_custom_pulse(0, duration, 1.0,
                            iswap_function, t_ramp=t_ramp, phase=phase, t_pulse=t_pulse, J_max=J_max,
                            J_to_voltage_relation=v_to_J, f_res_to_J_relation=f_res_to_J_relation)
    segment.reset_time()

    add_block(segment, padding, gates, tuple([0]*len(gates)))


if __name__ == '__main__':
    from pulse_templates.utility.plotting import plot_seg
    from pulse_templates.demo_pulse_lib.virtual_awg import get_demo_lib
    from pulse_lib.segments.utility.looping import linspace
    from pulse_templates.oper.operators import wait
    

    from core_tools.data.SQL.connect import set_up_local_storage
        
    # set_up_local_storage("xld_user", "XLDspin001", "vandersypen_data", "6dot", "XLD", "6D2S - SQ21-XX-X-XX-X")
    set_up_local_storage('stephan', 'magicc', 'test', "project_name", "set_up_name", "sample_name")
    pulse = get_demo_lib('six')
    seg = pulse.mk_segment()

    gates = ('vP1','vB1', 'vP2')
    base_level = (0,0,0)
    # seg.vP4 += 10
    # wait(seg, gates, 100, base_level)
    # iswap_basic(seg, gates, 'vB1' ,(0,4,0), (0,8,0), 2, 1e8, 100, 10)

    def return_amp(amp):
        def J_pulse(x):
            return np.sqrt(x)/np.sqrt(5e6)*amp
        return J_pulse

    def f_res(f_res, delta_fres) :
        def f_res_relation(J):
            return f_res + J**2/5e6**2*delta_fres
        return f_res_relation

    J_to_voltage_relation = (return_amp(-0.2), return_amp(1), return_amp(-0.23))
    f_res_relation_test = f_res(50e6, 100e3)
    sweep = linspace(0, 2*np.pi, 20, axis= 1)

    # import good_morning.static.J45 as J45
    iswap(seg, gates, np.pi, 0, 6e6, 80e6, J_to_voltage_relation, f_res_relation_test)

    # iswap(seg, J45.gates, np.pi, 0, 6e6, 80e6, J45.gen_J_to_voltage(), J45.return_delta_B_J_relation())
    # iswap_cal(seg, gates, 5e6, linspace(75e6, 85e6, 5, 'freq', 'Hz', 0), np.pi, J_to_voltage_relation, 20)
    # print(gates, J45.gates)
    # print(J_to_voltage_relation, J45.gen_J_to_voltage())
    # ratios =  J45.gen_J_to_voltage()
    # iswap_cal(seg, gates, 5e6, 80e6, 3.14, J_to_voltage_relation, 20)

    # iswap_cal(seg, J45.gates, 5e6, 5e6, 80e6, linspace(3.14, 2.65, 80, 'freq', 'Hz', 0), ratios, 20)

    # plot_seg(seg, 0)   
    # plot_seg(seg, 5)   
    plot_seg(seg, 0)
    # plot_seg(seg, 15)   
from pulse_templates.utility.template_wrapper import template_wrapper 
from pulse_templates.utility.oper import add_block, add_ramp, add_pulse_template
from pulse_templates.coherent_control.two_qubit_gates.cphase import calculate_cphase_properties

from pulse_lib.segments.utility.looping import loop_obj
import numpy as np
import copy

import matplotlib.pyplot as plt

@template_wrapper
def iswap_basic(segment, gates, barrier_gate,v_exchange_pulse_off, v_exchange_pulse_on, v_ac, f_ac, t_gate, t_ramp, padding = 2):
    '''
    basic iSWAP, with a linear ramp

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

def integrate_array(array):
    integral = np.zeros(array.shape)
    for i in range(1,array.size):
        integral[i] = integral[i-1] + array[i]
    return integral


def return_creation_fuction(angle, phase, J_max, delta_B, J_to_voltage_relation, f_res_to_J_relation):
    '''
        Adds a custom pulse to this segment.
        Args:
            angle (double) : angle to evolve (rad)
            J_max (double) : max J value that can be hit (Hz)
            delta_B (double) : frequency difference between the qubits
            J_to_voltage_relation (func) : function that converts J (Hz) to voltages (mV)
            f_res_to_J_relation (func) : function that returns for a given J (Hz) value the frequency (Hz)
    '''
    duration, t_ramp, t_pulse, J_max = calculate_cphase_properties(angle*2, J_max, delta_B)

    def iswap_function(duration, sample_rate, amplitude):
        sample_rate = sample_rate * 10
        n_points = int(round(duration*sample_rate*1e-9))
        J_valued_data = np.zeros([n_points])
        n_points_ramp = int(round(t_ramp*sample_rate*1e-9))

        J_valued_data[0:n_points_ramp] = (0.5-0.5*np.cos(np.arange(n_points_ramp)*np.pi/t_ramp/sample_rate*1e9))*J_max
        dc_stop = int(round((t_ramp + t_pulse ) * sample_rate * 1e-9))
        J_valued_data[n_points_ramp:dc_stop] = J_max
        offset = dc_stop - t_ramp - t_pulse
        
        J_valued_data[dc_stop:n_points] = (0.5-0.5*np.cos(np.arange(n_points-dc_stop)/sample_rate*1e9*np.pi/t_ramp+np.pi))*J_max
        envelope = J_to_voltage_relation(J_valued_data)*amplitude

        frequencies = f_res_to_J_relation(J_valued_data)

        # format as a phase modulation to be phase coherent.
        PM = np.sin(integrate_array(frequencies*2*np.pi*1/sample_rate)+phase)/2+.5

        return (envelope*PM)[::10]


    return iswap_function, duration

def return_creation_fuction_iswap_cal(J_eff, J_drive,f_drive, angle, J_to_voltage_relation):
    '''
        Adds a custom pulse to this segment.
        Args:
            J_eff (double) : max J value that can be hit (Hz)
            J_drive (double) : the J speed used for driving
            f_drive (double) : frequency difference between the qubits
            angle (double) : angle to rotate
            J_to_voltage_relation (func) : function that converts J (Hz) to voltages (mV)
    '''
    if J_eff < J_drive:
        raise ValueError('J dc needs to be always larger then J_ac (you cannot get a negative J) (at least if you don\'t use mediators ..)')
    
    duration, t_ramp, t_pulse, J_max = calculate_cphase_properties(1e3,  J_eff, f_drive)
    t_pulse = 1/J_drive*1e9*angle/np.pi/2
    duration = 2*t_ramp + t_pulse

    def iswap_function(duration, sample_rate, amplitude):
        n_points = int(round(duration * sample_rate * 1e-9))
        J_valued_data = np.zeros([n_points])
        n_points_ramp = int(round(t_ramp * sample_rate * 1e-9))

        J_valued_data[0:n_points_ramp] = (0.5-0.5*np.cos(np.arange(n_points_ramp)*np.pi/t_ramp))*J_eff
        dc_stop = int(round((t_ramp + t_pulse )/ sample_rate * 1e9))
        J_valued_data[n_points_ramp:dc_stop] = J_eff + J_drive*np.sin(np.arange(dc_stop-n_points_ramp)*2*np.pi*f_drive/sample_rate)
        offset = dc_stop - t_ramp - t_pulse
        
        J_valued_data[dc_stop:n_points] = (0.5-0.5*np.cos(np.arange(n_points-dc_stop)/sample_rate*1e9*np.pi/t_ramp+np.pi))*J_eff
        
        envelope = J_to_voltage_relation(J_valued_data)*amplitude

        return envelope

    return iswap_function, duration


def iswap_cal(segment, gates, J_value, J_excitation, f_excitation, angle, J_to_voltage_relation, padding = 5):
    '''
    Function to help with the calibration of iswap gates. A ramp is done to the target J, then a excitation with a desired amplitude is provided.
    
    Args:
        segment (segment_container) : segment to which to add this stuff
        gates (list<str>) : list of gates involved in the cphase gate (relations of J and f_res need to be provided for each gate)
        J_value (double) : value of J to go for (Hz)
        J_excitation (double) : value of J to excite with (Hz) (e.g. 500e3)
        f_excitation (double) : frequency of the J excitation (Hz)
        J_to_voltage_relation (list<func>) : function that returns the voltages to be applied for a certain amount of J (same order as the gates)
        padding (int) : padding to be added in ns around this experiment
    '''
    if isinstance(J_value, loop_obj):
        raise ValueError('J_value is a loop object, this is currently not supported for this function')
    if isinstance(J_excitation, loop_obj):
        raise ValueError('J_excitation is a loop object, this is currently not supported for this function')

    t_gate = 0
    amplitudes = tuple()
    pulse_templates = tuple()

    if isinstance(f_excitation, loop_obj):
        t_gate = copy.copy(f_excitation)
        amplitudes = tuple()
        pulse_templates = tuple()

        for i in range(len(gates)):
            functions = copy.copy(f_excitation)
            functions.data = np.empty(f_excitation.data.shape, dtype=object)
            for j in range(t_gate.data.size):
                func, duration = return_creation_fuction_iswap_cal(J_value, J_excitation, f_excitation.data[j], angle, J_to_voltage_relation[i])

                t_gate.data[j] = duration
                functions.data[j] = func

            pulse_templates += (functions, )
            amplitudes += (1,)
    if isinstance(angle, loop_obj):
        t_gate = copy.copy(angle)
        amplitudes = tuple()
        pulse_templates = tuple()

        for i in range(len(gates)):
            functions = copy.copy(angle)
            functions.data = np.empty(angle.data.shape, dtype=object)
            for j in range(t_gate.data.size):
                func, duration = return_creation_fuction_iswap_cal(J_value, J_excitation, f_excitation, angle.data[j], J_to_voltage_relation[i])

                t_gate.data[j] = duration
                functions.data[j] = func

            pulse_templates += (functions, )
            amplitudes += (1,)
    else: 
        for i in range(len(gates)):
            func, duration = return_creation_fuction_iswap_cal(J_value, J_excitation, f_excitation, angle, J_to_voltage_relation[i])
            t_gate = duration
            amplitudes += (1,)
            pulse_templates += (func, )


    add_block(segment, padding, gates, tuple([0]*len(gates)))
    add_pulse_template(segment, t_gate, gates, amplitudes, pulse_templates)
    add_block(segment, padding, gates, tuple([0]*len(gates)))



def iswap(segment, gates, iswap_angle, phase, J_max, delta_B, J_to_voltage_relation, f_res_to_J_relation, padding = 5):
    '''
    iSWAP gate for spins, this is basically a modulated verions of the cphase
    (convert to SWAP by running iSWAP and then CPHASE) -- this function does not guarantee that the accumalted ZZ phase is correct

    Args:
        segment (segment_container) : segment to which to add this stuff
        gates (list<str>) : list of gates involved in the cphase gate (relations of J and f_res need to be provided for each gate)
        iswap_angle (double) : angle to rotate with the iSWAP gate
        phase (double) : starting phase of the iswap gate (important if you sqrt(iSWAP))
        J_max (double) : maximum amount of J that should be reached
        delta_B (double) : frequency difference between the qubits
        J_to_voltage_relation (list<func>) : function that returns the voltages to be applied for a certain amount of J (same order as the gates)
        f_res_to_J_relation (func) : function that returns the resonance frequency for J
        padding (int) : padding to add around the swap gate.
    '''
    if isinstance(J_max, loop_obj):
        raise ValueError('J_max is a loop object, this is currently not supported for this function')

    if isinstance(delta_B, loop_obj):
        raise ValueError('delta_B is a loop object, this is currently not supported for this function')
    
    if len(gates) != len(J_to_voltage_relation):
        raise ValueError(f'found {len(gates)} gates and {len(len(J_to_voltage_relation))} J_to_voltage_relation\'s, something must be wrong here.')

    if isinstance(iswap_angle, loop_obj) and isinstance(phase, loop_obj):
        raise ValueError('No implementation yet to sweep iSWAP angle and phase.')

    if isinstance(iswap_angle, loop_obj):
        t_gate = copy.copy(iswap_angle)
        amplitudes = tuple()
        pulse_templates = tuple()

        for i in range(len(gates)):
            functions = copy.copy(iswap_angle)
            functions.data = np.empty(iswap_angle.data.shape, dtype=object)
            for j in range(t_gate.data.size):
                func, duration = return_creation_fuction(iswap_angle.data[j], phase, J_max, delta_B, J_to_voltage_relation[i], f_res_to_J_relation)
                t_gate.data[j] = duration
                functions.data[j] = func

            pulse_templates += (functions, )
            amplitudes += (1,)

    elif isinstance(phase, loop_obj):
        amplitudes = tuple()
        pulse_templates = tuple()

        for i in range(len(gates)):
            functions = copy.copy(phase)
            functions.data = np.empty(phase.data.shape, dtype=object)
            for j in range(phase.data.size):
                func, duration = return_creation_fuction(iswap_angle, phase.data[j], J_max, delta_B, J_to_voltage_relation[i], f_res_to_J_relation)
                t_gate = duration
                functions.data[j] = func

            pulse_templates += (functions, )
            amplitudes += (1,)

    else:
        t_gate = 0
        amplitudes = tuple()
        pulse_templates = tuple()

        for i in range(len(gates)):
            func, duration = return_creation_fuction(iswap_angle, phase, J_max, delta_B, J_to_voltage_relation[i], f_res_to_J_relation)
            t_gate = duration
            amplitudes += (1,)
            pulse_templates += (func, )


    add_block(segment, padding, gates, tuple([0]*len(gates)))
    add_pulse_template(segment, t_gate, gates, amplitudes, pulse_templates)
    add_block(segment, padding, gates, tuple([0]*len(gates)))



if __name__ == '__main__':
    from pulse_templates.utility.plotting import plot_seg
    from pulse_templates.demo_pulse_lib.virtual_awg import get_demo_lib
    from pulse_lib.segments.utility.looping import linspace
    from pulse_templates.oper.operators import wait
    pulse = get_demo_lib('six')
    seg = pulse.mk_segment()

    gates = ('vP1','vB1', 'vP2')
    base_level = (0,0,0)
    # seg.vP4 += 10
    wait(seg, gates, 100, base_level)
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
    
    sweep = linspace(0, 2*np.pi, 20, axis= 0)

    import good_morning.static.J23 as J23

    iswap(seg, J23.gates, np.pi, 0, 5e6, 50e6, J23.gen_J_to_voltage(), J23.return_delta_B_J_relation())
    # iswap_cal(seg, gates, 5e6, 0.5e6, 30e6, 30e6, J_to_voltage_relation)
    # plot_seg(seg, 0)   
    # plot_seg(seg, 5)   
    plot_seg(seg, 0)   
    # plot_seg(seg, 15)   
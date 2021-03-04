from pulse_templates.utility.template_wrapper import template_wrapper 
from pulse_templates.utility.oper import add_block, add_ramp, add_pulse_template
from pulse_templates.coherent_control.two_qubit_gates.cphase import calculate_cphase_properties

from pulse_lib.segments.utility.looping import loop_obj
import numpy as np
import copy


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


def return_creation_fuction(angle, phase, J_max, delta_B, voltage_to_J_relation, f_res_to_J_relation):
    '''
        Adds a custom pulse to this segment.
        Args:
            angle (double) : angle to evolve (rad)
            J_max (double) : max J value that can be hit (Hz)
            delta_B (double) : frequency difference between the qubits
            voltage_to_J_relation (func) : function that converts J (Hz) to voltages (mV)
            f_res_to_J_relation (func) : function that returns for a given J (Hz) value the frequency (Hz)
    '''
    duration, t_ramp, t_pulse, J_max = calculate_cphase_properties(angle*2, J_max, delta_B)

    def iswap_function(duration, sample_rate, amplitude):
        n_points = int(round(duration / sample_rate * 1e9))
        J_valued_data = np.zeros([n_points])
        n_points_ramp = int(round(t_ramp / sample_rate * 1e9))

        J_valued_data[0:n_points_ramp] = (0.5-0.5*np.cos(np.arange(n_points_ramp)*np.pi/t_ramp))*J_max
        dc_stop = int(round((t_ramp + t_pulse )/ sample_rate * 1e9))
        J_valued_data[n_points_ramp:dc_stop] = J_max
        offset = dc_stop - t_ramp - t_pulse
        
        J_valued_data[dc_stop:n_points] = (0.5-0.5*np.cos((np.arange(n_points-dc_stop)+ offset/sample_rate*1e9)*np.pi/t_ramp+np.pi))*J_max
        
        envelope = voltage_to_J_relation(J_valued_data)*amplitude
        frequencies = f_res_to_J_relation(J_valued_data)

        # format as a phase modulation to be phase coherent.
        PM = np.sin(integrate_array(frequencies*2*np.pi*1/sample_rate)+phase)/2+.5

        return envelope*PM


    return iswap_function, duration



def iswap(segment, gates, iswap_angle, phase, J_max, delta_B, voltage_to_J_relation, f_res_to_J_relation, padding = 5):
    '''
    iSWAP gate for spins, this is basically a modulated verions of the cphase
    (convert to SWAP by running iSWAP and then CPHASE) -- this function does not guarantee that the accumalted ZZ phase is correct

    Args:
        segment (segment_container) : segment to which to add this stuff
        gates (list<str>) : list of gates involved in the cphase gate (relations of J and f_res need to be provided for each gate)
        iswap_angle (double) : angle to rotate with the iSWAP gate
        phase (double) : starting phase of the iswap gate (important if you sqrt(iSWAP))
        J_max (double) : maximum amount of J that should be reached
        voltage_to_J_relation (list<func>) : function that returns the voltages to be applied for a certain amount of J (same order as the gates)
        f_res_to_J_relation (func) : function that returns the resonance frequency for J
        padding (int) : padding to add around the swap gate.
    '''
    if isinstance(J_max, loop_obj):
        raise ValueError('J_max is a loop object, this is currently not supported for this function')

    if isinstance(delta_B, loop_obj):
        raise ValueError('delta_B is a loop object, this is currently not supported for this function')
    
    if len(gates) != len(voltage_to_J_relation):
        raise ValueError(f'found {len(gates)} gates and {len(len(voltage_to_J_relation))} voltage_to_J_relation\'s, something must be wrong here.')

    if isinstance(iswap_angle, loop_obj) and isinstance(phase, loop_obj):
        raise ValueError('No implementation yet to sweep iSWAP angle and phase.')

    if isinstance(iswap_angle, loop_obj):
        t_gate = copy.copy(iswap_angle)
        padding_ = copy.copy(iswap_angle) #little hack, something goes wrong when calling reset_time on custom_pulse
        amplitudes = tuple()
        pulse_templates = tuple()

        for i in range(len(gates)):
            functions = copy.copy(iswap_angle)
            functions.data = np.empty(iswap_angle.data.shape, dtype=object)
            for j in range(t_gate.data.size):
                func, duration = return_creation_fuction(iswap_angle.data[j], phase, J_max, delta_B, voltage_to_J_relation[i], f_res_to_J_relation)
                t_gate.data[j] = duration
                functions.data[j] = func
                padding_.data[j] = padding + 1e-3*j

            pulse_templates += (functions, )
            amplitudes += (1,)
        padding = padding_
    elif isinstance(phase, loop_obj):
        padding_ = copy.copy(phase) #little hack, something goes wrong when calling reset_time on custom_pulse
        amplitudes = tuple()
        pulse_templates = tuple()

        for i in range(len(gates)):
            functions = copy.copy(phase)
            functions.data = np.empty(phase.data.shape, dtype=object)
            for j in range(phase.data.size):
                func, duration = return_creation_fuction(iswap_angle, phase.data[j], J_max, delta_B, voltage_to_J_relation[i], f_res_to_J_relation)
                t_gate = duration
                functions.data[j] = func
                padding_.data[j] = padding + 1e-3*j

            pulse_templates += (functions, )
            amplitudes += (1,)
        padding = padding_

    else:
        t_gate = 0
        amplitudes = tuple()
        pulse_templates = tuple()

        for i in range(len(gates)):
            func, duration = return_creation_fuction(iswap_angle, phase, J_max, delta_B, voltage_to_J_relation[i], f_res_to_J_relation)
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
    pulse = get_demo_lib('quad')
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
    voltage_to_J_relation = (return_amp(-0.2), return_amp(1), return_amp(-0.23))
    
    sweep = linspace(0, 2*np.pi, 20, axis= 0)

    iswap(seg, gates, np.pi, sweep, 5e6, 30e6, voltage_to_J_relation, f_res(30e6,30e6))
    # plot_seg(seg, 0)   
    # plot_seg(seg, 5)   
    plot_seg(seg, 10)   
    # plot_seg(seg, 15)   
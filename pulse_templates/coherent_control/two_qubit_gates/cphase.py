from pulse_templates.utility.template_wrapper import template_wrapper
from pulse_templates.utility.oper import add_block, add_ramp, add_pulse_template

from pulse_lib.segments.utility.looping import loop_obj
from pulse_lib.segments.utility.loops_to_numpy import loops_to_numpy

import numpy as np
import copy

@template_wrapper
def cphase_basic(segment, gates, v_exchange_pulse_off, v_exchange_pulse_on, t_gate, t_ramp, t_padding=5):
    '''
    basic cphase, with a linear ramp

    Args:
        segment (segment_container) : segment to which to add this stuff
        barrier (str) : barrier to pulse
        v_exchange_pulse (double) : voltage to pulse to
        t_gate (double) : total time of the gate not inclusing the ramps
        t_ramp (double) : ramp time
    '''
    add_block(segment, t_padding, gates, tuple([0]*len(gates)))
    add_ramp(segment, t_ramp, gates, v_exchange_pulse_off, v_exchange_pulse_on)
    add_block(segment, t_gate, gates, v_exchange_pulse_on)
    add_ramp(segment, t_ramp, gates, v_exchange_pulse_on, v_exchange_pulse_off)
    add_block(segment, t_padding, gates, tuple([0]*len(gates)))


def get_J_max(angle, delta_B):
    return abs(np.sqrt(delta_B**2*angle**2/((3*np.pi)**2 - angle**2)))

def t_ramp_(J_max, delta_B):
    return 3/np.sqrt(J_max**2 + delta_B**2)

@loops_to_numpy
def calculate_cphase_properties(angle:np.ndarray, J_max:np.ndarray, delta_B:np.ndarray) -> np.ndarray:
    # theoretically can be a bit faster, but here chosen to be safe (3 seems to be a good spot (-> Martinis and geller, PRA 2014))
    # here sqrt(J_max**2 + delta_B**2) is the effective Zeeman difference.
    ramp_time:np.ndarray = t_ramp_(J_max, delta_B)
    angle_ramp:np.ndarray = ramp_time*J_max*np.pi

    J_max = np.where(angle < angle_ramp*2,
                     get_J_max(angle/2, delta_B),
                     J_max)
    t_ramp = t_ramp_(J_max, delta_B)*1e9
    t_pulse = np.where(angle < angle_ramp*2,
                       0,
                       (angle-angle_ramp*2)/J_max/2/np.pi*1e9)

    duration = t_ramp*2 + t_pulse

    return duration, t_ramp, t_pulse, J_max

def cphase_function(duration, sample_rate, amplitude,
                    t_ramp=None, t_pulse=None, J_max=None,
                    voltage_to_J_relation=None):
    n_points = int(round(duration / sample_rate * 1e9))
    J_valued_data = np.zeros([n_points])
    n_points_ramp = int(round(t_ramp / sample_rate * 1e9))

    J_valued_data[0:n_points_ramp] = (0.5-0.5*np.cos(np.arange(n_points_ramp)*np.pi/t_ramp))*J_max
    dc_stop = int(round((t_ramp + t_pulse )/ sample_rate * 1e9))
    J_valued_data[n_points_ramp:dc_stop] = J_max
    offset = dc_stop - t_ramp - t_pulse

    J_valued_data[dc_stop:n_points] = (0.5-0.5*np.cos((np.arange(n_points-dc_stop)+ offset/sample_rate*1e9)*np.pi/t_ramp+np.pi))*J_max

    return voltage_to_J_relation(J_valued_data)*amplitude


def cphase(segment, gates, cphase_angle, J_max, delta_B, voltage_to_J_relation, padding=5):
    '''
    Makes a shaped cphase gate (with respect to adiabaticity)

    Args:
        segment (segment_container) : segment to which to add this stuff
        gates (list<str>) : list of gates involved in the cphase gate
        cphase_angle (double) : the angle to rotate (amount of J to apply (MHz))
        J_max (double) : the maximal value of J that should be applied (e.g. cosine window get converted into a tuckey one)
        delta_B (double) : frequency difference between the qubits (MHz).
        voltage_to_J_relation (list<func>) : function that returns the voltages to be applied for a certain amount of J
        padding (int) : amount of padding to add around the pulse (in ns)
    '''
    t_gate, t_ramp, t_pulse, J_max = calculate_cphase_properties(cphase_angle, J_max, delta_B)

    add_block(segment, padding, gates, tuple([0]*len(gates)))

    for gate, v_to_J in zip(gates, voltage_to_J_relation, ):
        ch = getattr(segment, gate)
        ch.add_custom_pulse(0, t_gate, 1.0,
                            cphase_function, t_ramp=t_ramp, t_pulse=t_pulse, J_max=J_max,
                            voltage_to_J_relation=v_to_J)
    segment.reset_time()

    add_block(segment, padding, gates, tuple([0]*len(gates)))


if __name__ == '__main__':
    from pulse_templates.utility.plotting import plot_seg
    from pulse_templates.demo_pulse_lib.virtual_awg import get_demo_lib
    from pulse_lib.segments.utility.looping import linspace
    from pulse_templates.oper.operators import wait
    import matplotlib.pyplot as plt

    from core_tools.data.SQL.connect import set_up_local_storage

    set_up_local_storage('stephan', 'magicc', 'test', "project_name", "set_up_name", "sample_name")
    
    pulse = get_demo_lib('six')
    seg = pulse.mk_segment()


    gates = ('vB0', 'vB1','vB2',)
    J = np.pi
    J_max = 10e6
    delta_B = 64e6
    gate_phases= np.pi

    v_exchange_pulse_off =  (0,0,0)
    v_exchange_pulse_on  = (0,50,0)

    def return_amp(amp):
        def J_pulse(x):
            return np.sqrt(x)/np.sqrt(5e6)*amp
        return J_pulse

    # import good_morning.static.J23 as J23

    # func, time = return_creation_fuction(np.pi-0.7, 5e6, 30e6, voltage_to_J_relation=J_pulse)
    # points = func(time, 1e9, 1)
    # plt.plot(points)
    # gate_phases = linspace(0.1, 4.1, 20, axis=0)
    J_max = linspace(5e6, 10e6, 20, axis=1)
    # cphase(seg, J23.gates, gate_phases, J_max, delta_B, J23.gen_J_to_voltage(), padding=30)

    cphase(seg, gates, gate_phases, J_max, delta_B, (return_amp(0.2), return_amp(1), return_amp(0.23)), padding=30)

    # cphase_basic(seg, gates, v_exchange_pulse_off, v_exchange_pulse_on, gate_phases*100, t_ramp=50)
    for i in range(20):
        plot_seg(seg, i)

        plt.show()
from pulse_templates.utility.template_wrapper import template_wrapper 
from pulse_templates.utility.oper import add_block, add_ramp, add_pulse_template
from pulse_lib.segments.utility.looping import loop_obj
import numpy as np

# @template_wrapper
def CROT_basic(segment, gates, v_exchange_pulse_off, v_exchange_pulse_on, gate_spec, t_ramp, padding = 2):
    '''
    basic cphase, with a linear ramp

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
    add_block(segment, gate_spec.t_pulse, gates, v_exchange_pulse_on, reset_time=False)
    gate_spec.build(segment)
    add_block(segment, padding, gates, v_exchange_pulse_on)

    add_ramp(segment, t_ramp, gates, v_exchange_pulse_on, v_exchange_pulse_off)

def t_ramp_(J_max, delta_B):
    return 3/np.sqrt(J_max**2 + delta_B**2)

def generate_cphase_ramp(J_target, delta_B, voltage_to_J_relation, direction = 0):
    t_pulse =  round(t_ramp_(J_target, delta_B)*1e9)

    def cphase_function(duration, sample_rate, amplitude):
        n_points = int(round(duration / sample_rate * 1e9))
        J_valued_data = (0.5-0.5*np.cos(np.arange(n_points)*np.pi/t_pulse+ direction))*J_target
        
        
        return voltage_to_J_relation(J_valued_data)*amplitude

    return cphase_function, t_pulse

def CROT(segment, gates, gate_spec, J_target, delta_B, voltage_to_J_relation, padding = 5):
    '''
    constructs a CROT gate

    Args:
        segment (segment_container) : container to add gate to
        gates (list<str>) : list with gates to use to construct CROT
        gate_spec (single_qubit_gate_spec) : spec of the gate to drive with
        J_target (double) : J value to target
        delta_B (double) : frequency difference between the two qubits
        voltage_to_J_relation (func) : function that returns the voltages needed to get a certain J
        padding (int) : padding to add around the pulse (internal padding gan be added in the gate spect (also to get some ZZ phase to pi))
    '''

    if isinstance(J_target, loop_obj):
        raise ValueError('looping of J currently not supported')

    t_gate = 0
    amplitudes = tuple()
    amp_J_target =  tuple()
    pulse_templates_up = tuple()
    pulse_templates_down = tuple()

    for i in range(len(gates)):
        func_up, duration = generate_cphase_ramp(J_target, delta_B, voltage_to_J_relation[i], direction = 0)
        func_down, duration = generate_cphase_ramp(J_target, delta_B, voltage_to_J_relation[i], direction = np.pi)
        t_gate = duration
        amplitudes += (1,)
        amp_J_target += (voltage_to_J_relation[i](J_target) ,)
        pulse_templates_up += (func_up, )
        pulse_templates_down += (func_down, )

    add_block(segment, padding, gates, tuple([0]*len(gates)))
    add_pulse_template(segment, t_gate, gates, amplitudes, pulse_templates_up)

    for gate, level in zip(gates, amp_J_target):
        getattr(segment, gate).add_block(0, gate_spec.t_pulse + gate_spec.padding*2, level)
    gate_spec.build(segment, reset=False)
    segment.reset_time()

    add_pulse_template(segment, t_gate, gates, amplitudes, pulse_templates_down)
    add_block(segment, padding, gates, tuple([0]*len(gates)))

if __name__ == '__main__':
    from pulse_templates.coherent_control.single_qubit_gates.single_qubit_gates import single_qubit_gate_spec
    from pulse_templates.demo_pulse_lib.virtual_awg import get_demo_lib
    from pulse_templates.utility.plotting import plot_seg
    from pulse_templates.oper.operators import wait

    from pulse_lib.segments.utility.looping import linspace

    import matplotlib.pyplot as plt

    pulse = get_demo_lib('six')
    seg = pulse.mk_segment()

    # gates = ('vB0', 'vP1', 'vB1', 'vP2', 'vSD1_P')
    # base_level = (0,0,0,0,0)

    f_qubit  = 1e3
    t_pulse = 100
    MW_power = 200  

    # CROT_basic(seg, gates, (0,0,0,0,0), (0,0,160,0,0), spec, 10, 100)
    # plot_seg(seg)   

    import good_morning.static.J12 as J12

    spec = single_qubit_gate_spec('qubit1_MW', f_qubit, t_pulse, MW_power)
    CROT(seg, J12.gates, spec, 5e6, 30e6, J12.gen_J_to_voltage(), 50)

    plot_seg(seg, 0)
    plt.show()
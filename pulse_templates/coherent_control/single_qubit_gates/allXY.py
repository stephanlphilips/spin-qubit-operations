from pulse_lib.segments.utility.looping import loop_obj, linspace
import numpy as np

class ALLXY:
    allXY_set = [['I', 'I'], ['X2', 'X2'], ['Y2', 'Y2'], ['X2', 'Y2'], ['Y2', 'X2'], ['X', 'I'], ['Y', 'I'], ['X', 'Y'], ['X', 'Y'], ['X', 'Y2'], ['Y', 'X2'], ['X2', 'Y'], ['Y2', 'X'], ['X', 'X2'], ['X2', 'X'], ['Y', 'Y2'], ['Y2', 'Y'], ['X2', 'I'], ['Y2', 'I'], ['X', 'X'], ['Y', 'Y']]
    setpoint = loop_obj()
    
    setpoint.add_data(np.linspace(1,len(allXY_set), len(allXY_set)), axis=-1, labels = 'ALL XY gate id', units='#')

def generate_all_XY(segment, gate_set, axis=-1):
    '''
    generate allXY experiment

    Args:
        segment (segment_container) : container of the segments
        gate_set (single_qubit_gate_spec) : object containg instruction of the gate set
    '''
    ALLXY.setpoint.axis = [axis]

    getattr(segment, gate_set.qubit).update_dim(ALLXY.setpoint)

    for i in range(ALLXY.setpoint.data.size):
        gate_set.load_std_gate(getattr(segment, gate_set.qubit)[i], ALLXY.allXY_set[i])

if __name__ == '__main__':
    from pulse_templates.coherent_control.single_qubit_gates.standard_set import single_qubit_std_set
    from pulse_templates.coherent_control.single_qubit_gates.single_qubit_gates import single_qubit_gate_spec
    from pulse_templates.demo_pulse_lib.virtual_awg import get_demo_lib
    from pulse_templates.utility.plotting import plot_seg
    from pulse_lib.segments.utility.looping import linspace
    pulse = get_demo_lib('quad')
    seg = pulse.mk_segment()
    xpi2 = single_qubit_gate_spec('qubit4_MW', 1e9+ linspace(0,50,20, axis=0), 100, 120)
    xpi = single_qubit_gate_spec('qubit4_MW', 1e9+ linspace(0,50,20, axis=0), 200, 120)
    ss_set = single_qubit_std_set()
    ss_set.X = xpi2
    ss_set.X2 = xpi

    generate_all_XY(seg, ss_set,0)
    plot_seg(seg, [1])
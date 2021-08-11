from pulse_lib.segments.utility.looping import loop_obj, linspace
import numpy as np

def get_allXY_specs(repeat):
    allXY_set = repeat * [['I', 'I'], ['X2', 'X2'], ['Y2', 'Y2'], ['X2', 'Y2'], ['Y2', 'X2'],
                            ['X', 'I'], ['Y', 'I'], ['X', 'Y'], ['X', 'Y'], ['X', 'Y2'], ['Y', 'X2'], ['X2', 'Y'], ['Y2', 'X'], ['X', 'X2'], ['X2', 'X'], ['Y', 'Y2'],
                            ['Y2', 'Y'], ['X2', 'I'], ['Y2', 'I'], ['X', 'X'], ['Y', 'Y']]
    setpoint = loop_obj()
    
    setpoint.add_data(np.linspace(1,len(allXY_set), len(allXY_set)), axis=0, labels = 'ALL XY gate id', units='#')
    return allXY_set, setpoint

def generate_all_XY(segment, gate_set, repeat = 1, axis=0):
    '''
    generate allXY experiment

    Args:
        segment (segment_container) : container of the segments
        gate_set (single_qubit_gate_spec) : object containg instruction of the gate set
        repeat (int) : the number of time to repeat the allxy experiment =
    '''

    allXY_set, setpoint = get_allXY_specs(repeat)
    setpoint.axis = [axis]

    getattr(segment, gate_set.qubit).update_dim(setpoint)

    for i in range(setpoint.data.size):
        gate_set.load_std_gate(getattr(segment, gate_set.qubit)[i], allXY_set[i])

if __name__ == '__main__':
    from pulse_templates.coherent_control.single_qubit_gates.standard_set import single_qubit_std_set
    from pulse_templates.coherent_control.single_qubit_gates.single_qubit_gates import single_qubit_gate_spec
    from pulse_templates.demo_pulse_lib.virtual_awg import get_demo_lib
    from pulse_templates.utility.plotting import plot_seg
    from pulse_lib.segments.utility.looping import linspace
    pulse = get_demo_lib('six')
    seg = pulse.mk_segment()

    ss_set = single_qubit_std_set()
    ss_set.X =  single_qubit_gate_spec('qubit4_MW', 1e9, 100, 120)
    # ss_set.X2 = single_qubit_gate_spec('qubit4_MW', 1e9, 200, 120)

    # ss_set.X.add(seg)
    print(seg)
    generate_all_XY(seg, ss_set)
    plot_seg(seg, 1)
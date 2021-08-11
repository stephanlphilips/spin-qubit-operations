from state_tomography.utility import generate_reduced_measurement_basis_str
from pulse_lib.segments.utility.looping import loop_obj, linspace
import numpy as np

def generate_measurement_operators(n_qubits):
    '''
    collects the expected measurement basis from the state tomography library and converts them in single qubit operations (only measurement in ZZ assumed)
    
    Args:
        n_qubits (int) : number of qubits to generate the gates for
    '''
    reformatted_operators = []
    meas_operators = generate_reduced_measurement_basis_str(n_qubits)
    for i in meas_operators:
        i ='_'.join(i)
        i.replace('X', 'mY90')
        i.replace('Y', 'X90')
        reformatted_operators.append(i)

    return reformatted_operators

def generate_state_tomography(segment, *qubits, repeat = 1,axis=0):
    '''
    perform a state tomography on the given qubits

    Args:
        segment (segment_container) : container of the segments
        *qubits  (single_qubit_gate_spec) : gate spec of the qubits to be targetted
        axis (int) : axis where this tomography should run on
    '''
    m_operators = generate_measurement_operators(len(qubits))*repeat
    setpoint = loop_obj()
    setpoint.add_data(np.linspace(1,len(m_operators), len(m_operators)), axis=axis, labels = 'State Tomography projection', units='#')

    for i in range(len(qubits)):
        segment[qubits[i].qubit].update_dim(setpoint)

    for i in range(setpoint.data.size):
        gates = m_operators[i].split('_')

        for j in range(len(qubits)):
            if gates[j] != 'I':
                qubits[j].load_std_gate(segment[i], gates[j])
                

if __name__ == '__main__':
    from pulse_templates.coherent_control.single_qubit_gates.standard_set import single_qubit_std_set
    from pulse_templates.coherent_control.single_qubit_gates.single_qubit_gates import single_qubit_gate_spec
    from pulse_templates.demo_pulse_lib.virtual_awg import get_demo_lib
    from pulse_templates.utility.plotting import plot_seg
    from pulse_lib.segments.utility.looping import linspace

    import matplotlib.pyplot as plt
    from core_tools.data.SQL.connect import set_up_local_storage

    set_up_local_storage('stephan', 'magicc', 'test', "project_name", "set_up_name", "sample_name")
    
    pulse = get_demo_lib('six')
    seg = pulse.mk_segment()

    ss_set4 = single_qubit_std_set()
    ss_set4.X =  single_qubit_gate_spec('qubit4_MW', 1e8, 100, 120)

    ss_set3 = single_qubit_std_set()
    ss_set3.X =  single_qubit_gate_spec('qubit3_MW', 3e8, 30, 240)
    # ss_set.X2 = single_qubit_gate_spec('qubit4_MW', 1e9, 200, 120)
    print('executing test')
    print(generate_measurement_operators(2))
    # ss_set.X.add(seg)
    generate_state_tomography(seg, ss_set3, ss_set4, axis=0)
    
    # print('test done')
    
    for i in range(9):
        plot_seg(seg, i)

    # plt.show()

# simple scrip that measures phase offsets because of the  drive of another qubit.
from pulse_lib.segments.utility.looping import loop_obj, linspace
import numpy as np

def phase_offset_charac(seg, gate_set_qubit_1, gate_to_test=None, npoints = 100, axis = 0):
    '''
    detects for example start shifts on other qubits due due to a drive
    '''
    gate_set_qubit_1.X.build(seg, phase_corrections = {})
    
    if gate_to_test is not None:
        if isinstance(gate_to_test, list):
            for gate in gate_to_test:
                gate.build(seg, phase_corrections = {})
        else:
            gate_to_test.build(seg, phase_corrections = {})   

    gate_set_qubit_1.Z(linspace(0,np.pi*4, npoints, axis=axis, name='Phase shift', unit='rad')).build(seg)
    gate_set_qubit_1.X.build(seg, phase_corrections = {})


if __name__ == '__main__':
    from pulse_templates.coherent_control.single_qubit_gates.standard_set import single_qubit_std_set
    from pulse_templates.coherent_control.single_qubit_gates.single_qubit_gates import single_qubit_gate_spec
    from pulse_templates.demo_pulse_lib.virtual_awg import get_demo_lib
    from pulse_templates.utility.plotting import plot_seg
    from pulse_lib.segments.utility.looping import linspace
    pulse = get_demo_lib('six')
    seg = pulse.mk_segment()

    X90 = single_qubit_gate_spec('qubit4_MW', 1e9, 200, 120, padding = 20,)
    ss_set = single_qubit_std_set()
    ss_set.X = X90

    test_pulse = single_qubit_gate_spec('qubit2_MW', 1e9, 200, 120, padding = 20,  phase_corrections= {'qubit4_MW' : 1*np.pi})

    phase_offset_charac(seg, ss_set, test_pulse, 0)
    plot_seg(seg)
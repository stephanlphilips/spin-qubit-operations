from pulse_templates.coherent_control.RB_single.randomised_benchmarking_definitions import single_qubit_gates_clifford_set, pauli_I
from pulse_templates.coherent_control.RB_generic.RB_mgr import RB_mgr
from pulse_lib.segments.utility.looping import linspace

def generature_single_qubit_RB(segment, gate_set, n_gates, n_rand, RB_type='XZ', interleave=None, seed=None):
    '''
    generate a RB sequence for a single qubit.

    Args:
        segment (segment_container) : container of the segments
        gate_set (load_set_single_qubit) : object containg instruction of the gate set
        n_gates (lp.loopobj) : x axis of the RB plot
        n_rand (int) : number of repetition for each n in n_gates
        RB_type (str) : 'XY' or 'XZ', which type of gate should be used for this RB
        interleave (gate) : gate of gate_set (e.g. gate_set.X)
        seed (int) : seed number to start from (if you want to generate multiple times the same RB sequence)
    '''
    # make sure current dimensions are applied (-- overwrite user specs)
    n_gates.axis= [0]
    n_gates.name='N Cliffords'
    n_gates.unit='#'
    rand = linspace(1, n_rand, n_rand, axis = [1], name='Nth rep', unit='#' )
    
    getattr(segment, gate_set.qubit).update_dim(rand)
    getattr(segment, gate_set.qubit).update_dim(n_gates)

    RB_mgmt = RB_mgr(gate_set, RB_type, seed)
    
    for n in range(n_rand):
        for m in range(n_gates.data.size):
            RB_mgmt.add_cliffords(getattr(segment, gate_set.qubit)[n,m], int(n_gates.data[m]))

if __name__ == '__main__':
    from pulse_templates.coherent_control.RB_single.randomised_benchmarking_definitions import load_set_single_qubit
    from pulse_templates.coherent_control.single_qubit_gates import single_qubit_gate_spec
    from pulse_templates.demo_pulse_lib.virtual_awg import get_demo_lib
    from pulse_templates.utility.plotting import plot_seg

    pulse = get_demo_lib('quad')
    seg = pulse.mk_segment()
    xpi2 = single_qubit_gate_spec('qubit4_MW', 1e9, 100, 120)
    xpi = single_qubit_gate_spec('qubit4_MW', 1e9, 200, 120)
    ss_set = load_set_single_qubit()
    ss_set.X = xpi2
    ss_set.X2 = xpi

    IQ_channel = getattr(seg, ss_set.qubit)
    generature_single_qubit_RB(seg, ss_set, linspace(5,50,10), 10)
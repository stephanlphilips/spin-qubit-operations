from pulse_templates.coherent_control.randomised_benchmarking_definitions_single_qubit_gates import single_qubit_gates_clifford_set, pauli_I

from pulse_lib.segments.utility.looping import linspace

def generature_single_qubit_RB(segment, RB_type, gate_set, n_gates, n_rand, seed=None):
	'''
	generate a RB sequence for a single qubit.

	Args:
		segment (segment_container) : container of the segments
		RB_type (str) : 'XY' or 'XZ', which type of gate should be used for this RB
		gate_set (single_qubit_gate_set) : object containg instruction of the gate set
		n_gates (np.ndarray) : x axis of the RB plot
		n_rand (int) : number of random gates to excecute for
		seed (int) : seed number to start from (if you want to generate multiple times the same RB sequence)
	'''

	n_gates = linspace(start, stop)
	rand = linspace(1, n_rand, n_rand)

	getattr(segment, gate_set.qubit).update_dim(n_gates)
	getattr(segment, gate_set.qubit).update_dim(n_rand)

	
	for n in range(n_rand):
		for m in range(n_gates.size):
			current_matrix = pauli_I
			for i in range(n_gates[m]):
				gate_set = get_rand
				seg[n,m].add(gate_seq)
				current_matrix *= gate_set

			inv_gate = gate_set.get_inv()
			seg[n,m].add(inv_gate)


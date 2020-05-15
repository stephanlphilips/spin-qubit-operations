import random
import copy

class RB_mgr:
    '''
    Function that loads RB sequences
    '''
    def __init__(self, gate_set, mode, seed=None):
        '''
        init rb manager
        
        Args:
            gate_set (TODO :: make parent type) :  set of gate to be used in the RB sequence
            mode (str) : mode for single qubit gates (e.g. allow Z gates) ('XY'/'XZ')
            seed (int) : seed to start from, if None : system clock will be used
        '''
        self.gate_set = gate_set
        
        self.mode = mode
        random.seed(seed)

    def add_cliffords(self, segment, N):
        '''
        adds a random gate to the segment

        Args:
            segment (segment)
            N (int) : number of random cliffords to add
            interleave (str) : gate to add to interleave (TODO)
        '''

        matrix = copy.deepcopy(self.gate_set.qubit_set.PAULI_I.matrix)

        for i in range(N-1):
            rand = random.randrange(0, self.gate_set.size)
            matrix *= self.gate_set.load_clifford_gate(segment, rand, self.mode)

        self.gate_set.load_inverting_clifford(segment, matrix, self.mode)


if __name__ == '__main__':
    from pulse_templates.coherent_control.single_qubit_gates.standard_set import single_qubit_std_set
    from pulse_templates.coherent_control.single_qubit_gates.single_qubit_gates import single_qubit_gate_spec
    from pulse_templates.demo_pulse_lib.virtual_awg import get_demo_lib
    from pulse_templates.utility.plotting import plot_seg

    pulse = get_demo_lib('quad')
    seg = pulse.mk_segment()

    xpi2 = single_qubit_gate_spec('qubit4_MW', 1e9, 100, 120)
    xpi = single_qubit_gate_spec('qubit4_MW', 1e9, 200, 120)
    ss_set = single_qubit_std_set()
    ss_set.X = xpi2
    ss_set.X2 = xpi

    seg_single = getattr(seg, ss_set.qubit)
    rb_managment = RB_mgr(ss_set, 'XY')
    rb_managment.add_cliffords(seg_single, 20)
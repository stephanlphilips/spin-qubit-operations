import random
import copy

class RB_mgr:
    '''
    Function that loads RB sequences
    '''
    def __init__(self, load_set, mode, seed=None):
        self.load_set = load_set
        
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

        matrix = copy.deepcopy(self.load_set.qubit_set.PAULI_I.matrix)

        for i in range(N-1):
            rand = random.randrange(0, self.load_set.size)
            matrix *= self.load_set.load_clifford_gate(segment, rand, self.mode)

        self.load_set.load_inverting_clifford(segment, matrix, self.mode)


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

    rb_managment = RB_mgr(ss_set, 'XY')
    rb_managment.add_cliffords(seg, 20)
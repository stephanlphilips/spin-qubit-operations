class RB_mgr:
    '''
    Function that load rb sequences
    '''
    def __init__(self, load_set, mode, seed=None):
        self.load_set = load_set
        self.load_set.check_gate_availability(mode)
        
        self.mode = mode
        random.seed(seed)

    def add_cliffords(self, segment, N):
        '''
        adds a random gate to the segment

        Args:
            segment (segment)
            N
        '''
        
        rand = random.randrange(0, self.load_set.size)

    def __add__inverse(self, segment, matrix):
        '''
        add the inverse gate to the end the sequence

        Args:
            segment (segment) :
            matrix (np.ndarray) : unitary of the previous sequence
        '''
        pass

rb_managment = RB_mgr(load_set_single_qubit(), 'XY')
rb_managment.add_rand_clifford(5)
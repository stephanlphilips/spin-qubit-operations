from pulse_templates.coherent_control.RB_single.RB_definitions import single_qubit_gates_clifford_set
from pulse_templates.coherent_control.single_qubit_gates.single_qubit_gates import single_qubit_gate_spec, _load_single_qubit_gate, single_qubit_gate_simple, gate_sequence_spec
from pulse_lib.segments.segment_container import segment_container

import numpy as np
import copy

class gate_descriptor:
    def __init__(self, ref_gate = None, amp = None, add_phase = 0, add_glob_phase = 0):
        self.gate_name = None
        if not isinstance(ref_gate, tuple):
            ref_gate = (ref_gate, )
        self.ref = ref_gate
        self.amp = amp
        self.add_phase = add_phase
        self.add_glob_phase = add_glob_phase
    
    def __set_name__(self, owner, name):
        self.name = name
        self.private_name = '_' + name

    def __set__(self, owner, gate_specification):
        if isinstance(gate_specification, single_qubit_gate_spec):
            setattr(gate_specification, '_segment_generator', getattr(owner, 'segment_generator'))
            setattr(owner, self.private_name, gate_specification)
        else: 
            raise ValueError('please assign the correct type to the gate (single_qubit_gate_spec type), current type is {}'.format(str(type(gate_specification))))

    def __get__(self, owner, objtype=None):
        if self.ref is None and not hasattr(owner, self.private_name):
            raise ValueError("Unable to get {}, gate undefined, please add it to the set.".format(self.gate_name))

        if not hasattr(owner, self.private_name):
            g = gate_sequence_spec([])
            for ref in self.ref:
                gate_obj = copy.copy(getattr(owner, ref))
                if self.amp is not None:
                    gate_obj.MW_power = self.amp

                gate_obj.permanent_phase_shift += self.add_glob_phase
                gate_obj.phase += self.add_phase
                g+= gate_obj
            return g

        return getattr(owner, self.private_name)

class single_qubit_std_set():
    '''
    Make a set to generate all the clifford for the single qubit RB.

    Type for the gates : 
        pulse_templates.coherent_control.single_qubit_gates.single_qubit_gate_spec

    Minimal gates to define
        * X and X2
        * the reset will be derived from the others
    '''
    # NMR notation
    I = gate_descriptor('X', amp = 0)
    X = gate_descriptor()
    Y = gate_descriptor('X', add_phase=np.pi/2)
    Z = gate_descriptor('X', amp = 0, add_glob_phase=np.pi/2)

    mX = gate_descriptor('X', add_phase=-np.pi)
    mY = gate_descriptor('X', add_phase=-np.pi/2)
    mZ = gate_descriptor('X', amp = 0, add_glob_phase=-np.pi/2)

    X2 = gate_descriptor(('X', 'X'))
    Y2 = gate_descriptor('X2', add_phase=np.pi/2)
    Z2 = gate_descriptor('X', amp = 0, add_glob_phase=np.pi)

    mX2 = gate_descriptor('X2', add_phase=-np.pi)
    mY2 = gate_descriptor('X2', add_phase=-np.pi/2)
    mZ2 = gate_descriptor('X', amp = 0, add_glob_phase=-np.pi)

    # transmon notation
    X90 = gate_descriptor('X')
    Y90 = gate_descriptor('X90', add_phase=np.pi/2)
    Z90 = gate_descriptor('X90', amp = 0, add_glob_phase=np.pi/2)

    mX90 = gate_descriptor('X90', add_phase=-np.pi)
    mY90 = gate_descriptor('X90', add_phase=-np.pi/2)
    mZ90 = gate_descriptor('X90', amp = 0, add_glob_phase=-np.pi/2)

    X180 = gate_descriptor(('X90', 'X90'))
    Y180 = gate_descriptor('X180', add_phase=np.pi/2)
    Z180 = gate_descriptor('X90', amp = 0, add_glob_phase=np.pi)

    mX180 = gate_descriptor('X180', add_phase=-np.pi)
    mY180 = gate_descriptor('X180', add_phase=-np.pi/2)
    mZ180 = gate_descriptor('X90', amp = 0, add_glob_phase=-np.pi)


    qubit_set = single_qubit_gates_clifford_set()
    size = len(qubit_set)

    def __init__(self, segment_generator=None):
        self.segment_generator = segment_generator

    def load_std_gate(self, segment, gate_name):
        '''
        load a standard gate defined in this object

        Args:
            segment (segment) : segment to which to add
            gate_name (str/list) : load gate
        '''
        if isinstance(gate_name, str):
            gate_name = [gate_name]

        for gate in gate_name:
            if isinstance(segment, segment_container):
                single_qubit_gate_simple(segment, getattr(self, gate))
            else:
                _load_single_qubit_gate(segment, getattr(self, gate))


    def load_clifford_gate(self, segment, clifford_number, mode):
        '''
        load a clifford to the segment (as the clifford is one of the gates defined in the RB set)

        Args:
            segment (segment) : segment to which to add
            clifford_number (int) : number of the clifford to load in qubit_set
            mode (str) : XY / XZ composed cliffords

        Returns:
            matrix (np.matrix) : matrix corresponding to the gate has been added
        '''
        clifford = self.qubit_set[clifford_number]

        seq = clifford.elementary_gates_XY if mode=='XY' else clifford.elementary_gates_XZ
        for gate in seq:
            _load_single_qubit_gate(segment, getattr(self, gate))

        return clifford.matrix

    def load_inverting_clifford(self, segment, matrix, mode):
        '''
        load invert gate defined in the RB set

        Args:
            segment (segment) : segment to which to add
            matrix (np.matrix) : unitary of all the gates that happened before
            mode (str) : XY / XZ composed cliffords
        '''
        clifford_number = self.qubit_set.get_inverting_gate(matrix)
        self.load_clifford_gate(segment, clifford_number, mode)

    def wait(self, segment, t_wait):
        '''
        wait t ns and then reset the time for the current channel
        
        Args:
            segment (segment) : segment to which to add
            time (double) : time to wait 
        '''
        getattr(segment, self.qubit).wait(t_wait) 
        getattr(segment, self.qubit).reset_time()
    
    @property
    def qubit(self):
        return self.X.qubit_name

if __name__ == '__main__':
    from pulse_templates.utility.plotting import plot_seg
    from pulse_templates.demo_pulse_lib.virtual_awg import get_demo_lib

    from pulse_templates.coherent_control.single_qubit_gates.single_qubit_gates import single_qubit_gate_spec


    pulse = get_demo_lib('quad')
    seg = pulse.mk_segment()
    
    test = single_qubit_std_set()
    test.X = single_qubit_gate_spec('qubit1_MW', 1e9, 100, MW_power=500, padding = 10)
    # test.wait(seg, 100)
    # create custom Z with custom phase -- 
    # test.Z(3.14).add(seg, f_qubit=1.12e9)
    # print(test.Z)
    # a = test.Z


    # print(test.Z(0))
    # test.Z(0).add(seg)
    # # test.Y2.add(seg)
    test.X180.add(seg)

    print('start second gate')
    # print(test.X)
    # print(test.X90)
    test.Y180.add(seg)

    plot_seg(seg)

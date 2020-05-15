from pulse_templates.coherent_control.RB_single.RB_definitions import single_qubit_gates_clifford_set
from pulse_templates.coherent_control.single_qubit_gates.single_qubit_gates import single_qubit_gate_spec, _load_single_qubit_gate, single_qubit_gate_simple
from pulse_lib.segments.segment_container import segment_container

import copy
class gate_descriptor:
    def __init__(self, ref_gate = None, amp = None, add_phase = 0, add_glob_phase = 0):
        self.gate_name = None
        self.ref = ref_gate
        self.amp = amp
        self.add_phase = add_phase
        self.add_glob_phase = add_glob_phase

    def __get__(self, instance, owner):
        gate_obj = instance.__dict__.get(self.gate_name, None)
        if gate_obj is None and self.ref is None:
            raise ValueError("Unable to get {}, gate undefined, please add it to the set.".format(self.gate_name))

        if gate_obj is None:
            gate_obj = copy.copy(instance.__dict__.get(self.ref, None))
            if self.amp is not None:
                gate_obj.MW_power = self.amp
            gate_obj.permanent_phase_shift += self.add_glob_phase
            gate_obj.phase += self.add_phase

        return gate_obj
    
    def __set__(self, instance, value):
        if not isinstance(value, single_qubit_gate_spec):
            raise ValueError('please assign the correct type to the gate (single_qubit_gate_spec type), current type is {}'.format(str(type(value))))
        instance.__dict__[self.gate_name] = value

class descriptor_mgr(type):
    def __new__(cls, name, bases, attrs):
        for name, value in attrs.items():
            if isinstance(value, gate_descriptor):
                value.gate_name = name
        return super(descriptor_mgr, cls).__new__(cls, name, bases, attrs)

class single_qubit_std_set(metaclass=descriptor_mgr):
    '''
    Make a set to generate all the clifford for the single qubit RB.

    Type for the gates : 
        pulse_templates.coherent_control.single_qubit_gates.single_qubit_gate_spec

    Minimal gates to define
        * X and X2
        * the reset will be derived from the others
    '''
    I = gate_descriptor('X', amp = 0)
    X = gate_descriptor()
    Y = gate_descriptor('X', add_phase=90)
    Z = gate_descriptor('X', amp = 0, add_glob_phase=90)
    
    mX = gate_descriptor('X', add_phase=-180)
    mY = gate_descriptor('X', add_phase=-90)
    mZ = gate_descriptor('X', amp = 0, add_glob_phase=-90)
    
    X2 = gate_descriptor()
    Y2 = gate_descriptor('X2', add_phase=90)
    Z2 = gate_descriptor('X', amp = 0, add_glob_phase=180)
    
    mX2 = gate_descriptor('X2', add_phase=-180)
    mY2 = gate_descriptor('X2', add_phase=-90)
    mZ2 = gate_descriptor('X', amp = 0, add_glob_phase=-180)

    qubit_set = single_qubit_gates_clifford_set()
    size = len(qubit_set)

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

    @property
    def qubit(self):
        return self.X.qubit_name
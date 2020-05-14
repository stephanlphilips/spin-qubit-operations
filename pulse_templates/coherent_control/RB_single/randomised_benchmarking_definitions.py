from pulse_templates.coherent_control.RB_single.unitaries_help_func import pauli_I, pauli_X, pauli_Y, pauli_Z, rot_mat
from pulse_templates.coherent_control.single_qubit_gates import single_qubit_gate_spec, _load_single_qubit_gate
from dataclasses import dataclass, field

import numpy as np
import random
import copy

@dataclass
class elem_gate:
    name : str
    mat  : np.ndarray

class elem_gates:
    I = elem_gate('I', rot_mat(0, [0,0,0]))

    X = elem_gate('X', rot_mat(np.pi/2, [1,0,0]))
    Y = elem_gate('Y', rot_mat(np.pi/2, [0,1,0]))
    Z = elem_gate('Z', rot_mat(np.pi/2, [0,0,1]))
    
    mX = elem_gate('-X', rot_mat(-np.pi/2, [1,0,0]))
    mY = elem_gate('-Y', rot_mat(-np.pi/2, [0,1,0]))
    mZ = elem_gate('-Z', rot_mat(-np.pi/2, [0,0,1]))
    
    X2 = elem_gate('X2', rot_mat(np.pi, [1,0,0]))
    Y2 = elem_gate('Y2', rot_mat(np.pi, [0,1,0]))
    Z2 = elem_gate('Z2', rot_mat(np.pi, [0,0,1]))

    def __getitem__(self, item):
        return getattr(self, item).mat

@dataclass
class single_qubit_gate_DS:
    human_readable_descript : str
    elementary_gates_XY : list
    elementary_gates_XZ : list
    matrix : np.matrix = None

    def __post_init__(self):
        self.elementary_gates_XY = self.__post_format(self.elementary_gates_XY)
        self.elementary_gates_XZ = self.__post_format(self.elementary_gates_XZ)

        my_elem_gates = elem_gates()
        self.matrix = copy.deepcopy(pauli_I)
        for i in self.elementary_gates_XY:
            self.matrix *= my_elem_gates[i]

    def __post_format(self, gates):
        new_names = []
        for gate in gates:
            new_names.append(gate.replace('-', 'm'))

        return new_names

class single_qubit_gates_clifford_set(object):
    """
    Clifford set for single qubit gates
    taken from Xiao Xue et al., PRX, 2019
    """
    qubit_set = list()

    qubit_set.append(single_qubit_gate_DS('PAULI_I', ['I'], ['X', '-X']))
    qubit_set.append(single_qubit_gate_DS('PAULI_X', ['X2'], ['X2']))
    qubit_set.append(single_qubit_gate_DS('PAULI_Y', ['Y2'], ['-Z', 'X2', 'Z']))
    qubit_set.append(single_qubit_gate_DS('PAULI_Z', ['Y2', 'X2'], ['X', 'Z2', 'X']))

    qubit_set.append(single_qubit_gate_DS('2pi/3_1', ['X', 'Y'], ['X', '-Z', 'X', 'Z']))
    qubit_set.append(single_qubit_gate_DS('2pi/3_2', ['X', '-Y'], ['X', 'Z', 'X', '-Z']))
    qubit_set.append(single_qubit_gate_DS('2pi/3_3', ['-X', 'Y'], ['-X', '-Z', 'X', 'Z']))
    qubit_set.append(single_qubit_gate_DS('2pi/3_4', ['-X', '-Y'], ['-X', 'Z', 'X', '-Z']))
    qubit_set.append(single_qubit_gate_DS('2pi/3_5', ['Y', 'X'], ['-Z', 'X', 'Z', 'X']))
    qubit_set.append(single_qubit_gate_DS('2pi/3_6', ['Y', '-X'], ['-Z', 'X', 'Z', '-X']))
    qubit_set.append(single_qubit_gate_DS('2pi/3_7', ['-Y', 'X'], ['Z', 'X', '-Z', 'X']))
    qubit_set.append(single_qubit_gate_DS('2pi/3_8', ['-Y', '-X'], ['Z', 'X', '-Z', '-X']))

    qubit_set.append(single_qubit_gate_DS('pi/2_1', ['X'], ['-Z', 'X', 'Z', 'X', '-Z']))
    qubit_set.append(single_qubit_gate_DS('pi/2_2', ['-X'], ['Z', '-X', '-Z', '-X', 'Z']))
    qubit_set.append(single_qubit_gate_DS('pi/2_3', ['Y'], ['X', 'Z', '-X']))
    qubit_set.append(single_qubit_gate_DS('pi/2_4', ['-Y'], ['X', '-Z', '-X']))
    qubit_set.append(single_qubit_gate_DS('pi/2_5', ['-X', 'Y', 'X'], ['-X', 'Z2', '-X', '-Z']))
    qubit_set.append(single_qubit_gate_DS('pi/2_6', ['-X', '-Y', 'X'], ['-X', '-Z2', '-X', 'Z']))

    qubit_set.append(single_qubit_gate_DS('Hadamard_1', ['X2', 'Y'], ['X', '-Z', 'X']))
    qubit_set.append(single_qubit_gate_DS('Hadamard_2', ['X2', '-Y'], ['X', 'Z', 'X']))
    qubit_set.append(single_qubit_gate_DS('Hadamard_3', ['Y2', 'X'], ['-Z', 'X', 'Z', 'X', 'Z']))
    qubit_set.append(single_qubit_gate_DS('Hadamard_4', ['Y2', '-X'], ['-Z', 'X', 'Z', '-X', '-Z']))
    qubit_set.append(single_qubit_gate_DS('Hadamard_5', ['X', 'Y', 'X'], ['X2', 'Z']))
    qubit_set.append(single_qubit_gate_DS('Hadamard_6', ['-X', 'Y', '-X'], ['-X2', '-Z']))

    def __init__(self):
        for gate in self.qubit_set:
            setattr(self, gate.human_readable_descript, gate)

    def __len__(self):
        return len(self.qubit_set)

    def __getitem__(self, item):
        return self.get_gate(item)

    def get_gate(self, N):
        if N>len(self):
            raise ValueError('Requested gate does not exist in this qubit set?')

        return self.qubit_set[N]

    def get_inverting_gate(self, matrix):
        for i in range(len(self)):
            end_oper = matrix*np.matrix(np.linalg.inv(self[i].matrix))
            end_oper *= np.exp(-1j*np.angle(end_oper[0,0]))
            
            return i

        raise ValueError("Error RB -- no inverting gate found. Is there an error in the set/it it uncomplete?")

def check_def(load_set, gates):
    for gate in gates:
        if getattr(load_set, gate) is None:
            raise ValueError('gate {} not defined in the clifford gate set. Please specify in order to run RB'.format(gate))

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

class load_set_single_qubit(metaclass=descriptor_mgr):
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
        '''
        _load_single_qubit_gate(segment, getattr(self, gate_name))


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
    
if __name__ == '__main__':
    from pulse_templates.demo_pulse_lib.virtual_awg import get_demo_lib
    from pulse_templates.utility.plotting import plot_seg

    pulse = get_demo_lib('quad')
    seg = pulse.mk_segment()

    xpi2 = single_qubit_gate_spec('qubit4_MW', 1e9, 100, 120)
    xpi = single_qubit_gate_spec('qubit4_MW', 1e9, 200, 120)
    ss_set = load_set_single_qubit()
    ss_set.X = xpi2
    ss_set.X2 = xpi

    k = ss_set.load_clifford_gate(seg, 20, 'XY')
    print(k)

    ss_set.qubit_set.get_inverting_gate(k)
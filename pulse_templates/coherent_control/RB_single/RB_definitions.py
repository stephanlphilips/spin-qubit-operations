from pulse_templates.coherent_control.RB_single.unitaries_help_func import pauli_I, pauli_X, pauli_Y, pauli_Z, rot_mat
from pulse_templates.coherent_control.single_qubit_gates.single_qubit_gates import single_qubit_gate_spec, _load_single_qubit_gate
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
        total_gate = self[0].matrix
        for i in range(len(self)):
            # end_oper = matrix*np.matrix(np.linalg.inv(self[i].matrix))
            end_oper = matrix.dot(self[i].matrix)
            end_oper *= np.exp(-1j*np.angle(end_oper[0,0]))
            end_oper =  end_oper.round(10) # FPE's
            if (end_oper == total_gate).all():
                return i
        raise ValueError("Error RB -- no inverting gate found. Is there an error in the set/it it uncomplete?")

if __name__ == '__main__':
    from pulse_templates.demo_pulse_lib.virtual_awg import get_demo_lib
    from pulse_templates.utility.plotting import plot_seg
    from pulse_templates.coherent_control.single_qubit_gates.standard_set import single_qubit_std_set
    
    pulse = get_demo_lib('quad')
    seg = pulse.mk_segment()

    xpi2 = single_qubit_gate_spec('qubit4_MW', 1e9, 100, 120)
    xpi = single_qubit_gate_spec('qubit4_MW', 1e9, 200, 120)
    std_set = single_qubit_std_set()
    std_set.X = xpi2
    std_set.X2 = xpi

    seg_single = getattr(seg, std_set.qubit)
    k = std_set.load_clifford_gate(seg_single, 5, 'XY')
    l = std_set.load_clifford_gate(seg_single, 3, 'XY')
    m = k*l
    a = std_set.qubit_set.get_inverting_gate(m)
    b = single_qubit_gates_clifford_set()
    print(b[a].elementary_gates_XY)
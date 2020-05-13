from pulse_templates.coherent_control.RB_single.unitaries_help_func import pauli_I, pauli_X, pauli_Y, pauli_Z, rot_mat

from dataclasses import dataclass, field
import numpy as np
import random

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

	def __getitem__(self, gate):
		gate =  gate.replace('-', 'm')
		return getattr(self, gate).mat

@dataclass
class single_qubit_gate_DS:
	human_readable_descript : str
	elementary_gates_XY : list
	elementary_gates_XY : list
	matrix : np.matrix = None

	def __post_init__(self):
		my_elem_gates = elem_gates()
		self.matrix = pauli_I
		for i in self.elementary_gates_XY:
			self.matrix *= my_elem_gates[i]


single_qubit_gate_DS('PAULI_I', ['I'], ['X', '-X'])

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

	def __len__(self):
		return len(self.qubit_set)

def check_def(load_set, gates):
	for gate in gates:
		if getattr(load_set, gate) is None:
			raise ValueError('gate {} not defined in the clifford gate set. Please specify in order to run RB'.format(gate))

class load_set_single_qubit:
	I = None
	X = None
	Y = None
	Z = None
	mX = None
	mY = None
	mZ = None
	X2 = None
	Y2 = None
	Z2 = None

	self.qubit_set = single_qubit_gates_clifford_set()
	self.size = len(self.qubit_set)

	def check_gate_availability(self, mode):
		for char in list(mode):
			gates = [char, 'm' + char, char + '2']
			check_def(self, gates)

	def load_gate(self, gate):
		pass


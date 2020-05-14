from dataclasses import dataclass, field
import numpy as np
import random

pauli_I = np.matrix([[1,0],[0,1]], dtype=complex)
pauli_X = np.matrix([[0,1],[1,0]], dtype=complex)
pauli_Y = np.matrix([[0,-1j],[1j,0]], dtype=complex)
pauli_Z = np.matrix([[1,0],[0,-1]], dtype=complex)

def rot_mat(theta, unit_vector):
	'''
	Generate a rotation unitary for an angle theta.

	Args:
		theta (double) : angle to rotate
		unit_vector (list) : list with the vector of rotation (XYZ)
	'''
	mat = (np.cos(theta/2)*pauli_I - 
			1j*np.sin(theta/2)*(unit_vector[0]*pauli_X +
								unit_vector[1]*pauli_Y +
								unit_vector[2]*pauli_Z
								)
			)
	return mat
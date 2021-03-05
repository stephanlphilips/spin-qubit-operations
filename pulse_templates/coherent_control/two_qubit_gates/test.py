import numpy as np


def theta(J, delta_B):
	return 3*np.pi*J/np.sqrt(J**2 + delta_B**2)

def solve(angle, delta_B):
	return abs(np.sqrt(delta_B**2*angle**2/((3*np.pi)**2 - angle**2)))

def t_ramp(J_max, delta_B):
	return 3/np.sqrt(J_max**2 + delta_B**2)

def integrate_array(array):
	integral = np.zeros(array.shape)
	for i in range(1,array.size):
		integral[i] = integral[i-1] + array[i]
	return integral

a = (5,)
b = (5,6)
print(tuple(a))
print(tuple(b))
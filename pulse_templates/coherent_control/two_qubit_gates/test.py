import numpy as np


def theta(J, delta_B):
	return 3*np.pi*J/np.sqrt(J**2 + delta_B**2)

def solve(angle, delta_B):
	return abs(np.sqrt(delta_B**2*angle**2/((3*np.pi)**2 - angle**2)))

def t_ramp(J_max, delta_B):
	return 3/np.sqrt(J_max**2 + delta_B**2)

db = 100e6
ang = np.pi

J_max = solve(ang, db)
print(J_max*1e-6)

print(theta(J_max, db))
print(t_ramp(J_max, db)*1e9)
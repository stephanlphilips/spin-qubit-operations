from pulse_templates.examples.two_qubit_PSB.var import gates
from pulse_templates.examples.two_qubit_PSB.basic_oper import do_EMPTY, do_LOAD, do_READ, do_MANIP

from pulse_templates.coherent_control.single_qubit_gates.standard_set import single_qubit_std_set
from pulse_templates.coherent_control.single_qubit_gates.single_qubit_gates import single_qubit_gate_spec

from pulse_templates.coherent_control.two_qubit_gates.cphase import cphase_basic

def make_sequence():
	EMPTY = do_EMPTY()
	LOAD = do_LOAD()
	MANIP = do_MANIP()
	READ = do_READ()

	# Example of defining a single qubit gates:
	X_q1 = single_qubit_gate_spec('qubit1_MW', 
									11.0998e9,
									174, 400, padding=10)
	
	X2_q1 = single_qubit_gate_spec('qubit1_MW', 
									11.0998e9,
									320, 400, padding=10)

	qubit1_ss_set = single_qubit_std_set()
	qubit1_ss_set.X = X_q1
	qubit1_ss_set.X2 = X2_q1


	# adding single qubit gates:
	qubit1_ss_set.X.add(MANIP) # add 90 degree around X
	qubit1_ss_set.Y2.add(MANIP) # add 180 degree around Y

	# Example of adding a two qubit gate:
	
	# voltages at the symm point
	vP1 =  6
	vP2 =  -4
	exhange_value =  180

	# time of the gate
	t_exchange = 80

	cphase_basic(MANIP, gates, (0,vP1,30,vP2,0), (0,vP1,exhange_value,vP2,0), t_exchange, 10)

	# correct phase on the qubit
	qubit1_ss_set.Z(0.23).add(MANIP)

	return [EMPTY, LOAD, MANIP, READ]


if __name__ == '__main__':
	from pulse_templates.utility.plotting import plot_seg
	from pulse_templates.demo_pulse_lib.virtual_awg import get_demo_lib
	import qcodes as qc

	station = qc.Station()
	pulse = get_demo_lib('quad')
	station.pulse = pulse

	EMPTY, LOAD, MANIP, READ = make_sequence()

	plot_seg(MANIP)

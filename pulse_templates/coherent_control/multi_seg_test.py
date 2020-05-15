'''
test for testing multisegment concatenation
'''

from pulse_templates.utility.plotting import plot_seg
from pulse_templates.demo_pulse_lib.virtual_awg import get_demo_lib
from pulse_templates.utility.oper import add_block, add_ramp
from pulse_templates.utility.plotting import plot_seg

from pulse_templates.coherent_control.single_qubit_gates.standard_set import single_qubit_std_set
from pulse_templates.coherent_control.single_qubit_gates.single_qubit_gates import single_qubit_gate_spec
from pulse_templates.elzerman_pulses.basic_elzerman_pulse import elzerman_read

pulse = get_demo_lib('quad')

INIT = pulse.mk_segment()
MANIP = pulse.mk_segment()
READ = pulse.mk_segment()

# assume 1QD -- elzerman init
t_init = 50e3
gates = ('vP1',)
p_0 = (200, )

add_block(INIT, t_init, gates, p_0)
#done.

# add single qubit gates in manip

# add default dc levels
MANIP.vP1 += 50

# define a set 
xpi2 = single_qubit_gate_spec('qubit1_MW', 1.1e8, 1000, 120, padding=2)
xpi = single_qubit_gate_spec('qubit1_MW', 1.1e8, 2000, 120, padding=2)

ss_set = single_qubit_std_set()
ss_set.X = xpi2
ss_set.X2 = xpi

ss_set.X.add(MANIP)
ss_set.X.add(MANIP)
ss_set.Y.add(MANIP)


# assume 1QD -- elzerman read -- simplified
t_read = 50e3
gates = ('vP1',)
p_readout = (-100, )

elzerman_read(READ, gates, t_read, p_readout)
#done.


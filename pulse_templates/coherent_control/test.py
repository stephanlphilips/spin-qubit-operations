import pulse_lib.segments.utility.looping as lp

from pulse_templates.coherent_control.single_qubit_gates.standard_set import single_qubit_std_set
from pulse_templates.coherent_control.single_qubit_gates.single_qubit_gates import single_qubit_gate_spec
from pulse_templates.demo_pulse_lib.virtual_awg import get_demo_lib
from pulse_templates.utility.plotting import plot_seg

pulse = get_demo_lib('quad')
seg = pulse.mk_segment()

xpi2 = single_qubit_gate_spec('qubit1_MW', 1.1e8, 100, 120, padding=2)
xpi = single_qubit_gate_spec('qubit1_MW', 1.1e8, 200, 120, padding=2)
ss_set = single_qubit_std_set()
ss_set.X = xpi2
ss_set.X2 = xpi
pulse.IQ_channels[0].virtual_channel_map[0].reference_frequency = 1.1e8


ss_set.X.add(seg)
ss_set.X.add(seg)
ss_set.Y.add(seg)
ss_set.Z.add(seg)
ss_set.X2.add(seg)
plot_seg(seg)
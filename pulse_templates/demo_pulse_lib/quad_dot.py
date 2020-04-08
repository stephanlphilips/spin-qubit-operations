import V2_software.drivers.virtual_gates.instrument_drivers.harware as hw
from pulse_lib.base_pulse import pulselib
from pulse_lib.virtual_channel_constructors import IQ_channel_constructor, virtual_gates_constructor

import numpy as np


class hardware(hw.harware_parent):

    def __init__(self, name):
        super().__init__(name, "_settings_quad_dot")

        virtual_gate_set_1 =  hw.virtual_gate('general',["B0", "P1", "B1", "P2", "B2", "P3", "B3", "P4", "B4", "S1", "S2", "SD1_P", "SD2_P"  ])
        self.virtual_gates.append(virtual_gate_set_1)

def return_pulse_lib_quad_dot():
	"""
	return pulse library object

	Returns:
		pulse : pulse lib main class
	"""
	pulse = pulselib(backend = "DEMO")

	# define channels
	pulse.define_channel('B0','AWG1', 1)
	pulse.define_channel('P1','AWG1', 2)
	pulse.define_channel('B1','AWG1', 3)
	pulse.define_channel('P2','AWG1', 4)
	pulse.define_channel('B2','AWG2', 1)
	pulse.define_channel('P3','AWG2', 2)
	pulse.define_channel('B3','AWG2', 3)
	pulse.define_channel('P4','AWG2', 4)
	pulse.define_channel('B4','AWG3', 1)
	pulse.define_channel('SD1_P','AWG3', 3)
	pulse.define_channel('SD2_P','AWG3', 4)

	quad_hardware = hardware('test')
	pulse.load_hardware(quad_hardware)
	
	return pulse



if __name__ == '__main__':
	pulse = return_pulse_lib_quad_dot()
	print(pulse.channels)
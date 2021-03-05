import core_tools.drivers.harware as hw
from pulse_lib.base_pulse import pulselib
from pulse_lib.virtual_channel_constructors import IQ_channel_constructor, virtual_gates_constructor

import numpy as np


class hardware(hw.harware_parent):

    def __init__(self, name):
        super().__init__(name, "_settings_quad_dot_")

        virtual_gate_set_1 =  hw.virtual_gate('general',["B0", "P1", "B1", "P2", "B2", "P3", "B3", "P4", "B4", "P5", "B5", "P6", "B6", "S1", "S6", "SD1_P", "SD2_P"  ])
        self.virtual_gates.append(virtual_gate_set_1)

def return_pulse_lib():
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
    pulse.define_channel('P5','AWG3', 2)
    pulse.define_channel('B5','AWG3', 3)
    pulse.define_channel('P6','AWG3', 4)
    # pulse.define_channel('B6','AWG4', 1)
    pulse.define_channel('S6','AWG4', 2)
    pulse.define_channel('SD1_P','AWG4', 3)
    pulse.define_channel('SD2_P','AWG4', 4)

    pulse.define_channel('I_MW','AWG5', 1)
    pulse.define_channel('Q_MW','AWG5', 2)
    pulse.define_marker('M1','AWG5', 3)
    pulse.define_channel('M2','AWG6', 2)
    pulse.define_channel('SCOPE1','AWG6', 2)

    six_dot_hardware = hardware('test')
    pulse.load_hardware(six_dot_hardware)

    IQ_chan_set_1 = IQ_channel_constructor(pulse)
    # set right association of the real channels with I/Q output.
    IQ_chan_set_1.add_IQ_chan("I_MW", "I")
    IQ_chan_set_1.add_IQ_chan("Q_MW", "Q")
    IQ_chan_set_1.add_marker("M1", 30, 30)
    IQ_chan_set_1.set_LO(11.25e9)
    IQ_chan_set_1.add_virtual_IQ_channel('qubit1_MW', LO_freq=11.0)
    IQ_chan_set_1.add_virtual_IQ_channel('qubit2_MW', LO_freq=11.1)
    IQ_chan_set_1.add_virtual_IQ_channel('qubit3_MW', LO_freq=11.2)
    IQ_chan_set_1.add_virtual_IQ_channel('qubit4_MW', LO_freq=11.3)
    IQ_chan_set_1.add_virtual_IQ_channel('qubit5_MW', LO_freq=11.4)
    IQ_chan_set_1.add_virtual_IQ_channel('qubit6_MW', LO_freq=11.5)
    IQ_chan_set_1.add_virtual_IQ_channel('pre_pulse', LO_freq=11.5)

    # just to make qcodes happy
    six_dot_hardware.close()
    
    return pulse



if __name__ == '__main__':
    pulse = return_pulse_lib()
    print(pulse.channels)
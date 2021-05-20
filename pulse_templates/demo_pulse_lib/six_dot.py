from core_tools.drivers.hardware.hardware import hardware
from pulse_lib.base_pulse import pulselib
from pulse_lib.virtual_channel_constructors import IQ_channel_constructor, virtual_gates_constructor

import numpy as np


def return_pulse_lib(hw=None):
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
    pulse.define_marker('M1','AWG5', 0)
    pulse.define_marker('M2','AWG6', 0)
    pulse.define_marker('M_SD1','AWG1', 0)
    pulse.define_marker('M_SD2','AWG2', 0)
    pulse.define_channel('SCOPE1','AWG6', 2)

    pulse.define_digitizer_channel_iq('SD1_IQ', 'Dig1', [1, 2])
    pulse.define_digitizer_channel_iq('SD2_IQ', 'Dig1', [3, 4])


    if hw is None:
        hw = hardware()
        hw.virtual_gates.add('general',["B0", "P1", "B1", "P2", "B2", "P3", "B3", "P4", "B4", "P5", "B5", "P6", "B6", "S1", "S6", "SD1_P", "SD2_P"  ])

    pulse.load_hardware(hw)

    IQ_chan_set_1 = IQ_channel_constructor(pulse)
    # set right association of the real channels with I/Q output.
    IQ_chan_set_1.add_IQ_chan("I_MW", "I")
    IQ_chan_set_1.add_IQ_chan("Q_MW", "Q")
    IQ_chan_set_1.add_marker("M1")
    IQ_chan_set_1.set_LO(11.25e9)
    IQ_chan_set_1.add_virtual_IQ_channel('qubit1_MW', LO_freq=11.0)
    IQ_chan_set_1.add_virtual_IQ_channel('qubit2_MW', LO_freq=11.1)
    IQ_chan_set_1.add_virtual_IQ_channel('qubit3_MW', LO_freq=11.2)
    IQ_chan_set_1.add_virtual_IQ_channel('qubit4_MW', LO_freq=11.3)
    IQ_chan_set_1.add_virtual_IQ_channel('qubit5_MW', LO_freq=11.4)
    IQ_chan_set_1.add_virtual_IQ_channel('qubit6_MW', LO_freq=11.5)
    IQ_chan_set_1.add_virtual_IQ_channel('pre_pulse', LO_freq=11.5)

    
    return pulse



if __name__ == '__main__':
    from core_tools.data.SQL.connect import set_up_local_storage
    set_up_local_storage("xld_user", "XLDspin001", "vandersypen_data", "6dot", "XLD", "6D2S - SQ21-XX-X-XX-X")

    pulse = return_pulse_lib()

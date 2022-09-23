from pulse_templates.coherent_control.single_qubit_gates.single_qubit_gates import single_qubit_gate_spec
from pulse_templates.coherent_control.single_qubit_gates.standard_set import single_qubit_std_set

from pulse_templates.coherent_control.two_qubit_gates.cphase import cphase_basic
from pulse_templates.coherent_control.two_qubit_gates.standard_set import two_qubit_std_set, two_qubit_gate_generic

from pulse_templates.oper.operators import wait

from pulse_templates.psb_pulses.readout_standard_set import readout_spec, readout_std_set
from pulse_templates.psb_pulses.readout_pulses import PSB_read
from pulse_templates.psb_pulses.readout_template import ReadoutTemplate

from pulse_templates.measurement.measurement import measurement, MeasurementSet
from pulse_templates.coherent_control.wait import wait_std_set

from pulse_templates.utility.sequence_template import SequenceTemplate
from pulse_templates.utility.conditional_template import Conditional
from pulse_templates.utility.simultaneous_template import SimultaneousTemplate

from pulse_lib.sequence_builder import sequence_builder, builder_policy



class six_dot_sample:
    def __init__(self, pulse):
#        pulse.q1.LO = 11.002e9

        self.wait = wait_std_set(gates=('P1',), p_0=(0,))
        self.q1 = single_qubit_std_set()
        self.q1.X = single_qubit_gate_spec('qubit1_MW', 11.002e9, 100, MW_power=5, gate_name='X')
#        self.q1.X2 = single_qubit_gate_spec('qubit1_MW', 11.002e9, 200, MW_power=5, gate_name='X2')

        self.q2 = single_qubit_std_set()
        self.q2.X = single_qubit_gate_spec('qubit2_MW', 11.103e9, 100, MW_power=5, gate_name='X')
#        self.q2.X2 = single_qubit_gate_spec('qubit2_MW', 11.103e9, 200, MW_power=5, gate_name='X2')

        self.q3 = single_qubit_std_set()
        self.q3.X = single_qubit_gate_spec('qubit3_MW', 11.201e9, 150, MW_power=5, gate_name='X')
#        self.q3.X2 = single_qubit_gate_spec('qubit3_MW', 11.201e9, 200, MW_power=5, gate_name='X2')

        self.q4 = single_qubit_std_set()
        self.q4.X = single_qubit_gate_spec('qubit4_MW', 11.303e9, 100, MW_power=5, gate_name='X')
#        self.q4.X2 = single_qubit_gate_spec('qubit4_MW', 11.303e9, 200, MW_power=5, gate_name='X2')

        self.q5 = single_qubit_std_set()
        self.q5.X = single_qubit_gate_spec('qubit5_MW', 11.405e9, 100, MW_power=5, gate_name='X')
#        self.q5.X2 = single_qubit_gate_spec('qubit5_MW', 11.405e9, 200, MW_power=5, gate_name='X2')

        self.q6 = single_qubit_std_set()
        self.q6.X = single_qubit_gate_spec('qubit6_MW', 11.508e9, 100, MW_power=5, gate_name='X')
#        self.q6.X2 = single_qubit_gate_spec('qubit6_MW', 11.508e9, 200, MW_power=5, gate_name='X2')


        cphase12 = two_qubit_gate_generic(cphase_basic, {'gates' : ('vP1','vB1', 'vP2'),
                                    'v_exchange_pulse_off' : (0,4,0),
                                    'v_exchange_pulse_on' : (0,8,0),
                                    't_gate' : 100,
                                    't_ramp' : 20},
                 {'qubit1_MW' : 0.231, 'qubit2_MW' : 0.802})

        self.q12 = two_qubit_std_set(self.q1, self.q2)
        self.q12.cphase = cphase12

        cphase23 = two_qubit_gate_generic(cphase_basic, {'gates' : ('vP2','vB2', 'vP3'),
                                    'v_exchange_pulse_off' : (0,4,0),
                                    'v_exchange_pulse_on' : (0,8,0),
                                    't_gate' : 100,
                                    't_ramp' : 20},
                 {'qubit2_MW' : 0.232, 'qubit3_MW' : 0.803})

        self.q23 = two_qubit_std_set(self.q2, self.q3)
        self.q23.cphase = cphase23

        cphase34 = two_qubit_gate_generic(cphase_basic, {'gates' : ('vP3','vB3', 'vP4'),
                                    'v_exchange_pulse_off' : (0,4,0),
                                    'v_exchange_pulse_on' : (0,8,0),
                                    't_gate' : 100,
                                    't_ramp' : 20},
                 {'qubit3_MW' : 0.233, 'qubit4_MW' : 0.804})

        self.q34 = two_qubit_std_set(self.q3, self.q4)
        self.q34.cphase = cphase34

        cphase45 = two_qubit_gate_generic(cphase_basic, {'gates' : ('vP4','vB4', 'vP5'),
                                    'v_exchange_pulse_off' : (0,4,0),
                                    'v_exchange_pulse_on' : (0,8,0),
                                    't_gate' : 100,
                                    't_ramp' : 20},
                 {'qubit4_MW' : 0.234, 'qubit5_MW' : 0.805})

        self.q45 = two_qubit_std_set(self.q4, self.q5)
        self.q45.cphase = cphase45

        cphase56 = two_qubit_gate_generic(cphase_basic, {'gates' : ('vP5','vB5', 'vP6'),
                                    'v_exchange_pulse_off' : (0,4,0),
                                    'v_exchange_pulse_on' : (0,8,0),
                                    't_gate' : 100,
                                    't_ramp' : 20},
                 {'qubit5_MW' : 0.235, 'qubit6_MW' : 0.806})

        self.q56 = two_qubit_std_set(self.q5, self.q6)
        self.q56.cphase = cphase56




        measure_12 = measurement(channel='SD1_IQ', t_measure=2e3, threshold=0.5)
        measure_56 = measurement(channel='SD2_IQ', t_measure=2e3, threshold=0.5)

        self.psb12 = ReadoutTemplate(
                PSB_read,
                measurement=measure_12,
                t_ramp=2e3,
                gates=('vP1','vB1', 'vP2'),
                p_0=(0,0,0),
                p_1=(5.5,0,-5.5)
                )

        self.psb56 = ReadoutTemplate(
                PSB_read,
                measurement=measure_56,
                t_ramp=2e3,
                gates=('vP5','vB5', 'vP6'),
                p_0=(0,0,0),
                p_1=(-5.5,0,5.5)
                )


        m = MeasurementSet()
        _init12 = m.add('init12', self.psb12, accept=0)
        _init3 = m.add('init3', self.psb12, accept=0)
        _init56 = m.add('init56', self.psb56, accept=0)
        _init4 = m.add('init4', self.psb56, accept=0)

        self.init12 = _init12

        self.init3 = SequenceTemplate(
                self.wait(100),
                self.q23.CNOT21,
                self.wait(100),
                _init3,
                )

        self.init123 = SequenceTemplate(
                _init12,
                self.wait(100),
                self.q23.CNOT12,
                self.wait(100),
                _init3,
                )

        self.init56 = _init56
        self.init4 = SequenceTemplate(
                self.wait(100),
                self.q45.CNOT12,
                self.wait(100),
                _init4,
                )


        _read12 = m.add('read12', self.psb12)
        _read12_cnot3 = m.add('read12_cnot3', self.psb12) # raw value and result value match
        _read3 = m.add('read3', m['read12'] ^ m['read12_cnot3']) # no raw value, only result

        _read12_cnot1 = m.add('read12_cnot1', self.psb12)
        _read1 = m.add('read1', m['read12'] ^ m['read12_cnot1']) # q1 = 1 if parity changed
        _read2 = m.add('read2', m['read12'] & m['read12_cnot1']) # q2 = 1 if odd parity in both measurements

        _read56 = m.add('read56', self.psb56)
        _read56_cnot4 = m.add('read56_cnot4', self.psb56)
        _read4 = m.add('read4', m['read56'] ^ m['read56_cnot4'])
        _read56_cnot6 = m.add('read56_cnot6', self.psb56)
        _read5 = m.add('read5', m['read56'] & m['read56_cnot6'])
        _read6 = m.add('read6', m['read56'] ^ m['read56_cnot6'])

        self.m_vote = m.majority_vote('majority', [_read4, _read5, _read6], 0.6)

        self.read12 = _read12
        self.read3 = SequenceTemplate(
                self.wait(100),
                self.q23.CNOT12,
                self.wait(100),
                _read12_cnot3,
                _read3,
                )

#        self.read123 = SequenceTemplate(
#                _read12,
#                self.wait(100),
#                self.q23.CNOT12,
#                self.wait(100),
#                _read12_cnot3,
#                _read3,
#                )

        self.read1 = SequenceTemplate(
                self.wait(100),
                self.q12.CNOT12,
                self.wait(100),
                _read12_cnot1,
                _read1,
                )
        self.read2 = SequenceTemplate(
                self.wait(100),
                self.q12.CNOT12,
                self.wait(100),
                _read12_cnot1,
                _read2,
                )

        self.read56 = _read56

        self.read4 = SequenceTemplate(
                self.wait(100),
                self.q45.CNOT12,
                self.wait(100),
                _read56_cnot4,
                _read4,
                )

        self.read5 = SequenceTemplate(
                self.wait(100),
                self.q56.CNOT21,
                self.wait(100),
                _read56_cnot6,
                _read5,
                )
        self.read6 = SequenceTemplate(
                self.wait(100),
                self.q56.CNOT21,
                self.wait(100),
                _read56_cnot6,
                _read6,
                )


#        # with correction
        _read12 = m.add('read12_b', self.psb12)

        _read12_cnot_q3_q2 = m.add('read12_cnot_q3_q2', self.psb12)

        _fix_123 = Conditional((m['read12_b'], m['read12_cnot_q3_q2']),
                               None, # (0,0)
                               [self.q2.X2, self.q3.X2], # (0,1)
                               self.q3.X2, # (1,0)
                               self.q2.X2, # (1,1)
                               )
#        _fix_q2 = Conditional(m['read12_cnot_q3_q2'],
#                               None, # (0,0)
#                               self.q2.X2, # (0,1)
#                               )
#        _fix_q3 = Conditional((m['read12'], m['read12_cnot_q3_q2']),
#                               None, # (0,0)
#                               self.q3.X2, # (0,1)
#                               self.q3.X2, # (1,0)
#                               None, # (1,1)
#                               )

        self.init123 = SequenceTemplate(
                _read12,
                self.wait(100),
                self.q23.CNOT21,
                self.wait(100),
                _read12_cnot_q3_q2,
                self.wait(620),
                _fix_123,
                )

#
#        # QEC
#
#        _read12 = m.add('read12', self.psb12)
#        _read23 = m.add('read23', self.psb23)
#
#        _fix_parity = Conditional((m['read12'], m['read23']),
#                                  None, # (0,0)
#                                  self.q3.X2, # (0,1)
#                                  self.q1.X2, # (1,0)
#                                  self.q2.X2, # (1,1)
#                                  )
#
#        self.qec = SequenceTemplate(
#                _read12,
#                _read23,
#                _fix_parity,
#                )
#
## --------

# ===
import logging
from pprint import pprint
import qcodes
import matplotlib.pyplot as pt

import pulse_lib.segments.utility.looping as lp
import core_tools.drivers.harware as hw
from pulse_lib.base_pulse import pulselib
from pulse_lib.virtual_channel_constructors import IQ_channel_constructor, virtual_gates_constructor

from pulse_lib.tests.mock_m3202a import MockM3202A_fpga
from pulse_lib.tests.mock_m3202a_qs import MockM3202A_QS
from pulse_lib.tests.mock_m3102a_qs import MockM3102A_QS
from pulse_lib.tests.hw_schedule_mock import HardwareScheduleMock

import qcodes.logger as logger
from qcodes.logger import start_all_logging


start_all_logging()
logger.get_file_handler().setLevel(logging.DEBUG)
try:
    qcodes.Instrument.close_all()
except: pass

class hardware(hw.harware_parent):

    def __init__(self, name):
        super().__init__(name, "_settings_6dotQS_dot")

        virtual_gate_set_1 =  hw.virtual_gate('general',
                                              ["B0", "P1", "B1", "P2", "B2", "P3", "B3", "P4", "B4",
                                               "P5", "B5", "P6", "B6", "S1", "S2", "SD1_P", "SD2_P"  ])
        self.virtual_gates.append(virtual_gate_set_1)

def return_pulse_lib(awgs, dig):
    """
    return pulse library object

    Returns:
        pulse : pulse lib main class
    """
    pulse = pulselib(backend = 'Keysight_QS')
    for awg in awgs:
        pulse.add_awg(awg)
    pulse.add_digitizer(dig)

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
    pulse.define_channel('B6','AWG4', 1)
    pulse.define_channel('SD1_P','AWG4', 3)
    pulse.define_channel('SD2_P','AWG4', 4)

    pulse.define_channel('I_MW1','AWG5', 1)
    pulse.define_channel('Q_MW1','AWG5', 2)
    pulse.define_marker('M1','AWG4', 0, setup_ns=60, hold_ns=60, amplitude=6)

    pulse.define_channel('I_MW2','AWG5', 3)
    pulse.define_channel('Q_MW2','AWG5', 4)
    pulse.define_marker('M2','AWG5', 0, setup_ns=60, hold_ns=60)

    pulse.define_digitizer_channel_iq('SD1_IQ', 'Dig1', [1, 2])
    pulse.define_digitizer_channel_iq('SD2_IQ', 'Dig1', [3, 4])

    six_dot_hardware = hardware('test')
    pulse.load_hardware(six_dot_hardware)

    IQ_chan_set_1 = IQ_channel_constructor(pulse)
    LO1 = 11.25e9
    # set right association of the real channels with I/Q output.
    IQ_chan_set_1.add_IQ_chan("I_MW1", "I")
    IQ_chan_set_1.add_IQ_chan("Q_MW1", "Q")
    IQ_chan_set_1.add_marker("M1")
    IQ_chan_set_1.set_LO(LO1)
    IQ_chan_set_1.add_virtual_IQ_channel('qubit1_MW', LO_freq=11.002e9)
    IQ_chan_set_1.add_virtual_IQ_channel('qubit2_MW', LO_freq=11.103e9)
    IQ_chan_set_1.add_virtual_IQ_channel('qubit3_MW', LO_freq=11.201e9)

    IQ_chan_set_2 = IQ_channel_constructor(pulse)
    LO2 = 11.25e9
    # set right association of the real channels with I/Q output.
    IQ_chan_set_2.add_IQ_chan("I_MW2", "I")
    IQ_chan_set_2.add_IQ_chan("Q_MW2", "Q")
    IQ_chan_set_2.add_marker("M2")
    IQ_chan_set_2.set_LO(LO2)
    IQ_chan_set_2.add_virtual_IQ_channel('qubit4_MW', LO_freq=11.303e9)
    IQ_chan_set_2.add_virtual_IQ_channel('qubit5_MW', LO_freq=11.405e9)
    IQ_chan_set_2.add_virtual_IQ_channel('qubit6_MW', LO_freq=11.508e9)

    # just to make qcodes happy
    six_dot_hardware.close()
    pulse.finish_init()

    return pulse


def plot(seq, job, awgs):
#    uploader = seq.uploader
    print(f'sequence: {seq.shape}')
    print(f'job index:{job.index}, sequences:{len(job.sequence)}')
    print(f'  sample_rate:{job.default_sample_rate} playback_time:{job.playback_time}')

    fig = pt.figure()
    fig.clear()

    for awg in awgs:
        awg.plot()

    pt.legend()
    pt.show()
    pt.ylim(-0.007, 0.007)


awgs = []
for i in range(1,5):
    awg = MockM3202A_fpga(f'AWG{i}', 1, i+1, marker_amplitude=6)
    awgs.append(awg)

awg5 = MockM3202A_QS(f'AWG5', 1, 6, marker_amplitude=6)
#awg5 = MockM3202A_fpga(f'AWG5', 1, 6, marker_amplitude=6)
awgs.append(awg5)

dig = MockM3102A_QS("Dig1", 0, 9)

pulse = return_pulse_lib(awgs, dig)
seg = pulse.mk_segment()

s = six_dot_sample(pulse)

seq = sequence_builder(pulse)#, policy=builder_policy.TinySegments)


seq.add(s.init12)

seq.add(s.wait(1e3))
seq.add(s.q1.X90)
seq.add(s.q2.X90)
seq.add(s.wait(1e3))
seq.add(SimultaneousTemplate(s.q1.X90, s.q2.X90))
seq.add(s.wait(1e3))
seq.add(SimultaneousTemplate(s.q1.X90, SequenceTemplate(s.wait(50), s.q2.X90)))

seq.add(s.wait(1e3))

my_seq = seq.forge()
my_seq.measurements_description.describe()
my_seq.set_hw_schedule(HardwareScheduleMock())
job = my_seq.upload()

my_seq.play(release=False)

awg5.describe()
dig.describe()
#pprint(job.upload_info)
plot(my_seq, job, [awgs[3],awg5])

my_seq.play(release=True)
my_seq.uploader.release_jobs()




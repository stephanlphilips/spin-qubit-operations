from pulse_templates.coherent_control.single_qubit_gates.single_qubit_gates import single_qubit_gate_spec
from pulse_templates.coherent_control.single_qubit_gates.standard_set import single_qubit_std_set

from pulse_templates.coherent_control.two_qubit_gates.cphase import cphase_basic
from pulse_templates.coherent_control.two_qubit_gates.standard_set import two_qubit_std_set, two_qubit_gate_generic

from pulse_templates.psb_pulses.readout_standard_set import readout_spec, readout_std_set
from pulse_templates.psb_pulses.readout_pulses import PSB_read

from pulse_templates.utility.measurement import measurement_manager, measurement
from pulse_templates.utility.segment_manager import segment_mgr

class six_dot_sample:
    def __init__(self, pulse):
        self.measurement_manager = measurement_manager()
        self.segment_mgr = segment_mgr(pulse)

        i_12 = measurement('PSB_12_init', chan=[1,2], accept=0, threshold=0.5, phase=0.3)
        init12_kwargs = {'gates' : ('vP1','vB1', 'vP2'), 't_ramp' : 2e3, 
                't_read' : 2e3, 'p_0' : (0,0,0), 'p_1' : (5.5,0,-5.5)}
        readout_spec_12 = readout_spec(i_12, PSB_read, init12_kwargs)
        self.init12 = readout_std_set(readout_spec_12, self.measurement_manager, self.segment_mgr)
        # self.init3  =
        # self.init4  = 
        # self.init56 =

        r_12 = measurement('PSB_12_init', chan=[1,2], threshold=0.5, phase=0.3)
        readout_spec_12 = readout_spec(r_12, PSB_read, init12_kwargs)
        self.read12_ZZ = readout_std_set(readout_spec_12, self.measurement_manager, self.segment_mgr)
        # self.read56_ZZ
        # self.read1
        # self.read2
        # self.read3
        # self.read4
        # self.read5
        # self.read6

        self.q1 = single_qubit_std_set(self.segment_mgr)
        self.q1.X = single_qubit_gate_spec('qubit1_MW', 1e9, 100, MW_power=5)
        self.q1.X2 = single_qubit_gate_spec('qubit1_MW', 1e9, 200, MW_power=5)

        self.q2 = single_qubit_std_set(self.segment_mgr)
        self.q2.X = single_qubit_gate_spec('qubit2_MW', 1e9, 100, MW_power=5)
        self.q2.X2 = single_qubit_gate_spec('qubit2_MW', 1e9, 200, MW_power=5)
        
        # self.q3 = ..
        # self.q4
        # self.q5
        # self.q6

        cphase12 = two_qubit_gate_generic(cphase_basic, {'gates' : ('vP1','vB1', 'vP2'), 
                                    'v_exchange_pulse_off' : (0,4,0),
                                    'v_exchange_pulse_on' : (0,8,0),
                                    't_gate' : 100,
                                    't_ramp' : 20},
                 {'qubit1_MW' : 0.23, 'qubit2_MW' : 0.8})

        self.q12 = two_qubit_std_set(self.q1, self.q2, self.segment_mgr)
        self.q12.cphase = cphase12

        # self.q23 = ..
        # self.q34
        # self.q45
        # self.q56

    def wait(self, time):
        pass

    def segment(self):
        return segment


from pulse_templates.demo_pulse_lib.virtual_awg import get_demo_lib

pulse = get_demo_lib('quad')
s = six_dot_sample(pulse)

s.init12.add()
s.init56.add()
s.init3.add()
s.init4.add()

# do a rabi on qubit 1
s.wait(5e3)
s.q2.X.add(time = lp.linspace(0, 1e3, 50, axis=0))

# do a cnot to qubit 3
s.q23.CNOT12.add()
s.q34.CNOT12.add()
s.q45.CNOT12.add()

s.wait(5e3)

s.read12.add()
s.read3.add(flip='qubit12')
s.read56.add()
s.read4.add(flip='qubit56')

run_PSB_exp(s)
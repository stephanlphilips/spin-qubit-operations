from pulse_templates.coherent_control.single_qubit_gates.single_qubit_gates import single_qubit_gate_spec
from pulse_templates.coherent_control.single_qubit_gates.standard_set import single_qubit_std_set

from pulse_templates.coherent_control.two_qubit_gates.cphase import cphase_basic
from pulse_templates.coherent_control.two_qubit_gates.standard_set import two_qubit_std_set, two_qubit_gate_generic

from pulse_templates.oper.operators import wait

from pulse_templates.psb_pulses.readout_standard_set import readout_spec, readout_std_set
from pulse_templates.psb_pulses.readout_pulses import PSB_read

from pulse_templates.utility.measurement import measurement_manager, measurement
from pulse_templates.utility.segment_manager import segment_mgr

from pulse_templates.coherent_control.wait import wait_std_set
from pulse_templates.utility.plotting import plot_seg

class six_dot_sample:
    def __init__(self, pulse):
        self.measurement_manager = measurement_manager()
        self.segment_mgr = segment_mgr(pulse)

        self.wait = wait_std_set(self.segment_mgr, gates=('P1',), p_0=(0,))
        self.q1 = single_qubit_std_set(self.segment_mgr)
        self.q1.X = single_qubit_gate_spec('qubit1_MW', 11.002e9, 100, MW_power=5)
        self.q1.X2 = single_qubit_gate_spec('qubit1_MW', 11.002e9, 200, MW_power=5)

        self.q2 = single_qubit_std_set(self.segment_mgr)
        self.q2.X = single_qubit_gate_spec('qubit2_MW', 11.103e9, 100, MW_power=5)
        self.q2.X2 = single_qubit_gate_spec('qubit2_MW', 11.103e9, 200, MW_power=5)
        
        self.q3 = single_qubit_std_set(self.segment_mgr)
        self.q3.X = single_qubit_gate_spec('qubit3_MW', 11.201e9, 100, MW_power=5)
        self.q3.X2 = single_qubit_gate_spec('qubit3_MW', 11.201e9, 200, MW_power=5)

        self.q4 = single_qubit_std_set(self.segment_mgr)
        self.q4.X = single_qubit_gate_spec('qubit4_MW', 11.303e9, 100, MW_power=5)
        self.q4.X2 = single_qubit_gate_spec('qubit4_MW', 11.303e9, 200, MW_power=5)
        
        self.q5 = single_qubit_std_set(self.segment_mgr)
        self.q5.X = single_qubit_gate_spec('qubit5_MW', 11.405e9, 100, MW_power=5)
        self.q5.X2 = single_qubit_gate_spec('qubit5_MW', 11.405e9, 200, MW_power=5)

        self.q6 = single_qubit_std_set(self.segment_mgr)
        self.q6.X = single_qubit_gate_spec('qubit6_MW', 11.508e9, 100, MW_power=5)
        self.q6.X2 = single_qubit_gate_spec('qubit6_MW', 11.508e9, 200, MW_power=5)


        cphase12 = two_qubit_gate_generic(cphase_basic, {'gates' : ('vP1','vB1', 'vP2'), 
                                    'v_exchange_pulse_off' : (0,4,0),
                                    'v_exchange_pulse_on' : (0,8,0),
                                    't_gate' : 100,
                                    't_ramp' : 20},
                 {'qubit1_MW' : 0.23, 'qubit2_MW' : 0.8})

        self.q12 = two_qubit_std_set(self.q1, self.q2, self.segment_mgr)
        self.q12.cphase = cphase12

        cphase23 = two_qubit_gate_generic(cphase_basic, {'gates' : ('vP2','vB2', 'vP3'), 
                                    'v_exchange_pulse_off' : (0,4,0),
                                    'v_exchange_pulse_on' : (0,8,0),
                                    't_gate' : 100,
                                    't_ramp' : 20},
                 {'qubit2_MW' : 0.23, 'qubit3_MW' : 0.8})

        self.q23 = two_qubit_std_set(self.q2, self.q3, self.segment_mgr)
        self.q23.cphase = cphase23

        cphase34 = two_qubit_gate_generic(cphase_basic, {'gates' : ('vP3','vB3', 'vP4'), 
                                    'v_exchange_pulse_off' : (0,4,0),
                                    'v_exchange_pulse_on' : (0,8,0),
                                    't_gate' : 100,
                                    't_ramp' : 20},
                 {'qubit3_MW' : 0.23, 'qubit4_MW' : 0.8})

        self.q34 = two_qubit_std_set(self.q3, self.q4, self.segment_mgr)
        self.q34.cphase = cphase34

        cphase45 = two_qubit_gate_generic(cphase_basic, {'gates' : ('vP4','vB4', 'vP5'), 
                                    'v_exchange_pulse_off' : (0,4,0),
                                    'v_exchange_pulse_on' : (0,8,0),
                                    't_gate' : 100,
                                    't_ramp' : 20},
                 {'qubit4_MW' : 0.23, 'qubit5_MW' : 0.8})

        self.q45 = two_qubit_std_set(self.q4, self.q5, self.segment_mgr)
        self.q45.cphase = cphase45

        cphase56 = two_qubit_gate_generic(cphase_basic, {'gates' : ('vP5','vB5', 'vP6'), 
                                    'v_exchange_pulse_off' : (0,4,0),
                                    'v_exchange_pulse_on' : (0,8,0),
                                    't_gate' : 100,
                                    't_ramp' : 20},
                 {'qubit5_MW' : 0.23, 'qubit6_MW' : 0.8})

        self.q56 = two_qubit_std_set(self.q5, self.q6, self.segment_mgr)
        self.q56.cphase = cphase56


        i_12 = measurement('PSB_12_init', chan=[1,2], accept=0, threshold=0.5, phase=0.3)
        init12_kwargs = {'gates' : ('vP1','vB1', 'vP2'), 't_ramp' : 2e3, 
                't_read' : 2e3, 'p_0' : (0,0,0), 'p_1' : (5.5,0,-5.5)}
        init_spec_12 = readout_spec(i_12, PSB_read, init12_kwargs)
        self.init12 = readout_std_set(init_spec_12, self.measurement_manager, self.segment_mgr)

        i_3 = measurement('PSB_3_init', chan=[1,2], accept=0, threshold=0.5, phase=0.3)
        init_spec_3 = readout_spec(i_3, PSB_read, init12_kwargs, (self.wait(100), self.q23.CNOT12, self.wait(100),))
        self.init3  = readout_std_set(init_spec_3, self.measurement_manager, self.segment_mgr)
        
        i_56 = measurement('PSB_56_init', chan=[3,4], accept=0, threshold=0.5, phase=0.3)
        init56_kwargs = {'gates' : ('vP5','vB5', 'vP6'), 't_ramp' : 2e3, 
                't_read' : 2e3, 'p_0' : (0,0,0), 'p_1' : (-5.5,0,5.5)}
        init_spec_56 = readout_spec(i_56, PSB_read, init56_kwargs)
        self.init56 = readout_std_set(init_spec_56, self.measurement_manager, self.segment_mgr)
        
        i_4 = measurement('PSB_4_init', chan=[1,2], accept=0, threshold=0.5, phase=0.3)
        init_spec_4 = readout_spec(i_4, PSB_read, init56_kwargs, (self.wait(100), self.q45.CNOT21, self.wait(100),))
        self.init4  = readout_std_set(init_spec_4, self.measurement_manager, self.segment_mgr)

        

        r_12 = measurement('read12', chan=[1,2], threshold=0.5, phase=0.3)
        readout_spec_12 = readout_spec(r_12, PSB_read, init12_kwargs)
        self.read12 = readout_std_set(readout_spec_12, self.measurement_manager, self.segment_mgr)

        r_1 = measurement('read1', chan=[1,2], threshold=0.5, phase=0.3)
        readout_spec_1 = readout_spec(r_1, PSB_read, init12_kwargs, (self.wait(100),self.q12.CNOT12,self.wait(100)))
        self.read1 = readout_std_set(readout_spec_1, self.measurement_manager, self.segment_mgr)

        r_2 = measurement('read2', chan=[1,2], threshold=0.5, phase=0.3)
        readout_spec_2 = readout_spec(r_2, PSB_read, init12_kwargs, (self.wait(100),self.q12.CNOT21,self.wait(100)))
        self.read2 = readout_std_set(readout_spec_2, self.measurement_manager, self.segment_mgr)

        r_3 = measurement('read3', flip='read12', chan=[1,2], threshold=0.5, phase=0.3)
        readout_spec_3 = readout_spec(r_3, PSB_read, init12_kwargs, (self.wait(100),self.q23.CNOT12,self.wait(100)))
        self.read3 = readout_std_set(readout_spec_3, self.measurement_manager, self.segment_mgr)

        r_56 = measurement('read56', chan=[3,4], threshold=0.5, phase=0.3)
        readout_spec_56 = readout_spec(r_56, PSB_read, init56_kwargs)
        self.read56 = readout_std_set(readout_spec_56, self.measurement_manager, self.segment_mgr)

        r_6 = measurement('read6', chan=[5,6], threshold=0.5, phase=0.3)
        readout_spec_6 = readout_spec(r_6, PSB_read, init56_kwargs, (self.wait(100),self.q56.CNOT21,self.wait(100)))
        self.read6 = readout_std_set(readout_spec_6, self.measurement_manager, self.segment_mgr)

        r_5 = measurement('read5', chan=[5,6], threshold=0.5, phase=0.3)
        readout_spec_5 = readout_spec(r_5, PSB_read, init56_kwargs, (self.wait(100),self.q56.CNOT12,self.wait(100)))
        self.read5 = readout_std_set(readout_spec_5, self.measurement_manager, self.segment_mgr)

        r_4 = measurement('read4', flip='read56', chan=[5,6], threshold=0.5, phase=0.3)
        readout_spec_4 = readout_spec(r_4, PSB_read, init56_kwargs, (self.wait(100),self.q45.CNOT21,self.wait(100)))
        self.read4 = readout_std_set(readout_spec_4, self.measurement_manager, self.segment_mgr)


    def segments(self):
        return self.segment_mgr.segments

    def plot_sequence(self):
        # print(self.segments())
        plot_seg(self.segments())


from pulse_templates.demo_pulse_lib.virtual_awg import get_demo_lib
import pulse_lib.segments.utility.looping as lp 
pulse = get_demo_lib('six')
s = six_dot_sample(pulse)

s.init12.add()
s.init56.add()
s.init3.add()
s.init4.add()

# do a rabi on qubit 1
s.wait(5e3).add()
s.q2.X.add(t_pulse = lp.linspace(0, 1e3, 50, axis=0))

# do a cnot to qubit 4
s.q23.CNOT12.add()
s.q34.CNOT12.add()
s.q45.CNOT12.add()

s.wait(5e3).add()

s.read12.add()
s.read3.add(flip='qubit12')
s.read56.add()
s.read4.add(flip='qubit56')

s.plot_sequence()

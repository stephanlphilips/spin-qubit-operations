from core_tools.sweeps.pulse_lib_sweep import spin_qubit_exp, dummy_multi_parameter
from pulse_templates.coherent_control.single_qubit_gates.single_qubit_gates import single_qubit_gate_spec
from pulse_templates.oper.operators import jump, wait
from pulse_templates.utility.plotting import plot_seg
import numpy as np

def T2_ramsey(seg, gate_set, t_wait, f_bg_oscillations):
    '''
    perform T2* measurement on the qubit

    Args:
        seg (segment_container) : segment container
        gate_set (single_qubit_gate_spec) : object containg instruction of the gate set
        t_wait (double) : time to wait
        f_bg_oscillations (double) : freq at which the the qubit needs to oscilate 
    '''
    gate_set.X.add(seg)
    getattr(seg, gate_set.qubit).wait(t_wait) 
    getattr(seg, gate_set.qubit).add_global_phase(t_wait*1e-9*f_bg_oscillations*np.pi*2)
    getattr(seg, gate_set.qubit).reset_time()
    gate_set.X.add(seg)

def T2_CPMG_t_tot(seg, gate_set, t_wait, N_rep,f_bg_oscillations):
    '''
    perform CPMG given tot total waiting time

    Args:
        seg (segment_container) : segment container
        gate_set (single_qubit_gate_spec) : object containg instruction of the gate set
        t_wait (double) : total time waited in the pulse
        N_rep (double) : amount of X gates you want to do
        f_bg_oscillations (double) : freq at which the the qubit needs to oscilate 
    
    TODO : problems is T_wait and N are loop objects? PULSE lib add support for multipying two param.
    '''
    
    gate_set.X.add(seg)

    for i in range(N_rep):
        getattr(seg, gate_set.qubit).wait(t_wait/N_rep/2) 
        getattr(seg, gate_set.qubit).reset_time()

        gate_set.X2.add(seg)

        getattr(seg, gate_set.qubit).wait(t_wait/N_rep/2) 
        getattr(seg, gate_set.qubit).reset_time()

    getattr(seg, gate_set.qubit).add_global_phase(t_wait*1e-9*f_bg_oscillations*np.pi*2)
    gate_set.X.add(seg)

def T2_CPMG_t_single(seg, gate_set, t_wait, N_rep, f_bg_oscillations):
    '''
    perform CPMG given tot total waiting time

    Args:
        seg (segment_container) : segment container
        gate_set (single_qubit_gate_spec) : object containg instruction of the gate set
        t_wait (double) : time to wait
        N_rep (double) : amount of X gates you want to do
        f_bg_oscillations (double) : freq at which the the qubit needs to oscilate 
    
    TODO : problems is T_wait and N are loop objects? PULSE lib add support for multipying two param.
    '''
    T2_CPMG_t_tot(seg, gate_set, t_wait*N_rep, N_rep, f_bg_oscillations)

def T2_hahn(seg, gate_set, t_wait, f_bg_oscillations):
    '''
    perform hahn echo

    Args:
        seg (segment_container) : segment container
        gate_set (single_qubit_gate_spec) : object containg instruction of the gate set
        t_wait (double) : time to wait
        f_bg_oscillations (double) : freq at which the the qubit needs to oscilate 
    '''
    T2_CPMG_t_tot(seg, gate_set, t_wait, 1, f_bg_oscillations)

if __name__ == '__main__':
    
    import pulse_lib.segments.utility.looping as lp

    from pulse_templates.coherent_control.single_qubit_gates.standard_set import single_qubit_std_set
    from pulse_templates.coherent_control.single_qubit_gates.single_qubit_gates import single_qubit_gate_spec
    from pulse_templates.demo_pulse_lib.virtual_awg import get_demo_lib
    from pulse_templates.utility.plotting import plot_seg

    pulse = get_demo_lib('quad')
    seg = pulse.mk_segment()

    xpi2 = single_qubit_gate_spec('qubit1_MW', 1e9, 100, 120)
    xpi = single_qubit_gate_spec('qubit1_MW', 1e9, 200, 120)
    ss_set = single_qubit_std_set()
    ss_set.X = xpi2
    ss_set.X2 = xpi

    pulse.IQ_channels[0].virtual_channel_map[0].reference_frequency = 1.01e9

    # seg = pulse.mk_segment()
    # T2_ramsey(seg, ss_set, lp.linspace(100,1000), 10e6)
    # plot_seg(seg)

    # seg = pulse.mk_segment()
    # T2_hahn(seg, ss_set, lp.linspace(200,1000, axis=0), 10e6)
    # plot_seg(seg)

    seg = pulse.mk_segment()
    T2_CPMG_t_tot(seg, ss_set, 5000, 20, 10e6)
    plot_seg(seg)
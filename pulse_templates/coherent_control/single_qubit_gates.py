from pulse_templates.utility.template_wrapper import template_wrapper 
from pulse_templates.utility.oper import add_block, add_ramp

@template_wrapper
def single_qubit_gate_simple(segment, qubit, t_drive, amp, freq, padding,**kwargs):
	'''
	add a single qubit gate (elementary -- no shaping)

	Args:
		segment (segment_container) : segment to which to add this stuff
        qubit (str) : name of the qubit (defined in the pulse lib config file)
        t_drive (double) : time to drive
        amp (double) : amplitude with which to drive
        freq (double) : frequency to apply to the qubit
        padding (double) : padding that needs to be put around the microwave (value added at each side).
	'''
	getattr(segment, qubit).wait(padding)
	getattr(segment, qubit).reset_time()
	getattr(segment, qubit).add_MW_pulse(0, t_drive, amp, freq)
	getattr(segment, qubit).reset_time()
	getattr(segment, qubit).wait(padding)
	segment.reset_time()

if __name__ == '__main__':
    from pulse_templates.utility.plotting import plot_seg
    from pulse_templates.demo_pulse_lib.virtual_awg import get_demo_lib
    
    pulse = get_demo_lib('quad')
    seg = pulse.mk_segment()

    gates = ('vP4',)

    seg.vP4 += 10
    qubit = 'qubit4_MW'
    t_drive = 100
    amp = 10
    freq = 200e8
    padding = 10

    # T2* measurement
    single_qubit_gate_simple(seg, qubit, t_drive, amp, freq, padding)
    seg.qubit4_MW.wait(1e3)
    seg.reset_time()

    # might be useful to add here extra phase if the qubit freq is not defined.
    single_qubit_gate_simple(seg, qubit, t_drive, amp, freq, padding)
    plot_seg(seg)
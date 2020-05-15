from pulse_templates.utility.template_wrapper import template_wrapper 
from pulse_templates.utility.oper import add_block, add_ramp


@template_wrapper
def cphase_basic(segment, gates, v_exchange_pulse, t_gate, t_ramp):
	'''
	basic cphase, with a linear ramp

	Args:
        segment (segment_container) : segment to which to add this stuff
        barrier (str) : barrier to pulse
        v_exchange_pulse (double) : voltage to pulse to
        t_gate (double) : total time of the gate not inclusing the ramps
        t_ramp (double) : ramp time
	'''

	gates = (gate, )
	v_exchange_pulse = (v_exchange_pulse, )
	
	add_ramp(segment, r_ramp, gates, (0, ), v_exchange_pulse)
	add_block(segment, t_gate, gates, v_exchange_pulse)
	add_ramp(segment, r_ramp, gates, (0, ), v_exchange_pulse)
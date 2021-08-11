'''
functions for appling multiple operations at the same time on a segment
'''
def add_pulse_template(segment, t_gate, gates, amplitudes, pulse_template, reset_time = True, **pulse_template_kwargs):
    '''
    Add a templated smooth functoin to the pulse template

    Args:
        segment (segment_container) : segment to which to add this stuff
        t_gate (double) : time of the block pulse
        gates (tuple<str>) : names of the gates to which to add the block
        amplitudes (tuple<double>) : amplitudes per channel of the final output function 
        pulse_template (func) : templates to add the seqeuence
        pulse_template_kwargs : arguments for the template

    '''
    for gate, amplitude,pulse_template in zip(gates, amplitudes, pulse_template):
        getattr(segment, gate).add_custom_pulse(0, t_gate, amplitude, pulse_template,**pulse_template_kwargs)

    if reset_time == True:
        segment.reset_time()

def add_block(segment, t_gate, gates, levels, reset_time=True):
    '''
    add a block to muliple segments at the same time and reset the time.

    Args:
        segment (segment_container) : segment to which to add this stuff
        t_gate (double) : time of the block pulse
        gates (tuple<str>) : names of the gates to which to add the block
        levels (tuple <double>) : levels of the block pulse
    '''
    for gate, level in zip(gates, levels):
        getattr(segment, gate).add_block(0, t_gate, level)

    if reset_time == True:
        segment.reset_time()

def add_block_ss(segment, t_gate_start, t_gates_stop, gates, levels, reset_time=True):
    '''
    add a block to muliple segments at the same time and reset the time.

    Args:
        segment (segment_container) : segment to which to add this stuff
        t_gate (double) : time of the block pulse
        gates (tuple<str>) : names of the gates to which to add the block
        levels (tuple <double>) : levels of the block pulse
    '''
    for gate, level in zip(gates, levels):
        getattr(segment, gate).add_block(t_gate_start, t_gates_stop, level)

    if reset_time == True:
        segment.reset_time()


def add_ramp(segment, t_gate, gates, level_in, level_out, reset_time=True):
    '''
    add a block to muliple segments at the same time and reset the time.

    Args:
        segment (segment_container) : segment to which to add this stuff
        gates (tuple<str>) : names of the gates to which to add the block
        t_block (double) : time of the block pulse
        levels (tuple <double>) : levels of the block pulse
    '''
    for gate, l_in, l_out in zip(gates, level_in, level_out):
        getattr(segment, gate).add_ramp_ss(0, t_gate, l_in, l_out)

    if reset_time == True:
        segment.reset_time()

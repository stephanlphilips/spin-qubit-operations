'''
functions for appling multiple operations at the same time on a segment
'''

def add_block(segment, t_gate, gates, levels, reset_time=True):
    '''
    add a block to muliple segments at the same time and reset the time.

    Args:
        segment (segment_container) : segment to which to add this stuff
        gates (tuple<str>) : names of the gates to which to add the block
        t_block (double) : time of the block pulse
        levels (tuple <double>) : levels of the block pulse
    '''
    for gate, level in zip(gates, levels):
        getattr(segment, gate).add_block(0, t_gate, level)

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

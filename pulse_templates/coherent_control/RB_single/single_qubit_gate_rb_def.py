def load_single_qubit_gate(segment, gate_object, padding = 0,**kwargs):
    '''
    add a single qubit gate (elementary -- no shaping)

    Args:
        segment (segment) : segment to which to add this stuff
        gate_object (single_qubit_gate_spec) : gate object describing the microwave pulse
        padding (double) : padding that needs to be put around the microwave (value added at each side).
    '''
    segment.add_MW_pulse(padding, gate_object.t_pulse + padding, gate_object.MW_power, gate_object.f_qubit, gate_object.phase ,  gate_object.AM_mod,  gate_object.PM_mod)
    segment.reset_time()
    segment.wait(padding)
    segment.reset_time()
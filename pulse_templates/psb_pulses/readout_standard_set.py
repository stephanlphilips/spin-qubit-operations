from pulse_templates.utility.segment_manager import segment_mgr
from pulse_templates.utility.measurement import measurement
from dataclasses import dataclass, field

import inspect
import copy

def unwrap(func):
    while hasattr(func, '__wrapped__'):
        func = func.__wrapped__
    return func

@dataclass
class readout_spec:
    '''
    spec for readout of the sample

    Args;
        measurement_obj (measurement) : object that defined what the threshold is/what to measure
        PSB_call_function (function) : function that generates the segment for the psb readout
        PSB_call_kwargs (dict) : dictionart containg the kwargs for the function described before.
        gate_instructions (tuple) : instruction that are excecuted before the readout. This could be a X gate
    '''
    measurement_obj : measurement
    PSB_call_function : any
    PSB_call_kwargs : dict
    gate_instructions : tuple = field(default_factory=lambda: tuple())
    _segment_generator : segment_mgr = None

    def add(self, segment=None, **kwargs):
        if segment is None and self._segment_generator is None:
            raise ValueError('no segment privided')
        if segment is None:
            for instruction in self.gate_instructions:
                instruction.add()
            
            segment = self._segment_generator.generate_segment()
        else:
            for instruction in self.gate_instructions:
                instruction.add(segment)

        self.PSB_call_function(segment, **kwargs)


class readout_std_set:
    def __init__(self, readout_specification, measurement_mgr, segment_generator=None):
        self.readout_spec = readout_specification
        self.measurement_mgr = measurement_mgr
        self.readout_spec._segment_generator = segment_generator

        self.__measurement_kwargs = ['name', 'chan', 'threshold', 'accept', 'phase', 'flip', '_0_on_high']
    
    def add(self, segment=None, **kwargs):
        meas = copy.copy(self.readout_spec.measurement_obj)
        PSB_call_kwargs = copy.copy(self.readout_spec.PSB_call_kwargs)
        
        valid_kwargs = list(inspect.getfullargspec(unwrap(self.readout_spec.PSB_call_function))[0]) + list(meas.__dict__.keys())
        for key, value in kwargs.items():
            if key not in valid_kwargs:
                raise ValueError(f'Bad keyword detected ({key}) in readout descriptor. Accepected keywords are : {valid_kwargs}')

        for key,value in kwargs.items():
            if key in self.__measurement_kwargs:
                setattr(meas, key, value)
            else:
                PSB_call_kwargs[key] = value

        if 't_read' not in PSB_call_kwargs.keys():
            raise ValueError('Please use the variable name t_read in the PSB call function. -- not able the register the measurment time')
        self.measurement_mgr.add(meas)
        self.readout_spec.add(segment, **PSB_call_kwargs)

        self.measurement_mgr.t_meas = PSB_call_kwargs['t_read']


if __name__ == '__main__':
    from pulse_templates.utility.measurement import measurement_manager
    from pulse_templates.psb_pulses.readout_pulses import PSB_read
    from pulse_templates.demo_pulse_lib.virtual_awg import get_demo_lib
    from pulse_templates.utility.plotting import plot_seg

    pulse = get_demo_lib('quad')

    ss = segment_mgr(pulse)
    mm = measurement_manager()

    m = measurement('PSB_12_init', chan=[1,2], accept=0, threshold=0.5, phase=0.3)
    readout_kwargs = {'gates' : ('vP1','vB1', 'vP2'), 't_ramp' : 2e3, 
                't_read' : 2e3, 'p_0' : (0,0,0), 'p_1' : (5.5,0,-5.5)}
    rs = readout_spec(m, PSB_read, readout_kwargs)


    read_set = readout_std_set(rs, mm, ss)
    read_set.add()
    read_set.add()
    plot_seg(ss.segments)
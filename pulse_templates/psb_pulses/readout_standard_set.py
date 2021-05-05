from pulse_lib.segments.utility.template_base import pulse_template
from pulse_templates.measurement.measurement import measurement
from dataclasses import dataclass, field

import inspect
import copy

def unwrap(func):
    while hasattr(func, '__wrapped__'):
        func = func.__wrapped__
    return func

@dataclass
class readout_spec(pulse_template):
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
    gate_instructions : tuple = field(default_factory=tuple)

    def replace(self, **kwargs):
        raise NotImplementedError()

    def build(self, segment, reset=False, **kwargs):
        for instruction in self.gate_instructions:
            instruction.build(segment)

        self.PSB_call_function(segment, meas=self.measurement_obj, **kwargs)


class readout_std_set(pulse_template):
    def __init__(self, readout_specification):
        self.readout_spec = readout_specification

        self.__measurement_kwargs = ['name', 'chan', 'threshold', 'accept', 'phase', 'flip', '_0_on_high']

    def replace(self, **kwargs):
        raise NotImplementedError()

    def build(self, segment, reset=False, **kwargs):
        self.readout_spec.measurement_obj = copy.copy(self.readout_spec.measurement_obj)
        meas = self.readout_spec.measurement_obj
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

#        if 't_meas' not in PSB_call_kwargs.keys():
#            raise ValueError('Please use the variable name t_meas in the PSB call function. -- not able the register the measurment time')

        self.readout_spec.build(segment, **PSB_call_kwargs)



if __name__ == '__main__':
    from pulse_lib.sequence_builder import sequence_builder
    from pulse_templates.psb_pulses.readout_pulses import PSB_read
    from pulse_templates.demo_pulse_lib.virtual_awg import get_demo_lib
#    from pulse_templates.utility.plotting import plot_seg

    pulse = get_demo_lib('quad')

    m = measurement(channel='SD1_I',
                    t_measure=2e3, accept=0, threshold=0.5)
    readout_kwargs = {'gates' : ('vP1','vB1', 'vP2'), 't_ramp' : 2e3,
                      'p_0' : (0,0,0), 'p_1' : (5.5,0,-5.5)}
    rs = readout_spec(m, PSB_read, readout_kwargs)
    read_set = readout_std_set(rs)

    seq = sequence_builder(pulse)
    seq.add(read_set)
    seq.add(read_set)
    seq._segment.plot()

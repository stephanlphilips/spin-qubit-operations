from dataclasses import dataclass
from typing import Optional, Any
import copy

from pulse_lib.segments.utility.template_base import pulse_template
from pulse_lib.segments.utility.measurement_ref import MeasurementExpressionBase, MeasurementRef
from pulse_templates.psb_pulses.readout_template import ReadoutTemplate

@dataclass
class measurement(pulse_template):
    channel : str
    t_measure : float
    threshold : Optional[float] = None
    accept : Optional[int] = None
    zero_on_high : bool = False
    mref : Optional[Any] = None

    def replace(self, **kwargs):
        cpy = copy.copy(self)
        for key, value in kwargs.items():
            if key not in self.__dict__.keys():
                raise ValueError(f'invalid keyword argument detected for measurement objecct, {key}, options are {list(self.__dict__.keys())}')
            setattr(cpy, key, value)
        return cpy

    def build(self, segment, **kwargs):
        # TODO @@@ kwargs
        segment[self.channel].acquire(
                0, self.t_measure, ref=self.mref, accept_if=self.accept,
                threshold=self.threshold, zero_on_high=self.zero_on_high)

@dataclass
class measurement_expression(pulse_template):
    name : str
    expression : MeasurementExpressionBase
    accept : Optional[int] = None

    def replace(self, **kwargs):
        raise NotImplementedError()

    def build(self, segment, **kwargs):
        # TODO @@@ kwargs
        segment.add_measurement_expression(self.expression, accept_if=self.accept, name=self.name)



class MeasurementSet:
    def __init__(self):
        self.measurements = {}

    def add(self, name, func, **kwargs):
        if isinstance(func, ReadoutTemplate):
            readout = func
            mref = MeasurementRef(name)
            self.measurements[name] = mref

            kwargs = kwargs.copy()
            kwargs['mref'] = mref
            return readout.replace(**kwargs)
        if isinstance(func, MeasurementExpressionBase):
            mref = func
            self.measurements[name] = mref
            return measurement_expression(name, mref, **kwargs)
        else:
            raise ValueError(f'unknown func {func}')

    def __getitem__(self, index):
        return self.measurements[index]
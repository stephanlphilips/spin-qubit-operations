from typing import List, Any, Union
from collections.abc import Iterable

from pulse_lib.segments.utility.template_base import pulse_template
from pulse_lib.segments.utility.measurement_ref import MeasurementRef

from .sequence_template import SequenceTemplate

class Conditional(pulse_template):
    def __init__(self,
                 condition:Union[List[MeasurementRef], MeasurementRef],
                 *templates):
        self.condition = condition
        self.templates = []
        for template in templates:
            if isinstance(template, Iterable):
                template = SequenceTemplate(*template)
            self.templates.append(template)

    def replace(self, **kwargs):
        raise NotImplementedError()

    def build(self, sequence_builder, reset=False, **kwargs):
        sequence_builder.add_conditional(self.condition, self.templates)




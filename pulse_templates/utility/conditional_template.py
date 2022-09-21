from typing import List, Union
from collections.abc import Iterable

from pulse_lib.segments.utility.template_base import pulse_template
from pulse_lib.segments.utility.measurement_ref import MeasurementRef
from pulse_lib.sequence_builder import sequence_builder as SequenceBuilder

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
        if not isinstance(sequence_builder, SequenceBuilder):
            raise Exception('ConditionalTemplate cannot be nested in Conditional or Simultaneous')
        sequence_builder.add_conditional(self.condition, self.templates)




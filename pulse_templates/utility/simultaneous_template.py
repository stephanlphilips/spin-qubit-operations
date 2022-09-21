from pulse_lib.segments.utility.template_base import pulse_template
from pulse_lib.sequence_builder import sequence_builder as SequenceBuilder


class SimultaneousTemplate(pulse_template):
    def __init__(self, *args):
        self.templates = args

    def replace(self, **kwargs):
        raise NotImplementedError()

    def build(self, sequence_builder, reset=False, **kwargs):
        if not isinstance(sequence_builder, SequenceBuilder):
            raise Exception('ConditionalTemplate cannot be nested in Conditional or Simultaneous')
        sequence_builder.add_simultaneous(self.templates)


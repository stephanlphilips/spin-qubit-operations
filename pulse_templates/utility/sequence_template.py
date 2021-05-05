from pulse_lib.segments.utility.template_base import pulse_template


class SequenceTemplate(pulse_template):
    def __init__(self, *args):
        self.templates = args

    def replace(self, **kwargs):
        raise NotImplementedError()

    def build(self, segment, reset=False, **kwargs):
        for template in self.templates:
            template.build(segment, **kwargs)




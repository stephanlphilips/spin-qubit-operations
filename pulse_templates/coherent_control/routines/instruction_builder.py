from pulse_lib.segments.utility.template_base import pulse_template
from pulse_lib.segments.utility.looping import loop_obj, linspace

import numpy as np

def get_target(obj, name):
    name = name.split('_')

    for operator in name:
        obj = getattr(obj, operator)
    
    return obj

class quasi_quasm_adder(pulse_template):
    def __init__(self, system, instruction_list, repeat = 1):
        '''
        Args:
            system (object) : system that has buildable object to generate the gates in the measurement list
            instruction_list (instruction_mgr) : object with that hold a list of operations to be executed on the device 
        '''
        self.system = system
        self.instruction_list = instruction_list
        self.repeat = repeat

    def replace(self, **kwargs):
        cpy = copy.copy(self)
        return cpy

    def build(self, segment, reset=True, **kwargs):
        setpoint = loop_obj()
        setpoint.add_data(np.linspace(1,len(self.instruction_list)*self.repeat, len(self.instruction_list)*self.repeat), axis=0, labels = self.instruction_list.name)


        segment = segment._get_segment()
        segment[segment.channels[0]].update_dim(setpoint)

        for r in range(self.repeat):
            for i in range(len(self.instruction_list)):
                for gate in self.instruction_list[i].instruction:
                    get_target(self.system, gate).build(segment[i + r*len(self.instruction_list)], reset=True, **kwargs)

        return segment

# setpoint = loop_obj()
# setpoint.add_data(np.linspace(1,20, 20), axis=0, labels =' self.instruction_list.name')
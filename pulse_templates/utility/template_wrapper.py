'''
wrapper that collect information about the template and prints it.

Long term goal : add to the segment/sequence and save when the scan start
'''

from pulse_templates.utility.name_generator import format_name
from functools import wraps
import inspect 

def template_wrapper(f):
    '''
    wrapper for a template, will extract the name of the template.
    Also adds support for debug functionalty in the experiment.

    Args :
        f (lamda) : template to be wrapped.
    '''
    @wraps(f)
    def my_wrapper(*args, **kwargs):
        args_name = inspect.getfullargspec(f)[0]
        if 'debug' in kwargs.keys():
            if kwargs['debug'] == True:
                print('Debug argument detected in {}'.format(f.__name__))
                # arg[0] is always the segment, [1] gates
                segment = args[0]
                gates = args[1] #cleaner directly add in the HVI variable, but was a bit layzy
                getattr(segment, gates[0]).add_HVI_marker("dig_wait_1")
                getattr(segment, gates[0]).add_HVI_variable("t_measure", 100)
                # usually this is not done via HVI averaging, so time is just set to a dummy variable atm (thight might change in a later stage)
        function_info = format_name(f,args_name, args, kwargs)
        f(*args, **kwargs)
        return function_info

    return my_wrapper


if __name__ == '__main__':
    from pulse_lib.segments.utility.looping import loop_obj, linspace
    from pulse_templates.demo_pulse_lib.virtual_awg import get_demo_lib

    pulse = get_demo_lib('quad')
    seg = pulse.mk_segment() 
    @template_wrapper
    def pulse_intra(segment, gates, t_wait, t_ramp, p_0, p_1, **kwargs):
        pass

    info = pulse_intra(seg, ('P1', 'P2'), 1000, 100, (0,0), (0.1,3), debug=True)
    print(info)

    info = pulse_intra(seg, ('P1', 'P2'), 1000, linspace(0,1, axis=0), (0,1), (0.1,3))
    print(info)

    info = pulse_intra(seg, ('P1', 'P2'), 1000, 100, (0,linspace(0,1, axis=1)), (0.1,3))
    print(info)

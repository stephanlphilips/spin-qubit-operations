'''
wrapper that collect information about the template and prints it.

Long term goal : add to the segment/sequence and save when the scan start
'''

from pulse_lib.segments.utility.looping import loop_obj
import dataclasses
from si_prefix import si_format
import numbers

def format_name(function, arg_names, args, kwargs):
    '''
    Formatting of a name for the template function that includes its set variables.

    Args:
        function (lamda) : function that needs nice formatting
        args_names (list<str>) : list with names of the arguments of the function
        args (list<any>) : list with data to be send into the function
    '''
    param_description =  function.__name__ + ' [ '

    for i in range(len(arg_names)):
        if arg_names[i] == 'segment':
            continue
            
        if i < len(args):
            param_description += arg_names[i] + ' : ' + format_name_item(function.__name__, arg_names[i], args[i])
        else:
            try:
                param_description += arg_names[i] + ' : ' + format_name_item(function.__name__, arg_names[i], kwargs[arg_names[i]])
            except:
                pass
        if i+1 != len(arg_names):
            param_description += ', '
        else:
            param_description += ']'

    return param_description

def format_name_item(func_name, arg_name, arg_value):
    '''
    format the name of a single argument of a function.

    Args:
        func_name (str) : name of the function
        arg_name (str) : name of the argument
        arg_value (any) : value of the argument provided to the function
    '''
    if arg_name == 'segment' or arg_value is None:
        return ''

    unit_type = 'V'
    multiplier = 1e-3
    if arg_name.startswith('t_'):
        unit_type = 'ns'
        multiplier = 1
    if arg_name.startswith('f_'):
        unit_type = 'GHz'
        multiplier = 1e-9

    if isinstance(arg_value, numbers.Number):
        return si_format(arg_value*multiplier, precision=1) + unit_type

    if isinstance(arg_value, str):
        return arg_value

    if isinstance(arg_value, loop_obj):
        axis = tuple(arg_value.axis)
        if len(axis) == 1:
            axis = axis[0]
        return 'VAR ' + str(axis)

    if dataclasses.is_dataclass(arg_value):
        items = '[ '
        key_values_pairs = list(arg_value.__dict__.items())
        for i in range(len(key_values_pairs)):
            items += str(key_values_pairs[i][0]) + ' '
            items += format_name_item(func_name, key_values_pairs[i][0], key_values_pairs[i][1]) + ' '
        return items + ' ]'

    if isinstance(arg_value, tuple):
        items = []
        for i in arg_value:
            items.append(format_name_item(func_name, arg_name, i))
        return str(tuple(items))

    raise ValueError('Invalid input provided for function {}. Valid input arguments are Numeric/loop_obj types or tuples of those.'.format(func_name))

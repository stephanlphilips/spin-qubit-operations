'''
wrapper that collect information about the template and prints it.

Long term goal : add to the segment/sequence and save when the scan start
'''

from functools import wraps
import inspect, itertools 
from pulse_lib

def template_wrapper(f):

    @wraps(f)
    def wrapper(*args, **kwargs):
        args_name = inspect.getargspec(f)[0]
        

        f(*args, **kwargs)

    return wrapper

@template_wrapper
def example(test, t2, g):
    print(test)

example('test', 't2', 'g')
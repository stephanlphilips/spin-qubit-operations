import numpy as np
from functools import wraps
from copy import copy
from collections.abc import Iterable

from pulse_templates.utility.oper import add_block
from pulse_lib.segments.utility.looping import loop_obj

### this part must be added to pulse_lib.segments.utility

def to_numpy(obj:loop_obj):
    shape = [1] * (max(obj.axis)+1)
    for dim, l in zip(obj.axis, obj.shape):
        shape[dim] = l
    return obj.data.reshape(shape)

def select(tup, indices):
    return tuple(value for i,value in enumerate(tup) if i in indices)

def to_loop_obj(obj, joined_loops):
    res = copy(joined_loops)
    res_axis = []
    selected_loop_axis = []
    for idim, l in enumerate(obj.shape):
        if l > 1 and idim not in joined_loops.axis:
            raise Exception(f'Cannot convert {obj.shape} using axis {joined_loops.axis}')
        res_axis.append(idim)
        selected_loop_axis.append(joined_loops.axis.index(idim))

    res_axis.reverse()
    res.labels = select(res.labels, selected_loop_axis)
    res.setvals = select(res.setvals, selected_loop_axis)
    res.units = select(res.units, selected_loop_axis)
    res.axis = res_axis
    res.data = obj
    return res

def to_loop_objs(objs, loop_objs):
    joined_loops = sum(loop_objs)
    if isinstance(objs, Iterable):
        res = (to_loop_obj(obj, joined_loops) for obj in objs)
    else:
        res = to_loop_obj(objs, joined_loops)
    return res

def loop_to_numpy(func):
    '''
    Checks if there are there are parameters given that are loopable.

    If loop:
        * then check how many new loop parameters on which axis
        * extend data format to the right shape (simple python list used).
        * loop over the data and add called function

    if no loop, just apply func on all data (easy)
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        loop_objs = []
        arg_list = list(args)
        for i in range(0,len(arg_list)):
            if isinstance(arg_list[i], loop_obj):
                loop_objs.append(arg_list[i])
                arg_list[i] = to_numpy(arg_list[i])

        for key in kwargs.keys():
            if isinstance(kwargs[key], loop_obj):
                loop_objs.append(kwargs[key])
                kwargs[key] = to_numpy(kwargs[key])

        res = func(*arg_list, **kwargs)
        print(res)
        return to_loop_objs(res, loop_objs)


    return wrapper

### end looping utility




## Helper functions to compute c_phase parameters
def get_J_max(angle:np.ndarray, delta_B:np.ndarray):
    return np.abs(np.sqrt(delta_B**2*angle**2/((3*np.pi)**2 - angle**2)))

def t_ramp_(J_max:np.ndarray, delta_B:np.ndarray):
    return 3/np.sqrt(J_max**2 + delta_B**2)

@loop_to_numpy
def calculate_cphase_properties(angle:np.ndarray, J_max:np.ndarray, delta_B:np.ndarray) -> np.ndarray:
    # theoretically can be a bit faster, but here chosen to be safe (3 seems to be a good spot (-> Martinis and geller, PRA 2014))
    # here sqrt(J_max**2 + delta_B**2) is the effective Zeeman difference.
    ramp_time:np.ndarray = t_ramp_(J_max, delta_B)
    angle_ramp:np.ndarray = ramp_time*J_max*np.pi

    J_max = np.where(angle < angle_ramp*2,
                     get_J_max(angle/2, delta_B),
                     J_max)
    t_ramp = t_ramp_(J_max, delta_B)*1e9
    t_pulse = np.where(angle < angle_ramp*2,
                       0,
                       (angle-angle_ramp*2)/J_max/2/np.pi*1e9)

    duration = t_ramp*2 + t_pulse

    return duration, t_ramp, t_pulse, J_max


## custom pulse function with keyword arguments.
## Pulse lib expands loobobj parameters before calling this function
def cphase_function(duration, sample_rate, amplitude,
                    t_ramp=None, t_pulse=None, J_max=None,
                    voltage_to_J_relation=None):
    n_points = int(round(duration / sample_rate * 1e9))
    J_valued_data = np.zeros([n_points])
    n_points_ramp = int(round(t_ramp / sample_rate * 1e9))

    J_valued_data[0:n_points_ramp] = (0.5-0.5*np.cos(np.arange(n_points_ramp)*np.pi/t_ramp))*J_max
    dc_stop = int(round((t_ramp + t_pulse )/ sample_rate * 1e9))
    J_valued_data[n_points_ramp:dc_stop] = J_max
    offset = dc_stop - t_ramp - t_pulse

    J_valued_data[dc_stop:n_points] = (0.5-0.5*np.cos((np.arange(n_points-dc_stop)+ offset/sample_rate*1e9)*np.pi/t_ramp+np.pi))*J_max

    return voltage_to_J_relation(J_valued_data)*amplitude


def cphase(segment, gates, cphase_angle, J_max, delta_B, voltage_to_J_relation, padding=5):
    '''
    Makes a shaped cphase gate (with respect to adiabaticity)

    Args:
        segment (segment_container) : segment to which to add this stuff
        gates (list<str>) : list of gates involved in the cphase gate
        cphase_angle (double) : the angle to rotate (amount of J to apply (MHz))
        J_max (double) : the maximal value of J that should be applied (e.g. cosine window get converted into a tuckey one)
        delta_B (double) : frequency difference between the qubits (MHz).
        voltage_to_J_relation (list<func>) : function that returns the voltages to be applied for a certain amount of J
        padding (int) : amount of padding to add around the pulse (in ns)
    '''
    t_gate, t_ramp, t_pulse, J_max = calculate_cphase_properties(cphase_angle, J_max, delta_B)

    add_block(segment, padding, gates, tuple([0]*len(gates)))
    for gate, v_to_J in zip(gates, voltage_to_J_relation):
        #ch = segment[gate]
        ch = getattr(segment, gate)
        ch.add_custom_pulse(0, t_gate, 1.0,
                            cphase_function, t_ramp=t_ramp, t_pulse=t_pulse, J_max=J_max,
                            voltage_to_J_relation=v_to_J)
    segment.reset_time()

    add_block(segment, padding, gates, tuple([0]*len(gates)))


if __name__ == '__main__':
    from pulse_templates.utility.plotting import plot_seg
    from pulse_templates.demo_pulse_lib.virtual_awg import get_demo_lib
    from pulse_lib.segments.utility.looping import linspace
    import matplotlib.pyplot as plt

    pulse = get_demo_lib('six')
    seg = pulse.mk_segment()


    gates = ('vB1', )
    J = np.pi
    J_max = 5e6
    delta_B = 30e6

    v_exchange_pulse_off =  (0,0,0)
    v_exchange_pulse_on  = (0,50,0)

    def return_amp(amp):
        def J_pulse(x):
            return np.sqrt(x)/np.sqrt(5e6)*amp
        return J_pulse

#    import good_morning.static.J12 as J12
    print('running ')
    # func, time = return_creation_fuction(np.pi-0.7, 5e6, 30e6, voltage_to_J_relation=J_pulse)
    # points = func(time, 1e9, 1)
    # plt.plot(points)
    gate_phases = linspace(0, np.pi*2, 20, axis=0)
    # t = linspace(5e6, 6e6, 20, axis=1)
    cphase(seg, gates, gate_phases, t, delta_B, (return_amp(0.2),), padding=30)

    # cphase(seg, gates, gate_phases, J_max, delta_B, (return_amp(0.2), return_amp(1), return_amp(0.23)), padding=30)

    # cphase_basic(seg, gates, v_exchange_pulse_off, v_exchange_pulse_on, gate_phases*100, t_ramp=50)
    plot_seg(seg, 0)
    plot_seg(seg, 5)
    plot_seg(seg, 10)
    plt.show()
from pulse_lib.segments.utility.data_handling_functions import find_common_dimension, update_dimension

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os

def plot_seg(segments, idx=0, multi_dim=False):
    '''
    plot all the segments that are operated in a segment, if looped, also plot some parts of the loop.

    Args:
        segments (pulse_container_combined) : segment to plot
        multi_dim (bool) : detects if there are loop/multiple dimenions in the pulse and plots them. #TODO
    '''
    
    plt.figure()

    if not isinstance(segments, list):
        segments = [segments]

    data_x = dict()
    data_y = dict()

    for ch_name in segments[0].channels:
        data_x[ch_name] = list()
        data_y[ch_name] = list()

    _shape = (1,)
    for seg_container in segments:
            seg_container.enter_rendering_mode()
            _shape = find_common_dimension(seg_container.shape, _shape)

    for seg_container in segments:
        for ch_name in segments[0].channels:
            data = update_dimension(getattr(seg_container, ch_name)._pulse_data_all, _shape, True)
            setattr(getattr(seg_container, ch_name), '_pulse_data_all', data)

    for ch_name in segments[0].channels:
        for seg in segments:
            ch = getattr(seg, ch_name)
            pulse_data_curr_seg = ch.pulse_data_all.flat[idx]

            sample_rate = 1e9
            data_y[ch_name].append(pulse_data_curr_seg.render(sample_rate))
            # offset = 0
            # if len(data_x[ch_name]) != 0:
            #     print(ch_name)
            #     offset = data_x[ch_name][-1][-1] 
            data_x[ch_name].append(np.linspace(0, pulse_data_curr_seg.total_time, len(data_y[ch_name][-1])))

    data_x_concatenated = dict()
    data_y_concatenated = dict()
    for ch_name in segments[0].channels:
        data_x_concatenated[ch_name] = np.asarray([])
        data_y_concatenated[ch_name] = np.asarray([])

        for i in range(len(segments)):
            data_x_concatenated[ch_name] = np.concatenate((data_x_concatenated[ch_name], data_x[ch_name][i]))
            data_y_concatenated[ch_name] = np.concatenate((data_y_concatenated[ch_name], data_y[ch_name][i]))

        plt.plot(data_x_concatenated[ch_name],data_y_concatenated[ch_name], label=ch_name)
        plt.xlabel("time (ns)")
        plt.ylabel("amplitude (mV)")

    plt.legend()
    plt.show()

def save_segment(segments, location, idx=0):
    if not isinstance(segments, list):
        segments = [segments]
    
    os.mkdir(location)
    for seg_number in range(len(segments)):
        os.mkdir(location + f'_{seg_number}/')

        _shape = (1,)
        segments[seg_number].enter_rendering_mode()
        _shape = find_common_dimension(segments[seg_number].shape, _shape)

        for ch_name in segments[seg_number].channels:
            data = update_dimension(getattr(segments[seg_number], ch_name)._pulse_data_all, _shape, True)
            setattr(getattr(segments[seg_number], ch_name), '_pulse_data_all', data)

        for ch_name in segments[seg_number].channels:
            ch = getattr(seg, ch_name)
            pulse_data_curr_seg = ch.pulse_data_all.flat[idx]

            sample_rate = 1e9
            y = pulse_data_curr_seg.render(sample_rate)
            x = np.linspace(0, pulse_data_curr_seg.total_time, y.size)
            np.save(f'{location}_{seg_number}/{ch_name}', np.asarray([x,y]))

if __name__ == '__main__':
    from pulse_templates.demo_pulse_lib.virtual_awg import get_demo_lib
    from pulse_templates.psb_pulses.init_pulses import pulse_intra
    pulse = get_demo_lib('six')

    seg = pulse.mk_segment()

    pulse_intra(seg, ('vP1', 'vP2'), 1000, 2000, (-5,0), (0,1))

    save_segment(seg, '/Users/Stephan/coding/test/')
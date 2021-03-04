import matplotlib
import matplotlib.pyplot as plt
import numpy as np

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

    for ch_name in segments[0].channels:
        for seg in segments:
            ch = getattr(seg, ch_name)
            pulse_data_curr_seg = ch.pulse_data_all.flat[idx]

            sample_rate = 1e9
            data_y[ch_name].append(pulse_data_curr_seg.render(sample_rate))
            offset = 0
            if len(data_x[ch_name]) != 0:
                offset = data_x[ch_name][-1][-1] 
            data_x[ch_name].append(np.linspace(0, pulse_data_curr_seg.total_time, len(data_y[ch_name][-1]))+offset)

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

if __name__ == '__main__':
    from pulse_templates.demo_pulse_lib.virtual_awg import get_demo_lib
    from pulse_templates.psb_pulses.init_pulses import pulse_intra
    pulse = get_demo_lib('quad')

    seg = pulse.mk_segment()

    pulse_intra(seg, ('vP1', 'vP2'), 1000, 2000, (-5,0), (0,1))

    plot_seg(seg)
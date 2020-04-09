import matplotlib.pyplot as plt
import numpy as np

def plot_seg(seg, multi_dim=False):
	'''
	plot all the segments that are operated in a segment, if looped, also plot some parts of the loop.

	Args:
		seg (pulse_container_combined) : segment to plot
		multi_dim (bool) : detects if there are loop/multiple dimenions in the pulse and plots them. #TODO
	'''
	
	# etstablish which channels are used
	channels_to_render = list()
	for channel in seg.channels:
		seg_single = getattr(seg, channel)
		v_max = seg_single.v_max( np.unravel_index([0],seg_single.shape)[0])
		v_min = seg_single.v_min( np.unravel_index([0],seg_single.shape)[0])

		if v_max != 0 or v_min != 0:
			channels_to_render.append(channel)

	# plot relevant channels
	plt.figure()

	for channel in channels_to_render:
		getattr(seg, channel).plot_segment(index=np.unravel_index([0],seg_single.shape)[0])

	plt.show()
if __name__ == '__main__':
	from pulse_templates.demo_pulse_lib.virtual_awg import get_demo_lib
	from pulse_templates.psb_pulses.init_pulses import pulse_intra
	pulse = get_demo_lib('quad')

	seg = pulse.mk_segment()

	pulse_intra(seg, ('vP1', 'vP2'), 1000, 2000, (-5,0), (0,1))

	plot_seg(seg)
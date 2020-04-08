from pulse_templates.demo_pulse_lib.quad_dot import return_pulse_lib_quad_dot

def get_demo_lib(sample):
	if sample == 'quad' :
		return return_pulse_lib_quad_dot()
	else:
		raise ValueError('sample not defined. Please add or use a existing one (e.g. quad)')


if __name__ == '__main__':
	print(get_demo_lib('quad'))
	print(get_demo_lib('sample'))
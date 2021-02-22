from pulse_templates.demo_pulse_lib.quad_dot import return_pulse_lib_quad_dot

from pulse_templates.demo_pulse_lib.six_dot import return_pulse_lib

def get_demo_lib(sample):
	if sample == 'quad' :
		return return_pulse_lib_quad_dot()
	if sample == 'six' :
		return return_pulse_lib()
	else:
		raise ValueError('sample not defined. Please add or use a existing one (e.g. quad)')


if __name__ == '__main__':
	print(get_demo_lib('quad'))
	print(get_demo_lib('six'))
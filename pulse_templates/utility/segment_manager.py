class segment_mgr():
	def __init__(self, pulse):
		self.segments = list()
		self.pulse = pulse
	
	def generate_segment(self):
		seg = self.pulse.mk_segment()
		self.segments.append(seg)
		return seg

	def __len__(self):
		return len(self.segments)
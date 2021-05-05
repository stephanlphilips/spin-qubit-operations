from pulse_templates.oper.operators import wait
import copy

class wait_std_set():
    def __init__(self, **kwargs):
        self.wait_time = 100
        self.kwargs = kwargs

    def __call__(self, value):
        self.wait_time = value
        return copy.copy(self)

    def build(self, segment, reset=True, **kwargs):
        if len(kwargs) == 0:
            self.kwargs['t_wait']= self.wait_time
        else:
            self.kwargs['t_wait'] = kwargs['t_wait']
        wait(segment, **self.kwargs)

    def __copy__(self):
        cpy = wait_std_set(**self.kwargs)
        cpy.wait_time = self.wait_time
        return cpy

if __name__ == '__main__':
    from pulse_templates.utility.segment_manager import segment_mgr

    from pulse_templates.demo_pulse_lib.virtual_awg import get_demo_lib

    pulse = get_demo_lib('quad')
    ss = segment_mgr(pulse)
    w = wait_std_set(ss, gates=('P1',), p_0=(0,))
    w.add()
    a = w(150)
    b = w(50)
    a.add()
    b.add()
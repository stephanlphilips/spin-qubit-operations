'''
Typical init pulses. This is a file that contains very simple pulse.
The reason to have this basic functionanlity is that before more advanved
experiments are done, it is better to work with a limited amount of control.

In this case this is achieved by only allowing plunger control of 2 dots.
A more advanced version would also have full barrier control/more levels.

The main pulse are described here,
    * pulse_intra(*args) : pulse over a transition line of 1 dot (e.g. N=0->N=1)
    * pulse_inter(*args) : pulse trough a anticrossing
'''
from pulse_templates.utility.template_wrapper import template_wrapper 
from pulse_templates.utility.oper import add_block, add_ramp


@template_wrapper
def pulse_intra(segment, gates, t_wait, t_ramp, p_0, p_1, **kwargs):
    '''
    pulse over a transition line of 1 dot (e.g. N=0->N=1).
    first wait at p_0, the adiabatically ramp to p_1

    Args:
        segment (segment_container) : segment to which to add this stuff
        gates (tuple<str>) : plunger gate names
        t_wait (double) : time wait at p_0
        p_0 (tuple <double>) : starting point
        p_1 (tuple<double>) : end point after the ramp
    '''
    # wait a bit at the first point, e.g. make sure you are in the right charge state
    add_block(segment, t_wait, gates, p_0)

    # ramp slowly to where you want to be.
    add_ramp(segment, t_ramp, gates, p_0, p_1)

@template_wrapper
def pulse_inter(segment, gates, t_ramp, p_0, p_1, p_2, p_3, **kwargs):
    '''
    pulse sequence to go adiabatically trough an interdot.
    The standard time to go from p_0 to p_1 and p_2 to p_3 is 100ns

    Args:
        segment (segment_container) : segment to which to add this stuff
        gates (tuple<str>) : plunger gate names
        t_ramp (double) : time to linearly ramp trought the anticrossing
        p_0 (tuple <double>) : starting point
        p_1 (tuple<double>) : point where goig in the anticrossin
        p_2 (tuple <double>) : point where going out of the anti-crossing
        p_3 (tuple<double>) : end point
    '''
    # move towards anti-crossing, standaard 100ns
    add_ramp(segment, 100, gates, p_0, p_1)

    # go though the anti-crossing
    add_ramp(segment, t_ramp, gates, p_1, p_2)

    # move towards anti-crossing, standaard 100ns
    add_ramp(segment, 100, gates, p_2, p_3)

if __name__ == '__main__':
    from pulse_templates.utility.plotting import plot_seg
    from pulse_templates.demo_pulse_lib.virtual_awg import get_demo_lib
    
    pulse = get_demo_lib('quad')
    seg = pulse.mk_segment()

    gates = ('P1', 'P2')
    
    p_0 = (-7, -4)
    p_1 = (-5, -4)
    pulse_intra(seg, gates, t_wait=1000, t_ramp=2000, p_0=p_0, p_1=p_1)
    
    p_0 = (-3, -4)
    p_1 = (-0, -4)
    pulse_intra(seg, gates, t_wait=1000, t_ramp=2000, p_0=p_0, p_1=p_1)
    
    p_0 = ( 0, -4)
    p_1 = ( 1, -1)
    p_2 = (-1,  1)
    p_3 = (-5,  5)
    pulse_inter(seg, gates, t_ramp=5000, p_0=p_0, p_1=p_1, p_2=p_2, p_3=p_3)
    
    plot_seg(seg)
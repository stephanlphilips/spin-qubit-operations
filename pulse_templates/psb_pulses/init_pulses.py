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
# import 


def pulse_intra(segment, gates, t_wait, t_ramp, p_0, p_1):
    P1, P2 = gates

    # wait at start point to relax in the hot spot
    getattr(segment, P1).add_block(0, t_wait, p_0[0])
    getattr(segment, P2).add_block(0, t_wait, p_0[1])
    segment.reset_time()

    # jumpt out of the relaxation spot -- stay in the eigenstates
    getattr(segment, P1).add_ramp_ss(0, t_ramp, p_0[0], p_1[0])
    getattr(segment, P2).add_ramp_ss(0, t_ramp, p_0[1], p_1[1])
    segment.reset_time()
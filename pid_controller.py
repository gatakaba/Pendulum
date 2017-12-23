import math

from base_controller import BaseController


class PIDController(BaseController):
    def __init__(self):
        super().__init__()
        self.cum_e = 0
        self.old_e = 0

    def manipulate2(self, state):
        kp = 0.005
        kd = 0.01
        ki = 0.000001

        e = (state[0] - math.pi)

        d_e = e - self.old_e
        self.cum_e += e
        self.old_e = e

        torque = 0.005 * e + 0.000001 * self.cum_e + 0.01 * d_e

        return torque

    def manipulate(self, state):
        point = 3.14
        kp = 0.002

        pd = point - state[0]

        acc = pd * kp

        calc_torque = acc

        return calc_torque

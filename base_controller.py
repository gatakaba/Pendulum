"""
Controllerベースクラス
"""
import abc


class BaseController(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    @abc.abstractclassmethod
    def manipulate(self, state):
        return 0

class PIDController(BaseController):
    def __init__(self):
        super().__init__()

    def manipulate(self, state):
        return torque
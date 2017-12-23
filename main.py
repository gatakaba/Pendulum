import sys
import tkinter
import math

# from controller import QLearning
from pid_controller import PIDController
from q_controller import QLearning


class Pendulum(object):
    def __init__(self, dt):
        self.dt = dt
        self.theta = 0
        self.theta_dot = 0.01
        self.l = 200

    def update(self, torque=0):
        """オイラー法によって、振り子の角度を計算する"""
        c = 50
        self.theta_dot += (-9.8 / self.l ** 2 * math.sin(self.theta) - c / (
            self.l ** 2) * self.theta_dot) * self.dt + torque
        self.theta += self.theta_dot * self.dt

        self.theta = self.theta % (2 * math.pi)
        return

    def get_state(self):
        return self.theta, self.theta_dot

    def get_position(self):
        x = self.l * math.sin(self.theta)
        y = self.l * math.cos(self.theta)
        return x, y


class PendulumViewer():
    def __init__(self):
        # 描画処理
        self.root = tkinter.Tk()
        self.root.title(u"PendulumViewer")
        self.root.geometry("800x600")
        self.canvas = tkinter.Canvas(self.root, width=800, height=400)
        self.canvas.pack()

        self.circle_radius = 10
        self.gx = 400
        self.gy = 175
        self.dt = 5
        self.torque = 0
        # 振り子初期化
        self.pendulum = Pendulum(self.dt)
        # self.controller = QLearning()
        self.root.bind("<Key>", self.key)
        self.controller = QLearning()

    def key(self, event):
        torque = 0
        if event.char == 'z':
            torque = -0.01
        elif event.char == 'x':
            torque = 0.01
        else:
            torque = 0
        self.pendulum.update(torque)

    def update(self):
        torque = self.controller.manipulate(self.pendulum.get_state())
        self.pendulum.update(torque)

    def draw(self):
        self.update()

        x, y = self.pendulum.get_position()
        x += self.gx
        y += self.gy
        self.canvas.delete("all")
        self.canvas.create_oval(-self.circle_radius + x,
                                - self.circle_radius + y,
                                self.circle_radius + x,
                                self.circle_radius + y, tag="oval")

        self.canvas.create_line(self.gx, self.gy, x, y)
        self.root.after(self.dt, self.draw)


p = PendulumViewer()

for i in range(100000):
    p.update()

p.draw()
p.root.mainloop()

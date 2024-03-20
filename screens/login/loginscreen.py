from kivy.animation import Animation
from kivy.uix.button import Button
from kivymd.uix.screen import MDScreen
from kivy.config import Config
from kivy.uix.widget import Widget
from kivy.graphics import Line, Color
from random import randint
from kivy.clock import Clock
from kivy.properties import ListProperty
from math import sin, cos


class LoginScreen(MDScreen):
    def handle_key_down(self, window, key, *args):
        if key == 'shift':
            print("Shift key pressed")

class ParticleMesh(Widget):
    points = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.direction = []
        self.point_number = 70
        Clock.schedule_once(lambda dt: self.plot_points(), 6)

    def verificador(self,root):
        if root.current!="LoginScreen" or root.current!="LoadingScreen":
            self.point_number=0


    def plot_points(self):
        for _ in range(self.point_number):
            x = randint(0, self.width)
            y = randint(0, self.height)
            self.points.extend([x, y])
            self.direction.append(randint(0, 359))
        Clock.schedule_interval(self.update_positions, 0)

    def draw_lines(self):
        self.canvas.after.clear()
        with self.canvas.after:
            for i in range(0, len(self.points), 2):
                for j in range(i + 2, len(self.points), 2):

                    d = self.distance_between_points(self.points[i], self.points[i + 1], self.points[j],
                                                     self.points[j + 1])
                    if d > 120:
                        continue
                    color = d / 120
                    Color(rgba=[color, color, color, 1])
                    Line(points=[self.points[i], self.points[i + 1], self.points[j], self.points[j + 1]])

    def update_positions(self, *args):
        step = 1
        for i, j in zip(range(0, len(self.points), 2), range(len(self.direction))):
            theta = self.direction[j]
            self.points[i] += step * cos(theta)
            self.points[i + 1] += step * sin(theta)

            if self.off_screen(self.points[i], self.points[i + 1]):
                self.direction[j] = 90 + self.direction[j]

        self.draw_lines()

    @staticmethod
    def distance_between_points(x1, y1, x2, y2):
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def off_screen(self, x, y):
        return x < -5 or x > self.width + 5 or y < -5 or y > self.height + 5



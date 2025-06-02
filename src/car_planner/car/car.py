from math import cos, sin

import numpy as np

from gridsim.shapes import Rectangle
import gridsim.glutils as GLUtils


class Car:
    def __init__(self, x0: float, y0: float, yaw: float) -> None:
        self.rect = Rectangle(x0, y0, 0.05, 0.1, yaw)

    def draw(self) -> None:
        self.rect.draw()

    def to_grid(self) -> list:
        upper = 0.25 * self.rect.h * np.array(
            [-sin(self.rect.yaw), cos(self.rect.yaw)]
        )
        points = [
            self.rect.center + upper, 
            self.rect.center - upper
        ]
        for point in points:
            GLUtils.draw_point(*point, size=5)
        return points


import math

import numpy as np

import gridsim.glutils as GLUtils


class Point:
    def __init__(self, x: float, y: float) -> None:
        self.coords = np.array([x, y])

    def draw(self, **kwargs) -> None:
        x, y = self.coords
        GLUtils.draw_point(x, y, **kwargs)


class Circle:
    def __init__(self, x: float, y: float, r: float) -> None:
        self.coords = np.array([x, y])
        self.r = r

    def draw(self, **kwargs) -> None:
        pts = [
            [
                self.coords[0] + self.r * np.cos(th),
                self.coords[1] + self.r * np.sin(th),
            ]
            for th in np.linspace(0, 2*np.pi, 50)
        ]
        GLUtils.draw_polygon(pts, **kwargs)


class Rectangle:
    def __init__(self, x: float, y: float, w: float, h: float, yaw: float) -> None:
        self.center = np.array([x, y])
        self.w = w
        self.h = h
        self.yaw = yaw

    def draw(self, **kwargs) -> None:
        w_cth = self.w * math.cos(self.yaw)
        w_sth = self.w * math.sin(self.yaw)
        h_cth = self.h * math.cos(self.yaw)
        h_sth = self.h * math.sin(self.yaw)
        points = self.center + 0.5*np.array([
            [w_cth - h_sth, w_sth + h_cth],
            [-w_cth - h_sth, -w_sth + h_cth],
            [-w_cth + h_sth, -w_sth - h_cth],
            [w_cth + h_sth, w_sth - h_cth],
        ])

        GLUtils.draw_polygon(points, **kwargs)


class Line:
    def __init__(self, end_a: list, end_b: list) -> None:
        self.end_a = end_a
        self.end_b = end_b

    def draw(self, **kwargs) -> None:
        GLUtils.draw_line([self.end_a, self.end_b], **kwargs)

    @property
    def slope(self) -> float:
        return math.atan2(
            self.end_b[1] - self.end_a[1],
            self.end_b[0] - self.end_a[0]
        )

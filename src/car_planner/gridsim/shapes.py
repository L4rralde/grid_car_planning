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

        GLUtils.draw_polygon(pts)
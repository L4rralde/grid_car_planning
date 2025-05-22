import numpy as np

import gridsim.glutils as GLUtils


class Point:
    def __init__(self, x: float, y: float) -> None:
        self.coords = np.array([x, y])

    def draw(self, **kwargs) -> None:
        x, y = self.coords
        GLUtils.draw_point(x, y, **kwargs)

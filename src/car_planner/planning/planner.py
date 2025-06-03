import numpy as np

from car.car import Car
from reeds_shepp.reeds_shepp import get_optimal_path
from reeds_shepp.draw import trace_path_points
import gridsim.glutils as GLUtils

class Planner:
    def __init__(self, grid: object) -> None:
        self.grid = grid

    def sample(self, r: float=0.02) -> list:
        while True:
            x, y, yaw = np.random.uniform(-1, 1, 3)
            car = Car(x, y, yaw)
            if car.collides(self.grid):
                continue
            return x, y, yaw

    def steer(self, start: tuple, end: tuple) -> bool:
        path = get_optimal_path(start, end)
        poses = trace_path_points(path, start)
        pts = np.array([(x, y) for x, y, _ in poses])
        GLUtils.draw_line(pts, size=4)

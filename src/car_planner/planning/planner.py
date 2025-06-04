import random

import numpy as np

from car.car import Car
from reeds_shepp.reeds_shepp import get_optimal_path, path_length
from reeds_shepp.draw import trace_path_points
import gridsim.glutils as GLUtils
from planning.tree import Tree


def distance(a: list, b: list) -> float:
    acc = 0.0
    for i in range(len(a)):
        acc += (a[i] - b[i])**2
    d = acc**0.5
    return d


class Path:
    def __init__(self, start: list, path: object) -> None:
        self.start = start
        self.path = path

    @property
    def length(self) -> float:
        return path_length(self.path)

    @classmethod
    def optimal_path(cls, start: list, goal: list) -> "Path":
        path = get_optimal_path(start, goal, 0.1)
        object = cls(start, path)
        return object

    def draw(self) -> None:
        poses = trace_path_points(self.path, self.start, 0.1)
        pts = np.array([[x, y] for x, y, _ in poses])
        GLUtils.draw_line(pts, size=3)


class Planner:
    def __init__(self, grid: object, start: list, goal: list) -> None:
        self.grid = grid
        self.start = start
        self.goal = goal
        self.milestones = [start]
        self.tree = Tree(start)

    def pose_collides(self, pose: list) -> bool:
        x, y, yaw = pose
        car = Car(x, y, yaw)
        return car.collides(self.grid)

    def sample(self) -> list:
        while True:
            x, y, yaw = np.random.uniform(-1, 1, 3)
            if self.pose_collides((x, y, yaw)):
                continue
            return x, y, yaw

    def nearest(self, sample: list, r: float = 0.5) -> list:
        #Find in a ball
        near = [
            vertex for vertex in self.milestones
            if distance(vertex, sample) < r
        ]
        if not near:
            return []
        #Optimal path
        min_dist = np.inf
        nearest_v = None
        for vertex in near:
            dist = Path.optimal_path(vertex, sample).length
            if  dist < min_dist:
                min_dist = dist
                nearest_v = vertex
        return nearest_v

    def update(self) -> bool:
        sample = self.sample()
        nearest = self.nearest(sample, 0.5)
        if not nearest:
            return
        self.milestones.append(sample)
        paren_node = self.tree.find(nearest)
        paren_node.append(sample)

    def draw_tree(self, start_node=None) -> None:
        current = start_node or self.tree.root
        for child in current.children:
            Path.optimal_path(current.data, child.data).draw()
            self.draw_tree(child)

    def draw_milestones(self) -> None:
        for x, y, _ in self.milestones:
            GLUtils.draw_point(x, y, size=10)

    def draw(self) -> None:
        self.draw_milestones()
        self.draw_tree()
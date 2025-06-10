import random
import math

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

    def draw(self, **kwargs) -> None:
        poses = self.get_poses()
        pts = np.array([[x, y] for x, y, _ in poses])
        GLUtils.draw_line(pts, **kwargs)

    def get_poses(self) -> list:
        return trace_path_points(self.path, self.start, 0.1)

class Planner:
    def __init__(self, grid: object, start: list, goal: list) -> None:
        self.grid = grid
        self.start = start
        self.goal = goal
        self.milestones = [start]
        self.tree = Tree(start)

    def reset(self, *, start: list=None, goal: list=None) -> None:
        if start is not None:
            self.start = start
        if goal is not None:
            self.goal = goal
        self.milestones = [self.start]
        self.tree = Tree(self.start)

    def pose_collides(self, pose: list) -> bool:
        x, y, yaw = pose
        car = Car(x, y, yaw)
        return car.collides(self.grid)

    def sample(self) -> list:
        if random.random() > 0.75:
            almost_goal = list(np.random.normal(self.goal, (.1, .1, 0.2)))
            return almost_goal
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

    def steer(self, vertex: list, sample: list, step_size = 0.2) -> None:
        dx = sample[0] - vertex[0]
        dy = sample[1] - vertex[1]
        d = math.hypot(dx, dy)
        angle = math.atan2(dy, dx)

        #Sample inside circle. No need to project.
        if d <= step_size:
            return sample

        new_x = vertex[0] + step_size * math.cos(angle)
        new_y = vertex[1] + step_size * math.sin(angle)
        #new_theta = angle  # align orientation to movement direction

        new_sample = (new_x, new_y, sample[2])
        return new_sample

    def path_collides(self, start: list, end: list) -> bool:
        path = Path.optimal_path(start, end)
        for pose in path.get_poses():
            if self.pose_collides(pose):
                return True
        return False

    def update(self) -> bool:
        sample = self.sample()
        nearest = self.nearest(sample, )
        if not nearest:
            return False
        sample = self.steer(nearest, sample, 0.15)
        if self.path_collides(nearest, sample):
            return False
        self.milestones.append(sample)
        parent_node = self.tree.find(nearest)
        parent_node.append(sample)
        finished = self.close_enough(sample, 0.04)
        if finished:
            self.goal = sample
        return finished

    def draw_tree(self, start_node=None) -> None:
        current = start_node or self.tree.root
        for child in current.children:
            #path = Path.optimal_path(current.data, child.data)
            #path.draw(size=2, color=(0.96, 0.5, 0.6, 1.0))
            self.draw_tree(child)

    def draw_milestones(self) -> None:
        for x, y, _ in self.milestones:
            GLUtils.draw_point(x, y, size=3)

    def get_route(self) -> list:
        current = self.tree.find(self.goal)
        if current is None:
            return []
        rev_hierarchy = [current.data]
        while current.parent is not None:
            current = current.parent
            rev_hierarchy.append(current.data)
        hierarchy = rev_hierarchy[::-1]

        poses = []
        for i in range(len(hierarchy) - 1):
            current_path = Path.optimal_path(hierarchy[i], hierarchy[i+1])
            poses += current_path.get_poses()

        return poses

    def draw_route(self) -> None:
        route = self.get_route()
        if route == []:
            return
        pts = [(x, y) for x,y,_ in route]
        GLUtils.draw_line(pts, size=3, color=(0.52, 0.11, 0.24, 1))

    def draw(self) -> None:
        self.draw_tree()
        self.draw_route()
        self.draw_milestones()

    def close_enough(self, sample: list, th: float=0.2) -> bool:
        goal_x, goal_y, goal_yaw = self.goal
        x, y, yaw = sample
        weighed_d = (
            (goal_x - x)**2 + (goal_y - y)**2 +
            0.001*(goal_yaw - yaw)**2
        )
        weighed_d = weighed_d**0.5
        return weighed_d < th

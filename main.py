import numpy as np
import pygame

from gridsim.scenes import GLScene
from collisions.grid import Grid
from utils.utils import GIT_ROOT
from gridsim.glutils import load_texture_from_image, draw_background, draw_point
from gridsim.shapes import Line
from car.car import Car
from planning.planner import Planner


class GridScene(GLScene):
    def __init__(self, title: str, width: int, height: int, max_fps: int) -> None:
        super().__init__(title, width, height, max_fps)
        self.grid = Grid()
        self.texture_bg = self.load_surface()
        self.goal_pose_line = None
        self.goal = [0.2, 0.2, 0.0]
        x0, y0, yaw0 = (0, 0, 0)
        self.start = [x0, y0, yaw0]
        self.planner = Planner(self.grid, self.start, self.goal)
        self.car = Car(x0, y0, yaw0)
        self.state = "SAMPLING"

    def reset(self, *, start: list=None, goal: list=None) -> None:
        if start is not None:
            self.start = start
        if goal is not None:
            self.goal = goal
        self.state = "SAMPLING"
        self.planner.reset(start=start, goal=goal)
        x0, y0, yaw0 = self.start
        self.car.reset(x0, y0, yaw0)

    def render(self, **kwargs) -> None:
        super().render(**kwargs)
        draw_background(*self.texture_bg)
        #self.grid.draw(point_size = 5)
        draw_point(self.goal[0], self.goal[1], size=10, color=(1, 0, 0, 1))
        self.planner.draw()
        self.car.draw()
        #Path.optimal_path(self.start, self.goal).draw()
        if self.state == "SET_POSE":
            self.goal_pose_line.draw(size=2)

    def get_inputs(self, **kwargs) -> None:
        super().get_inputs(**kwargs)

        for event in self.events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.state = "SET_POSE"
                x, y = pygame.mouse.get_pos()
                ortho_x, ortho_y = self.to_ortho(x, y)
                self.goal_pose_line = Line([ortho_x, ortho_y], [ortho_x, ortho_y])
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                x, y = pygame.mouse.get_pos()
                ortho_x, ortho_y = self.to_ortho(x, y)
                start = [ortho_x, ortho_y, 0.0]
                self.reset(start=start)
            if self.state == "SET_POSE" and event.type == pygame.MOUSEMOTION:
                x, y = pygame.mouse.get_pos()
                ortho_x, ortho_y = self.to_ortho(x, y)
                enda_x, enda_y = self.goal_pose_line.end_a
                dx, dy = ortho_x - enda_x, ortho_y - enda_y
                len = (dx**2 + dy**2)**0.5
                dx, dy = 0.1*dx/len, 0.1*dy/len
                self.goal_pose_line.end_b = [enda_x + dx, enda_y + dy]
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                goal = [*self.goal_pose_line.end_a, self.goal_pose_line.slope]
                self.reset(start=self.car.pose, goal=goal)
                self.state = "SAMPLING"

    def load_surface(self) -> object:
        image_path = f"{GIT_ROOT}/world/parking.jpeg"
        surface = pygame.image.load(image_path)
        #surface = pygame.transform.flip(surface, False, True)  # Flip vertically
        image = pygame.image.tostring(surface, "RGB", True)
        width, height = surface.get_size()
        return load_texture_from_image(image, width, height)

    def update(self, **kwargs) -> None:
        super().update(**kwargs)
        if self.state == "SAMPLING":
            finished = self.planner.update()
            if finished:
                self.state = "DRIVING"
                self.car.trigger(self.planner.get_route())
        if self.state == "DRIVING":
            self.car.drive()

def main():
    scene = GridScene("Grid", 750, 750, 100)
    scene.run()


if __name__ == '__main__':
    main()

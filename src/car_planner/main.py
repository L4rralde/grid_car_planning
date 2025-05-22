import numpy as np
import pygame

from gridsim.scenes import GLScene
from gridsim.grid import Grid
from utils.utils import GIT_ROOT
from gridsim.glutils import load_texture_from_image, draw_background
from gridsim.shapes import Circle

class GridScene(GLScene):
    def __init__(self, title: str, width: int, height: int, max_fps: int) -> None:
        super().__init__(title, width, height, max_fps)
        self.left_mouse_down = False
        self.right_mouse_down = False
        self.grid = Grid()
        self.texture_bg = self.load_surface()
        self.circle = Circle(0, 0, 0.1)

    def render(self, **kwargs) -> None:
        super().render(**kwargs)
        draw_background(*self.texture_bg)
        self.grid.draw(point_size = 5)
        self.circle.draw()

    def get_inputs(self, **kwargs) -> None:
        return super().get_inputs(**kwargs)
        for event in self.events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
                self.left_mouse_down = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button==3:
                self.right_mouse_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.left_mouse_down = False
                self.right_mouse_down = False
            elif event.type == pygame.MOUSEMOTION and self.left_mouse_down:
                x, y = pygame.mouse.get_pos()
                ortho_x, ortho_y = self.to_ortho(x, y)
                self.grid.append(ortho_x, ortho_y)
            elif event.type == pygame.MOUSEMOTION and self.right_mouse_down:
                x, y = pygame.mouse.get_pos()
                ortho_x, ortho_y = self.to_ortho(x, y)
                self.grid.pop(ortho_x, ortho_y)

    def load_surface(self) -> object:
        image_path = f"{GIT_ROOT}/world/parking.jpeg"
        surface = pygame.image.load(image_path)
        #surface = pygame.transform.flip(surface, False, True)  # Flip vertically
        image = pygame.image.tostring(surface, "RGB", True)
        width, height = surface.get_size()
        return load_texture_from_image(image, width, height)


def main():
    scene = GridScene("Grid", 800, 800, 20)
    scene.run()


if __name__ == '__main__':
    main()

import sys

import pygame
from pygame.locals import DOUBLEBUF, OPENGL

import gridsim.glutils as GLUtils


class Scene:
    def __init__(self, title: str, width: int, height: int, max_fps: int) -> None:
        self.title = title
        self.max_fps = max_fps
        self.screen_width = width
        self.screen_height = height
        pygame.init()
        self.display = pygame.display.set_mode(
            (width, height),
            DOUBLEBUF | OPENGL
        )
        self.clock = pygame.time.Clock()

    def run(self, **kwargs) -> None:
        self.setup(**kwargs)
        while True:
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.finish(**kwargs)
                    sys.exit()
            self.delta_time = self.clock.tick(self.max_fps)/1000
            self.get_inputs(**kwargs)
            self.update(**kwargs)
            self.render(**kwargs)

            pygame.display.flip()
            pygame.display.set_caption(
                f"{self.title} ({self.clock.get_fps():.2f} fps)"
            )
    
    def setup(self, **kwargs) -> None:
        pass

    def get_inputs(self, **kwargs) -> None:
        pass

    def update(self, **kwargs) -> None:
        pass

    def render(self, **kwargs) -> None:
        GLUtils.prepare_render(**kwargs)

    def finish(self, **kwargs) -> None:
        pass


class GLScene(Scene):
    def setup(self, **kwargs) -> None:
        GLUtils.init_ortho(-1, 1, -1, 1)

    def to_ortho(self, x, y) -> tuple:
        return (
            (2*x - self.screen_width)/self.screen_width,
            -(2*y - self.screen_height)/self.screen_height
        )
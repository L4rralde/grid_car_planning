from OpenGL.GL import *
from OpenGL.GLU import *


def init_ortho(left: int, right: int, top: int, bottom: int) -> None:
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(left, right, top, bottom)
  

def prepare_render(**kwargs) -> None:
    bg_color = kwargs.get("background_color", (0.0, 0.0, 0.0, 1.0))
    glClearColor(*bg_color)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def draw_point(x: int, y: int, **kwargs) -> None:
    color = kwargs.get("color", (1, 1, 1, 1))
    size = kwargs.get("size", 1)

    glColor(*color)
    glPointSize(size)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def draw_polygon(points: list, **kwargs) -> None:
        color = kwargs.get("color", (0.1, 0.1, 0.2, 1))
        size = kwargs.get("size", 1)

        glColor(*color)
        glPointSize(size)
        glBegin(GL_TRIANGLE_FAN)
        for x, y in points:
            glVertex2f(x, y)
        glEnd()


def load_texture_from_image(image: object, width: int, height):
    # Generate OpenGL texture
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,
                 0, GL_RGB, GL_UNSIGNED_BYTE, image)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return texture_id, width, height


def draw_background(tex_id, width, height):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
    glColor4f(1.0, 1.0, 1.0, 1.0)

    # Cover full normalized viewport [-1, 1]
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(-1, -1)
    glTexCoord2f(1, 0); glVertex2f( 1, -1)
    glTexCoord2f(1, 1); glVertex2f( 1,  1)
    glTexCoord2f(0, 1); glVertex2f(-1,  1)
    glEnd()

    glDisable(GL_TEXTURE_2D)
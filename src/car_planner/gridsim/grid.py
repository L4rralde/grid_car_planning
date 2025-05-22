import numpy as np

from gridsim.shapes import Point
from utils.utils import GIT_ROOT


class Grid:
    def __init__(self, res: int=101) -> None:
        self.res = res
        self.occupancy = np.ones((self.res, self.res))
        grid_file = np.flip(np.load(f"{GIT_ROOT}/grid.npy").T, axis=1)
        self.occupancy[0:100, 0:100] = grid_file.copy()
        self.points = [
            [
                Point(*self.grid_to_ortho(i, j))
                if self.occupancy[i][j] == 1.0 else None
                for j in range(self.res)
                
            ]
            for i in range(self.res)
        ]

    def draw(self, **kwargs) -> None:
        color = kwargs.get('grid_color', (0.9, 0.2, 0.2, 1.0))
        for row in self.points:
            for pt in row:
                if pt is None:
                    continue
                pt.draw(size=5, color = color)

    def grid_to_ortho(self, i: int, j: int) -> None:
        ortho_x = 2*i/self.res - 1
        ortho_y = 2*j/self.res - 1
        return ortho_x, ortho_y

    def ortho_to_grid(self, x: float, y: float) -> None:
        i = round((x + 1)*self.res/2)
        j = round((y + 1)*self.res/2)
        return i, j

    def append(self, x: float, y: float) -> None:
        i, j = self.ortho_to_grid(x, y)
        print(i,)
        if i >= self.res or j >= self.res:
            return
        if self.occupancy[i][j] == 1.0:
            return
        self.occupancy[i][j] = 1.0
        x, y = self.grid_to_ortho(i, j)
        self.points[i][j] = Point(x, y)

    def pop(self, x: float, y: float) -> None:
        i, j = self.ortho_to_grid(x, y)
        if i >= self.res or j >= self.res:
            return
        if self.occupancy[i][j] == 0.0:
            return
        self.occupancy[i][j] = 0.0
        self.points[i][j] = None

    def save(self, path: str="grid") -> None:
        np.save(path, self.occupancy)

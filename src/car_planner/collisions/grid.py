import numpy as np

from gridsim.shapes import Point
from utils.utils import GIT_ROOT


class Grid:
    def __init__(self, res: int=101) -> None:
        self.res = res
        self.occupancy = np.load(f"{GIT_ROOT}/grid.npy")
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
        pt_size = kwargs.get('point_size', 1)
        for row in self.points:
            for pt in row:
                if pt is None:
                    continue
                pt.draw(size=pt_size, color = color)

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

    def idx_collides(self, i: int, j: int, r: int=1) -> bool:
        sub_grid = self.occupancy[
            max(0, i-r): min(i + r + 1, self.res),
            max(0, j-r): min(j + r + 1, self.res)
        ]
        return sub_grid.sum() > 0

    def point_collides(self, x: float, y: float, r: float=0.02) -> bool:
        i, j = self.ortho_to_grid(x, y)
        r = np.round(r * self.res//2).astype(int)
        return self.idx_collides(i, j, r)

    def sample(self, r: float) -> None:
        while True:
            x, y = np.random.uniform(-1.0, 1.0, 2)
            if not self.point_collides(x, y, r):
                return x, y
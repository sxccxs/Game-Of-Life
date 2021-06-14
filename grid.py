import numpy as np
import pygame as pg
from abc import ABC


colors = {
    'alive': '#000000',
    'dead': '#ffffff'
}


class AbstractGrid(ABC):

    def get_cols(self) -> int:
        return self.cells.shape[0]

    def get_rows(self) -> int:
        return self.cells.shape[1]

    def draw(self, screen: pg.Surface) -> None:
        for y in range(self.get_cols()):
            for x in range(self.get_rows()):
                rect = pg.Rect(x * self.cell_size, y * self.cell_size,
                               self.cell_size, self.cell_size)
                if self.cells[y, x] == 1:
                    pg.draw.rect(screen, colors.get('alive'), rect)
                else:
                    pg.draw.rect(screen, colors.get('dead'), rect)


class Grid(AbstractGrid):

    def __init__(self, cells: np.ndarray, cell_size: int):
        self.cells = cells
        self.cell_size = cell_size

    def update(self) -> None:
        new_generation = np.empty(self.cells.shape)
        for i in range(self.get_cols()):
            for j in range(self.get_rows()):
                state = self.cells[i, j]
                neighbors = self.count_alive_neighbours(j, i)
                if state == 0 and neighbors == 3:
                    new_generation[i, j] = 1
                elif state == 1 and (neighbors < 2 or neighbors > 3):
                    new_generation[i, j] = 0
                else:
                    new_generation[i, j] = state
        self.cells = new_generation

    def count_alive_neighbours(self, x: int, y: int) -> int:
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if ((i == x and j == y) or (y + i < 0) or
                   (x + j < 0) or (y + i >= self.get_cols()) or
                   (x + j >= self.get_rows())):
                    continue
                count += self.cells[y + i, x + j]

        return count


class SelectGrid(AbstractGrid):

    def __init__(self, cols: int, rows: int, cell_size: int):
        self.cell_size = cell_size
        self.cells = np.zeros((cols, rows))

    def cell_mouse_click(self, x: int, y: int,
                         click_pos: tuple[float, float]) -> bool:

        rect = pg.Rect(x * self.cell_size, y * self.cell_size,
                       self.cell_size, self.cell_size)
        return rect.collidepoint(click_pos)

    def update(self) -> None:
        for y in range(self.get_cols()):
            for x in range(self.get_rows()):
                if self.cell_mouse_click(x, y, pg.mouse.get_pos()):
                    self.cells[y, x] = 0 if self.cells[y, x] == 1 else 1

    def return_grid(self) -> Grid:
        return Grid(self.cells, self.cell_size)

    def randomize_grid(self) -> None:
        self.cells = np.random.randint(0, 2, (self.cells.shape))

    def clear(self) -> None:
        self.cells = np.zeros(self.cells.shape)

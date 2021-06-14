import numpy as np
import pygame as pg


class Grid:
    colors = {
        'alive': '#000000',
        'dead': '#ffffff'
    }

    def __init__(self, cols: int, rows: int, cell_size: int):
        self.cells = np.random.randint(0, 2, (cols, rows))
        self.cell_size = cell_size

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
                    pg.draw.rect(screen, self.colors.get('alive'), rect)
                else:
                    pg.draw.rect(screen, self.colors.get('dead'), rect)

    def update(self) -> None:
        new_generation = np.empty(self.cells.shape)
        for i in range(self.get_cols()):
            for j in range(self.get_rows()):
                state = self.cells[i, j]
                neighbors = self.count_alive_neighbours(i, j)
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
                   (x + j < 0) or (y + i == self.get_cols()) or
                   (x + j == self.get_rows())):
                    continue
                count += self.cells[y + i, x + j]

        return count

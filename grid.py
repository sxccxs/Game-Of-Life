import numpy as np
import pygame as pg
from abc import ABC


# Colors for dead and alive cells
colors = {
    'alive': '#000000',
    'dead': '#ffffff'
}


class AbstractGrid(ABC):
    '''
        Abstract class for Grid and SelectGrid classes, made
        to not repeat some code.
    '''

    def get_cols(self) -> int:
        '''Returns amount of columns.'''
        return self.cells.shape[0]

    def get_rows(self) -> int:
        '''Returns amount of rows.'''
        return self.cells.shape[1]

    def get_step(self):
        return (self.cell_size + self.grid_size)

    def draw(self, screen: pg.Surface) -> None:
        '''Draws cells numpy array to given screen.'''
        for y in range(self.get_cols()):
            for x in range(self.get_rows()):
                rect = pg.Rect(x * self.get_step(),
                               y * self.get_step(),
                               self.cell_size, self.cell_size)
                if self.cells[y, x] == 1:
                    pg.draw.rect(screen, colors.get('alive'), rect)
                else:
                    pg.draw.rect(screen, colors.get('dead'), rect)


class Grid(AbstractGrid):
    '''
        Grid class which handles main game logic.
        '''

    def __init__(self, cells: np.ndarray, cell_size: int, grid_size: int):
        self.cells = cells
        self.cell_size = cell_size
        self.grid_size = grid_size

    def update(self) -> None:
        '''Updates grid state depending on game rules:
              1) Any live cell with fewer than two live neighbours dies,
                 as if by underpopulation.
              2) Any live cell with two or three live neighbours
                 lives on to the next generation.
              3) Any live cell with more than three live neighbours dies,
                 as if by overpopulation.
              4) Any dead cell with exactly three live neighbours becomes
                 a live cell, as if by reproduction.
        '''
        new_generation = np.empty(self.cells.shape)
        for i in range(self.get_cols()):
            for j in range(self.get_rows()):
                state = self.cells[i][j]
                neighbors = self.count_alive_neighbours(j, i)
                if state == 0 and neighbors == 3:
                    new_generation[i][j] = 1
                elif state == 1 and (neighbors < 2 or neighbors > 3):
                    new_generation[i][j] = 0
                else:
                    new_generation[i][j] = state
        self.cells = new_generation

    def count_alive_neighbours(self, x: int, y: int) -> int:
        '''Count an amount of alive neighbours for a cell with given
            array indexes. If cell is on the edge or corner, just skips
            not existing cells.
        '''
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if ((i == 0 and j == 0) or (y + i < 0) or
                   (x + j < 0) or (y + i >= self.get_cols()) or
                   (x + j >= self.get_rows())):
                    continue
                count += self.cells[y + i][x + j]

        return count


class SelectGrid(AbstractGrid):
    '''
        Grid class which handles generation of grid, which will
        be used in the game. Allows user to generate random grid or
        to create one with mouse clicks.
    '''

    def __init__(self, cols: int, rows: int, cell_size: int,
                 grid_size: int):
        self.cell_size = cell_size
        self.cells = np.zeros((cols, rows))
        self.grid_size = grid_size

    def cell_mouse_click(self, x: int, y: int,
                         click_pos: tuple[float, float]) -> bool:
        '''Checks if cell with given coords was clicked by user'''
        rect = pg.Rect(x * self.get_step(), y * self.get_step(),
                       self.cell_size, self.cell_size)
        return rect.collidepoint(click_pos)

    def update(self) -> None:
        '''Updates grid on user click'''
        for y in range(self.get_cols()):
            for x in range(self.get_rows()):
                if self.cell_mouse_click(x, y, pg.mouse.get_pos()):
                    self.cells[y][x] = 0 if self.cells[y][x] == 1 else 1

    def return_grid(self) -> Grid:
        '''Generates Grid object based on created grid'''
        return Grid(self.cells, self.cell_size, self.grid_size)

    def randomize_grid(self) -> None:
        '''Fill grid with random values'''
        self.cells = np.random.randint(0, 2, (self.cells.shape))

    def clear(self) -> None:
        '''Clears grid'''
        self.cells = np.zeros(self.cells.shape)

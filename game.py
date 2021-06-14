from grid import Grid, SelectGrid
import pygame as pg


class Game:
    '''
        Main game class, which manages game state and calling
        game logic or user input classes.
    '''

    def __init__(self, w: int, h: int, grid_selector: SelectGrid,
                 cell_size: int, bg_color: str = '#ffffff',
                 grid_color: str = '#000000'):
        self.screen = pg.display.set_mode((w, h))
        self.bg_color = pg.Color(bg_color)
        self.grid_color = pg.Color(grid_color)
        self.cell_size = cell_size
        self.grid_selector = grid_selector
        self.grid_size = self.cell_size - self.grid_selector.cell_size
        self.grid = None

    def reset(self):
        '''Reset grid to allow user to create a new one.'''
        self.grid = None
        self.grid_selector.clear()

    def update(self, pressed: bool, finished: bool,
               randomize: bool = False) -> None:
        '''Updates and draws all background and other game objects.'''

        self.screen.fill(self.bg_color)  # draw background
        for i in range(0, self.screen.get_width(),
                       self.cell_size):
            for j in range(0, self.screen.get_height(),
                           self.cell_size):
                rect = pg.Rect(i, j, self.cell_size,
                               self.cell_size)
                pg.draw.rect(self.screen, self.grid_color, rect, 1)

        if isinstance(self.grid, Grid):  # draw grid if exists
            self.grid.draw(self.screen)
            self.grid.update()
        else:  # else draw grid input
            self.grid_selector.draw(self.screen)
            if pressed:
                self.grid_selector.update()
            if finished:
                self.grid = self.grid_selector.return_grid()
            if randomize:
                self.grid_selector.randomize_grid()

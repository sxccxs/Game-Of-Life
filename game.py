from grid import Grid, SelectGrid
import pygame as pg


class Game:
    '''
        Main game class, which manages game state and calling
        game logic or user input classes.
    '''

    def __init__(self, w: int, h: int, grid_selector: SelectGrid,
                 color: str = '#ffffff'):
        self.screen = pg.display.set_mode((w, h))
        self.color = pg.Color(color)
        self.grid_selector = grid_selector
        self.grid = None

    def reset(self):
        '''Reset grid to allow user to create a new one.'''
        self.grid = None
        self.grid_selector.clear()

    def update(self, pressed: bool, finished: bool,
               randomize: bool = False) -> None:
        '''Updates and draws all background and other game objects.'''

        self.screen.fill(self.color)  # draw background

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

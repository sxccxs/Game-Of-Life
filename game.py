from grid import Grid, SelectGrid
import pygame as pg


class Game:
    def __init__(self, w: int, h: int, grid_selector: SelectGrid,
                 color: str = '#ffffff'):
        self.screen = pg.display.set_mode((w, h))
        self.color = pg.Color(color)
        self.grid_selector = grid_selector
        self.grid = None

    def reset(self):
        self.grid = None
        self.grid_selector.clear()

    def update(self, pressed: bool, finished: bool,
               randomize: bool = False) -> None:
        self.screen.fill(self.color)
        if isinstance(self.grid, Grid):
            self.grid.draw(self.screen)
            self.grid.update()
        else:
            self.grid_selector.draw(self.screen)
            if pressed:
                self.grid_selector.update()
            if finished:
                self.grid = self.grid_selector.return_grid()
            if randomize:
                self.grid_selector.randomize_grid()

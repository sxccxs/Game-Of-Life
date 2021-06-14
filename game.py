from grid import Grid
import pygame as pg


class Game:
    def __init__(self, w: int, h: int, grid: Grid, color: str = '#ffffff'):
        self.screen = pg.display.set_mode((w, h))
        self.color = pg.Color(color)
        self.grid = grid

    def update(self):
        self.screen.fill(self.color)
        self.grid.draw(self.screen)
        self.grid.update()

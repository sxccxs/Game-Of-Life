from game import Game
from grid import Grid
import pygame as pg


pg.init()
fps = 60
clock = pg.time.Clock()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
CELL_SIZE = 15


grid = Grid(SCREEN_WIDTH//CELL_SIZE, SCREEN_HEIGHT//CELL_SIZE, CELL_SIZE)
game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, grid)


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit(0)

    game.update()

    pg.display.update()
    clock.tick(fps)

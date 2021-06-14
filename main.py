from game import Game
from grid import SelectGrid
import pygame as pg


pg.init()
fps = 60
clock = pg.time.Clock()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
CELL_SIZE = 10


grid_selector = SelectGrid(SCREEN_HEIGHT//CELL_SIZE, SCREEN_WIDTH//CELL_SIZE,
                           CELL_SIZE)
game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, grid_selector)

finish = False

while True:
    pressed = False
    randomize = False
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit(0)
        if event.type == pg.MOUSEBUTTONDOWN:
            pressed = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                finish = True
                restart = False
            elif event.key == pg.K_SPACE:
                randomize = True
            elif event.key == pg.K_ESCAPE:
                finish = False
                game.reset()

    game.update(pressed, finish, randomize)

    pg.display.update()
    clock.tick(fps)

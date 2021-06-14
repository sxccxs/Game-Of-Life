from game import Game
from grid import SelectGrid
import pygame as pg

# Pygame initializitaion
pg.init()
fps = 60
clock = pg.time.Clock()

# Game constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
CELL_SIZE = 10

# Game objects
grid_selector = SelectGrid(SCREEN_HEIGHT//CELL_SIZE,
                           SCREEN_WIDTH//CELL_SIZE,
                           CELL_SIZE)
game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, grid_selector)

# Controls if player ended creation of the starting grid
finish = False

while True:
    # Controls if mouse was pressed
    pressed = False

    # Controls if it is needed to generate random starting grid
    randomize = False

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit(0)
        if event.type == pg.MOUSEBUTTONDOWN:  # If mouse clicked
            pressed = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:  # If Enter clicked
                finish = True
                restart = False
            elif event.key == pg.K_SPACE:  # If Space clicked
                randomize = True
            elif event.key == pg.K_ESCAPE:  # If Escape clicked
                finish = False
                game.reset()

    game.update(pressed, finish, randomize)  # update game

    pg.display.update()
    clock.tick(fps)

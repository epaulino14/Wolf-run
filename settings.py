import pygame as pg



# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BLUE = (0,0,255)
FONT_NAME = 'arial'

# game settings
WIDTH = 500   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 300  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Tilemap Demo"
BGCOLOR = LIGHTBLUE
SPRITESHEET = "spritesheet_jumper.png"

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Player settings
PLAYER_SPEED = 300
idle= pg.image.load('standing.png')
walkRight = [pg.image.load('R1.png'), pg.image.load('R2.png'), pg.image.load('R3.png'), pg.image.load('R4.png'), pg.image.load('R5.png'), pg.image.load('R6.png'), pg.image.load('R7.png'), pg.image.load('R8.png')]
PLAYER_HIT_RECT = pg.Rect(0,0,32,48)

# items
coins = [pg.image.load("star coin 1.png"), pg.image.load("star coin 2.png"), pg.image.load("star coin 3.png"),pg.image.load("star coin 4.png"),pg.image.load("star coin 5.png"),pg.image.load("star coin 6.png")]


# mobs
bee = [pg.image.load("fly1.png"), pg.image.load("fly2.png")]
RM = [pg.image.load("RM1.png"), pg.image.load("RM2.png"),pg.image.load("RM3.png"), pg.image.load("RM4.png"),pg.image.load("RM5.png"), pg.image.load("RM6.png"), pg.image.load("RM7.png"), pg.image.load("RM8.png")]

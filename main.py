# KidsCanCode - Game Development with Pygame video series
# Tile-based game - Part 4
# Scrolling Map/Camera
# Video link: https://youtu.be/3zV2ewk-IGU
import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *
import random

def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x,y,fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        self.spritesheet = Spritesheet(path.join(img_folder, SPRITESHEET))
        map_folder = path.join(game_folder, 'map')
        self.map = TileMap(path.join(map_folder, 'world1.tmx'))
        #self.map = TileMap(path.join(map_folder, 'level2.tmx'))
        self.dim_screen =pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0,0,0,180))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
##        for row, tiles in enumerate(self.map.data):
##            for col, tile in enumerate(tiles):
##                if tile == '1':
##                    Wall(self, col, row)
##                if tile == 'P':
##                    self.player = Player(self, col, row)

        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width/2,
                             tile_object.y + tile_object.height/2)
            if tile_object.name == 'player':
                self.player = Player(self,obj_center.x, obj_center.y)
           
            if tile_object.name == 'wall':
                Obstacle(self,tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'coin':
                Coin(self,tile_object.x, tile_object.y)
            if tile_object.name == 'mob':
                Mob(self,tile_object.x, tile_object.y)
            if tile_object.name == 'RM':
                RockMonster(self,tile_object.x, tile_object.y)
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        coin_hits = pg.sprite.spritecollide(self.player, self.items,True)
        if coin_hits:
            self.player.collected_coins += 1

        # mobs hit player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False)
        for hit in hits:
            
            self.player.health -= 10
            hit.vel = vec(0,0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            if hits[0].rect.centerx > self.player.rect.centerx:
                self.player.rect.center += vec(-50, 0)
            else:
                if hits[0].rect.centerx < self.player.rect.centerx:
                    self.player.rect.center += vec(50, 0)
        
            
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)
    

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        #self.screen.fill(BGCOLOR)
        #self.draw_grid()
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        self.draw_text("coins:" + str(self.player.collected_coins), 22, YELLOW, 35, 10)
        draw_player_health(self.screen, 100, 10, self.player.health / 100)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()

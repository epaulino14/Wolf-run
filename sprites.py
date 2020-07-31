import pygame as pg
from settings import *
vec=  pg.math.Vector2

class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        #grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x, y, width, height))
        image = pg.transform.scale(image, (width//2, height//2))
        return image

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.onGround = False
        self.left = False
        self.right = False
        self.current_frame = 0
        self.last_update = 0
        self.collected_coins = 0
        self.health = 100
        self.walking =False
        self.load_images()
        self.image = self.walking_frame_r[0]
        self.rect = self.image.get_rect()
        self.rect.center = vec(x,y)
        self.vx = 0
        self.vy = 0

    def load_images(self):
            
        self.walking_frame_r = walkRight
        for frame in self.walking_frame_r:
            frame.set_colorkey(BLACK)
        
        self.walking_frame_l =[]
        for frame in self.walking_frame_r:
            frame.set_colorkey(BLACK)
            self.walking_frame_l.append(pg.transform.flip(frame,True, False))

    def animate(self):
        now = pg.time.get_ticks()
        if self.vx != 0:
            self.walking = True
        else:
            self.walking =False

        if self.walking:
            if now - self.last_update > 60:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frame_l)
                
                if self.vx > 0 and self.right:
                    self.image = self.walking_frame_r[self.current_frame]
                    self.left = False
                else:
                    if self.left:
                        self.image = self.walking_frame_l[self.current_frame]
                        self.right = False
             

        
        if self.right and not self.walking:
            self.image = self.walking_frame_r[0]
            
            
        if self.left and not self.walking:
            self.image = self.walking_frame_l[0]
                
    def get_keys(self):
        self.vx= 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -5
            self.left =True
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = 5
            self.right = True
        
        if keys [pg.K_SPACE]:
            if self.onGround:
                self.vy -= 10
          
                       
    def collide_with_walls(self,vxDelta, vyDelta,platforms ):

        for i in platforms:
            if pg.sprite.collide_rect(self, i, ):
                if vxDelta > 0:
                    self.rect.right = i.rect.left
                if vxDelta < 0:
                    self.rect.left = i.rect.right
                if vyDelta > 0:
                    self.rect.bottom  = i.rect.top
                    self.vy = 0
                    self.onGround = True
                if vyDelta < 0:
                    self.rect.top = i.rect.bottom
            
            
    
    def update(self):
        self.animate()
        

        if not self.onGround and self.vy < 100:
            self.vy += 0.5

        self.get_keys()
        self.rect.x += self.vx
        self.collide_with_walls(self.vx,0,self.game.walls)
        self.rect.y += self.vy
        self.onGround = False
        self.collide_with_walls(0,self.vy,self.game.walls) 

        

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self._layer = 3
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game =  game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x 
        self.rect.y = y


class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image =  self.coin[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    

    def load_images(self):
        self.coin= coins
        for frame in self.coin:
            frame.set_colorkey(BLACK)
    def animate(self):
        now = pg.time.get_ticks()
    
        if now - self.last_update > 180:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.coin)
            
            self.image = self.coin[self.current_frame]
            #self.rect = self.image.get_rect()
            
    def update(self):
        self.animate()

class Mob(pg.sprite.Sprite):
    def __init__(self,game, x, y):
        self._layer = 3
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.flying_frame_l[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vx = -1
        self.vy = 0
        self.dy = 0.5

    def load_images(self):
            
        self.flying_frame_r = bee
        for frame in self.flying_frame_r:
            frame.set_colorkey(BLACK)
        
        self.flying_frame_l =[]
        for frame in self.flying_frame_r:
            frame.set_colorkey(BLACK)
            self.flying_frame_l.append(pg.transform.flip(frame,True, False))

    def animate(self):
        now = pg.time.get_ticks()
        
        if now - self.last_update > 60:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.flying_frame_l)
            
        if self.vx > 0:
            self.image = self.flying_frame_l[self.current_frame]
        
        else:
            self.image = self.flying_frame_r[self.current_frame]
            

    def update(self):
        
        self.rect.x += self.vx
        self.vy += self.dy
        self.animate()
        if self.vy > 3 or self.vy < -3:
            self.dy *= -1
        self.mask = pg.mask.from_surface(self.image)
        
        self.rect.y += self.vy
        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()

class RockMonster(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.onGround = False
        self.left = False
        self.right = False
        self.current_frame = 0
        self.last_update = 0
        self.collected_coins = 0
        self.walking =False
        self.load_images()
        self.image = self.walking_frame_r[0]
        self.rect = self.image.get_rect()
        self.rect.center = vec(x,y)
        self.vx = -1
        self.vy = 0

    def load_images(self):
            
        self.walking_frame_r = RM
        for frame in self.walking_frame_r:
            frame.set_colorkey(BLACK)
        
        self.walking_frame_l =[]
        for frame in self.walking_frame_r:
            frame.set_colorkey(BLACK)
            self.walking_frame_l.append(pg.transform.flip(frame,True, False))

    def animate(self):
        now = pg.time.get_ticks()
        
        if now - self.last_update > 60:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.walking_frame_l)
            
        if self.vx > 0:
            self.image = self.walking_frame_l[self.current_frame]
            
        else:
            self.image = self.walking_frame_r[self.current_frame]
                    
    def collide_with_walls(self,vxDelta, vyDelta,platforms ):
        for i in platforms:
            if pg.sprite.collide_rect(self, i, ):
                if vxDelta > 0:
                    self.rect.right = i.rect.left
                    self.right = True
                if vxDelta < 0:
                    self.rect.left = i.rect.right
                    self.left = True
                if vyDelta > 0:
                    self.rect.bottom  = i.rect.top
                    self.vy = 0
                    self.onGround = True
                if vyDelta < 0:
                    self.rect.top = i.rect.bottom
            
    def update(self):
        self.animate()
        if not self.onGround and self.vy < 100:
            self.vy += 0.5

       
        if self.vx < 0:
            if self.left:
                self.vx = 1
    
        if self.vx >0:
            if self.right:
                self.vx = -1
                      
        
        print(self.vx)
        self.rect.x += self.vx
        self.collide_with_walls(self.vx,0,self.game.walls)
        self.rect.y += self.vy
        self.onGround = False
        self.collide_with_walls(0,self.vy,self.game.walls) 

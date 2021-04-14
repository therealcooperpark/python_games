#! /usr/bin/env python3
'''
A simple platformer game made with PyGame
'''

import os
import pygame
from pygame.locals import *
import random
import sys
import time

os.environ['DISPLAY'] = ': 0.0' # Fix Ubuntu terminal settings

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((30,30)) # Player dimensions
        self.surf.fill((128,255,40)) # Player color (R,G,B) format
        self.rect = self.surf.get_rect(center = (10, 420)) # Spawn point

        self.pos = vec((10, 360)) # Starting position
        self.vel = vec(0,0)       # Starting velocity
        self.acc = vec(0,0)       # Starting acceleration
        self.jumping = False
        self.score = 0

    def jump(self):
        '''
        Make the player jump!
        '''
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -15 # Negative sends the player up, 15 is arbitrary

    def cancel_jump(self):
        '''
        Stop the jump (allow short/long jumping)
        '''
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def move(self):
        '''
        Move the player left or right based on keystroke
        '''
        self.acc = vec(0,0.5) # Reset acceleration
        
        pressed_keys = pygame.key.get_pressed() # Log key stroke
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC

        # Update parameters for character
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # Keep character inbounds
        if self.rect.right > WIDTH:
            self.pos.x = WIDTH - self.surf.get_width()/2
        if self.rect.left < 0:
            self.pos.x = 0 + self.surf.get_width()/2
        self.rect.midbottom = self.pos
    
    def update(self):
        '''
        Check for collision between player and platforms
        '''
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if self.vel.y > 0:
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    if hits[0].point == True:
                        hits[0].point = False
                        self.score += 1
                    self.pos.y = hits[0].rect.top + 1
                    self.vel.y = 0
                    self.jumping = False
                    ## Trying to keep the piece moving with the platform. Almost works
                    # if hits[0].moving == True:
                    #    self.vel.x = hits[0].speed + 1



class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((random.randint(50,100), 12)) # Surface dimensions
        self.surf.fill((255,0,0))
        self.rect = self.surf.get_rect(center = (random.randint(0,WIDTH-10),
                                                 random.randint(0,HEIGHT-30)))# Spawn point
        self.point = True
        self.moving = True
        self.speed = random.randint(-1, 1)

    def move(self):
        if self.moving == True:
            self.rect.move_ip(self.speed, 0)
            if self.speed > 0 and self.rect.right > WIDTH:
                self.speed = self.speed * -1
            if self.speed < 0 and self.rect.left < 0:
                self.speed = self.speed * -1
        pass # Lets platforms "move" in the game loop


def plat_gen():
    '''
    Generate a new platform
    '''
    while len(platforms) < HARD:
        width = random.randrange(50,100)
        p = Platform()
        C = True

        while C:
            p = Platform()
            p.rect.center = (random.randrange(0, WIDTH - width),
                             random.randrange(-50, 0))
            C = check(p, platforms)

        platforms.add(p)
        all_sprites.add(p)


def check(platform, groupies):
    '''
    Check for proper spacing between platforms
    '''
    if pygame.sprite.spritecollideany(platform, groupies):
        return True
    else:
        for entity in groupies:
            if entity == platform:
                continue
            if (abs(platform.rect.top - entity.rect.bottom) < 50) and (abs(platform.rect.bottom - entity.rect.top) < 50):
                return True
        return False

'''
Pregame settings
'''
pygame.init()
vec = pygame.math.Vector2 # 2 for two dimensional game

HEIGHT = 450   # Game screen height
WIDTH  = 400   # Game screen width
ACC    = 0.5   # Acceleration?
FRIC   = -0.12 # Friction?
FPS    = 60    # Frames per second
HARD   = 6     # Max number of platforms

FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Platformer')

'''
Create player, platforms, and groups
'''
PT1 = Platform()
PT1.surf = pygame.Surface((WIDTH, 20))
PT1.surf.fill((255,0,0))
PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT-10))
PT1.moving = False
PT1.point = False

P1  = Player()

platforms = pygame.sprite.Group() # Stores platforms only
platforms.add(PT1)

all_sprites = pygame.sprite.Group() # Store sprites in a group to manage asthetics?
all_sprites.add(PT1)
all_sprites.add(P1)

'''
Generate the first 5-6 random platforms for the game
'''
for x in range(random.randint(4, 5)):
    C = True
    p1 = Platform()
    while C:
        p1 = Platform()
        C = check(p1, platforms)
    platforms.add(p1)
    all_sprites.add(p1)

'''
Game Loop
'''
while True:
    # Check game input including quit and jump
    P1.update() # Update player velocity and position
    for event in pygame.event.get(): 
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                P1.jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                P1.cancel_jump()

    # Initiate "Game Over" shutdown
    if P1.rect.top > HEIGHT:
        for entity in all_sprites:
            entity.kill()
            time.sleep(1)
            displaysurface.fill((255,0,0))
            pygame.display.update()
            time.sleep(1)
            pygame.quit()
            sys.exit()


    # Update infinite scrolling screen
    if P1.rect.top <= HEIGHT / 3:
        P1.pos.y += abs(P1.vel.y)
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill()
    
    plat_gen() # Generate new platforms

    displaysurface.fill((0,0,0)) # Fill background with black
    f = pygame.font.SysFont("Verdana", 20)
    g = f.render(str(P1.score), True, (123,255,0))
    displaysurface.blit(g, (WIDTH/2, 10))

    # Draw in all sprites with new positions (Group does this in a single command)
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        entity.move()

    pygame.display.update() # Push changes to the screen
    FramePerSec.tick(FPS)   # Limit update to 60 FPS

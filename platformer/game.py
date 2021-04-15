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
        self.moving = False       # Track if player in movement
        self.jumping = False      # Track if player is jumping
        self.score = 0            # Track player score

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
            self.moving = True
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
            self.moving = True

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
                    if hits[0].moving and not self.moving:
                        self.pos.x += hits[0].speed 



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
        dist = 0 # Allow the criteria for distance between platforms to shrink

        while C:
            p = Platform()
            p.rect.center = (random.randrange(0, WIDTH - width),
                             random.randrange(-50, 0))
            C = check(p, platforms, dist)
            dist += 1

        platforms.add(p)
        all_sprites.add(p)


def check(platform, groupies, dist):
    '''
    Check for proper spacing between platforms
    '''
    if pygame.sprite.spritecollideany(platform, groupies):
        return True
    else:
        for entity in groupies:
            if entity == platform:
                continue
            if abs(platform.rect.bottom - entity.rect.top) < 45 - (dist / 5):
                return True
        return False


def home_screen():
    '''
    Home screen on initial bootup or game over
    '''
    # Create fonts
    title_font = pygame.font.SysFont('Verdana', 40)
    button_font = pygame.font.SysFont('Verdana', 20)
    
    # Make title
    title = title_font.render('Splatformer!', True, ((0,0,255)))
    title_rect = title.get_rect(center=(WIDTH/2, 40))
    
    # Make buttons
    play = button_font.render('Play', True, ((0,255,0)))
    play_rect = play.get_rect(center=(WIDTH/2, HEIGHT/2))
    quit = button_font.render('Quit', True, ((0,255,0)))
    quit_rect = quit.get_rect(center=(WIDTH/2, HEIGHT/2 + 80))


    # Set display background and button text
    displaysurface.fill((255,255,255))
    displaysurface.blit(title, title_rect)
    play_button = displaysurface.blit(play, play_rect)
    quit_button = displaysurface.blit(quit, quit_rect)
    
    while True:
        # Log clicks
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                print('Registered the click!')
                if play_button.collidepoint(event.pos):
                    print('Made it here!')
                    return None 
                if quit_button.collidepoint(event.pos):
                    sys.exit()


        # Update state of game
        pygame.display.update()

'''
Pregame settings
'''
pygame.init()
vec = pygame.math.Vector2 # 2 for two dimensional game

HEIGHT = 450   # Game screen height
WIDTH  = 400   # Game screen width
ACC    = 0.5   # Acceleration?
FRIC   = -0.16 # Friction?
FPS    = 60    # Frames per second
HARD   = 6     # Max number of platforms

FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Platformer')


def game_start_settings():
    '''
    Setup game start settings
    '''
    
    global PT1
    global P1
    global platforms
    global all_sprites

    # Setup base platform
    PT1 = Platform()
    PT1.surf = pygame.Surface((WIDTH, 20))
    PT1.surf.fill((255,0,0))
    PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT-10))
    PT1.moving = False
    PT1.point = False

    platforms = pygame.sprite.Group() # Stores platforms only
    platforms.add(PT1)

    all_sprites = pygame.sprite.Group() # Store sprites in a group to manage asthetics?
    all_sprites.add(PT1)

    # Setup player
    P1  = Player()
    all_sprites.add(P1)


    # Generate the first 5-6 random platforms for the game
    for x in range(random.randint(4, 5)):
        C = True
        p1 = Platform()
        while C:
            p1 = Platform()
            C = check(p1, platforms, 0)
        platforms.add(p1)
        all_sprites.add(p1)


def game_over():
    '''
    Wrap the game up
    '''

    # Kill the current game instance
    for entity in all_sprites:
        entity.kill()
    time.sleep(1)
    displaysurface.fill((255,0,0))
    game_over = f.render('GAME OVER', True, (255,255,255))
    game_over_rect = game_over.get_rect(center=(WIDTH/2, HEIGHT + 80))
    displaysurface.blit(game_over, game_over_rect)
    pygame.display.update()
    time.sleep(1)
    
    # Update leaderboard
    with open('leaderboard.txt', 'r') as leaderboard:
        scores = [line.strip().split() for line in leaderboard]

    # Update scores list with player score
    if P1.score > int(scores[-1][1]):
        name = leaderboard_name()
        player_score_logged = False
        new_scores = []
        for idx in range(len(scores)):
            score = int(scores[idx][1])
            if P1.score > score and not player_score_logged:
                scores.insert(idx, [name, str(P1.score)])
                player_score_logged = True
        else:
            scores.append([name, str(P1.score)])

    # Write out new leaderboard
    with open('leaderboard.txt', 'w') as outfile:
        for idx in range(10):
            outfile.write('\t'.join(scores[idx]))
            if idx < 9:
                outfile.write('\n')

    # Head to home screen and wait for new game to start 
    home_screen()
    game_start_settings()


def leaderboard_name():
    '''
    Get a name for the leaderboard
    '''

    # Set leaderboard rect
    leaderboard = f.render('Name:', True, (255,255,255))
    leaderboard_rect = leaderboard.get_rect(center=(WIDTH/2 - 80, HEIGHT/2))

    # Set input rect
    name = ''
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.unicode.isalpha():
                    name += event.unicode
                elif event.key == K_BACKSPACE:
                    if len(name) == 0:
                        continue
                    else:
                        name = name[:-1]
                elif event.key == K_RETURN:
                    if name == '':
                        return 'FakeName'
                    else:
                        return name

        displaysurface.fill((255,0,0))
        name_box = f.render(name, True, (255,255,255))
        name_rect = name_box.get_rect(center=(WIDTH/2, HEIGHT/2))
        displaysurface.blit(leaderboard, leaderboard_rect)
        displaysurface.blit(name_box, name_rect)
        pygame.display.flip()

# Bootup home screen
home_screen()
game_start_settings()

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
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                P1.moving = False

    # Initiate "Game Over" shutdown
    if P1.rect.top > HEIGHT:
        game_over()
        continue

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

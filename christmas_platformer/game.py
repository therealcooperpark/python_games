#! /usr/bin/env python3
'''
A Christmas themed platformer
'''
from assets import *
import os
import pygame
from pygame.locals import *
import sys
import time

# Game constants
WIDTH = 1280
HEIGHT = 900
FPS = 60

# Create display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Player Test")
clock = pygame.time.Clock()

# Create player
player = Player(  # Use lowercase 'player' to avoid conflict
    x=WIDTH // 2,
    y=HEIGHT - 100
)

# Create platforms group and ground
platforms = pygame.sprite.Group()
ground = SimplePlatform(
    x=WIDTH // 2,
    y=HEIGHT - 50,
    width=WIDTH,
    height=100
)
platforms.add(ground)

# Set player starting position on the ground
player.pos.y = ground.rect.top - player.rect.height // 2
player.rect.midbottom = player.pos

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump(platforms)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                player.cancel_jump()
    
    # Get key states for movement
    keys = pygame.key.get_pressed()
    player.move(left=keys[K_LEFT], right=keys[K_RIGHT], screen_width=WIDTH)
    
    # Update player
    player.update(platforms)
    
    # Draw everything
    screen.fill((50, 50, 100))  # Background color
    ground.draw(screen)
    player.draw(screen)
    
    pygame.display.flip()
    clock.tick(FPS)
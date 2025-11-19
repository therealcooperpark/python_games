"""
Simple platform class
"""

import pygame

class SimplePlatform(pygame.sprite.Sprite):
        def __init__(self, x, y, width, height):
            super().__init__()
            self.surf = pygame.Surface((width, height))
            self.surf.fill((255, 0, 0))
            self.rect = self.surf.get_rect(center=(x, y))
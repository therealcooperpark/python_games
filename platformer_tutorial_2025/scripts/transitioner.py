import pygame

class Transitioner:
    def __init__(self, game, pos, size, load_level):
        self.game = game
        self.img = self.game.assets['transitioner'][0]
        self.pos = pos # Tuple of X/Y position
        self.size = size # Tuple of Width/Height
        self.load_level = load_level # For later use

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
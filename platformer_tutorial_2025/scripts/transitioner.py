'''
Sample version of the transitioner class... not implemented due to issues with existing code at the time
'''

import pygame

class Transitioner:
    def __init__ (self, game, pos, size, load_level):
        self.game = game
        self.img = self.game.assets['transitioner'].copy().fill((127, 0, 255)) # Grey out
        self.pos = pos # Tuple of X/Y position
        self.size = size # Tuple of Width/Height
        self.load_level = load_level
        self.transition = -30 # Transition speed when moving to a new level

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self):
        if len(self.game.state.enemies) == 0: # All enemies defeated, unlock next room

            if self.game.player.rect().colliderect(self.pos):
                self.game.state.transition += 1

            if self.transition > 30:
                self.game.state.load_level(self.load_level)

        if self.game.state.transition < 0: # Open up the transition circle
            self.game.state.transition += 1
    
    def render(self, offset=(0, 0)):
        if self.transition:
            self.game.display.blit(self.img, (self.pos[0] - offset[0], self.pos[1] - offset[1]))

import math
import pygame
from scripts.particle import Particle
from scripts.spark import Spark
import random

class Projectile():
    def __init__(self, game, pos, direction, timer, damage=0):
        self.game = game
        self.pos = pos
        self.direction = direction
        self.timer = timer
        self.damage = damage
        self.img = game.assets['projectile']

    def move(self):
        self.pos[0] += self.direction
        self.timer += 1

    def update(self):
        '''
        Handle collision logic and apply damage where appropriate
        '''
        if self.game.tilemap.solid_check(self.pos): # Remove on collision with physics tile
            self.game.state.projectiles.remove(self)
            for i in range(4):
                self.game.state.sparks.append(Spark(self.pos, random.random() - 0.5 + (math.pi if self.direction > 0 else 0), 2 + random.random()))
        elif self.timer > 360: # Time out the projectile
            self.game.state.projectiles.remove(self)
        elif abs(self.game.player.dashing) < 50:
            if self.game.player.rect().collidepoint(self.pos):
                self.game.state.projectiles.remove(self)
                self.game.sfx['hit'].play()
                alive = self.game.player.take_damage(self.damage)
                for i in range(30):
                        angle = random.random() * math.pi * 2
                        speed = random.random() * 5
                        self.game.state.sparks.append(Spark(self.game.player.rect().center, angle, 2 + random.random()))
                        self.game.state.particles.append(Particle(self.game, 'particle', self.game.player.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))
                if alive:
                    self.game.screenshake = max(8, self.game.screenshake)
                    print(f'PLAYER HIT!\nDamage Taken:{self.damage}\nHealth Remaining:{self.game.player.health}')
                else:
                    self.game.state.dead += 1
                    self.game.screenshake = max(16, self.game.screenshake)
                    print('PLAYER KILLED!')

    def render(self, surf, offset=(0, 0)):
        surf.blit(self.img, 
                  (self.pos[0] - self.img.get_width() / 2 - offset[0], 
                   self.pos[1] - self.img.get_height() / 2 - offset[1])
        )
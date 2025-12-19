import math
import pygame
from scripts.particle import Particle
from scripts.spark import Spark
import random

class Projectile():
    def __init__(self, game, pos, direction, timer, damage=0, img=None):
        self.game = game
        self.pos = pos
        self.direction = direction
        self.timer = timer
        self.damage = damage
        if img:
            self.img = img
        else:
            self.img = game.assets['projectile']

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.img.get_width(), self.img.get_height())

    def update(self, tilemap):
        self.pos[0] += self.direction
        self.timer += 1

    def render(self, surf, offset=(0, 0)):
        surf.blit(self.img, 
                  (self.pos[0] - self.img.get_width() / 2 - offset[0], 
                   self.pos[1] - self.img.get_height() / 2 - offset[1])
        )

    def _destroy_projectile(self, sparks=False):
        '''
        Destroys projectile and queues some Sparks if necessary
        '''
        self.game.state.projectiles.remove(self)
        if sparks:
            for i in range(4):
                self.game.state.sparks.append(Spark(self.pos, random.random() - 0.5 + (math.pi if self.direction > 0 else 0), 2 + random.random()))

class EnemyProjectile(Projectile):
    """
    A projectile fired by enemies that can damage the player.

    Unlike the base Projectile class, EnemyProjectile handles collision with the player,
    applies damage, and manages its own destruction upon hitting the player or a solid tile.
    """
    def __init__(self, game, pos, direction, timer, damage=0, img=None):
        super().__init__(game, pos, direction, timer, damage, img)

    def update(self, tilemap):
        '''
        Handle collision logic and apply damage to player where appropriate
        '''
        super().update(tilemap)
        
        if tilemap.solid_check(self.pos): # Remove on collision with physics tile
            super()._destroy_projectile(sparks=True)
        elif self.timer > 360: # Time out the projectile
            super()._destroy_projectile(sparks=False)
        elif abs(self.game.player.dashing) < 50 and self.game.player.iframes == 0:
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
                    print(f'PLAYER HIT!\nDamage Taken: {self.damage}\nHealth Remaining: {self.game.player.health}')
                else:
                    self.game.state.dead += 1
                    self.game.screenshake = max(16, self.game.screenshake)
                    print('PLAYER KILLED!')

    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset)


class PlayerShuriken(Projectile):
    """
    A projectile type representing the player's special shuriken attack.

    Features rotating img (adjusting based on player direction) and piercing damage
    instead of destruction on first enemy contact.
    
    Walls will still break the projectile.
    """
    def __init__(self, game, pos, direction, timer, damage=0, img=None):
        super().__init__(game, pos, direction, timer, damage, img=game.assets['shuriken'])

        self.rotation_angle = 0 # Rotation of the img
        self.rotation_rate = 5 if self.direction < 1 else -5 # Rate of the rotation changing per frame

    def update(self, tilemap):
        '''
        Handle collision logic and apply damage to enemies where appropriate
        '''
        super().update(tilemap)

        # Rotate img for rendering
        self.rotation_angle += self.rotation_rate

        enemy_hit = super().rect().collideobjectsall(self.game.state.enemies, key=lambda e: e.rect())

        if tilemap.solid_check(self.pos): # Remove on collision with physics tile
            super()._destroy_projectile(sparks=True)
        elif self.timer > 360: # Time out the projectile
            super()._destroy_projectile(sparks=False)
        elif len(enemy_hit) > 0: # Enemy hit by projectile
            enemy_hit = enemy_hit[0]
            self.game.sfx['hit'].play()
            alive = enemy_hit.take_damage(self.damage)
            if alive:
                print(f'ENEMY HIT!\nDamage taken: {self.damage}\nRemaining health: {enemy_hit.health}')
                enemy_hit.iframes += enemy_hit.i_window
                for i in range(30):
                    angle = random.random() * math.pi * 2
                    speed = random.random() * 5
                    self.game.state.sparks.append(Spark(self.rect().center, angle, 2 + random.random()))
                    self.game.state.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))
            else:
                for i in range(30):
                    angle = random.random() * math.pi * 2
                    speed = random.random() * 5
                    self.game.state.sparks.append(Spark(self.rect().center, angle, 2 + random.random()))
                    self.game.state.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))
                print('ENEMY KILLED!')
                self.game.state.sparks.append(Spark(self.rect().center, 0, 5 + random.random()))
                self.game.state.sparks.append(Spark(self.rect().center, math.pi, 5 + random.random()))
                self.game.state.enemies.remove(enemy_hit)

    def render(self, surf, offset=(0, 0)):
        rotated_img = pygame.transform.rotozoom(self.img, self.rotation_angle, 1.0)
        rotated_rect = rotated_img.get_rect(center=(self.pos[0] - offset[0],
                                                    self.pos[1] - offset[1]))
        surf.blit(rotated_img, rotated_rect)


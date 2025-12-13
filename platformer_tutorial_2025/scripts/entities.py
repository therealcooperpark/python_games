import math
import pygame
from scripts.particle import Particle
from scripts.projectile import Projectile
from scripts.spark import Spark
import random

class PhysicsEntity:
    def __init__ (self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}
        
        self.action = ''
        self.anim_offset = (-3, -3) # Buffer space for animation images to exceed the "hitbox" of the entity
        self.flip = False
        self.set_action('idle')
        self.last_movement = [0, 0]

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def set_action(self, action):
        # Reset the action for the entity, including the animation loop
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()

    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False} # Reset collision record
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1]) # Every frame we add velocity

        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0: # Movement to the right gets blocked, so snap left
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0: # Movement to the left gets blocked, so snap right
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0: # Movement to the bottom gets blocked, so snap up
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0: # Movement to the top gets blocked, so snap down
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y
        
        # Handle flipping the graphic when facing left (assets are facing the right)
        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

        self.last_movement = movement

        self.velocity[1] = min(5, self.velocity[1] + 0.1) # Apply gravity acceleration after the movement has been calculated 

        if self.collisions['down'] or self.collisions['up']: # Reset veloicty when up/down contact has been made
            self.velocity[1] = 0

        self.animation.update()

    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))


class Enemy(PhysicsEntity):
    def __init__(self, game, pos, size, health, damage, i_window=30):
        super().__init__(game, 'enemy', pos, size)

        # Stats
        self.health = health
        self.damage = damage

        # Combat
        self.i_window = i_window # How many frames of invincibility granted on hit
        self.iframes = 0 # How many frames of invincibility left

        self.walking = 0 # Frame timer to track when they should be walking in one direction

    def update(self, tilemap, movement=(0, 0)):
        if self.walking:
            if tilemap.solid_check((self.rect().centerx + (-7 if self.flip else 7), self.pos[1] + 23)): # Using magic numbers relative to graphic images
                if (self.collisions['left'] or self.collisions['right']): # Change direction at wall collision
                    self.flip = not self.flip
                else:
                    movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])
            else:
                self.flip = not self.flip
            self.walking = max(0, self.walking - 1)
            if not self.walking: # Shoot when the entity is done walking, before it cycles the walking routine again
                dis = (self.game.player.pos[0] - self.pos[0], self.game.player.pos[1] - self.pos[1])
                if (abs(dis[1]) < 16):
                    if (self.flip and dis[0] < 0): # Enemy must be facing player
                        self.game.sfx['shoot'].play()
                        self.game.state.projectiles.append(Projectile(self.game, [self.rect().centerx - 7, self.rect().centery], -1.5, 0, self.damage))
                        for i in range(4):
                            self.game.state.sparks.append(Spark(self.game.state.projectiles[-1].pos, random.random() - 0.5 + math.pi, 2 + random.random()))
                    if (not self.flip and dis[0] > 0):
                        self.game.sfx['shoot'].play()
                        self.game.state.projectiles.append(Projectile(self.game, [self.rect().centerx + 7, self.rect().centery], 1.5, 0, self.damage))
                        for i in range(4):
                            self.game.state.sparks.append(Spark(self.game.state.projectiles[-1].pos, random.random() - 0.5, 2 + random.random()))
        elif random.random() < 0.01: # Start walking on a semi-random cadence if not already walking
            self.walking = random.randint(30, 120)

        super().update(tilemap, movement=movement)

        if movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')

        # Process any attack received
        self.iframes = max(0, self.iframes - 1)
        if abs(self.game.player.dashing) >= 50:
            if self.rect().colliderect(self.game.player.rect()) and self.iframes == 0: # If enemy collides with rect of dashing player and isn't immune
                self.game.screenshake = max(16, self.game.screenshake)
                self.game.sfx['hit'].play()
                alive = self.take_damage(self.game.player.damage)
                if alive:
                    print(f'ENEMY HIT!\nDamage taken: {self.game.player.damage}\nRemaining health: {self.health}')
                    self.iframes += self.i_window
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
                    return True

    def take_damage(self, damage):
        self.health -= damage
        return True if self.health > 0 else False

    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset=offset)

        if self.flip:
            surf.blit(pygame.transform.flip(self.game.assets['gun'], True, False), (self.rect().centerx - 4 - self.game.assets['gun'].get_width() - offset[0], self.rect().centery - offset[1]))
        else:
            surf.blit(self.game.assets['gun'], (self.rect().centerx + 4 - offset[0], self.rect().centery - offset[1]))

class Player(PhysicsEntity):
    # Handles the animation logic for the Player physics entity (and probably other stuff)
    def __init__(self, game, pos, size, health=1, damage=10, i_window=30):
        super().__init__(game, 'player', pos, size)
        
        # Stats
        self.max_health = health
        self.health = health
        self.damage = damage
        
        # Combat
        self.i_window = i_window # How many frames of invincibility granted on hit
        self.iframes = 0 # How many frames of invincibility left
        self.dashing = 0 # How many frames left to dash

        # Movement
        self.air_time = 0
        self.jumps = 1
        self.wall_slide = False

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)

        # Process iframes
        self.iframes = max(0, self.iframes - 1)
        
        # Reset jump
        self.air_time += 1

        if self.air_time > 120: # Avoid infinite fall
            self.game.state.dead = 1
            self.game.screenshake = max(16, self.game.screenshake)

        if self.collisions['down']:
            self.air_time = 0
            self.jumps = 1

        # Track and handle logic for wall slide
        self.wall_slide = False
        if (self.collisions['left'] or self.collisions['right']) and self.air_time > 4:
            self.wall_slide = True
            self.velocity[1] = min(self.velocity[1], 0.5) # Cap wall sliding velocity
            self.air_time = 5 # Freeze and reset air_time to prevent permanent fall death on long slide
            if self.collisions['right']:
                self.flip = False
            else:
                self.flip = True
            self.set_action('wall_slide') 
        
        # Set the animation based on movement status
        if not self.wall_slide:
            if self.air_time > 4:
                self.set_action('jump')
            elif movement[0] != 0:
                self.set_action('run')
            else:
                self.set_action('idle')

        # Handle dashing
        # Generate a random burst particle with random directions when triggered
        if abs(self.dashing) in {60, 50}:
            for i in range(20):
                angle = random.random() * math.pi * 2
                speed = random.random() * 0.5 + 0.5
                pvelocity = [math.cos(angle) * speed, math.sin(angle) * speed] # Particle velocity
                self.game.state.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=pvelocity, frame = random.randint(0, 7)))
        if self.dashing > 0:
            self.dashing = max(self.dashing - 1, 0)
        if self.dashing < 0:
            self.dashing = min(self.dashing + 1, 0)
        if abs(self.dashing) > 50:
            self.velocity[0] = abs(self.dashing) / self.dashing * 8
            if abs(self.dashing) == 51:
                self.velocity[0] *= 0.1
                # Generate a stream of particles behind player during dash
                pvelocity = [abs(self.dashing) / self.dashing * random.random() * 3, 0]
                self.game.state.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=pvelocity, frame = random.randint(0, 7)))

        # Stop player from moving on x-axis permanently
        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, 0)
        else:
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)

    def take_damage(self, damage):
        self.health -= damage
        return True if self.health > 0 else False

    def render(self, surf, offset=(0, 0)):
        if abs(self.dashing) <= 50:
            super().render(surf, offset=offset)


    def jump(self):
        if self.wall_slide:
            if self.flip and self.last_movement[0] < 0:
                self.velocity[0] = 3.5
                self.velocity[1] = -2.5
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True
            elif not self.flip and self.last_movement[0] > 0:
                self.velocity[0] = -3.5
                self.velocity[1] = -2.5
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True
        elif self.jumps:
            self.velocity[1] = -3 # Change velocity
            self.jumps -= 1 # Decrease jumps
            self.air_time = 5 # Add air_time, forcing jump animation
            return True
        
    def dash(self):
        if not self.dashing:
            self.game.sfx['dash'].play()
            if self.flip:
                self.dashing = -60
            else:
                self.dashing = 60
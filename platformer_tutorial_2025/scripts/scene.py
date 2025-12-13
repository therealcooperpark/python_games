import math
import os
import pygame
import random
from scripts.clouds import Cloud, Clouds
from scripts.entities import Enemy
from scripts.particle import Particle
from scripts.spark import Spark
from scripts.tilemap import Tilemap
import sys

class Scene:
    '''
    Base class for game scenes
    '''
    def __init__(self, game):
        self.game = game

    def update(self):
        pass

    def render(self, display, offset=(0, 0)):
        pass

    def handle_event(self, event):
        pass

class GameplayScene(Scene):
    '''
    Scene specific to the main gameplay loop
    '''
    def __init__(self, game, level):
        super().__init__(game)
        
        # Metadata
        self.level = level
        self.complete = False
        self.transition_loc = None # To be filled with a pygame rect

        # Map stuff
        self.clouds = Clouds(self.game.assets['clouds'], count=16)
        self.tilemap = Tilemap(self.game, tile_size=16)

        # Level stuff
        self.movement = [False, False] # Used to track movement triggers by the player

    def load_level(self, map_id):
        '''
        Reset the game on the given level (map_id)
        '''
        # Load map
        self.tilemap.load('data/maps/' + str(map_id) + '.json')

        # Handle leaf spawners
        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13)) # Offset by 4 pixels for leaf falling. Numbers based on tree img size

        # Handle original Player/Enemy Spawners
        self.enemies = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 0: # Player variant
                # Spawn player
                self.game.player.pos = list(spawner['pos'])
                self.game.player.air_time = 0 # Reset on respawn
                
                # Load transition location
                self.transition_loc = pygame.Rect(spawner['pos'][0], spawner['pos'][1], 8, 15)
            else:
                self.enemies.append(Enemy(self.game, spawner['pos'], (8, 15), 0, 10))
        
        # Reset other entity collections
        self.projectiles = []
        self.particles = []
        self.sparks = []

        # Reset values
        self.game.player.health = self.game.player.max_health
        self.dead = 0 # Number boolean for if player is dead
        self.complete = False
        self.transition = -30 # Transition speed when moving to a new level
        self.game.scroll = [0, 0] # Offset which emulates a "camera" experience

    def update(self):
        # Finish load level animation
        if self.transition < 0:
            self.transition += 1

        # Background assets
        self.clouds.update()

        for rect in self.leaf_spawners:
            if random.random() * 49999 < rect.width * rect.height: # Control spawn rate in relation to the size of the tree
                pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                self.particles.append(Particle(self.game, 'leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20)))

        # Check for progression to next level
        if len(self.enemies) == 0: # All enemies defeated, unlock next room
            self.complete = True
            print(f'Player: {self.game.player.rect()}\nTransitioner: {self.transition_loc}')

            if self.game.player.rect().colliderect(self.transition_loc): # Start the countdown to new level
                self.transition += 1

            if self.transition > 30: # Trigger the new level load
                self.level = min(self.level + 1, len(os.listdir('data/maps')) - 1)
                self.load_level(self.level)

        # Handle enemies
        for enemy in self.enemies.copy():
            kill = enemy.update(self.tilemap, (0, 0))
            if kill:
                self.enemies.remove(enemy)

        # Check Player death
        if self.dead: # You died, start over in 40 frames
            self.dead += 1
            if self.dead >= 10:
                self.transition = min(30, self.state.transition + 1)
            if self.dead > 40:
                self.load_level(self.state.level)
        else: # Update as usual and continue
            self.game.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))

        # Resolve sparks
        for spark in self.sparks.copy():
            kill = spark.update()
            if kill:
                self.sparks.remove(spark)
        
        # Resolve Projectiles
        for projectile in self.projectiles.copy():
            projectile.move() # TODO: Consider putting move in update
            projectile.update(self.tilemap)

        # Resolve Particles
        for particle in self.particles.copy():
            kill = particle.update()
            if particle.type == 'leaf':
                particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3 # Put a wobble on the leaf fall with a sin wave
            if kill:
                self.particles.remove(particle)

    def render(self, offset=(0, 0)):
        # Background
        self.clouds.render(self.game.display_2, offset=offset)

        # Tilemap
        self.tilemap.render(self.game.display, offset=offset)

        # Special conditions
        if self.complete:
            asset = self.game.assets['spawners'][0].fill((127, 0, 255))
            self.game.display.blit(self.game.assets['spawners'][0],
                (self.transition_loc[0] - offset[0],
                 self.transition_loc[1] - offset[1])  
            )

        # Enemies
        for enemy in self.enemies:
            enemy.render(self.game.display, offset=offset)
        
        # Player
        if not self.dead:
            self.game.player.render(self.game.display, offset=offset)

        # Sparks
        for spark in self.sparks:
            spark.render(self.game.display, offset=offset)

        # Projectiles
        for projectile in self.projectiles:
            projectile.render(self.game.display, offset=offset)

        # Particles
        for particle in self.particles:
            particle.render(self.game.display, offset=offset)
    

class PauseScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.pause_display = pygame.Surface((self.game.screen.get_width() // 4, self.game.screen.get_height() // 4)) # Set pause space
        self.is_paused = False

    def update(self):
        pass # To be used for any updates later

    def handle_input(self):
        for event in pygame.event.get(): # event is where the... events get stored
                if event.type == pygame.QUIT: # Clicking the 'x' in the window
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause()

    def render(self):
        # TODO: This is centered correctly, but I need a proper pause screen...
        pygame.draw.circle(self.pause_display, (255, 255, 255), (self.pause_display.get_width() // 2, self.pause_display.get_height() // 2), self.pause_display.get_width() // 3)
        self.game.screen.blit(self.pause_display, (self.game.screen.get_width() // 2 - self.pause_display.get_width() // 2, self.game.screen.get_height() // 2 - self.pause_display.get_height() // 2))

    def pause(self):
        self.is_paused = not self.is_paused


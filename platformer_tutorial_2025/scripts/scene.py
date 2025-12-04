import pygame
from scripts.entities import Enemy
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
        self.level = level

    def load_level(self, map_id):
        '''
        Reset the game on the given level (map_id)
        '''
        # Load map
        self.game.tilemap.load('data/maps/' + str(map_id) + '.json')

        # Handle leaf spawners
        self.leaf_spawners = []
        for tree in self.game.tilemap.extract([('large_decor', 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13)) # Offset by 4 pixels for leaf falling. Numbers based on tree img size

        # Handle original Player/Enemy Spawners
        self.enemies = []
        for spawner in self.game.tilemap.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 0: # Player variant
                self.game.player.pos = spawner['pos']
                self.game.player.air_time = 0 # Reset on respawn
            else:
                self.enemies.append(Enemy(self.game, spawner['pos'], (8, 15), 20, 10))
        
        # Reset other entity collections
        self.projectiles = []
        self.particles = []
        self.sparks = []

        # Reset values
        self.dead = 0 # Number boolean for if player is dead
        self.transition = -30 # Transition speed when moving to a new level
        self.game.scroll = [0, 0] # Offset which emulates a "camera" experience

    

class PauseScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.pause_display = pygame.Surface((self.game.screen.get_width() // 4, self.game.screen.get_height() // 4)) # Set pause space

    def handle_input(self):
        for event in pygame.event.get(): # event is where the... events get stored
                if event.type == pygame.QUIT: # Clicking the 'x' in the window
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game.is_paused = not self.game.is_paused

    def render_pause(self):
        # TODO: This is centered correctly, but I need a proper pause screen...
        pygame.draw.circle(self.pause_display, (255, 255, 255), (self.pause_display.get_width() // 2, self.pause_display.get_height() // 2), self.pause_display.get_width() // 3)
        self.game.screen.blit(self.pause_display, (self.game.screen.get_width() // 2 - self.pause_display.get_width() // 2, self.game.screen.get_height() // 2 - self.pause_display.get_height() // 2))



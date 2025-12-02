import pygame
from scripts.entities import Enemy

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
                self.enemies.append(Enemy(self.game, spawner['pos'], (8, 15)))
        
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

    def pause(self):
        is_paused = True
        while True:
            
            # TODO: A nested event loop doesn't work, so how can I track pause/unpause without letting the core game play on?
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        break

            # TODO: This is centered correctly, but I need a proper pause screen...
            pygame.draw.circle(self.pause_display, (255, 255, 255), (self.pause_display.get_width(), self.pause_display.get_height()), 100)
            self.game.screen.blit(self.pause_display, (self.game.screen.get_width() // 2 - self.pause_display.get_width() // 2, self.game.screen.get_height() // 2 - self.pause_display.get_height() // 2))
            pygame.display.update()




import pygame
from scripts.entities import PhysicsEntity
from scripts.utils import *
from scripts.tilemap import *
import sys


class Game: # Manage game settings
    def __init__(self):
        pygame.init() # Turn the game on?

        pygame.display.set_caption('Ninja Game') # Set window name
        self.screen = pygame.display.set_mode((640, 480)) # Creating the window for the game
        self.display = pygame.Surface((320, 240)) # What I render to. We scale this up to the window size later to multiply the size of all our assets

        self.clock = pygame.time.Clock() # Used to force the game to run at X FPS

        self.movement = [False, False] # Used to track movement triggers by the player

        self.assets = {
            'decor' : load_images('tiles/decor'),
            'grass' : load_images('tiles/grass'),
            'large_decor' : load_images('tiles/large_decor'),
            'stone' : load_images('tiles/stone'),
            'player' : load_image('entities/player.png')
        }

        self.player = PhysicsEntity(self, 'player', (50, 50), (8, 15))

        self.tilemap = Tilemap(self, tile_size=16)

    def run(self):
        # Game Loop
        while True:
            self.display.fill((14, 219, 248)) # Default screen color

            self.tilemap.render(self.display)

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display)

            for event in pygame.event.get(): # event is where the... events get stored
                if event.type == pygame.QUIT: # Clicking the 'x' in the window
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.player.velocity[1] = -3
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)) # Where the resizing happens for the pixel art
            pygame.display.update() # Updates the display
            self.clock.tick(60) # Limits the game to 60 FPS

Game().run()
import pygame
from scripts.clouds import *
from scripts.entities import *
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
            'player' : load_image('entities/player.png'),
            'background' : load_image('background.png'),
            'clouds': load_images('clouds'),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/jump': Animation(load_images('entities/player/jump')),
            'player/slide': Animation(load_images('entities/player/slide')),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide'))
        }

        self.clouds = Clouds(self.assets['clouds'], count=16)

        self.player = Player(self, (50, 50), (8, 15))

        self.tilemap = Tilemap(self, tile_size=16)
        self.tilemap.load('map.json')

        self.scroll = [0, 0] # The offset which simulates the concept of a "camera" (i.e., moving everything X and Y distance)

    def run(self):
        # Game Loop
        while True:
            self.display.blit(self.assets['background'], (0, 0)) # Default screen background

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30 # The camera position is the top-left. So we need to subtract the screen size to center the player
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30 # The camera position is the top-left. So we need to subtract the screen size to center the player
            render_scroll = (int(self.scroll[0]), int(self.scroll[1])) # Solves sub-pixel camera jittering by using int rounding/truncation

            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)

            self.tilemap.render(self.display, offset=render_scroll)

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=self.scroll)

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
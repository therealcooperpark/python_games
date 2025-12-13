import pygame
import math
import os
import random
from scripts.entities import Enemy, PhysicsEntity, Player
from scripts.particle import Particle
from scripts.scene import Scene, GameplayScene, PauseScene
from scripts.spark import Spark
from scripts.utils import load_image, load_images, Animation
import sys

class Game: # Manage game settings
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 128) # Lower buffer for mixer to improve latency
        pygame.init() # Initialize pygame resources

        pygame.display.set_caption('Ninja Game') # Set window name
        self.screen = pygame.display.set_mode((640, 480)) # Creating the window for the game
        self.display = pygame.Surface((320, 240), pygame.SRCALPHA) # What I render to. We scale this up to the window size later to multiply the size of all our assets
        self.display_2 = pygame.Surface((320, 240)) # For content that should have outline

        self.clock = pygame.time.Clock() # Used to force the game to run at X FPS

        self.assets = {
            'decor' : load_images('tiles/decor'),
            'grass' : load_images('tiles/grass'),
            'large_decor' : load_images('tiles/large_decor'),
            'stone' : load_images('tiles/stone'),
            'player' : load_image('entities/player.png'),
            'background' : load_image('background.png'),
            'clouds': load_images('clouds'),
            'spawners': load_images('tiles/spawners'),
            'transitioner': load_images('tiles/transitioner'),
            'enemy/idle': Animation(load_images('entities/enemy/idle'), img_dur=6),
            'enemy/run': Animation(load_images('entities/enemy/run'), img_dur=4),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/jump': Animation(load_images('entities/player/jump')),
            'player/slide': Animation(load_images('entities/player/slide')),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),
            'particle/leaf': Animation(load_images('particles/leaf'), img_dur=20, loop=False),
            'particle/particle': Animation(load_images('particles/particle'), img_dur=6, loop=False),
            'gun': load_image('gun.png'),
            'projectile': load_image('projectile.png'),
        }

        # Setting sound affects
        self.sfx = {
            'jump': pygame.mixer.Sound('data/sfx/jump.wav'),
            'dash': pygame.mixer.Sound('data/sfx/dash.wav'),
            'hit': pygame.mixer.Sound('data/sfx/hit.wav'),
            'shoot': pygame.mixer.Sound('data/sfx/shoot.wav'),
            'ambience': pygame.mixer.Sound('data/sfx/ambience.wav'),
        }

        self.sfx['ambience'].set_volume(0.2)
        self.sfx['shoot'].set_volume(0.4)
        self.sfx['hit'].set_volume(0.8)
        self.sfx['dash'].set_volume(0.3)
        self.sfx['jump'].set_volume(0.7)

        self.state = GameplayScene(self, 0)
        self.pause_state = PauseScene(self)
        self.screenshake = 0
        
        self.player = Player(self, (50, 50), (8, 15), health=30)
    
        self.state.load_level(self.state.level)
    

    def update(self):
        '''
        Handle per-frame logic updates
        '''

        # Add basic background fill and asset
        self.display.fill((0, 0, 0, 0))
        self.display_2.blit(self.assets['background'], (0, 0)) # Default screen background

        # Update Screenshake
        self.screenshake = max(0, self.screenshake - 1)

        # Calculate camera position and offset for future object placement
        self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30 # The camera position is the top-left. So we need to subtract the screen size to center the player
        self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30 # The camera position is the top-left. So we need to subtract the screen size to center the player
        render_scroll = (int(self.scroll[0]), int(self.scroll[1])) # Solves sub-pixel camera jittering by using int rounding/truncation

        self.state.update()
        self.state.render(render_scroll)

        # Handle outlining
        display_mask = pygame.mask.from_surface(self.display)
        display_sillhouette = display_mask.to_surface(setcolor=(0, 0, 0, 180), unsetcolor = (0, 0, 0, 0))
        for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            self.display_2.blit(display_sillhouette, offset)

    def handle_input(self):
        '''
        Handle user input
        '''
        for event in pygame.event.get(): # event is where the... events get stored
            if event.type == pygame.QUIT: # Clicking the 'x' in the window
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.state.movement[0] = True
                if event.key == pygame.K_RIGHT:
                    self.state.movement[1] = True
                if event.key == pygame.K_UP:
                    if self.player.jump():
                        self.sfx['jump'].play()
                if event.key == pygame.K_x:
                    self.player.dash()
                if event.key == pygame.K_ESCAPE:
                    self.pause_state.pause()
                    self.state.movement = [False, False]
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.state.movement[0] = False
                if event.key == pygame.K_RIGHT:
                    self.state.movement[1] = False

    def render(self):
        # Handle transition effect
        if self.state.transition:
            transition_surf = pygame.Surface(self.display.get_size())
            pygame.draw.circle(transition_surf, 
                (255, 255, 255), 
                (self.display.get_width() // 2, self.display.get_height() // 2), 
                (30 - abs(self.state.transition)) * 8
            )
            transition_surf.set_colorkey((255, 255, 255))
            self.display.blit(transition_surf, (0, 0))

        # Blit display over background
        self.display_2.blit(self.display, (0, 0))

        # Screenshake
        screenshake_offset = (random.random() * self.screenshake - self.screenshake / 2, random.random() * self.screenshake - self.screenshake / 2)

        # Put all displays onto the screen
        self.screen.blit(pygame.transform.scale(self.display_2, self.screen.get_size()), screenshake_offset) # Where the resizing happens for the pixel art
        
        # Render pause menu
        if self.pause_state.is_paused:
            self.pause_state.render()

    def run(self):
        # Play the background music
        pygame.mixer.music.load('data/music.wav')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1) # Num = loops, -1 is infinite loop

        self.sfx['ambience'].play(-1)

        # Game Loop
        while True:

            if self.pause_state.is_paused:
                self.pause_state.update()
                self.pause_state.handle_input()
            else:
                self.update()
                self.handle_input()
            self.render()

            pygame.display.update() # Updates the display
            self.clock.tick(60) # Limits the game to 60 FPS
        

Game().run()
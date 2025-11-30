'''
A game level editor leveraging many of the same resources that are called in game.py
'''

import pygame
from scripts.utils import load_images
from scripts.tilemap import Tilemap
import sys

RENDER_SCALE = 2.0


class Editor: # Manage game settings
    def __init__(self):
        pygame.init() # Turn the game on?

        pygame.display.set_caption('Editor') # Set window name
        self.screen = pygame.display.set_mode((640, 480)) # Creating the window for the game
        self.display = pygame.Surface((320, 240)) # What I render to. We scale this up to the window size later to multiply the size of all our assets

        self.clock = pygame.time.Clock() # Used to force the game to run at X FPS

        self.assets = {
            'decor' : load_images('tiles/decor'),
            'grass' : load_images('tiles/grass'),
            'large_decor' : load_images('tiles/large_decor'),
            'stone' : load_images('tiles/stone'),
        }

        self.movement = [False, False, False, False] # Used to track movement of camera

        self.tilemap = Tilemap(self, tile_size=16)
        try:
            self.tilemap.load('map.json') # Load beginning file
        except FileNotFoundError:
            pass

        self.scroll = [0, 0] # The offset which simulates the concept of a "camera" (i.e., moving everything X and Y distance)

        self.tile_list = list(self.assets) # Get asset keys
        self.tile_group = 0
        self.tile_variant = 0

        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.ongrid = True

    def run(self):
        # Game Loop
        while True:
            self.display.fill ((0, 0, 0)) # Default screen background

            self.scroll[0] += (self.movement[1] - self.movement[0]) * 2
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 2

            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, offset=render_scroll)

            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy() # Retrieve the tile img
            current_tile_img.set_alpha(100) # Set img to partially transparent

            mpos = pygame.mouse.get_pos() # Cursor to place a tile
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE) # Translate cursor position to original render scale
            tile_pos = (int((mpos[0] + self.scroll[0]) // self.tilemap.tile_size), int((mpos[1] + self.scroll[1]) // self.tilemap.tile_size)) # Get mouse position relative to tile coordinates

            if self.ongrid:
                self.display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0], tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))
            else:
                self.display.blit(current_tile_img, mpos)

            if self.clicking and self.ongrid:
                self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': tile_pos}
            if self.right_clicking:
                tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc]
                for tile in self.tilemap.offgrid_tiles.copy(): # Deleting offgrid tiles
                    tile_img = self.assets[tile['type']][tile['variant']]
                    tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], tile_img.get_width(), tile_img.get_height())
                    if tile_r.collidepoint(mpos):
                        self.tilemap.offgrid_tiles.remove(tile)


            

            for event in pygame.event.get(): # event is where the... events get stored
                if event.type == pygame.QUIT: # Clicking the 'x' in the window
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # Left click
                        self.clicking = True
                        if not self.ongrid: # Putting this here so the offgrid placement only happens once per click
                            self.tilemap.offgrid_tiles.append({'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': (mpos[0] + self.scroll[0], mpos[1] + self.scroll[1])})
                    if event.button == 3: # Right click
                        self.right_clicking = True
                    if self.shift:
                        if event.button == 4: # Scroll up, iterate through the tile groups
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                        if event.button == 5: # Scroll down, iterate through the tile groups
                            self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
                    else:
                        if event.button == 4: # Scroll up, iterate through the tile groups
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                            self.tile_variant = 0
                        if event.button == 5: # Scroll down, iterate through the tile groups
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False
                        

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_g: # Toggle on grid snapping
                        self.ongrid = not self.ongrid
                    if event.key == pygame.K_o:
                        self.tilemap.save('map.json')
                    if event.key == pygame.K_t:
                        self.tilemap.autotile()
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)) # Where the resizing happens for the pixel art
            pygame.display.update() # Updates the display
            self.clock.tick(60) # Limits the game to 60 FPS

Editor().run()
import pygame

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, 1), (1, 0), (0, 0), (-1 , 1), (0, 1), (1, 1)]
PHYSICS_TILES = {'grass', 'stone'}

class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {} # Tracking all of the organized tiles that make up the map. Each tile is mapped using location as a key. Tiles without a map are assumed to be "empty space"
        self.offgrid_tiles = [] # Tracking non-grid tiles. Components of this are the same as tilemap objects, but their position is calculated by pixel, not tile.

        for i in range(10): # Make some starter tiles
            self.tilemap[str(3 + i) + ';10'] = {'type': 'grass', 'variant': 1, 'pos': (3 + i, 10)} # Could store tile as an object too, maybe better depending on the number of attributes necessary
            self.tilemap['10;' + str(5 + i)] = {'type': 'stone', 'variant': 1, 'pos': (10, 5 + i)}

    def tiles_around(self, pos): # Find all tiles that collide with a given position
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    def physics_rects_around(self, pos): # Find all rects that collide with a given position
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size)) # A single-tile sized rect
        return rects

    def render(self, surf, offset=(0, 0)):
        for tile in self.offgrid_tiles: # Rendered first so tilemap takes precedence
            # Tiles off grid have their position tracked by pixels, not tiles. So no need to multiply here
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))


        # Render only the tiles that could reasonably appear on the display by calculating number of tiles between camera position (top-left of display) and the bottom-right of the display and rendering tiles in that space
        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    # For the first argument - the type points to the assets, the variant says which file number we should be using. In this case we're using all 1.png files from the asset type
                    # The second argument multiplies position by tile_size so the coordinates translate properly to the pixel distance on the screen
                    surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
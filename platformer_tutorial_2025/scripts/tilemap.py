import json
import pygame

    # Presorted tuple arrangements to determine the autotile system logic
AUTOTILE_MAP = {
    tuple(sorted([(1, 0), (0, 1)])): 0, # Make top-left because you have a bottom and right tile
    tuple(sorted([(1, 0), (0, 1), (-1, 0)])): 1, # Make middle because you have left right and bottom
    tuple(sorted([(-1, 0), (0, 1)])): 2,
    tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 3,
    tuple(sorted([(-1, 0), (0, -1)])): 4,
    tuple(sorted([(-1, 0), (0, -1), (1, 0)])): 5,
    tuple(sorted([(1, 0), (0, -1)])): 6,
    tuple(sorted([(1, 0), (0, 1), (0, -1)])): 7,
    tuple(sorted([(1, 0), (0, 1), (-1, 0), (0, -1)])): 8
}


NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, 1), (1, 0), (0, 0), (-1 , 1), (0, 1), (1, 1)]
PHYSICS_TILES = {'grass', 'stone'}
AUTOTILE_TYPES = {'grass', 'stone'}

class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {} # Tracking all of the organized tiles that make up the map. Each tile is mapped using location as a key. Tiles without a map are assumed to be "empty space"
        self.offgrid_tiles = [] # Tracking non-grid tiles. Components of this are the same as tilemap objects, but their position is calculated by pixel, not tile.

    def tiles_around(self, pos): # Find all tiles that collide with a given position
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    def save(self, path):
        # Save existing tilemap to json
        f = open(path, 'w')
        json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size, 'offgrid': self.offgrid_tiles}, f)
        f.close()

    def load(self, path):
        # Load json formatted tilemap into editor
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()

        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid']
    
    def physics_rects_around(self, pos): # Find all rects that collide with a given position
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size)) # A single-tile sized rect
        return rects
    
    def autotile(self):
        # Get neighboring tiles to determine what the next one should be
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            neighbors = set()
            for shift in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
                check_loc = str(tile['pos'][0] + shift[0]) + ';' + str(tile['pos'][1] + shift[1])
                if check_loc in self.tilemap: # Neighbor has been found
                    if self.tilemap[check_loc]['type'] == tile['type']:
                        neighbors.add(shift)
            neighbors = tuple(sorted(neighbors))
            if (tile['type'] in AUTOTILE_TYPES) and (neighbors in AUTOTILE_MAP):
                tile['variant'] = AUTOTILE_MAP[neighbors]


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
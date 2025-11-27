class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {} # Tracking all of the organized tiles that make up the map. Each tile is mapped using location as a key. Tiles without a map are assumed to be "empty space"
        self.offgrid_tiles = [] # Tracking non-grid tiles. Components of this are the same as tilemap objects, but their position is calculated by pixel, not tile.

        for i in range(10): # Make some starter tiles
            self.tilemap[str(3 + i) + ';10'] = {'type': 'grass', 'variant': 1, 'pos': (3 + i, 10)} # Could store tile as an object too, maybe better depending on the number of attributes necessary
            self.tilemap['10;' + str(5 + i)] = {'type': 'stone', 'variant': 1, 'pos': (10, 5 + i)}

    def render(self, surf):
        for tile in self.offgrid_tiles: # Rendered first so tilemap takes precedence
            # Tiles off grid have their position tracked by pixels, not tiles. So no need to multiply here
            surf.blit(self.game.assets[tile['type']][tile['variant']], tile['pos'])

        for loc in self.tilemap:
            tile = self.tilemap[loc]
                # For the first argument - the type points to the assets, the variant says which file number we should be using. In this case we're using all 1.png files from the asset type
                # The second argument multiplies position by tile_size so the coordinates translate properly to the pixel distance on the screen
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size)) 
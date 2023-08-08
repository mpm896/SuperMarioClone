import pygame, json
from scripts.utils import get_image_variation

# Up to two tiles away
NEIGHBOR_OFFSETS = [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1),
                    (0, -2), (-1, -2), (-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2), (-1, 2), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (2, -1), (2, -2), (1, -2)]
PHYSICS_TILES = {'block'} # Set for assets where all tiles have collisions
PHYSICS_TILES_VARIANTS = {
    'decor': get_image_variation('Tilesets/decor', 'pipe')
} # Dict for assets where only some assets have collisions, such as pipes in the decor assets

class Tilemap:

    def __init__(self, game, tilesize=16):
        self.game = game
        self.tilesize = tilesize
        self.tilemap = {}
        self.offgrid_tiles = []

    # Get tiles directly around the position (i.e. tiles directly next to the player)
    def tiles_around(self, pos): 
        tiles = []
        tile_loc = (int(pos[0]) // self.tilesize, int(pos[1]) // self.tilesize)
        for offset in NEIGHBOR_OFFSETS:
            tile_position = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1]) # Convert neighboring tile position to a string to search the tilemap dict

            if tile_position in self.tilemap: # If the neighboring tile position is actually a tile in the tile map
                tiles.append(self.tilemap[tile_position])

        return tiles
    
    # Get rects of nearby tiles, for collision purposes
    def tile_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tilesize, tile['pos'][1] * self.tilesize, self.tilesize, self.tilesize))

            if tile['type'] in PHYSICS_TILES_VARIANTS and tile['variant'] in PHYSICS_TILES_VARIANTS[tile['type']]:
                rects.append(pygame.Rect(tile['pos'][0] * self.tilesize, tile['pos'][1] * self.tilesize, self.game.assets[tile['type']][tile['variant']].get_width(), self.game.assets[tile['type']][tile['variant']].get_width()))

        return rects

    def render(self, surface, offset=(0, 0)):       
                
        # Render offgrid tiles
        for tile in self.offgrid_tiles:
            surface.blit(self.game.assets[tile['type']][tile['variant']],
                        (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))

        # Optimized way of rendering, only try to render what's currently on the display coordinates
        for x in range(offset[0] // self.tilesize - 5, (offset[0] + surface.get_width()) // self.tilesize + 1):
            for y in range(offset[1] // self.tilesize, (offset[1] + surface.get_height()) // self.tilesize + 1):
                
                # Render ongrid tiles
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surface.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tilesize - offset[0],
                                                                                tile['pos'][1] * self.tilesize - offset[1]))

    # Load map
    def load(self, path):
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()

        self.tilemap = map_data['tilemap']
        self.tilesize = map_data['tilesize']
        self.offgrid_tiles = map_data['offgrid']

    # Save map
    def save(self, path):
        f = open(path, 'w')
        json.dump({
            'tilemap': self.tilemap,
            'tilesize': self.tilesize,
            'offgrid': self.offgrid_tiles
        }, f)
        f.close()
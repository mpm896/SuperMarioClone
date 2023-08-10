import pygame, json

MAP_PATH = 'maps/level_01.json'
TILE = 'coin/collect'

def load_map(path=MAP_PATH):
    f = open(path, 'r')
    map_data = json.load(f)
    f.close()

    return map_data

def delete_tile(tilemap, tile=TILE):
    for loc in tilemap['tilemap']:
        if tilemap['tilemap'][loc]['type'] == tile:
            del tilemap['tilemap'][loc]

    for loc in tilemap['offgrid'].copy():
        if loc['type'] == tile:
            tilemap['offgrid'].remove(loc)


def save_map(tilemap, path=MAP_PATH):
        f = open(path, 'w')
        json.dump(tilemap, f)
        f.close()

map = load_map(path=MAP_PATH)
delete_tile(map, tile=TILE)
save_map(map, path=MAP_PATH)
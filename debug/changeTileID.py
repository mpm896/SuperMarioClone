import pygame, json

MAP_PATH = 'maps/level_01.json'
OLD_TYPE = 'coins'
NEW_TYPE = 'coin/collect'

def load_map(path=MAP_PATH):
    f = open(path, 'r')
    map_data = json.load(f)
    f.close()

    return map_data

def change_tile_type(tilemap, old_type=OLD_TYPE, new_type=OLD_TYPE):
    for loc in tilemap['tilemap']:
        if tilemap['tilemap'][loc]['type'] == old_type:
            tilemap['tilemap'][loc]['type'] = new_type

    for item in tilemap['offgrid']:
        if item['type'] == old_type:
            item['type'] = new_type

def save_map(tilemap, path=MAP_PATH):
        f = open(path, 'w')
        json.dump(tilemap, f)
        f.close()

tilemap = load_map(path=MAP_PATH)
change_tile_type(tilemap, old_type=OLD_TYPE, new_type=NEW_TYPE)
save_map(tilemap, path=MAP_PATH)


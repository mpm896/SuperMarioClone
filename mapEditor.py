import pygame, sys, os
from pygame.locals import *
from scripts.tilemap import Tilemap
from scripts.utils import load_image, load_images

RENDER_SCALE = 1.5
WINDOW_SIZE = (640, 480)
FPS = 60
COLORKEY = (255,255,255)
MAP_PATH = 'maps/'
MAP_NAME = 'level_01.json'

class Editor:

    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
        pygame.display.set_caption('Map editor')
        self.display = pygame.Surface((int(WINDOW_SIZE[0] / RENDER_SCALE), int(WINDOW_SIZE[1] / RENDER_SCALE))) # This will be the main surface for rendering

        self.clock = pygame.time.Clock()

        # Add code later to load all assets
        self.assets = {
            'block': load_images('Tilesets/blocks', colorkey=COLORKEY),
            'decor': load_images('Tilesets/decor', colorkey=COLORKEY),
            'items': load_images('Misc/items', colorkey=COLORKEY),
            'coin/collect': load_images('Misc/coin/collect')
        }

        # Clicking-related attributes
        self.click = False
        self.right_click = False
        self.shift = False
        self.ongrid = True
        self.flip = False

        # Left, right, up, down
        self.movement = [False, False, False, False]

        # Blocks are as follows: 00 - ground; 01 - breakable; 02 - used; 03 - mystery; 04 - static block
        self.scroll = [0, 0]

        self.tilemap = Tilemap(self, tilesize=16)
        try:
            self.tilemap.load(MAP_PATH + MAP_NAME)
        except FileNotFoundError:
            pass

        self.tile_list = list(self.assets) # Gets a list of keys
        self.tile_group = 0
        self.tile_variant = 0

    def run(self):
        while True: # Main game loop
            self.display.fill((7, 155, 176))
            
            # Set the scroll
            self.scroll[0] += (self.movement[1] - self.movement[0]) * 10
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 10
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            
            # Render the tilemap
            self.tilemap.render(self.display, offset=render_scroll)

            # Get the currently selected tile, set it to be ~half transparent
            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha(100)

            self.display.blit(current_tile_img, (5, 5)) # Show tile in top left corner

            # Get mouse position on the rendering display, the the corresponding tile coordinate
            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE) # Change it to the scale of the rendering display
            tile_pos = (int((mpos[0] + self.scroll[0]) // self.tilemap.tilesize), 
                        int((mpos[1] + self.scroll[1]) // self.tilemap.tilesize))
            
            # Display the tile where the mouse is
            if self.ongrid:
                self.display.blit(pygame.transform.flip(current_tile_img, False, self.flip),
                                  (tile_pos[0] * self.tilemap.tilesize - self.scroll[0], 
                                   tile_pos[1] * self.tilemap.tilesize - self.scroll[1]))
            else:
                self.display.blit(pygame.transform.flip(current_tile_img, False, self.flip), mpos)

            # Add tile to tilemap if click
            if self.click and self.ongrid: # Tiles snapped to grid
                self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {
                    'type': self.tile_list[self.tile_group],
                    'variant': self.tile_variant,
                    'pos': tile_pos
                }

            if self.click and not self.ongrid: # Tiles off the grid
                self.tilemap.offgrid_tiles.append({
                    'type': self.tile_list[self.tile_group],
                    'variant': self.tile_variant,
                    'pos': (mpos[0] + self.scroll[0], mpos[1] + self.scroll[1])
                })

            # Remove tiles from tilemap if right click
            if self.right_click:
                tile_loc = (str(tile_pos[0]) + ';' + str(tile_pos[1]))

                # Delete on grid tiles
                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc]
                
                # Delete off grid tiles
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_img = self.assets[tile['type']][tile['variant']]
                    tile_rect = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], 
                                            tile_img.get_width(), tile_img.get_height())
                    if tile_rect.collidepoint(mpos):
                        self.tilemap.offgrid_tiles.remove(tile)

            # Get events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1: # Left click
                        self.click = True
                    if event.button == 3: # Right click
                        self.right_click = True
                    
                    if self.shift: # Shift + scroll wheel, change the tile variant
                        if event.button == 4: # Scroll wheel up
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                        if event.button == 5: # Scroll wheel down
                            self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
                    else: # Scroll wheel, change the tile group
                        if event.button == 4:
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                            self.tile_variant = 0
                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0
                
                if event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        self.click = False
                    if event.button == 3:
                        self.right_click = False

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == K_UP or event.key == K_w:
                        self.movement[2] = True
                    if event.key == K_DOWN or event.key == K_s:
                        self.movement[3] = True
                    if event.key == K_RIGHT or event.key == K_d:
                        self.movement[1] = True
                    if event.key == K_LEFT or event.key == K_a:
                        self.movement[0] = True
                    if event.key == K_LSHIFT:
                        self.shift = True
                    if event.key == K_f:
                        self.flip = not self.flip
                    if event.key == K_g:
                        self.ongrid = not self.ongrid
                    if event.key == K_o:
                        self.tilemap.save(MAP_PATH + MAP_NAME)

                if event.type == KEYUP:
                    if event.key == K_UP or event.key == K_w:
                        self.movement[2] = False
                    if event.key == K_DOWN or event.key == K_s:
                        self.movement[3] = False
                    if event.key == K_RIGHT or event.key == K_d:
                        self.movement[1] = False
                    if event.key == K_LEFT or event.key == K_a:
                        self.movement[0] = False
                    if event.key == K_LSHIFT:
                        self.shift = False

            self.screen.blit(pygame.transform.scale(self.display, WINDOW_SIZE), (0, 0))
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    Editor().run()

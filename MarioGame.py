import pygame, sys, random, os
from pygame.locals import *
from scripts.entities import PhysicsEntity, Player
from scripts.utils import load_image, load_images, get_image_variation, Spritesheet, Animation
from scripts.tilemap import Tilemap

WINDOW_SIZE = (640, 480)
FPS = 60
COLORKEY = None
RENDER_SCALE = 1.5

class Game:

    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
        pygame.display.set_caption('Classic Super Mario Bros Clone')
        self.display = pygame.Surface((int(WINDOW_SIZE[0] / RENDER_SCALE), int(WINDOW_SIZE[1] / RENDER_SCALE))) # This will be the main surface for rendering

        self.clock = pygame.time.Clock()

        # Only code for left and right movement. Down will be gravity, and up will be temporarily reversing gravity
        self.movement = [False, False] # Left is [0], right is [1]

        # Add code later to load all assets
        self.assets = {
            'block': load_images('Tilesets/blocks', colorkey=COLORKEY),
            'decor': load_images('Tilesets/decor', colorkey=COLORKEY),
        }

        # Load all player assets
        for action in next(os.walk('data/images/Characters/player'))[1]: # Gets directory names from the directory to walk
            self.assets['player/' + action] = Animation(load_images('Characters/player/'+ action))

        # Blocks are as follows: 00 - ground; 01 - breakable; 02 - used; 03 - mystery; 04 - static block
        self.scroll = [0, 0]

        #self.player = PhysicsEntity(self, 'player', (50, 50), (14, 17))
        self.player_img = load_image('Characters/player/idle/00.png')
        self.player = Player(self, (50, 250), (self.player_img.get_width(), self.player_img.get_height()))

        self.tilemap = Tilemap(self, tilesize=16)
        try:
            self.tilemap.load('maps/level_01.json')
        except FileNotFoundError:
            pass
        
        # Get list of tile X coordinates, for camera scroll purposes
        self.x_loc_list = []
        for loc in list(self.tilemap.tilemap):
            pos = self.tilemap.tilemap[loc]['pos'][0]
            self.x_loc_list.append(pos)
        self.x_loc_list = list(sorted(set(self.x_loc_list)))

    def run(self):
        while True: # Main game loop
            self.display.fill((7, 155, 176))
            
            # Don't scroll in X if in the first 50 pixels of the map of if the right-most tile is at the edge of the screen
            # The second term of the conditional statement is the pixel position of the last tile (before the bounding wall), minus the scroll value plus the player width. Don't scroll if the last tile position on the display is less than the display width
            if (100 < self.player.rect().centerx) and (self.x_loc_list[-2] * self.tilemap.tilesize - self.scroll[0] + self.player.size[0] >= self.display.get_width()):
               self.scroll[0] += (self.player.rect().centerx - 100 - self.scroll[0])
            
            # Only scroll the Y if player is above a certain height
            if self.player.rect().centery < self.display.get_height() / 2:
                self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1])

            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            
            self.tilemap.render(self.display, offset=render_scroll)

            self.player.update(self.tilemap, ((self.movement[1] - self.movement[0]), 0))
            self.player.render(self.display, offset=render_scroll)
            
            # Get events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == K_UP or event.key == K_w or event.key == K_SPACE:
                        self.player.jump()
                    if event.key == K_DOWN or event.key == K_s:
                        pass
                    if event.key == K_RIGHT or event.key == K_d:
                        self.movement[1] = True
                    if event.key == K_LEFT or event.key == K_a:
                        self.movement[0] = True
                    if event.key == K_q:
                        pass

                if event.type == KEYUP:
                    if event.key == K_UP or event.key == K_w:
                        pass
                    if event.key == K_DOWN or event.key == K_s:
                        pass
                    if event.key == K_RIGHT or event.key == K_d:
                        self.movement[1] = False
                    if event.key == K_LEFT or event.key == K_a:
                        self.movement[0] = False

            self.screen.blit(pygame.transform.scale(self.display, WINDOW_SIZE), (0, 0))
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    Game().run()
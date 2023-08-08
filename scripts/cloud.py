import pygame, random

class Cloud:

    def __init__(self, pos, img, speed, depth):
        self.pos = list(pos)
        self.img = img
        self.speed = speed
        self.depth = depth
        
    def update(self):
        self.pos[0] += self.speed

    def render(self, surface, offset=(0, 0)):
        # Want to render so that it loops. Get render position and modulo by the display width + img width, for looping effect
        render_pos = (self.pos[0] - offset[0] * self.depth, self.pos[1] - offset[1] * self.depth)
        
        surface.blit(self.img, (render_pos[0] % (surface.get_width() + self.img.get_width()) - self.img.get_width(),
                                  render_pos[1] % (surface.get_height() + self.img.get_height()) - self.img.get_height()))
        
class Clouds:

    def __init__(self, game, images, count=5):
        self.game = game
        self.images = images
 
        self.clouds = []
        for i in range(count):
            depth = random.random() * 0.6 + 0.2 # Range from 0.2 to 0.8
            speed = random.random() * 0.3 + 0.05 # Range from 0.05 to 0.1
            
            # If there is more than one cloud image
            if hasattr(self.images, '__iter__'):
                img = random.choice(self.images)
            else: # If only one cloud image
                img = self.images

            pos = (random.random() * 99999, random.random() * (self.game.display.get_height() - 2 * self.game.tilemap.tilesize))
            self.clouds.append(Cloud(pos, img, speed, depth))

        self.clouds.sort(key=lambda x: x.depth, reverse=True) # Sorting clouds. Sort by depth to layer it properly

    def update(self):
        for cloud in self.clouds:
            cloud.update()
    
    def render(self, surface, offset=(0, 0)):
        for cloud in self.clouds:
            cloud.render(surface, offset=offset)



    
        
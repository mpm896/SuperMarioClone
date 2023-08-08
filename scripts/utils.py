import pygame, os

BASE_IMG_PATH = 'data/images/'

def load_image(path, colorkey=None): # If using directly, include filename in path
    img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha() # Since image has transparency already in image, use convert_alpha() instead of convert()
    img.set_colorkey(colorkey)
    return img

def load_images(path, colorkey=None):
    images = []
    for image in sorted(os.listdir(BASE_IMG_PATH + path)):
        if image[0] == '.': # skip hidden files
            pass
        else:
            img = load_image(path + '/' + image, colorkey=colorkey)
            images.append(img)
    return images

def get_image_variation(path, string):
    """
    Vars: path - path to where the specific image is found
          string - part of the image name that is unique to that asset (i.e. 'pipe' in Mario)
    """
    variation_nums = []
    count = 0
    for image in sorted(os.listdir(BASE_IMG_PATH + path)):
        if image[0] == '.' or image == None: # skip hidden files and None values
           pass
        elif string.lower() in image.lower(): 
            variation_nums.append(count)
            count += 1
        else:
            count += 1

    return variation_nums

# This class handles sprite sheets
# This was taken from https://www.pygame.org/wiki/Spritesheet
# I've added some code to fail if the file wasn't found..
# Note: When calling images_at the rect is the format:
# (x, y, x + offset, y + offset)
class Spritesheet:

    def __init__(self, path, colorkey=(0, 0, 0)): # Path should include the filename
        try:
            self.sheet = load_image(path, colorkey=colorkey)
        except pygame.error:
            print('Unable to load spritesheet image: ', path)

    # Load specific image from specific rect (area) of the spritesheet
    def load_image_at(self, rect, colorkey=(0, 0, 0)):
        img_rect = pygame.Rect(rect)
        img = pygame.Surface(img_rect.size).convert()
        img.blit(self.sheet, (0, 0), img_rect)
        img.set_colorkey(colorkey)
        return img
    
    # Load a bunch of images from the spritesheet and load them as a list
    def load_images_at(self, rects, colorkey=(0, 0, 0)):
        return [self.load_image_at(rect, colorkey=colorkey) for rect in rects]
    
    # Load a whole strip of images and return them as a list
    def load_strip(self, rect, image_count, colorkey=(0, 0, 0)):
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3]) for x in range(image_count)]
        return self.load_images_at(tups, colorkey=colorkey)


class Animation:
    
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.img_duration = img_dur
        self.done = False
        self.loop = loop
        self.frame = 0 # Frame of the game

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)
    
    def update(self): # Update the frame
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True

    def img(self):
        return self.images[int(self.frame / self.img_duration)]
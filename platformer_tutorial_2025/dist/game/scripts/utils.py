import os
import pygame

BASE_IMG_PATH = 'data/images/'

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert() # Convert image for better optimization
    img.set_colorkey((0,0,0)) # Take out black
    return img

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)): # Sorted ensures the use of filename stays alphabetical. Filenames should also be 0 padded to prevent 10 from coming before 2 (for example)
        images.append(load_image(path + '/' + img_name))
    return images

class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images)) # Don't exceed the max number of frames in the animation, but loop
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1) # Don't exceed the max number of frames, stop at the max length of animation
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True

    def img(self):
        return self.images[int(self.frame / self.img_duration)]
    

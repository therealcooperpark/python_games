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
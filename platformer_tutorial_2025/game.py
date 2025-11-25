import pygame
import sys

# Turn the game on?
pygame.init()

pygame.display.set_caption('Ninja Game') # Set window name
screen = pygame.display.set_mode((640, 480)) # Creating the window for the game

clock = pygame.time.Clock() # Used to force the game to run at X FPS

# Game Loop
while True:
    for event in pygame.event.get(): # event is where the... events get stored
        if event.type == pygame.QUIT: # Clicking the 'x' in the window
            pygame.quit()
            sys.exit()

    pygame.display.update() # Updates the display
    clock.tick(60) # Limits the game to 60 FPS
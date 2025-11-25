import pygame
import sys


class Game: # Manage game settings
    def __init__(self):
        pygame.init() # Turn the game on?

        pygame.display.set_caption('Ninja Game') # Set window name
        self.screen = pygame.display.set_mode((640, 480)) # Creating the window for the game

        self.clock = pygame.time.Clock() # Used to force the game to run at X FPS

        self.img = pygame.image.load('data/images/clouds/cloud_1.png')
        self.img.set_colorkey((0, 0, 0)) # Pure black gets replaced with transparency by using colorkey
        self.img_pos = [160, 260]
        self.movement = [False, False]

        self.collision_area = pygame.Rect(50, 50, 300, 50) # Make a basic rectangle for collision practice

    def run(self):
        # Game Loop
        while True:
            self.screen.fill((14, 219, 248)) # Default screen color

            img_r = pygame.Rect(self.img_pos[0], self.img_pos[1], self.img.get_width(), self.img.get_height()) # Make collision space for the cloud
            if img_r.colliderect(self.collision_area): # If rects are overlapping somehow
                pygame.draw.rect(self.screen, (0, 100, 255), self.collision_area)
            else:
                pygame.draw.rect(self.screen, (0, 50, 155), self.collision_area)
            
            self.img_pos[1] += (self.movement[1] - self.movement[0]) * 5 # Cancel movement when both are True, otherwise go up/down
            self.screen.blit(self.img, self.img_pos)

            for event in pygame.event.get(): # event is where the... events get stored
                if event.type == pygame.QUIT: # Clicking the 'x' in the window
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.movement[0] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.movement[0] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = False

            pygame.display.update() # Updates the display
            self.clock.tick(60) # Limits the game to 60 FPS

Game().run()
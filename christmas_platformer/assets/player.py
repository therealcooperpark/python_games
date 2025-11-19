"""
Player class for platformer games
Decoupled from game-specific logic for easy reuse
"""

import pygame
from pygame.math import Vector2 as vec


class Player(pygame.sprite.Sprite):
    """
    A generic player character for 2D platformer games with physics-based movement.
    
    Args:
        x (int): Starting x position
        y (int): Starting y position
        width (int): Player width in pixels (default: 30)
        height (int): Player height in pixels (default: 30)
        color (tuple): RGB color tuple (default: (128, 255, 40))
        jump_strength (float): Upward velocity when jumping (default: 15)
        acceleration (float): Movement acceleration (default: 0.5)
        friction (float): Friction coefficient (default: -0.16)
        gravity (float): Downward acceleration (default: 0.5)
    """
    
    def __init__(self, x=10, y=420, width=30, height=30, color=(128, 255, 40),
                 jump_strength=15, acceleration=0.5, friction=-0.16, gravity=0.5):
        super().__init__()
        
        # Visual properties
        self.surf = pygame.Surface((width,height)) # Player dimensions
        self.surf.fill(color) # Player color (R,G,B) format
        self.rect = self.surf.get_rect(center = (x, y)) # Spawn point
        self.image = None  # Can be set to a sprite image
        
        # Physics properties
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        
        # Physics constants
        self.jump_strength = jump_strength
        self.base_acceleration = acceleration
        self.friction = friction
        self.gravity = gravity
        
        # State tracking
        self.jumping = False
        self.on_ground = False
        
    def jump(self, platform_group):
        """
        Make the player jump if on a platform.
        
        Args:
            platform_group (pygame.sprite.Group): Group of platform sprites to check collision
        """
        hits = pygame.sprite.spritecollide(self, platform_group, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -self.jump_strength
            
    def cancel_jump(self):
        """
        Reduce upward velocity for variable jump height.
        Call this when jump button is released.
        """
        if self.jumping and self.vel.y < -3:
            self.vel.y = -3
            
    def move(self, left=False, right=False, screen_width=None):
        """
        Update player movement based on input.
        
        Args:
            left (bool): True if moving left
            right (bool): True if moving right
            screen_width (int): Width of game screen for boundary checking (optional)
        """
        # Reset acceleration with gravity
        self.acc = vec(0, self.gravity)
        
        # Apply horizontal acceleration based on input
        if left:
            self.acc.x = -self.base_acceleration
        if right:
            self.acc.x = self.base_acceleration
            
        # Apply friction and update physics
        self.acc.x += self.vel.x * self.friction
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        
        # Boundary checking
        if screen_width:
            if self.pos.x > screen_width - self.rect.width / 2:
                self.pos.x = screen_width - self.rect.width / 2
            if self.pos.x < self.rect.width / 2:
                self.pos.x = self.rect.width / 2
                
        # Update rect position
        self.rect.midbottom = self.pos
        
    def update(self, platform_group):
        """
        Handle collision detection with platforms.
        
        Args:
            platform_group (pygame.sprite.Group): Group of platform sprites to check collision
        """
        hits = pygame.sprite.spritecollide(self, platform_group, False)
        
        if hits and self.vel.y > 0:  # Moving downward and hit something
            self.pos.y = hits[0].rect.top + 1
            self.vel.y = 0
            self.jumping = False
            self.on_ground = True
        else:
            self.on_ground = False
    
    def set_image(self, image_path):
        """
        Set a sprite image for the player.
        
        Args:
            image_path (str): Path to image file
        """
        self.image = pygame.image.load(image_path)
        
    def draw(self, surface):
        """
        Draw the player on the given surface.
        
        Args:
            surface (pygame.Surface): Surface to draw on
        """
        if self.image:
            surface.blit(self.image, self.rect)
        else:
            surface.blit(self.surf, self.rect)


# Example usage
if __name__ == "__main__":
    """
    Example of how to use the generic Player class
    """
    pygame.init()
    
    # Game constants
    WIDTH = 400
    HEIGHT = 450
    FPS = 60
    
    # Create display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Player Test")
    clock = pygame.time.Clock()
    
    # Create player
    player = Player(
        x=WIDTH // 2,
        y=HEIGHT - 100,
        width=30,
        height=30,
        color=(128, 255, 40),
        jump_strength=15,
        acceleration=0.5
    )
    
    # Create a simple platform for testing
    class SimplePlatform(pygame.sprite.Sprite):
        def __init__(self, x, y, width, height):
            super().__init__()
            self.surf = pygame.Surface((width, height))
            self.surf.fill((255, 0, 0))
            self.rect = self.surf.get_rect(center=(x, y))
    
    platforms = pygame.sprite.Group()
    ground = SimplePlatform(WIDTH // 2, HEIGHT - 10, WIDTH, 20)
    platforms.add(ground)
    
    # Game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump(platforms)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    player.cancel_jump()
        
        # Get input
        keys = pygame.key.get_pressed()
        left = keys[pygame.K_LEFT]
        right = keys[pygame.K_RIGHT]
        
        # Update
        player.move(left, right, WIDTH)
        player.update(platforms)
        
        # Draw
        screen.fill((0, 0, 0))
        screen.blit(ground.surf, ground.rect)
        player.draw(screen)
        
        pygame.display.update()
        clock.tick(FPS)
    
    pygame.quit()

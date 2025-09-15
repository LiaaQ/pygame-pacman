"""
Pacman Game Module

This module defines the Pacman class, representing the player character in the Pacman game.
Pacman is controlled by the player and must navigate the maze, collect coins, and avoid ghosts.

Attributes:
    tile_height (int): The height of a game tile.
    tile_width (int): The width of a game tile.

Classes:
    Pacman (pygame.sprite.Sprite): A class representing the Pacman character in the game.
        - __init__: Initializes a new instance of the Pacman class.
        - image_state: Sets the image of Pacman based on its direction and animation index.
        - move: Moves Pacman in the current direction, considering collisions with walls and ghost doors.
        - respawn: Respawns Pacman at the starting position with a decreased life count.
        - change_direction: Changes Pacman's direction based on the user input.
        - update: Updates Pacman's position and image for the current frame.
"""
import pygame

tile_height = 27
tile_width = 27

class Pacman(pygame.sprite.Sprite):
    """
    A class representing the Pacman character in the game.

    Attributes:
        pacman_image (list): A list of Pacman images for its animation.
        image (pygame.Surface): The current image of Pacman.
        rect (pygame.Rect): The rectangle representing the position of Pacman.
        score (int): The score accumulated by Pacman.
        lives (int): The number of lives remaining for Pacman.
        direction (int): The current direction of Pacman (0: right, 1: left, 2: up, 3: down).
        speed (int): The speed at which Pacman moves.
    """
    def __init__(self):
        super().__init__()
        pcmn1_surf = pygame.image.load("Graphics/Pacman/1.png").convert_alpha()
        pcmn1_surf = pygame.transform.scale(pcmn1_surf, (20, 20))
        pcmn2_surf = pygame.image.load("Graphics/Pacman/2.png").convert_alpha()
        pcmn2_surf = pygame.transform.scale(pcmn2_surf, (20, 20))
        pcmn3_surf = pygame.image.load("Graphics/Pacman/3.png").convert_alpha()
        pcmn3_surf = pygame.transform.scale(pcmn3_surf, (20, 20))
        pcmn4_surf = pygame.image.load("Graphics/Pacman/4.png").convert_alpha()
        pcmn4_surf = pygame.transform.scale(pcmn4_surf, (20, 20))
        self.pacman_image = [pcmn1_surf, pcmn2_surf, pcmn3_surf, pcmn4_surf]
        self.image = self.pacman_image[0]
        self.rect = self.image.get_rect(center = (15*tile_height,24*tile_width))
        self.score = 0
        self.lives = 3
        self.direction = 0
        self.speed = 1

    def image_state(self, index):
        """
        Sets the image of Pacman based on its direction and animation index.

        Parameters:
            index (int): The animation index to determine Pacman's current state.
        """
        if self.direction == 0:
            self.image = self.pacman_image[index // 5]
        elif self.direction == 1:
            self.image = pygame.transform.flip(self.pacman_image[index // 5], True, False)
        elif self.direction == 2:
            self.image = pygame.transform.rotate(self.pacman_image[index // 5], 90)
        elif self.direction == 3:
            self.image = pygame.transform.rotate(self.pacman_image[index // 5], 270)

    def move(self, wall_group, ghost_door):
        """
        Moves Pacman in the current direction, considering collisions with walls and ghost doors.

        Parameters:
            wall_group (pygame.sprite.Group): A group containing wall sprites.
            ghost_door (pygame.sprite.Group): A group containing ghost door sprites.
        """
        original_pos = (self.rect.x, self.rect.y)

        dx = dy = 0
        if self.direction == 0:
            dx = self.speed
        elif self.direction == 1:
            dx = -self.speed
        elif self.direction == 2:
            dy = -self.speed
        elif self.direction == 3:
            dy = self.speed

        self.rect.x += dx
        self.rect.y += dy

        if self.rect.centerx > 800:
            self.rect.centerx = 0
        if self.rect.centerx < 0:
            self.rect.centerx = 800

        if pygame.sprite.spritecollideany(self, wall_group) or pygame.sprite.spritecollideany(self, ghost_door):
            self.rect.x, self.rect.y = original_pos

    def respawn(self):
        """
        Respawns Pacman at the starting position with a decreased life count.
        """
        self.rect.centerx = 15*tile_height
        self.rect.centery = 24*tile_width
        self.lives-=1

    def change_direction(self, event):
        """
        Changes Pacman's direction based on the user input.

        Parameters:
            event (pygame.event.Event): The pygame event object.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == ord('w'):
                self.direction = 2
            elif event.key == pygame.K_DOWN or event.key == ord('s'):
                self.direction = 3
            elif event.key == pygame.K_LEFT or event.key == ord('a'):
                self.direction = 1
            elif event.key == pygame.K_RIGHT or event.key == ord('d'):
                self.direction = 0

    def update(self, index, wall_group, ghost_door):
        """
        Updates Pacman's position and image for the current frame.

        Parameters:
            index (int): The animation index to determine Pacman's sprite image.
            wall_group (pygame.sprite.Group): A group containing wall sprites.
            ghost_door (pygame.sprite.Group): A group containing ghost door sprites.
        """
        self.move(wall_group, ghost_door)
        self.image_state(index)

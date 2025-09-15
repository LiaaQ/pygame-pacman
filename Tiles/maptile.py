"""
The Tiles module contains classes related to the tiles on the game map.

Classes:
    MapTile: Represents a tile on the game map.

Attributes:
    - COIN_IMAGE: Image for coins on the map.
    - POWERUP_IMAGE: Image for power-ups on the map.
    - WALL_IMAGE_3 to WALL_IMAGE_13: Images for different wall types on the map.

Usage:
    Import the MapTile class into your game module and use it to represent tiles on the map.
"""
import pygame

class MapTile(pygame.sprite.Sprite):
    """
    MapTile class represents a tile on the game map.

    Attributes:
        COIN_IMAGE: Image for coins on the map.
        POWERUP_IMAGE: Image for power-ups on the map.
        WALL_IMAGE_3 to WALL_IMAGE_13: Images for different wall types on the map.

    Methods:
        load_image: Loads the appropriate image based on the tile type.
        update: Updates the image of the MapTile.
    """

    COIN_IMAGE = pygame.image.load("Graphics/coin.png")
    POWERUP_IMAGE = pygame.image.load("Graphics/powerup.png")
    WALL_IMAGE_3 = pygame.image.load("Graphics/wall3.png")
    WALL_IMAGE_4 = pygame.image.load("Graphics/wall4.png")
    WALL_IMAGE_5 = pygame.image.load("Graphics/wall5.png")
    WALL_IMAGE_6 = pygame.image.load("Graphics/wall6.png")
    WALL_IMAGE_7 = pygame.image.load("Graphics/wall7.png")
    WALL_IMAGE_8 = pygame.image.load("Graphics/wall8.png")
    WALL_IMAGE_10 = pygame.image.load("Graphics/wall10.png")
    WALL_IMAGE_11 = pygame.image.load("Graphics/wall11.png")
    WALL_IMAGE_12 = pygame.image.load("Graphics/wall12.png")
    WALL_IMAGE_13 = pygame.image.load("Graphics/wall13.png")

    def __init__(self, x, y, tile_type):
        """
        Initializes a MapTile instance.

        Args:
            x (int): X-coordinate of the tile on the screen.
            y (int): Y-coordinate of the tile on the screen.
            tile_type (int): Type of the tile, determining its appearance.
        """
        super().__init__()
        self.tile_type = tile_type
        image_surf = self.load_image()
        image_surf = pygame.transform.scale(image_surf, (27, 27))
        self.image = image_surf
        self.rect = self.image.get_rect(center = (x,y))

    def load_image(self):
        """
        Loads the appropriate image based on the tile type.

        Returns:
            pygame.Surface: Image representing the tile.
        """
        image_mapping = {
        1: self.COIN_IMAGE,
        2: self.POWERUP_IMAGE,
        3: self.WALL_IMAGE_3,
        4: self.WALL_IMAGE_4,
        5: self.WALL_IMAGE_5,
        6: self.WALL_IMAGE_6,
        7: self.WALL_IMAGE_7,
        8: self.WALL_IMAGE_8,
        10: self.WALL_IMAGE_10,
        11: self.WALL_IMAGE_11,
        12: self.WALL_IMAGE_12,
        13: self.WALL_IMAGE_13
        }

        if self.tile_type == 0:
            image = pygame.Surface((27, 27))
            image.fill((0, 0, 0))
            return image
        if self.tile_type == 9:
            image = pygame.Surface((27, 27))
            image.fill((0, 0, 0))
            pygame.draw.line(image, (255, 255, 255), (0, 12), (24, 12), 3)
            return image
        image = image_mapping.get(self.tile_type, pygame.Surface((27, 27)))
        return image

    def update(self):
        """
        Updates the image of the MapTile.
        """
        self.image = self.load_image()

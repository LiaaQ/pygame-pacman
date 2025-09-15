"""
Pacman Game Map Module

This module defines the Map class, which represents the game map. It includes methods to create
and draw the game board, and there is also a function for applying effects to tiles based on player interactions.

Dependencies:
- NumPy: A library for multi-dimensional arrays and matrices, which is used for storing the boards.

Usage:
Import this module and create an instance of the Map class to represent the game map.
Use the methods and functions provided to draw the map on the screen and apply effects to tiles.
"""
import numpy as np
import pygame
from Tiles.maptile import MapTile

class Map():
    """
    A class representing the game map for the Pacman game.

    Attributes:
    - simple_board (numpy.ndarray): A 2D array representing a simplified version of the game board.
    - tiles_board (pygame.sprite.Group): A sprite group containing all non-wall tiles.
    - wall_group (pygame.sprite.Group): A sprite group containing all wall tiles.
    - ghostdoor_group (pygame.sprite.Group): A sprite group containing all ghost door tiles.
    """
    def __init__(self):
        board = np.array([
[6, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 0],
[3, 6, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 0, 0, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 3, 0],
[3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 10, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 12, 3],
[3, 3, 1, 6, 13, 13, 5, 1, 6, 13, 13, 13, 5, 1, 10, 3, 1, 6, 13, 13, 13, 5, 1, 6, 4, 4, 5, 1, 12, 3],
[3, 3, 2, 12, 0, 0, 12, 1, 12, 0, 0, 0, 12, 1, 10, 3, 1, 12, 0, 0, 0, 12, 1, 12, 13, 13, 12, 2, 12, 3],
[3, 3, 1, 7, 13, 13, 8, 1, 7, 13, 13, 13, 8, 1, 7, 8, 1, 7, 13, 13, 13, 8, 1, 7, 11, 11, 8, 1, 12, 3],
[3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 12, 3],
[3, 3, 1, 6, 4, 4, 5, 1, 6, 5, 1, 6, 4, 4, 4, 4, 4, 4, 5, 1, 6, 5, 1, 6, 4, 4, 5, 1, 12, 3],
[3, 3, 1, 7, 11, 11, 8, 1, 10, 3, 1, 7, 11, 11, 0, 0, 11, 11, 8, 1, 10, 3, 1, 7, 11, 11, 8, 1, 12, 3],
[3, 3, 1, 1, 1, 1, 1, 1, 10, 3, 1, 1, 1, 1, 10, 3, 1, 1, 1, 1, 10, 3, 1, 1, 1, 1, 1, 1, 12, 3],
[3, 0, 4, 4, 4, 4, 5, 1, 10, 0, 4, 4, 5, 0, 10, 3, 0, 6, 4, 4, 0, 3, 1, 6, 4, 4, 4, 4, 3, 3],
[3, 0, 0, 0, 0, 0, 3, 1, 10, 0, 11, 11, 8, 0, 7, 8, 0, 7, 11, 11, 0, 3, 1, 10, 0, 0, 0, 0, 3, 3],
[3, 0, 0, 0, 0, 0, 3, 1, 10, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 3, 1, 10, 0, 0, 0, 0, 3, 3],
[8, 0, 0, 0, 0, 0, 3, 1, 10, 3, 0, 6, 4, 4, 9, 9, 4, 4, 5, 0, 10, 3, 1, 10, 0, 0, 0, 0, 3, 11],
[11, 11, 11, 11, 11, 11, 8, 1, 7, 8, 0, 10, 0, 0, 0, 0, 0, 0, 3, 0, 7, 8, 1, 7, 11, 11, 11, 11, 11, 11],
[0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 10, 6, 4, 4, 4, 4, 5, 3, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
[4, 4, 4, 4, 4, 4, 5, 1, 6, 5, 0, 10, 10, 0, 0, 0, 0, 3, 3, 0, 6, 5, 1, 6, 4, 4, 4, 4, 4, 4],
[5, 0, 0, 0, 0, 0, 3, 1, 10, 3, 0, 7, 13, 13, 13, 13, 13, 13, 8, 0, 10, 3, 1, 10, 0, 0, 0, 0, 0, 6],
[3, 0, 0, 0, 0, 0, 3, 1, 10, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 3, 1, 10, 0, 0, 0, 0, 0, 10],
[3, 0, 0, 0, 0, 0, 3, 1, 10, 3, 0, 6, 4, 4, 4, 4, 4, 4, 5, 0, 10, 3, 1, 10, 0, 0, 0, 0, 0, 10],
[3, 0, 11, 11, 11, 11, 8, 1, 7, 8, 0, 7, 11, 11, 0, 0, 11, 11, 8, 0, 7, 8, 1, 7, 11, 11, 11, 11, 0, 10],
[3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 10, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 10, 10],
[3, 3, 1, 6, 4, 4, 5, 1, 6, 4, 4, 4, 5, 1, 10, 3, 1, 6, 4, 4, 4, 5, 1, 6, 4, 4, 5, 1, 10, 10],
[3, 3, 1, 7, 11, 0, 3, 1, 7, 11, 11, 11, 8, 1, 7, 8, 1, 7, 11, 11, 11, 8, 1, 10, 0, 11, 8, 1, 10, 10],
[3, 3, 2, 1, 1, 10, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 10, 3, 1, 1, 2, 10, 10],
[3, 0, 4, 5, 1, 10, 3, 1, 6, 5, 1, 6, 4, 4, 4, 4, 4, 4, 5, 1, 6, 5, 1, 10, 3, 1, 6, 4, 0, 10],
[3, 0, 11, 8, 1, 7, 8, 1, 10, 3, 1, 7, 11, 11, 0, 0, 11, 11, 8, 1, 10, 3, 1, 7, 8, 1, 7, 11, 0, 10],
[3, 3, 1, 1, 1, 1, 1, 1, 10, 3, 1, 1, 1, 1, 10, 3, 1, 1, 1, 1, 10, 3, 1, 1, 1, 1, 1, 1, 10, 10],
[3, 3, 1, 6, 4, 4, 4, 4, 0, 0, 4, 4, 5, 1, 10, 3, 1, 6, 4, 4, 0, 0, 4, 4, 4, 4, 5, 1, 10, 10],
[3, 3, 1, 7, 11, 11, 11, 11, 11, 11, 11, 11, 8, 1, 7, 8, 1, 7, 11, 11, 11, 11, 11, 11, 11, 11, 8, 1, 10, 10],
[3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 10, 10],
[3, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 10],
[0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0]
])
        self.simple_board = np.vectorize(lambda x: 1 if x < 3 or x==9 else 0)(board)
        self.simple_board = np.transpose(self.simple_board)
        self.tiles_board = pygame.sprite.Group()
        self.wall_group = pygame.sprite.Group()
        self.ghostdoor_group = pygame.sprite.Group()
        self.create_board(board)

    def create_board(self, board):
        """
        Create the game board based on the provided 2D array.

        Parameters:
        - board (numpy.ndarray): 2D array representing the game board.

        Returns:
        None
        """
        for i, row in enumerate(board):
            for j, tile_type in enumerate(row):
                x = j * 27
                y = i * 27
                tile = MapTile(x, y, tile_type)
                if tile_type < 3:
                    self.tiles_board.add(tile)
                elif tile_type == 9:
                    self.ghostdoor_group.add(tile)
                else: self.wall_group.add(tile)

    def draw_board(self, screen):
        """
        Draw the game board on the screen.

        Parameters:
        - screen (pygame.Surface): The surface to draw the game board on.

        Returns:
        None
        """
        self.tiles_board.draw(screen)
        self.wall_group.draw(screen)
        self.ghostdoor_group.draw(screen)

def apply_effect_to_tile(tile, player, game, ghosts):
    """
    Apply effects to a specific tile based on player interaction.

    Parameters:
    - tile (MapTile): The tile to apply effects to.
    - player (Pacman): The player object.
    - game (Game): The game object.
    - ghosts (list): A list of ghost objects.

    Returns:
    None
    """
    tile_type = tile.tile_type
    if tile_type == 1:
        player.score += 10
        tile.tile_type = 0
        game.remaining_coins-=1
    elif tile_type == 2:
        player.score += 50
        game.vulnerable_mode = True
        game.vulnerable_timer = 16
        tile.tile_type = 0
        for ghost in ghosts:
            ghost.freightened = True

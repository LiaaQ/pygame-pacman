"""
Ghost Module

This module defines the Ghost class hierarchy for the Pacman game.
The module also includes a Breadth-First Search (BFS) algorithm for pathfinding.

Attributes:
    tile_height (int): The height of a game tile.
    tile_width (int): The width of a game tile.

Classes:
    Ghost (pygame.sprite.Sprite): The base class for all ghosts in the game.
        - __init__: Initializes a new instance of the Ghost class.
        - move_base: The base movement logic for ghosts, overridden by specific ghost classes.
        - move_freightened: The movement logic for frightened ghosts.
        - update: Updates the ghost's position and behavior for the current frame.

    Pinky (Ghost): A class representing the Pinky ghost in the game.
        - __init__: Initializes a new instance of the Pinky class.
        - respawn: Respawns Pinky at the starting position.
        - move_base: Overrides the base movement logic for Pinky.
        - update: Updates Pinky's position and behavior for the current frame.

    Blinky (Ghost): A class representing the Blinky ghost in the game.
        - __init__: Initializes a new instance of the Blinky class.
        - respawn: Respawns Blinky at the starting position.
        - move_base: Overrides the base movement logic for Blinky.
        - move_freightened: Calls the superior class' implementation of move_freightened.
        - update: Updates Blinky's position and behavior for the current frame.

    Inky (Ghost): A class representing the Inky ghost in the game.
        - __init__: Initializes a new instance of the Inky class.
        - respawn: Respawns Inky at the starting position.
        - move_base: Overrides the base movement logic for Inky.
        - update: Updates Inky's position and behavior for the current frame.

    Clyde (Ghost): A class representing the Clyde ghost in the game.
        - __init__: Initializes a new instance of the Clyde class.
        - respawn: Respawns Clyde at the starting position.
        - move_base: Overrides the base movement logic for Clyde.
        - move_freightened: Overrides the movement logic for frightened Clyde.
        - update: Updates Clyde's position and behavior for the current frame.

Functions:
    bfs: Breadth-First Search algorithm for pathfinding.
        - Parameters:
            - simple_board (numpy.ndarray): A 2D numpy array representing the game board.
            - start (tuple): The starting position.
            - target (tuple): The target position.
        - Returns:
            - list or None: The path from start to target, or None if no path is found.

    get_neighbors: Retrieves valid neighboring positions for pathfinding.
        - Parameters:
            - current (tuple): The current position.
            - simple_board (numpy.ndarray): A 2D numpy array representing the game board.
        - Returns:
            - list: List of valid neighboring positions.
"""
from queue import SimpleQueue
from abc import ABC, abstractmethod
import random
import pygame

tile_height = 27
tile_width = 27

class Ghost(ABC, pygame.sprite.Sprite):
    """
    Ghost Class

    Represents a base ghost in the Pacman game. Specific ghost classes (Pinky, Blinky, Inky, Clyde)
    inherit from this class.

    Attributes:
        - speed (float): The movement speed of the ghost.
        - freightened (bool): Flag indicating whether the ghost is in a frightened state.
        - target_tile (tuple): The target tile position for the ghost.
        - direction (tuple): The current movement direction (x, y).
        - outside (bool): Flag indicating whether the ghost had set foot outside the ghost house.

    Methods:
        - __init__: Initializes a new instance of the Ghost class.
        - move_base: The base movement logic for ghosts, overridden by specific ghost classes.
        - move_freightened: The movement logic for frightened ghosts.
        - update: Updates the ghost's position and behavior for the current frame.
    """
    FREIGHTENED_IMAGE = pygame.image.load("Graphics/Ghosts/Vulnerable.png")
    FREIGHTENED_IMAGE = pygame.transform.scale(FREIGHTENED_IMAGE, (27,27))
    def __init__(self):
        super().__init__()
        self.speed = 1
        self.freightened = False
        self.target_tile = (15, 12)
        self.direction = (0, 0)
        self.outside = False

    @abstractmethod
    def move_base(self, wall_group=None, ghost_door=None, simple_board=None, pac_pos=None):
        """
        Base Movement Logic for Ghosts

        This method defines the base movement logic for ghosts. It is intended to be overridden
        by specific ghost classes (Pinky, Blinky, Inky, Clyde).

        Raises:
            NotImplementedError: This is an abstract method; it should be implemented in
            the derived classes.
        """
        raise NotImplementedError("move_base method must be implemented in derived classes.")

    def move_freightened(self, wall_group, ghost_door):
        """
        Movement Logic for Frightened Ghosts

        This method defines the movement logic for frightened ghosts.
        Ghost subclasses (Pinky, Blinky, Inky, Clyde) inherit it.

        Parameters:
            - wall_group (pygame.sprite.Group): The group of wall sprites.
            - ghost_door (pygame.sprite.Sprite): The sprite representing the ghost door.
        """
        original_pos = self.rect.x, self.rect.y
        self.speed = 0.8
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        while True:
            if(self.rect.centerx % tile_width == 0 and self.rect.centery % tile_height == 0):
                self.direction = random.choice(directions)
                if self.rect.center in ((14 * tile_height, 12 * tile_width), (15 * tile_height, 12 * tile_width)):
                    self.outside = True
            self.rect.x += self.direction[0] * self.speed
            self.rect.y += self.direction[1] * self.speed

            if pygame.sprite.spritecollideany(self, wall_group):
                self.rect.x, self.rect.y = original_pos
            if self.outside and pygame.sprite.spritecollideany(self, ghost_door):
                self.rect.x, self.rect.y = original_pos
            else: break

    def update(self, wall_group=None, ghost_door=None, simple_board=None, pac_pos=None):
        """
        Update Ghost Position and Behavior

        This method updates the ghost's position and behavior for the current frame.
        If the ghost walks through the teleport, position is changed.
        It is intended to be overridden by specific ghost classes (Pinky, Blinky, Inky, Clyde).
        """
        super().update(wall_group, ghost_door, simple_board, pac_pos)
        if self.rect.centerx > 800:
            self.rect.centerx = 0
        if self.rect.centerx < 0:
            self.rect.centerx = 800


class Pinky(Ghost):
    """
    Pinky Class

    Represents the Pinky ghost in the Pacman game. Pinky has unique behavior and attributes.
    Pinky is a semi-chasing ghost.

    Methods:
        - __init__: Initializes a new instance of the Pinky class.
        - respawn: Respawns Pinky at the starting position.
        - move_base: Overrides the base movement logic for Pinky.
        - update: Updates Pinky's position and behavior for the current frame.
    """
    BASIC_IMAGE = pygame.image.load("Graphics/Ghosts/Pinky.png")
    BASIC_IMAGE = pygame.transform.scale(BASIC_IMAGE, (27,27))

    def __init__(self):
        super().__init__()
        image_surf = self.BASIC_IMAGE
        self.image = image_surf
        self.rect = self.image.get_rect(center = (12*tile_width,14*tile_height))
        self.path = [(13,14), (14,14), (14,13), (14,12)]
        self.prev_centerx = 12
        self.prev_centery = 14

    def respawn(self):
        """
        Respawns Pinky at the Starting Position.
        """
        self.__init__()

    def move_base(self, wall_group=None, ghost_door=None, simple_board=None, pac_pos=None):
        """
        Overrides the Base Movement Logic for Pinky.

        This method implements Pinky's unique movement behavior.
        Pinky finds the shortest path to Pacman with BFS and travels it. When path is empty,
        it recalculates path based on Pacman's new position.

        Parameters:
            - simple_board (numpy.ndarray): A 2D numpy array representing the game board.
            - pac_pos (tuple): The current position of Pacman.
        """
        if(self.rect.centerx % tile_width == 0 and self.rect.centery % tile_height == 0): # If Pinky is in the middle of a tile
            self.prev_centerx = self.rect.centerx//27
            self.prev_centery = self.rect.centery//27
            # If there's nowhere to go anymore, calculate new path
            if self.path == []:
                self.target_tile = pac_pos
                self.path = bfs(simple_board, (self.rect.centerx // tile_width, self.rect.centery // tile_height), pac_pos)
            ## If we reached another tile from the path, delete it from the path
            elif (self.rect.centerx//27, self.rect.centery//27) == self.path[0]:
                self.path.pop(0)
        if self.path!=[]:
            self.rect.centerx += (self.path[0][0] - self.prev_centerx) * self.speed
            self.rect.centery += (self.path[0][1] - self.prev_centery) * self.speed

    def update(self, wall_group=None, ghost_door=None, simple_board=None, pac_pos=None):
        super().update()
        if self.freightened:
            self.image = self.FREIGHTENED_IMAGE
            self.speed = 0.8
            self.move_base(wall_group, ghost_door, simple_board, pac_pos)
        else:
            self.image = self.BASIC_IMAGE
            self.move_base(wall_group, ghost_door, simple_board, pac_pos)

class Blinky(Ghost):
    """
    Blinky Class

    Represents the Blinky ghost in the Pacman game.
    Blinky is a short-sighted ghost that only looks in front of him.

    Methods:
        - __init__: Initializes a new instance of the Blinky class.
        - respawn: Respawns Blinky at the starting position.
        - move_base: Overrides the base movement logic for Blinky.
        - update: Updates Blinky's position and behavior for the current frame.
    """
    BASIC_IMAGE = pygame.image.load("Graphics/Ghosts/Blinky.png")
    BASIC_IMAGE = pygame.transform.scale(BASIC_IMAGE, (27,27))

    def __init__(self):
        super().__init__()
        image_surf = self.BASIC_IMAGE
        self.image = image_surf
        self.rect = self.image.get_rect(center = (13*tile_width, 11*tile_height))
        self.outside = True
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        self.direction = random.choice(directions)

    def respawn(self):
        """
        Respawns Blinky at the Starting Position.
        """
        self.__init__()

    def move_base(self, wall_group=None, ghost_door=None, simple_board=None, pac_pos=None):
        """
        Overrides the Base Movement Logic for Blinky.

        This method implements Blinky's unique movement behavior.
        Blinky moves randomly through the maze, changing direction when hitting walls or encountering the ghost door,
        because this poor fella can't look to the sides.

        Parameters:
            - wall_group (pygame.sprite.Group): A sprite group containing wall sprites.
            - ghost_door (pygame.sprite.Group): A sprite group containing the ghost door sprite.
            - simple_board (numpy.ndarray): A 2D numpy array representing the game board.
            - pac_pos (tuple): The current position of Pacman.
        """
        original_pos = self.rect.x, self.rect.y
        self.speed = 1
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

        # When wall is hit, decide on a new direction
        while (pygame.sprite.spritecollideany(self, wall_group) or pygame.sprite.spritecollideany(self, ghost_door)):
            self.rect.x, self.rect.y = original_pos
            if(self.rect.centerx % tile_width == 0 and self.rect.centery % tile_height == 0):
                self.direction = random.choice(directions)
            self.rect.x += self.direction[0] * self.speed
            self.rect.y += self.direction[1] * self.speed

    def update(self, wall_group=None, ghost_door=None, simple_board=None, pac_pos=None):
        """
        Updates Blinky's Position and Behavior for the Current Frame.

        This method is called in each frame of the game loop to update Blinky's position and behavior.
        If Blinky is in frightened mode, it calls the move_freightened method; otherwise, it calls the move_base method.

        Parameters:
            - wall_group (pygame.sprite.Group): A sprite group containing wall sprites.
            - ghost_door (pygame.sprite.Group): A sprite group containing the ghost door sprite.
            - simple_board (numpy.ndarray): A 2D numpy array representing the game board.
            - pac_pos (tuple): The current position of Pacman.
        """
        if self.freightened:
            self.image = self.FREIGHTENED_IMAGE
            self.move_freightened(wall_group, ghost_door)
        else:
            self.image = self.BASIC_IMAGE
            self.move_base(wall_group, ghost_door, simple_board, pac_pos)
        if self.rect.centerx > 800:
            self.rect.centerx = 0
        if self.rect.centerx < 0:
            self.rect.centerx = 800

class Inky(Ghost):
    """
    Inky Class

    Represents the Inky ghost in the Pacman game. Inky has unique behavior and attributes.
    Inky is a an aggressive chasing ghost.

    Methods:
        - __init__: Initializes a new instance of the Inky class.
        - respawn: Respawns Inky at the starting position.
        - move_base: Overrides the base movement logic for Inky.
        - update: Updates Inky's position and behavior for the current frame.
    """
    BASIC_IMAGE = pygame.image.load("Graphics/Ghosts/Inky.png")
    BASIC_IMAGE = pygame.transform.scale(BASIC_IMAGE, (27,27))

    def __init__(self):
        super().__init__()
        image_surf = self.BASIC_IMAGE
        image_surf= pygame.transform.scale(image_surf, (27, 27))
        self.image = image_surf
        self.rect = self.image.get_rect(center = (14*tile_height, 14*tile_width))
        self.path = []
        self.prev_centerx = 14
        self.prev_centery = 14

    def respawn(self):
        """
        Respawns Inky at the Starting Position.
        """
        self.__init__()

    def move_base(self, wall_group=None, ghost_door=None, simple_board=None, pac_pos=None):
        """
        Overrides the Base Movement Logic for Inky.

        This method implements Inky's unique movement behavior.
        Inky uses BFS to find the shortest path to Pacman and travels it. On every center of a tile,
        it recalculates the path based on Pacman's new position.

        Parameters:
            - wall_group (pygame.sprite.Group): A sprite group containing wall sprites.
            - ghost_door (pygame.sprite.Group): A sprite group containing the ghost door sprite.
            - simple_board (numpy.ndarray): A 2D numpy array representing the game board.
            - pac_pos (tuple): The current position of Pacman.
        """
        if(self.rect.centerx % tile_width == 0 and self.rect.centery % tile_height == 0):
            self.prev_centerx = self.rect.centerx//27
            self.prev_centery = self.rect.centery//27
            self.target_tile = pac_pos
            self.path = bfs(simple_board, (self.rect.centerx // tile_width, self.rect.centery // tile_height), pac_pos)
        if self.path!=[]:
            self.rect.centerx += (self.path[0][0] - self.prev_centerx) * self.speed
            self.rect.centery += (self.path[0][1] - self.prev_centery) * self.speed
        if self.path is None:
            raise Exception("Uh oh")

    def update(self, wall_group=None, ghost_door=None, simple_board=None, pac_pos=None):
        """
        Updates Inky's Position and Behavior for the Current Frame.

        This method is called in each frame of the game loop to update Inky's position and behavior.

        Parameters:
            - wall_group (pygame.sprite.Group): A sprite group containing wall sprites.
            - ghost_door (pygame.sprite.Group): A sprite group containing the ghost door sprite.
            - simple_board (numpy.ndarray): A 2D numpy array representing the game board.
            - pac_pos (tuple): The current position of Pacman.
        """
        if self.freightened:
            self.image = self.FREIGHTENED_IMAGE
            self.speed = 0.8
            self.move_base(wall_group, ghost_door, simple_board, pac_pos)
        else:
            self.image = self.BASIC_IMAGE
            self.move_base(wall_group, ghost_door, simple_board, pac_pos)

class Clyde(Ghost):
    """
    Clyde Class

    Represents the Clyde ghost in the Pacman game. Clyde has unique behavior and attributes.
    Clyde has random and unpredictable movement with bigger chance to continue with the current direction.

    Methods:
        - __init__: Initializes a new instance of the Clyde class.
        - respawn: Respawns Clyde at the starting position.
        - move_base: Overrides the base movement logic for Clyde.
        - update: Updates Clyde's position and behavior for the current frame.
    """
    BASIC_IMAGE = pygame.image.load("Graphics/Ghosts/Clyde.png")
    BASIC_IMAGE = pygame.transform.scale(BASIC_IMAGE, (27,27))

    def __init__(self):
        super().__init__()
        image_surf = self.BASIC_IMAGE
        image_surf = pygame.transform.scale(image_surf, (27, 27))
        self.image = image_surf
        self.rect = self.image.get_rect(center = (16*tile_height,14*tile_width))
        self.direction = (1,0)

    def respawn(self):
        """
        Respawns Clyde at the Starting Position.
        """
        self.__init__()

    def move_base(self, wall_group=None, ghost_door=None, simple_board=None, pac_pos=None):
        """
        Overrides the Base Movement Logic for Clyde.

        This method implements Clyde's unique movement behavior.
        Clyde moves randomly through the maze, having better chances of continuing with the current direction.

        Parameters:
            - wall_group (pygame.sprite.Group): A sprite group containing wall sprites.
            - ghost_door (pygame.sprite.Group): A sprite group containing the ghost door sprite.
            - simple_board (numpy.ndarray): A 2D numpy array representing the game board.
            - pac_pos (tuple): The current position of Pacman.
        """
        original_pos = self.rect.x, self.rect.y
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), self.direction, self.direction, self.direction]
        while True:
            if(self.rect.centerx % tile_width == 0 and self.rect.centery % tile_height == 0):
                self.direction = random.choice(directions)
                if self.rect.center in {(14*tile_height, 12*tile_width), self.rect.center == (15*tile_height, 12*tile_width)}:
                    self.outside = True
            self.rect.centerx += self.direction[0] * self.speed
            self.rect.centery += self.direction[1] * self.speed

            if pygame.sprite.spritecollideany(self, wall_group):
                self.rect.x, self.rect.y = original_pos
            elif pygame.sprite.spritecollideany(self, ghost_door) and self.outside:
                self.rect.x, self.rect.y = original_pos
            else: break

    def update(self, wall_group=None, ghost_door=None, simple_board=None, pac_pos=None):
        """
        Updates Clyde's Position and Behavior for the Current Frame.

        This method is called in each frame of the game loop to update Clyde's position and behavior.
        If Clyde is in frightened mode, it calls the move_freightened method; otherwise, it calls the move_base method.

        Parameters:
            - wall_group (pygame.sprite.Group): A sprite group containing wall sprites.
            - ghost_door (pygame.sprite.Group): A sprite group containing the ghost door sprite.
            - simple_board (numpy.ndarray): A 2D numpy array representing the game board.
            - pac_pos (tuple): The current position of Pacman.
        """
        if self.freightened:
            self.image = self.FREIGHTENED_IMAGE
            self.move_freightened(wall_group, ghost_door)
        else:
            self.image = self.BASIC_IMAGE
            self.move_base(wall_group, ghost_door, simple_board, pac_pos)
        if self.rect.centerx > 800:
            self.rect.centerx = 0
        if self.rect.centerx < 0:
            self.rect.centerx = 800

def bfs(simple_board, start, target):
    """
    Breadth-First Search Algorithm.

    Finds the shortest path from the start position to the target position on the given game board.

    Parameters:
        - simple_board (numpy.ndarray): A 2D numpy array representing the game board - 0s for walls, 1s for paths.
        - start (tuple): The starting position for the search.
        - target (tuple): The target position to reach.

    Returns:
        - list or None: A list of positions representing the shortest path, or None if no path is found.
    """
    queue = SimpleQueue()
    visited = set()
    queue.put((start, []))

    while not queue.empty():
        current, path = queue.get()
        if current == target:
            return path

        for neighbor in get_neighbors(current, simple_board):
            if neighbor not in visited:
                queue.put((neighbor, path + [neighbor]))
                visited.add(neighbor)

    return None

def get_neighbors(current, simple_board):
    """
    Get Valid Neighbors for a Given Position on the Game Board.

    Parameters:
        - current (tuple): The current position.
        - simple_board (numpy.ndarray): A 2D numpy array representing the game board.

    Returns:
        - list: A list of valid neighboring positions.
    """
    neighbors = []
    for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        neighbor = (current[0] + direction[0], current[1] + direction[1])
        if 0 <= neighbor[0] < simple_board.shape[0] and 0 <= neighbor[1] < simple_board.shape[1] and simple_board[neighbor] == 1:
            neighbors.append(neighbor)
    return neighbors

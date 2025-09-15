"""
Pacman Game Buttons Module

This module defines two classes, Btn_Start and Btn_Stop, representing the start and stop buttons in the Pacman game menu.
These classes provide functionality for updating the buttons' appearance based on mouse interactions.

Classes:
    - Btn_Start: Represents the start button.
    - Btn_Stop: Represents the stop button.
"""
import pygame

class Btn_Start(pygame.sprite.Sprite):
    """
    Btn_Start Class

    Represents the start button in the Pacman game menu.

    Methods:
        - __init__: Initializes a new instance of the Btn_Start class.
        - image_state: Updates the button image based on the mouse position.
        - update: Updates the button's state for the current frame.
    """
    def __init__(self, width, height):
        """
        Initializes a new instance of the Btn_Start class.

        Parameters:
            - width (int): The width of the game window.
            - height (int): The height of the game window.
        """
        super().__init__()
        default_surf = pygame.image.load('Graphics/start.png').convert_alpha()
        default_surf = pygame.transform.scale(default_surf, (default_surf.get_width() // 2, default_surf.get_height() // 2))
        hover_surf = pygame.image.load('Graphics/start_hover.png').convert_alpha()
        hover_surf = pygame.transform.scale(hover_surf, (hover_surf.get_width() // 2, hover_surf.get_height() // 2))

        self.btn_start = [default_surf, hover_surf]
        self.btn_index = 0
        self.image = self.btn_start[self.btn_index]
        self.rect = self.image.get_rect(center = (width // 2, height // 2))

    def image_state(self):
        """
        Updates the button image based on the mouse position.
        """
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.btn_index = 1
        else:
            self.btn_index = 0

        self.image = self.btn_start[self.btn_index]

    def update(self):
        """
        Updates the button's state for the current frame.
        """
        self.image_state()

class Btn_Stop(pygame.sprite.Sprite):
    """
    Btn_Stop Class

    Represents the stop button in the Pacman game menu.

    Methods:
        - __init__: Initializes a new instance of the Btn_Stop class.
        - image_state: Updates the button image based on the mouse position.
        - update: Updates the button's state for the current frame.
    """
    def __init__(self, width, height):
        """
        Initializes a new instance of the Btn_Stop class.

        Parameters:
            - width (int): The width of the game window.
            - height (int): The height of the game window.
        """
        super().__init__()
        default_surf = pygame.image.load('Graphics/stop.png').convert_alpha()
        default_surf = pygame.transform.scale(default_surf, (default_surf.get_width() // 2, default_surf.get_height() // 2))
        hover_surf = pygame.image.load('Graphics/stop_hover.png').convert_alpha()
        hover_surf = pygame.transform.scale(hover_surf, (hover_surf.get_width() // 2, hover_surf.get_height() // 2))

        self.btn_stop = [default_surf, hover_surf]
        self.btn_index = 0
        self.image = self.btn_stop[self.btn_index]
        self.rect = self.image.get_rect(center = (width // 2, height // 2 + 200))

    def image_state(self):
        """
        Updates the button image based on the mouse position.
        """
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.btn_index = 1
        else:
            self.btn_index = 0

        self.image = self.btn_stop[self.btn_index]

    def update(self):
        """
        Updates the button's state for the current frame.
        """
        self.image_state()

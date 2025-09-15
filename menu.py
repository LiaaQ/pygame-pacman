"""
Pacman Game Launcher

This script initializes and launches the Pacman game, providing a graphical user interface
with start and stop buttons. It uses the Pygame library for graphics and input handling.

Dependencies:
- Pygame: A cross-platform set of Python modules designed for writing video games.

Usage:
Run this script to launch the Pacman game. It displays a simple GUI with start and stop buttons.
Clicking the start button initializes a new game, while clicking the stop button exits the program.
"""
import sys
import pygame
from GUI import button
from game import Game

def main():
    """
    Displays the menu of the Pacman game and starts it when the start button is clicked.
    """
    pygame.init()
    pygame.mixer.init()

    # SCREEN SETUP
    WIDTH = 795
    HEIGHT = 900
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Pacman')
    clock = pygame.time.Clock()

    logo_surf = pygame.image.load('Graphics/pacman_2013.png').convert_alpha()
    background_surf = pygame.image.load('Graphics/background.jpg').convert()

    # Scale them to a smaller size
    logo_surf = pygame.transform.scale(logo_surf, (logo_surf.get_width() // 2, logo_surf.get_height() // 2))
    background_surf = pygame.transform.scale(background_surf, (1.7*background_surf.get_width() // 2, 1.7*background_surf.get_height() // 2))

    logo_rect = logo_surf.get_rect(midtop = (WIDTH // 2, 50))
    music = pygame.mixer.Sound('Music/Pacman_mid.mp3')
    music.play(-1)

    buttons = pygame.sprite.Group()
    buttons.add(button.Btn_Start(WIDTH, HEIGHT), button.Btn_Stop(WIDTH, HEIGHT))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for btn in buttons:
                    if isinstance(btn, button.Btn_Start) and btn.rect.collidepoint(event.pos):
                        new_game = Game()
                        music.stop()
                        new_game.run_game(screen, clock)
                        music.play(-1)
                    elif isinstance(btn, button.Btn_Stop) and btn.rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

        screen.blit(background_surf, (-80,-10))
        screen.blit(logo_surf, logo_rect)
        buttons.draw(screen)
        buttons.update()
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()

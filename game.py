"""
Pacman Game Module

This module contains the main game logic for the Pacman game, including the Game class
that manages the game loop, player input, and overall game state. It also includes
functions for rendering win and lose messages.

Classes:
- Game: Manages the main game loop, player input, and game state.
- Pacman: Represents the player-controlled character.
- Pinky, Blinky, Inky, Clyde: Subclasses of Ghost representing different ghost characters.
- Map: Represents the game map and tiles.

Functions:
- win_render(screen): Renders a victory message on the screen.
- lose_render(screen): Renders a defeat message on the screen.

Usage:
This module is intended to be run as the main script to start the Pacman game.
"""
from math import inf
import sys
import pygame
from Players.pacman import Pacman
from Players.ghost import Pinky, Blinky, Inky, Clyde
from Tiles.map import Map
from Tiles.map import apply_effect_to_tile

class Game():
    """
    Class representing the main game logic and loop.

    Attributes:
    - player: Instance of the Pacman class.
    - map: Instance of the Map class.
    - vulnerable_mode: Boolean indicating if ghosts are in a vulnerable state.
    - vulnerable_timer: Countdown timer for the vulnerable state.
    - remaining_coins: Number of coins remaining in the game.
    - ghosts: List containing instances of Ghosts (Pinky, Blinky, Inky, Clyde).

    Methods:
    - run_game(screen, clock): Main game loop that handles user input, updates game state, and renders the game.
    - effects(last_time, ghost_group): Handles collision effects, power-ups, and updates timers.
    - closest_ghost_distance(self): Calculates distance between Pacman and the closest ghost.
    - choose_music(self): Changes the song based on the ghost and Pacman distance.
    - update_players(pacman_icon_idx): Updates player and ghosts based on the game state.
    - draw_elements(screen, pacman, ghost): Renders the game elements on the screen.
    - render_text(screen): Renders text displaying score, remaining coins, frightened timer, and lives.
    """
    def __init__(self):
        pygame.mixer.init()
        MUSIC_CLOSEST = pygame.mixer.Sound('Music/Pacman_closest.mp3')
        MUSIC_MID = pygame.mixer.Sound('Music/Pacman_mid.mp3')
        MUSIC_FAR = pygame.mixer.Sound('Music/Pacman_far.mp3')
        MUSIC_VULNERABLE = pygame.mixer.Sound('Music/Pacman_vulnerable.mp3')
        self.music = [MUSIC_CLOSEST, MUSIC_MID, MUSIC_FAR, MUSIC_VULNERABLE]
        for track in self.music:
            track.play(-1)
        MUSIC_CLOSEST.set_volume(0)
        MUSIC_FAR.set_volume(0)
        MUSIC_VULNERABLE.set_volume(0)
        self.player = Pacman()
        self.map = Map()
        self.vulnerable_mode = False
        self.vulnerable_timer = 0
        self.remaining_coins = 242
        self.ghosts = [Pinky(), Blinky(), Inky(), Clyde()]

    def run_game(self, screen, clock):
        """
        Main game loop that handles user input, updates game state, and renders the game.

        Parameters:
        - screen: Pygame display surface.
        - clock: Pygame Clock object.
        """
        pacman = pygame.sprite.GroupSingle()
        pacman.add(self.player)
        ghost = pygame.sprite.Group()
        ghost.add(self.ghosts)

        last_time = pygame.time.get_ticks()
        pacman_icon_idx = 0
        win = False

        # Game Loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.player.change_direction(event)

            self.update_players(pacman_icon_idx)
            last_time = self.effects(last_time, ghost)
            self.draw_elements(screen, pacman, ghost)
            self.choose_music()
            pygame.display.update()
            clock.tick(60)

            if pacman_icon_idx < 19:
                pacman_icon_idx += 1
            else: pacman_icon_idx = 0

            if self.remaining_coins == 0:
                win = True
                break

            if self.player.lives == 0:
                break

        pygame.display.update()

        if win:
            self.win_render(screen)
            return True
        self.lose_render(screen)
        return False

    def effects(self, last_time, ghost_group):
        """
        Handles collision effects, power-ups, and updates timers.

        Parameters:
        - last_time: Last recorded time in milliseconds.
        - ghost_group: Pygame sprite Group containing ghost instances.

        Returns:
        - Updated last_time.
        """
        collided_ghosts = pygame.sprite.spritecollide(self.player, ghost_group, False)

        if collided_ghosts:
            for ghost in collided_ghosts:
                if ghost.freightened:
                    self.player.score += 100
                    ghost.respawn()
                else:
                    self.player.respawn()

        # Coins and Powerups picking
        current_tile = pygame.sprite.spritecollide(self.player, self.map.tiles_board, False)
        for tile in current_tile:
            apply_effect_to_tile(tile, self.player, self, self.ghosts)
            tile.update()

        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - last_time

        if elapsed_time >= 1000:
            if self.vulnerable_mode:
                self.vulnerable_timer -= 1
                last_time = current_time

        if self.vulnerable_timer == 0:
            self.vulnerable_mode = False
            for tmp_ghost in self.ghosts:
                tmp_ghost.freightened = False
                tmp_ghost.speed = 1

        return last_time

    def closest_ghost_distance(self):
        """
        Calculates the Manhattan distance to the closest ghost.

        Returns:
        - int: The Manhattan distance to the closest ghost.
        """
        pacman_position = self.player.rect.topleft
        closest_distance = inf

        for ghost in self.ghosts:
            ghost_position = ghost.rect.topleft
            distance = abs(pacman_position[0] - ghost_position[0]) + abs(pacman_position[1] - ghost_position[1])
            closest_distance = min(closest_distance, distance)

        return closest_distance

    def choose_music(self):
        """
        Chooses which music track to play based on the ghosts proximities.
        """
        closest_distance = self.closest_ghost_distance()
        if self.vulnerable_mode:
            self.music[0].set_volume(0)
            self.music[1].set_volume(0)
            self.music[2].set_volume(0)
            self.music[3].set_volume(1)
        elif closest_distance < 100:
            self.music[0].set_volume(1)
            self.music[1].set_volume(0)
            self.music[2].set_volume(0)
            self.music[3].set_volume(0)
        elif closest_distance < 300:
            self.music[0].set_volume(0)
            self.music[1].set_volume(1)
            self.music[2].set_volume(0)
            self.music[3].set_volume(0)
        else:
            self.music[0].set_volume(0)
            self.music[1].set_volume(0)
            self.music[2].set_volume(1)
            self.music[3].set_volume(0)

    def update_players(self, pacman_icon_idx):
        """
        Updates player and ghost positions based on the game state.

        Parameters:
        - pacman_icon_idx: Index of the Pacman icon for animation.
        """
        current_tile = pygame.sprite.spritecollide(self.player, self.map.tiles_board, False)
        # Pacman can return collision with multiple tiles at once. Make sure we return one that isn't a wall.
        for tile in current_tile:
            if tile.tile_type < 3:
                pac_pos = (tile.rect.centerx // 27, tile.rect.centery // 27)
                break
        self.player.update(pacman_icon_idx, self.map.wall_group, self.map.ghostdoor_group)
        for tmp_ghost in self.ghosts:
            tmp_ghost.update(wall_group=self.map.wall_group, ghost_door=self.map.ghostdoor_group, simple_board=self.map.simple_board, pac_pos=pac_pos)

    def draw_elements(self, screen, pacman, ghost):
        """
        Renders the game elements on the screen.

        Parameters:
        - screen: Pygame display surface.
        - pacman: Pygame sprite Group containing the Pacman instance.
        - ghost: Pygame sprite Group containing the ghost instances.
        """
        screen.fill('black')
        self.map.draw_board(screen)
        pacman.draw(screen)
        ghost.draw(screen)
        self.render_text(screen)

    def render_text(self, screen):
        """
        Renders text displaying score, remaining coins, frightened timer, and lives.

        Parameters:
        - screen: Pygame display surface.
        """
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.player.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 860))
        remaining_text = font.render(f"Remaining: {self.remaining_coins}", True, (255, 255, 255))
        screen.blit(remaining_text, (300, 860))
        vulnerable_text = font.render(f"Frightened: {self.vulnerable_timer}", True, (255, 255, 255))
        screen.blit(vulnerable_text, (620, 860))
        lives_text = font.render(f"Lives: {self.player.lives}", True, (255, 255, 255))
        screen.blit(lives_text, (13*27, 15.1*27))

    def win_render(self, screen):
        """
        Renders the win text.

        Parameters:
        - screen: Pygame display surface.
        """
        font = pygame.font.Font(None, 36)
        win_text = font.render("YOU WON!", True, (255,255,255))
        screen.blit(win_text, (12*27, 13.4*27))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    for track in self.music:
                        track.stop()
                    return

    def lose_render(self, screen):
        """
        Renders the lose text.

        Parameters:
        - screen: Pygame display surface.
        """
        font = pygame.font.Font(None, 36)
        lose_text = font.render("YOU LOST!", True, (255,255,255))
        screen.blit(lose_text, (12*27, 13.4*27))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    for track in self.music:
                        track.stop()
                    return

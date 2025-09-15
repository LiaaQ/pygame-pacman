from unittest.mock import patch
import pytest
import inspect
import pygame
from pylint.lint import Run
from pylint.reporters import CollectingReporter
from Players.pacman import Pacman
from Players.ghost import Ghost, Pinky, Blinky, Inky, Clyde
from game import Game
from GUI.button import Btn_Start, Btn_Stop
from Tiles.map import Map
from Tiles.maptile import MapTile
import menu

pygame.init()
pygame.display.set_mode((795, 900))
screen = pygame.display.set_mode((795, 900))
clock = pygame.time.Clock()

@pytest.fixture
def pacman():
    return Pacman()

@pytest.fixture
def ghost():
    return Ghost()

@pytest.fixture
def ghost(request):
    ghost_class = request.param
    with patch('pygame.sprite.spritecollideany', return_value=False):
        return ghost_class()

@pytest.fixture
def btn_start():
    return Btn_Start(795, 900)

@pytest.fixture
def btn_stop():
    return Btn_Stop(795, 900)

@pytest.fixture
def map():
    return Map()

@pytest.fixture
def game():
    return Game()

"""
INIT TESTING
"""
def test_pacman_initialization(pacman):
    assert isinstance(pacman, Pacman)
    assert pacman.lives == 3
    assert pacman.score == 0

@pytest.mark.parametrize("ghost", [Pinky, Inky, Blinky, Clyde], indirect=True)
def test_ghost_initialization(ghost):
    assert isinstance(ghost, Ghost)
    assert ghost.freightened == False

def test_button_initialization(btn_start, btn_stop):
    assert isinstance(btn_start, Btn_Start)
    assert isinstance(btn_stop, Btn_Stop)

"""
PYLINT TESTING
"""
@pytest.fixture(scope="session", params=[Pacman, Ghost, Map, MapTile, Btn_Start, Game, menu])
def linter(request):
    """ Test codestyle for src file of render_tree function. """
    src_file = inspect.getfile(request.param)
    rep = CollectingReporter()
    # disabled warnings:
    # 0301 line too long
    # 0103 variables name (does not like shorter than 2 chars)
    # E1101 Module 'pygame' has no '...' member
    r = Run(['--disable=C0301,C0103,E1101 ', '-sn', src_file], reporter=rep, exit=False)
    return r.linter

@pytest.mark.parametrize("limit", [10])
def test_codestyle_score(linter, limit):
    """ Evaluate if codestyle rating is 10 """
    score = linter.stats.global_note
    print(f'pylint score = {score} limit = {limit}')
    assert score >= limit

"""
PACMAN TESTING
Directions:
0 - RIGHT
1 - LEFT
2 - UP
3 - DOWN
"""
# Tests if direction changes correctly by pressing keys
@pytest.mark.parametrize("key, expected_direction", [
    (pygame.K_UP, 2),    # UP key should set direction to 2
    (pygame.K_DOWN, 3),  # DOWN key should set direction to 3
    (pygame.K_LEFT, 1),  # LEFT key should set direction to 1
    (pygame.K_RIGHT, 0), # RIGHT key should set direction to 0
    (pygame.K_SPACE, None)  # Invalid key should not change direction
])
def test_change_direction(pacman, key, expected_direction):
    event = pygame.event.Event(pygame.KEYDOWN, key=key)
    pacman.change_direction(event)
    if expected_direction is not None:
        assert pacman.direction == expected_direction
    else:
        # If the key is invalid, direction should remain the same
        assert pacman.direction != expected_direction

# Tests if Pacman stops before a wall
def test_pacman_collision(pacman):
    wall = pygame.sprite.Sprite()
    wall.rect = pygame.Rect(20, 0, 27, 27)
    wall_group = pygame.sprite.Group()
    wall_group.add(wall)
    ghostdoor_group = pygame.sprite.Group()
    pacman.rect = pygame.Rect(0, 0, 20, 20)
    pacman.move(wall_group, ghostdoor_group)
    assert pacman.rect.topleft == (0,0)

# Tests if Pacman moves in the right direction
@pytest.mark.parametrize("direction, expected_change", [
    (1, lambda initial, current: current[0] < initial[0]),  # LEFT
    (0, lambda initial, current: current[0] > initial[0]),  # RIGHT
    (2, lambda initial, current: current[1] < initial[1]),  # UP
    (3, lambda initial, current: current[1] > initial[1]),  # DOWN
])
def test_pacman_move_direction(pacman, direction, expected_change):
    initial_position = pacman.rect.topleft
    pacman.direction = direction
    wall_group = pygame.sprite.Group()
    ghostdoor_group = pygame.sprite.Group()
    pacman.move(wall_group, ghostdoor_group)
    assert pacman.rect.topleft != initial_position
    assert expected_change(initial_position, pacman.rect.topleft)

# Checks if pacman's lives are lessened when it died
def test_respawn_lives(pacman):
    initial_lives = pacman.lives
    pacman.respawn()
    assert pacman.lives == initial_lives-1

"""
GHOSTS TESTING
"""
# Checks if ghost moves in the frightened mode
@pytest.mark.parametrize("ghost", [Pinky, Inky, Blinky, Clyde], indirect=True)
def test_ghost_move_freightened(ghost):
    print(type(ghost))
    wall_group = pygame.sprite.Group()
    ghost_door = pygame.sprite.Group()
    ghost_door.rect = pygame.Rect(0, 0, 27, 27)

    original_pos = ghost.rect.topleft
    ghost.move_freightened(wall_group, ghost_door)
    assert ghost.rect.topleft != original_pos

# Checks if ghost moves when using the base move
@pytest.mark.parametrize("ghost", [Pinky, Blinky, Inky, Clyde], indirect=True)
def test_ghost_move_base(ghost, map, pacman):
    initial_position = ghost.rect.topleft
    ghost.move_base(map.wall_group, map.ghostdoor_group, map.simple_board, (pacman.rect.centerx//27, pacman.rect.centery//27))
    assert initial_position != ghost.rect.topleft

# Checks if Ghost has a frightened render when frightened
@pytest.mark.parametrize("ghost", [Pinky, Blinky, Inky, Clyde], indirect=True)
def test_frightened(ghost, map, pacman):
    ghost.vulnerable = True
    ghost.update(map.wall_group, map.ghostdoor_group, map.simple_board, (pacman.rect.centerx//27, pacman.rect.centery//27))
    assert str(ghost.image) == str(Ghost.FREIGHTENED_IMAGE)

# Checks if Ghost has its normal render image when not frightened
@pytest.mark.parametrize("ghost", [Pinky, Blinky, Inky, Clyde], indirect=True)
def test_basic(ghost, map, pacman):
    ghost.vulnerable = False
    ghost.update(map.wall_group, map.ghostdoor_group, map.simple_board, (pacman.rect.centerx//27, pacman.rect.centery//27))
    assert str(ghost.image) == str(ghost.BASIC_IMAGE)

# Checks if Ghost is no longer frightened after reviving
@pytest.mark.parametrize("ghost", [Pinky, Blinky, Inky, Clyde], indirect=True)
def test_ghost_respawn(ghost):
    ghost.respawn()
    assert ghost.freightened == False

"""
GAME TESTING
"""
# Check if players lives lessen after colliding with a ghost
def test_ghost_collision(game):
    ghost = Pinky()
    ghost.rect.x, ghost.rect.y = (0,0)
    ghost_group = pygame.sprite.Group()
    ghost_group.add(ghost)
    last_time = 1000
    game.player.rect.x, game.player.rect.y = (0,0)
    game.effects(last_time, ghost_group)
    assert game.player.lives == 2

# Checks if player gets 100 score when colliding with a frightened ghost
def test_ghost_collision_vulnerable(game):
    ghost = Pinky()
    ghost.rect.x, ghost.rect.y = (0,0)
    ghost.freightened = True
    ghost_group = pygame.sprite.Group()
    ghost_group.add(ghost)
    last_time = 1000
    game.player.rect.x, game.player.rect.y = (0,0)
    game.effects(last_time, ghost_group)
    assert game.player.score == 100

# Checks if music is set to vulnerable when the game is in vulnerable mode
def test_music_vulnerable(game):
    game.vulnerable_mode = True
    game.choose_music()
    assert game.music[3].get_volume() == 1.0

# Checks if music is set to closest if ghost is very near
def test_music_closest(game):
    game.ghosts = []
    ghost = Pinky()
    ghost.rect.x, ghost.rect.y = (0,0)
    game.ghosts = [ghost]
    game.player.rect.x, game.player.rect.y = (1,0)
    game.choose_music()
    assert game.music[0].get_volume() == 1.0

# Tests ghost distance function
def test_ghost_distance(game):
    game.ghosts = []
    ghost = Pinky()
    ghost.rect.x, ghost.rect.y = (0,0)
    game.ghosts = [ghost]
    game.player.rect.x, game.player.rect.y = (1,0)
    assert game.closest_ghost_distance() == 1
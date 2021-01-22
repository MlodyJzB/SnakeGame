from game import Game
from run_snake_game import win1_set_up, win2_set_up
from snake import Snake
import curses


def test_game_init():
    snake = Snake([(10, 3), (10, 2)])
    win1 = win1_set_up
    win2 = win2_set_up
    game = Game(snake, win1, win2)
    assert game.quit_keys == (113, 81)
    assert game.move_keys == (curses.KEY_RIGHT,
                              curses.KEY_LEFT,
                              curses.KEY_UP,
                              curses.KEY_DOWN)
    assert game.all_keys == game.quit_keys + game.move_keys
    assert game.super_fruit is False
    assert game.key is None
    assert game.snake == snake
    assert game.win1 == win1
    assert game.win2 == win2
    assert game.walls == []
    assert game.ghost_coords == []
    assert game.fruits == []
    assert game.super_fruits == []
    assert game.poisoned_fruits == []
    assert game.removed_coords == []


def test_game_init_with_args():
    snake = Snake([(10, 3), (10, 2)])
    win1 = win1_set_up
    win2 = win2_set_up
    walls = [(10, 10)]
    fruits = [(11, 11)]
    super_fruits = [(12, 12)]
    poisoned_fruits = [(13, 13)]
    game = Game(snake, win1, win2, walls, fruits, super_fruits,
                poisoned_fruits)
    assert game.quit_keys == (113, 81)
    assert game.move_keys == (curses.KEY_RIGHT,
                              curses.KEY_LEFT,
                              curses.KEY_UP,
                              curses.KEY_DOWN)
    assert game.all_keys == game.quit_keys + game.move_keys
    assert game.super_fruit is False
    assert game.key is None
    assert game.snake == snake
    assert game.win1 == win1
    assert game.win2 == win2
    assert game.walls == walls
    assert game.ghost_coords == []
    assert game.fruits == fruits
    assert game.super_fruits == super_fruits
    assert game.poisoned_fruits == poisoned_fruits
    assert game.removed_coords == []


def test_game_spawn_object():
    snake = Snake([(10, 3), (10, 2)])
    win1 = win1_set_up
    win2 = win2_set_up
    game = Game(snake, win1, win2)
    assert game.fruits == []

    game.spawn_object(game.fruits)
    new_fruit = game.fruits[0]

    assert len(game.fruits) == 1
    assert type(new_fruit) == tuple
    assert len(new_fruit) == 2
    assert 0 < new_fruit[0] < 58
    assert 0 < new_fruit[1] < 18


def test_game_spawn_object_monkeypatch(monkeypatch):
    snake = Snake([(10, 3), (10, 2)])
    win1 = win1_set_up
    win2 = win2_set_up
    game = Game(snake, win1, win2)

    def return1(f, t):
        return 1
    monkeypatch.setattr('game.randint', return1)

    game.spawn_object(game.super_fruits)
    assert game.super_fruits[0] == (1, 1)


def test_game_spawn_object_monkeypatch2(monkeypatch):
    snake = Snake([(10, 3), (10, 2)])
    win1 = win1_set_up
    win2 = win2_set_up
    game = Game(snake, win1, win2)

    def return2(f, t):
        return 2
    monkeypatch.setattr('game.randint', return2)

    game.spawn_object(game.fruits)
    assert len(game.fruits) == 0

from snake import Snake
from run_snake_game import win1_set_up, win2_set_up
from game import Game
import curses


def test_snake_init():
    snake = Snake([(1, 7), (2, 7)])
    assert snake.coords == [(1, 7), (2, 7)]
    assert snake.score == 0
    assert snake.ghost_mode is False
    assert snake.ghost_start_time == 0
    assert snake.sign == '+'
    assert snake.is_alive is True


def test_snake_new_head_left():
    snake = Snake([(1, 7), (2, 7)])
    key = curses.KEY_LEFT
    assert snake.new_head(key) == (1, 7)


def test_snake_newhead__up():
    snake = Snake([(1, 7), (2, 7)])
    key = curses.KEY_UP
    assert snake.new_head(key) == (2, 6)


def test_snake_new_head_up_off_map():
    snake = Snake([(2, 2), (2, 1)])
    key = curses.KEY_UP
    assert snake.new_head(key) == (2, 17)


def test_snake_new_head_down_off_map():
    snake = Snake([(2, 16), (2, 17)])
    key = curses.KEY_DOWN
    assert snake.new_head(key) == (2, 1)


def test_snake_new_head_right_off_map():
    snake = Snake([(56, 7), (57, 7)])
    key = curses.KEY_RIGHT
    assert snake.new_head(key) == (1, 7)


def test_snake_new_head_left_off_map():
    snake = Snake([(2, 7), (1, 7)])
    key = curses.KEY_LEFT
    assert snake.new_head(key) == (57, 7)


def test_snake_move_up():
    snake = Snake([(10, 10), (9, 10)])
    win1 = win1_set_up
    win2 = win2_set_up
    game = Game(snake, win1, win2)
    game.key = curses.KEY_UP
    snake.move(game)
    assert snake.coords == [(9, 10), (9, 9)]
    assert game.removed_coords == [(10, 10)]


def test_snake_move_right_off_map():
    snake = Snake([(56, 7), (57, 7)])
    win1 = win1_set_up
    win2 = win2_set_up
    game = Game(snake, win1, win2)
    game.key = curses.KEY_RIGHT
    snake.move(game)
    assert snake.coords == [(57, 7), (1, 7)]
    assert game.removed_coords == [(56, 7)]


def test_snake_move_down_fruits():
    snake = Snake([(10, 10), (9, 10)])
    win1 = win1_set_up
    win2 = win2_set_up
    fruits = [(9, 11)]
    game = Game(snake, win1, win2, fruits=fruits)
    game.key = curses.KEY_DOWN
    snake.move(game)
    assert snake.coords == [(10, 10), (9, 10), (9, 11)]
    assert game.removed_coords == []


def test_snake_move_up_fruits_not_on_road():
    snake = Snake([(10, 10), (9, 10)])
    win1 = win1_set_up
    win2 = win2_set_up
    fruits = [(10, 10)]
    game = Game(snake, win1, win2, fruits)
    game.key = curses.KEY_UP
    snake.move(game)
    assert snake.coords == [(9, 10), (9, 9)]
    assert game.removed_coords == [(10, 10)]


def test_snake_move_down_ghost_mode(monkeypatch):
    snake = Snake([(10, 10), (9, 10)])
    win1 = win1_set_up
    win2 = win2_set_up
    game = Game(snake, win1, win2)
    game.ghost_coords = [(9, 11)]
    game.key = curses.KEY_DOWN

    def return1():
        return 1
    monkeypatch.setattr('snake.time', return1)

    snake.move(game)
    assert snake.coords == [(9, 10), (9, 11)]
    assert snake.ghost_mode is True
    assert game.removed_coords == [(10, 10)]
    assert snake.ghost_start_time == 1


def test_snake_move_up_super_fruits():
    snake = Snake([(10, 10), (9, 10)])
    win1 = win1_set_up
    win2 = win2_set_up
    super_fruits = [(9, 9)]
    game = Game(snake, win1, win2, super_fruits=super_fruits)
    game.key = curses.KEY_UP

    snake.move(game)

    assert snake.coords == [(10, 10), (9, 10), (9, 9)]
    assert game.removed_coords == []
    assert game.super_fruit is True

    snake.move(game)

    assert snake.coords == [(10, 10), (9, 10), (9, 9), (9, 8)]
    assert game.removed_coords == []
    assert game.super_fruit is False

    snake.move(game)

    assert snake.coords == [(9, 10), (9, 9), (9, 8), (9, 7)]
    assert game.removed_coords == [(10, 10)]
    assert game.super_fruit is False


def test_snake_move_up_super_fruits__off_map():
    snake = Snake([(10, 3), (10, 2)])
    win1 = win1_set_up
    win2 = win2_set_up
    super_fruits = [(10, 1)]
    game = Game(snake, win1, win2, super_fruits=super_fruits)
    game.key = curses.KEY_UP

    snake.move(game)

    assert snake.coords == [(10, 3), (10, 2), (10, 1)]
    assert game.removed_coords == []
    assert game.super_fruit is True

    snake.move(game)

    assert snake.coords == [(10, 3), (10, 2), (10, 1), (10, 17)]
    assert game.removed_coords == []
    assert game.super_fruit is False

    snake.move(game)

    assert snake.coords == [(10, 2), (10, 1), (10, 17), (10, 16)]
    assert game.removed_coords == [(10, 3)]
    assert game.super_fruit is False


def test_snake_choose_sign():
    snake = Snake([(10, 3)])
    assert snake.sign == '+'

    snake.ghost_mode = True
    assert snake.sign == '+'

    snake.choose_sign()
    assert snake.sign == '*'

    snake.ghost_mode = False
    assert snake.sign == '*'

    snake.choose_sign()
    assert snake.sign == '+'

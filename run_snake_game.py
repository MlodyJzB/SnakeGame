import curses
import os
from time import time
from random import randint
from load_map import Map, InvalidMapError, InvalidSnakeError
from pathlib import Path
from settings import Settings
from game import Game
from snake import Snake


def win1_set_up():
    height = 19
    width = 59
    win1 = curses.newwin(height, width)
    win1.keypad(True)
    win1.border(0)
    win1.nodelay(True)
    return win1


def win2_set_up():
    heigth2 = 11
    width2 = 59
    win2 = curses.newwin(heigth2, width2, 19, 0)
    win2.addstr(2, 2, '-'*55)

    # left side
    win2.addstr(1, 2, 'Score: 0')
    win2.addstr(3, 2, 'O - food')
    win2.addstr(4, 2, 'S - super food')
    win2.addstr(5, 2, '0 - poisoned food')
    win2.addstr(6, 2, '# - wall')
    win2.addstr(7, 2, 'G - ghost mode')
    win2.addstr(9, 2, 'Press "Q" to quit')

    # right side
    win2.addstr(1, 43, 'Ghost ends in:  ')

    return win2


def terminal_game_config():
    os.system('clear')
    curses.initscr()
    curses.noecho()
    curses.curs_set(False)


def terminal_default_config():
    curses.endwin()
    curses.echo()
    curses.curs_set(True)


def main():
    # settings
    settings_path = Path(__file__).parent / "settings.json"
    settings = Settings(settings_path)
    do_change_settings = None
    while do_change_settings not in ['Y', 'y', 'N', 'n', '']:
        do_change_settings = input('Do you want to change settings?[y/N]: ')
    if do_change_settings in ['Y', 'y']:
        map_num = None
        speed = 'nothing'
        ghost_mode_time = 'nothing'
        super_food_probability = 'nothing'
        poisoned_food_probability = 'nothing'

        while map_num not in ['1', '2', '3', '4', '5', '6', 'custom']:
            map_num = input('Choose map from 1 to 6 or "custom": ')

        while not speed.isdigit() or int(speed) not in range(1, 11):
            speed = input('Choose speed from 1 to 10 (fast - slow): ')

        while (not ghost_mode_time.isdigit() or
                int(ghost_mode_time) not in range(1, 31)):
            ghost_mode_time = input('Choose ghost mode time from 1 to 30: ')

        while (not super_food_probability.isdigit() or
                int(super_food_probability) not in range(1, 11)):
            msg = 'Choose super food probability from 1 to 10 (often - rare): '
            super_food_probability = input(msg)

        while (not poisoned_food_probability.isdigit() or
                int(poisoned_food_probability) not in range(1, 11)):
            msg = 'Choose poisoned food probability \
from 1 to 10 (often - rare): '
            poisoned_food_probability = input(msg)
        settings.write_to_json(map_num,
                               speed,
                               ghost_mode_time,
                               super_food_probability,
                               poisoned_food_probability)
    settings.load()

    # map
    map_path = Path(__file__).parent / settings.map_path
    map = Map(map_path)

    # terminal config
    terminal_game_config()

    # window1 - snake movement
    win1 = win1_set_up()

    # window2 - score and info window
    win2 = win2_set_up()

    # snake, fruits
    snake = Snake(map.snake_coords)
    walls = map.walls
    game = Game(snake, win1, win2, walls)
    fruits = game.fruits
    poisoned_fruits = game.poisoned_fruits
    super_fruits = game.super_fruits
    ghost_coords = game.ghost_coords

    # game loop
    while (game.key not in game.quit_keys) and snake.is_alive:

        # windows params
        game.win1.timeout(settings.speed)
        prev_key = game.key
        game.key = game.win1.getch()
        game.win2.refresh()
        if game.key not in game.all_keys:
            game.key = prev_key

        # spawning/clearing fruits etc
        game.spawn_object(fruits)

        game.spawn_object(super_fruits, settings.super_food_probability)

        game.spawn_object(poisoned_fruits, settings.poisoned_food_probability)

        if len(game.walls) > 0:
            game.spawn_object(ghost_coords, 350)

        clear_super_fruits_probability = 350
        clear_poisoned_fruits_probability = 400
        rand_int1 = randint(0, clear_super_fruits_probability)
        rand_int2 = randint(0, clear_poisoned_fruits_probability)

        if rand_int1 == 0:
            game.removed_coords += super_fruits
            super_fruits.clear()

        if rand_int2 == 0:
            game.removed_coords += poisoned_fruits
            poisoned_fruits.clear()

        # snake movement
        snake.move(game)

        # displaying snake and fruits
        snake.choose_sign()
        game.display_object_list(game.removed_coords, ' ')
        game.display_object_list(game.walls, '#')
        game.display_object_list(fruits, 'O')
        game.display_object_list(super_fruits, 'S')
        game.display_object_list(poisoned_fruits, '0')
        game.display_object_list(ghost_coords, 'G')
        game.display_object_list(snake.coords, snake.sign)

        game.removed_coords.clear()

        # displaying ghost mode end time
        ghost_time = settings.ghost_mode_time
        ghost_time_difference = (time() - snake.ghost_start_time)

        if ghost_time_difference > ghost_time:
            snake.ghost_mode = False

        if 3 > ghost_time - ghost_time_difference > 0:
            win2.addch(1, 58, str(ghost_time - int(ghost_time_difference)))

        else:
            win2.addch(1, 58, ' ')
        # displaying score
        snake.count_score()
        win2.addstr(1, 9, str(snake.score))

    # game over loop
    while game.key not in game.quit_keys:
        game.win1.timeout(400)
        game.key = game.win1.getch()
        game.over()

    # Default terminal configuration
    terminal_default_config()


if __name__ == "__main__":
    try:
        main()
    except InvalidMapError as e:
        print('MAP ERROR: ', end='')
        print(e)
    except InvalidSnakeError as e:
        print('MAP ERROR: ', end='')
        print(e)

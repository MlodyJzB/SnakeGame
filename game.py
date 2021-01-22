import curses
from random import randint


class Game():
    def __init__(self, snake, win1, win2, walls=None,
                 fruits=None, super_fruits=None, poisoned_fruits=None):
        q_button = 113
        Q_button = 81
        self.quit_keys = (q_button, Q_button)
        self.move_keys = (curses.KEY_RIGHT,
                          curses.KEY_LEFT,
                          curses.KEY_UP,
                          curses.KEY_DOWN)
        self.all_keys = self.quit_keys + self.move_keys
        self.super_fruit = False
        self.key = None
        self.snake = snake
        self.win1 = win1
        self.win2 = win2
        self.walls = walls if walls else []
        self.ghost_coords = []
        self.fruits = fruits if fruits else []
        self.super_fruits = super_fruits if super_fruits else []
        self.poisoned_fruits = poisoned_fruits if poisoned_fruits else []
        self.removed_coords = []

    def display_object_list(self, listing, sign):
        for x, y in listing:
            self.win1.addch(y, x, sign)

    def spawn_object(self, object_list, probability=1, max_len=1):
        rand_int = randint(1, probability)
        object_coords = None

        if rand_int == 1 and len(object_list) < max_len:
            min_x = 1
            max_x = 57
            min_y = 1
            max_y = 17
            non_empty_coords = (self.snake.coords + self.fruits +
                                self.super_fruits + self.poisoned_fruits +
                                self.walls + self.ghost_coords +
                                [object_coords])
            while (object_coords in non_empty_coords):
                object_x = randint(min_x, max_x)
                object_y = randint(min_y, max_y)
                object_coords = (object_x, object_y)
        if object_coords:
            object_list.append(object_coords)

    def over(self):
        self.win1.addstr(0, 25, 'GAME-OVER')
        self.win1.addstr(18, 25, 'GAME-OVER')
        shift = 0
        for ch in 'GAME|OVER':
            self.win1.addstr(5 + shift, 0, ch)
            shift += 1
        shift = 0
        for ch in 'GAME|OVER':
            self.win1.addstr(5 + shift, 58, ch)
            shift += 1

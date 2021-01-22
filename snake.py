import curses
from time import time


class Snake():
    def __init__(self, coords):
        self.coords = coords
        self.score = 0
        self.ghost_mode = False
        self.ghost_start_time = 0
        self.sign = '+'
        self.is_alive = True

    def new_head(self, key):
        head = self.coords[-1]
        new_x, new_y = head
        min_x = 1
        max_x = 57
        min_y = 1
        max_y = 17
        if key == curses.KEY_RIGHT:
            new_x += 1
        if key == curses.KEY_LEFT:
            new_x -= 1
        if key == curses.KEY_UP:
            new_y -= 1
        if key == curses.KEY_DOWN:
            new_y += 1
        if new_x < min_x:
            new_x = max_x
        if new_x > max_x:
            new_x = min_x
        if new_y < min_y:
            new_y = max_y
        if new_y > max_y:
            new_y = min_y
        return (new_x, new_y)

    def count_score(self):
        self.score = len(self.coords) - 1
        if self.score < 0:
            self.is_alive = False

    def move(self, game):
        new_head_coords = self.new_head(game.key)
        prev_super_fruit = game.super_fruit
        game.super_fruit = False

        if game.key:
            dead_coords = self.coords.copy()
            if not self.ghost_mode:
                dead_coords += game.walls
            if new_head_coords in dead_coords:
                self.is_alive = False

            self.coords.append(new_head_coords)

            if new_head_coords in game.fruits:
                game.fruits.remove(new_head_coords)
            elif new_head_coords in game.super_fruits:
                game.super_fruit = True
                game.super_fruits.remove(new_head_coords)
            elif prev_super_fruit is False:
                tail = self.coords.pop(0)
                game.removed_coords.append(tail)
            if new_head_coords in game.poisoned_fruits:
                tail = self.coords.pop(0)
                game.removed_coords.append(tail)
                game.poisoned_fruits.remove(new_head_coords)
            if new_head_coords in game.ghost_coords:
                self.ghost_mode = True
                self.ghost_start_time = time()
                game.ghost_coords.remove(new_head_coords)

    def choose_sign(self):
        self.sign = '*' if self.ghost_mode else '+'

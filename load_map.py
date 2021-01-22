import os


class InvalidPathExtension(Exception):
    def __init__(self, path_extension):
        error_msg = f'{path_extension} is not correct extension of map file.'
        super().__init__(error_msg)


class InvalidMapError(Exception):
    def __init__(self, char=None, x=None, y=None):
        if char and x and y:
            error_msg = f'"{char}" char not expected, position: ({x}, {y}).'
        else:
            error_msg = ''
        super().__init__(error_msg)


class InvalidSnakeError(Exception):
    pass


class Map():
    def __init__(self, path):
        self.path = path
        self.walls = []
        self.snake_coords = []
        self.load()

    def path_extension(self):
        _, path_extension = os.path.splitext(self.path)
        return path_extension

    def load(self):
        if self.path_extension() != '.txt':
            raise InvalidPathExtension(self.path_extension())

        with open(self.path, 'r') as file_handle:
            for y, line in enumerate(file_handle):
                line = line[0:-1]
                line += ' ' * 58
                if y == 0:
                    for x, char in enumerate(line):
                        if not ((x == 0 and char == '┌') or not
                                (x == 58 and char == '┐') or not
                                (57 > y > 0 and char == '─')):
                            raise InvalidMapError(char, x, y)
                        if x > 58:
                            break

                elif y == 18:
                    for x, char in enumerate(line):
                        if not ((x == 0 and char == "└") or not
                                (x == 58 and char == '┘') or not
                                (57 > y > 0 and char == '─')):
                            raise InvalidMapError(char, x, y)
                        if x > 58:
                            break

                elif y > 18:
                    break

                else:
                    for x, char in enumerate(line):
                        if x in (0, 58):
                            if char != '│':
                                raise InvalidMapError(char, x, y)
                        elif char == '#':
                            self.walls.append((x, y))
                        elif char == '+':
                            self.snake_coords.append((x, y))
                        elif char != ' ':
                            raise InvalidMapError(char, x, y)
                        if len(self.snake_coords) > 1:
                            raise InvalidSnakeError('Invalid snake size.')
                        if x > 58:
                            break
            if len(self.snake_coords) == 0:
                raise InvalidSnakeError('Invalid snake size.')

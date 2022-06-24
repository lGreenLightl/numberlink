import sys
from collections import defaultdict
from string import ascii_letters, digits

from PyQt6.QtWidgets import QMessageBox

from src.color import Color


class Utils:
    TWO, LEFT, RIGHT = range(3)
    color_collection = []
    current_color = Color(255, 255, 255)
    current_cell = [-1, -1]
    start = ""
    finish = ""
    cells = []
    best_score = [1000000000000000000000000] * 40


    path_dictionary = {
        (0, 2, 0): '\\', (0, -2, 0): '\\',
        (2, 0, 0): '/', (-2, 0, 0): '/',
        (-1, 1, -1): '^', (1, -1, 1): '^',
        (-1, 1, 1): 'v', (1, -1, -1): 'v',
        (1, 1, -1): '>', (-1, -1, 1): '>',
        (1, 1, 1): '<', (-1, -1, -1): '<'
    }

    correct_pipes = {
        '/-': '┐', '\\-': '┌',
        '/|': '└', '\\|': '┘',
        ' -': '-', ' |': '|',
    }

    raw_pipes = {
        '/-': [(0, 1)], '\\-': [(1, 0), (0, 1)], '/|': [(1, 0)],
        ' -': [(1, 0)], ' |': [(0, 1)], 'v|': [(0, 1)],
        '>|': [(1, 0)], 'v-': [(0, 1)], '>-': [(1, 0)],
    }

    @staticmethod
    def sign(x):
        """ sign function """
        if x == 0:
            return x
        return -1 if x < 0 else 1

    @staticmethod
    def inverse(x, y, dx, dy):
        """ inverse rotate (x, y) by (dx, dy) where
            (dx, dy) = (0, 1) means 0 degrees """
        while (dx, dy) != (0, 1):
            x, y, dx, dy = -y, x, -dy, dx
        return x, y

    @staticmethod
    def pair_check(grid, pair_finder):
        """ check for a pair of endpoints next to each other """
        for y in range(grid.height):
            for x in range(grid.width):
                for dx, dy in ((1, 0), (0, 1)):
                    xn, yn = x + dx, y + dy
                    if xn < grid.width and yn < grid.height:
                        if (grid[x, y] == grid[xn, yn] == 'x' and
                                pair_finder.find((x, y)) ==
                                pair_finder.find((xn, yn))):
                            return True
        return False

    @staticmethod
    def intersection_check(grid, pair_finder):
        """ check for a point with three neighbors of the same color """
        for y in range(grid.height):
            for x in range(grid.width):
                r = pair_finder.find((x, y))
                nbs = 0
                for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
                    xn, yn = x + dx, y + dy
                    if (0 <= xn < grid.width and
                            0 <= yn < grid.height and
                            pair_finder.find((xn, yn)) == r):
                        nbs += 1
                if nbs >= 3:
                    return True
        return False

    @staticmethod
    def loops_check(grid, pair_finder):
        """ check for loops that aren't related to the endpoint """
        ends = sum(bool(grid[x, y] in 'v^<>')
                   for y in range(grid.height)
                   for x in range(grid.width))
        pairs = len({pair_finder.find((x, y))
                     for y in range(grid.height)
                     for x in range(grid.width)})
        return 2 * pairs != ends

    @staticmethod
    def check_grid(grid, min_amount, max_amount):
        """ checking grid ready to be returned """
        compressed_grid = grid.grid_compression()
        piped_grid, pair_finder = compressed_grid.make_pipes()
        numbers = list(piped_grid.values()).count('x') // 2
        return (max_amount >= numbers >= min_amount
                and not Utils.loops_check(compressed_grid, pair_finder)
                and not Utils.pair_check(piped_grid, pair_finder)
                and not Utils.intersection_check(piped_grid, pair_finder))

    @staticmethod
    def get_correct_field(grid):
        """ returns correct field """
        try:
            field, pair_finder = grid.make_pipes()

            letters = digits[1:] + ascii_letters
            char = defaultdict(lambda: letters[len(char)])

            for x in range(field.width):
                for y in range(field.height):
                    if field[x, y] == 'x':
                        field[x, y] = char[pair_finder.find((x, y))]

            return field, char
        except ValueError:
            print('Incorrect grid!')

    @staticmethod
    def create_message(label, text):
        mess = QMessageBox()
        mess.setWindowTitle(label)
        mess.setText(text)
        mess.setIcon(QMessageBox.Icon.Warning)
        mess.setStandardButtons(QMessageBox.StandardButton.Ok)
        mess.exec()

    @staticmethod
    def is_digit(line):
        try:
            int(line)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_in_collection(color) -> bool:
        answer = False
        for c in Utils.color_collection:
            if color == c:
                answer = True
                return answer
        Utils.color_collection.append(color)
        return answer

    @staticmethod
    def loading():
        with open('src/resource/help.txt', 'r', encoding='utf-8') as file:
            return file.read()

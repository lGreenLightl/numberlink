from collections import defaultdict
from string import ascii_letters, digits

from PyQt6.QtWidgets import QMessageBox


class Utils:
    T, L, R = range(3)
    color_collection = []

    @staticmethod
    def sign(x):
        if x == 0:
            return x
        return -1 if x < 0 else 1

    @staticmethod
    def inverse(x, y, dx, dy):
        while (dx, dy) != (0, 1):
            x, y, dx, dy = -y, x, -dy, dx
        return x, y

    @staticmethod
    def pair_check(tg, pf):
        for y in range(tg.height):
            for x in range(tg.width):
                for dx, dy in ((1, 0), (0, 1)):
                    xn, yn = x + dx, y + dy
                    if xn < tg.width and yn < tg.height:
                        if (tg[x, y] == tg[xn, yn] == 'x' and
                                pf.find((x, y)) == pf.find((xn, yn))):
                            return True
        return False

    @staticmethod
    def intersection_check(tg, pf):
        for y in range(tg.height):
            for x in range(tg.width):
                r = pf.find((x, y))
                nbs = 0
                for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
                    xn, yn = x + dx, y + dy
                    if (0 <= xn < tg.width and
                            0 <= yn < tg.height and
                            pf.find((xn, yn)) == r):
                        nbs += 1
                if nbs >= 3:
                    return True
        return False

    @staticmethod
    def loops_check(grid, pf):
        ends = sum(bool(grid[x, y] in 'v^<>')
                   for y in range(grid.height)
                   for x in range(grid.width))
        pairs = len({pf.find((x, y))
                     for y in range(grid.height)
                     for x in range(grid.width)})
        return 2 * pairs != ends

    @staticmethod
    def check_grid(grid, min_amount, max_amount):
        sg = grid.split_grid()
        stg, pf = sg.make_tubes()
        numbers = list(stg.values()).count('x') // 2
        return (max_amount >= numbers >= min_amount
                and not Utils.loops_check(sg, pf)
                and not Utils.pair_check(stg, pf)
                and not Utils.intersection_check(stg, pf))

    @staticmethod
    def color_tubes(grid):
        try:
            tube_grid, pf = grid.make_tubes()

            letters = digits[1:] + ascii_letters
            char = defaultdict(lambda: letters[len(char)])

            for x in range(tube_grid.width):
                for y in range(tube_grid.height):
                    if tube_grid[x, y] == 'x':
                        tube_grid[x, y] = char[pf.find((x, y))]

            return tube_grid, char
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
    def in_collection(color) -> bool:
        answer = False
        for c in Utils.color_collection:
            if color == c:
                answer = True
                return answer
        Utils.color_collection.append(color)
        return answer

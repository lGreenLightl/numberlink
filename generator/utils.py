import colorama
from colorama import Fore

import string
from collections import defaultdict

T, L, R = range(3)


def sign(x):
    if x == 0:
        return x
    return -1 if x < 0 else 1


def inverse(x, y, dx, dy):
    while (dx, dy) != (0, 1):
        x, y, dx, dy = -y, x, -dy, dx
    return x, y


def pair_check(tg, pf):
    for y in range(tg.height):
        for x in range(tg.width):
            for dx, dy in ((1, 0), (0, 1)):
                xn, yn = x + dx, y + dy
                if xn < tg.width and yn < tg.height:
                    if tg[x, y] == tg[xn, yn] == 'x' and pf.find((x, y)) == pf.find((xn, yn)):
                        return True
    return False


def intersection_check(tg, pf):
    for y in range(tg.height):
        for x in range(tg.width):
            r = pf.find((x, y))
            nbs = 0
            for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
                xn, yn = x + dx, y + dy
                if 0 <= xn < tg.width and 0 <= yn < tg.height and pf.find((xn, yn)) == r:
                    nbs += 1
            if nbs >= 3:
                return True
    return False


def loops_check(grid, pf):
    ends = sum(bool(grid[x, y] in 'v^<>') for y in range(grid.height) for x in range(grid.width))
    pairs = len({pf.find((x, y)) for y in range(grid.height) for x in range(grid.width)})
    return 2 * pairs != ends


def check_grid(grid, min_amount, max_amount):
    sg = grid.split_grid()
    stg, pf = sg.make_tubes()
    numbers = list(stg.values()).count('x') // 2
    return (max_amount >= numbers >= min_amount
            and not loops_check(sg, pf) and not pair_check(stg, pf) and not intersection_check(stg, pf))


def color_tubes(grid):
    colorama.init()
    colors = [Fore.WHITE, Fore.YELLOW, Fore.RED, Fore.BLUE, Fore.GREEN,
              Fore.CYAN, Fore.MAGENTA, Fore.LIGHTRED_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTGREEN_EX]
    colors = colors + [c + colorama.Style.BRIGHT for c in colors]
    reset = colorama.Style.RESET_ALL + Fore.RESET

    tube_grid, pf = grid.make_tubes()

    letters = string.digits[1:] + string.ascii_letters
    char = defaultdict(lambda: letters[len(char)])
    color = defaultdict(lambda: colors[len(color) % len(colors)])

    for x in range(tube_grid.width):
        for y in range(tube_grid.height):
            if tube_grid[x, y] == 'x':
                tube_grid[x, y] = char[pf.find((x, y))]

            tube_grid[x, y] = color[pf.find((x, y))] + tube_grid[x, y] + reset

    return tube_grid, char

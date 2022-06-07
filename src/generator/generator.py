import argparse
import math
import random

from src.utils import Utils
from src.generator.table import Table
from src.generator.grid import Grid


def create_grid(width, height, table, min_amount=0, max_amount=20):
    grid = Grid(2 * width + 1, 2 * height + 1)

    while True:
        grid.clear()

        path = table.random_path(height, height, 0, -1)
        if not grid.test_path(path, 0, 0):
            continue
        grid.draw_path(path, 0, 0)
        grid[0, 0], grid[0, 2 * height] = '\\', '/'

        path2 = table.random_path(height, height, 0, -1)
        if not grid.test_path(path2, 2 * width, 2 * height, 0, -1):
            continue
        grid.draw_path(path2, 2 * width, 2 * height, 0, -1)
        grid[2 * width, 0], grid[2 * width, 2 * height] = '/', '\\'

        if Utils.check_grid(grid, min_amount, max_amount):
            return grid.split_grid()

        tg, _ = grid.make_tubes()

        for tries in range(1000):
            x, y = 2 * random.randrange(width), 2 * random.randrange(height)

            if tg[x, y] not in '-|':
                continue

            path = table.random_loop(clock=1 if tg[x, y] == '-' else -1)
            if grid.test_path(path, x, y):
                grid.clear_path(path, x, y)
                grid.draw_path(path, x, y, loop=True)
                tg, _ = grid.make_tubes()

                sg = grid.split_grid()
                stg, pf = sg.make_tubes()
                numbers = list(stg.values()).count('x') // 2
                if numbers > max_amount:
                    break
                if Utils.check_grid(grid, min_amount, max_amount):
                    return sg


def start_generator():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('width', type=int, default=5)
    args_parser.add_argument('height', type=int, default=5)
    args = args_parser.parse_args()

    width, height = args.width, args.height
    numbers_amount = int(math.sqrt(width * height))
    min_amount = numbers_amount * 2 // 3
    max_amount = numbers_amount * 3 // 2
    table = Table(2, 1)
    table.prepare_table(min(20, max(height, 6)))

    grid = create_grid(width, height, table, min_amount, max_amount)
    color_grid, mapping = Utils.color_tubes(grid)

    for y in range(color_grid.height):
        for x in range(color_grid.width):
            if grid[x, y] in 'v^<>':
                print(color_grid[x, y], end='')
            else:
                print('.', end='')
        print()
    print()
    print(repr(color_grid).replace('-', '─').replace('|', '│'))


if __name__ == '__main__':
    start_generator()

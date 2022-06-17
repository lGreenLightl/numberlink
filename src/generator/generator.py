from random import randrange

from src.generator.grid import Grid
from src.utils import Utils


def create_raw_grid(width, height, table, min_amount=0, max_amount=20):
    """ creates a raw grid of size (width x height)
        without any loops or squares
        :param table: lookup table
        :param height: grid height
        :param width: grid width
        :param min_amount: optimal minimum pairs
        :param max_amount: optimal maximum pairs
        """

    # use double size grid to handle intersection
    grid = Grid(2 * width + 1, 2 * height + 1)

    while True:
        grid.clear()

        # add left side path
        path = table.random_path(height, height, 0, -1)
        if not grid.test_path(path, 0, 0):
            continue
        grid.draw_path(path, 0, 0)
        grid[0, 0], grid[0, 2 * height] = '\\', '/'

        # add right side path
        path_2 = table.random_path(height, height, 0, -1)
        if not grid.test_path(path_2, 2 * width, 2 * height, 0, -1):
            continue
        grid.draw_path(path_2, 2 * width, 2 * height, 0, -1)
        grid[2 * width, 0], grid[2 * width, 2 * height] = '/', '\\'

        # probably the puzzle is ready to return
        if Utils.check_grid(grid, min_amount, max_amount):
            return grid.grid_compression()

        # add loops in the grid middle
        piped_grid, _ = grid.make_pipes()

        # maximum optimal number of tries before retrying main loop
        for tries in range(1000):
            x, y = 2 * randrange(width), 2 * randrange(height)

            # if
            # 1) the square doesn't have an orientation
            # 2) it's a corner
            # 3) it's an endpoint
            # so there's no point trying to add a loop there
            if piped_grid[x, y] not in '-|':
                continue

            path = table.random_loop(clock=1 if piped_grid[x, y] == '-' else -1)
            if grid.test_path(path, x, y):
                grid.clear_path(path, x, y)

                # add path and recalculate orientation
                grid.draw_path(path, x, y, loop=True)
                piped_grid, _ = grid.make_pipes()

                # check puzzle for correctness
                compressed_grid = grid.grid_compression()
                numbers = list(
                    compressed_grid.make_pipes()[0].values()).count('x') // 2
                if numbers > max_amount:
                    break
                if Utils.check_grid(grid, min_amount, max_amount):
                    return compressed_grid

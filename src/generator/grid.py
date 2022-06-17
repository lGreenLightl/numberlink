from src.generator.pair_finder import PairFinder
from src.utils import Utils


class Grid:
    def __init__(self, width, height):
        self.grid = {}
        self.width, self.height = width, height

    def __getitem__(self, item):
        return self.grid.get(item, ' ')

    def __setitem__(self, key, value):
        self.grid[key] = value

    def __delitem__(self, key):
        del self.grid[key]

    def __iter__(self):
        return iter(self.grid.items())

    def __contains__(self, item):
        return item in self.grid

    def __repr__(self):
        result = []
        for y in range(self.height):
            result.append(''.join(self[x, y] for x in range(self.width)))
        return '\n'.join(result)

    def values(self):
        return self.grid.values()

    def clear(self):
        self.grid.clear()

    def make_pipes(self):
        """ creates a grid with pipes """
        pair_finder = PairFinder()
        grid = Grid(self.width, self.height)
        for x in range(self.width):
            symbol = '-'
            for y in range(self.height):
                for dx, dy in Utils.raw_pipes.get(self[x, y] + symbol, []):
                    pair_finder.pair((x, y), (x + dx, y + dy))

                grid[x, y] = Utils.correct_pipes.get(self[x, y] + symbol, 'x')

                if self[x, y] in '\\/v^':
                    symbol = '|' if symbol == '-' else '-'
        return grid, pair_finder

    def draw_path(self, path, x0, y0, dx0=0, dy0=1, loop=False):
        """ draws path on the grid with no overlaps """
        paths = list(path.get_positions(dx0, dy0))

        if loop:
            assert paths[0] == paths[-1], (path, paths)
            paths.append(paths[1])
        for i in range(1, len(paths) - 1):
            x, y = paths[i]
            xp, yp = paths[i - 1]
            xn, yn = paths[i + 1]
            self[x0 - x + y, y0 + x + y] = \
                Utils.path_dictionary[xn - xp, yn - yp,
                                      Utils.sign
                                      ((x - xp) * (yn - y) - (xn - x) * (y - yp))]

    def clear_path(self, path, x, y):
        """ clears everything contained in the path located at x, y """
        grid = Grid(self.width, self.height)
        grid.draw_path(path, x, y, loop=True)
        for key, value in grid.make_pipes()[0]:
            if value == '|':
                self.grid.pop(key, None)

    def test_path(self, path, x0, y0, dx0=0, dy0=1):
        """ checking the safety of drawing a path on the grid,
            starting from x0, y0 """
        return all(0 <= x0 - x + y < self.width and
                   0 <= y0 + x + y < self.height and
                   (x0 - x + y, y0 + x + y) not in self
                   for x, y in path.get_positions(dx0, dy0))

    def grid_compression(self):
        """ creates a new grid of half width and height """
        grid_half = Grid(self.width // 2, self.height // 2)
        for y in range(self.height // 2):
            for x in range(self.width // 2):
                grid_half[x, y] = self[2 * x + 1, 2 * y + 1]
        return grid_half

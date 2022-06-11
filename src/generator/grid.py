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

    def make_tubes(self):
        pf = PairFinder()
        grid = Grid(self.width, self.height)
        for x in range(self.width):
            symbol = '-'
            for y in range(self.height):
                for dx, dy in {
                    '/-': [(0, 1)], '\\-': [(1, 0), (0, 1)], '/|': [(1, 0)],
                    ' -': [(1, 0)], ' |': [(0, 1)], 'v|': [(0, 1)],
                    '>|': [(1, 0)], 'v-': [(0, 1)], '>-': [(1, 0)],
                }.get(self[x, y] + symbol, []):
                    pf.pair((x, y), (x + dx, y + dy))

                grid[x, y] = {
                    '/-': '┐', '\\-': '┌',
                    '/|': '└', '\\|': '┘',
                    ' -': '-', ' |': '|',
                }.get(self[x, y] + symbol, 'x')

                if self[x, y] in '\\/v^':
                    symbol = '|' if symbol == '-' else '-'
        return grid, pf

    def draw_path(self, path, x0, y0, dx0=0, dy0=1, loop=False):
        ps = list(path.get_positions(dx0, dy0))

        if loop:
            assert ps[0] == ps[-1], (path, ps)
            ps.append(ps[1])
        for i in range(1, len(ps) - 1):
            x, y = ps[i]
            xp, yp = ps[i - 1]
            xn, yn = ps[i + 1]
            self[x0 - x + y, y0 + x + y] = {
                (0, 2, 0): '\\', (0, -2, 0): '\\',
                (2, 0, 0): '/', (-2, 0, 0): '/',
                (-1, 1, -1): '^', (1, -1, 1): '^',
                (-1, 1, 1): 'v', (1, -1, -1): 'v',
                (1, 1, -1): '>', (-1, -1, 1): '>',
                (1, 1, 1): '<', (-1, -1, -1): '<'
            }[xn - xp, yn - yp,
              Utils.sign((x - xp) * (yn - y) - (xn - x) * (y - yp))]

    def clear_path(self, path, x, y):
        grid = Grid(self.width, self.height)
        grid.draw_path(path, x, y, loop=True)
        for key, value in grid.make_tubes()[0]:
            if value == '|':
                self.grid.pop(key, None)

    def test_path(self, path, x0, y0, dx0=0, dy0=1):
        return all(0 <= x0 - x + y < self.width and
                   0 <= y0 + x + y < self.height and
                   (x0 - x + y, y0 + x + y) not in self
                   for x, y in path.get_positions(dx0, dy0))

    def split_grid(self):
        grid_half = Grid(self.width // 2, self.height // 2)
        for y in range(self.height // 2):
            for x in range(self.width // 2):
                grid_half[x, y] = self[2 * x + 1, 2 * y + 1]
        return grid_half

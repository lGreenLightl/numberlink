from collections import defaultdict
from random import choice, choices

from src.generator.path import Path
from src.utils import Utils


class Table:
    def __init__(self, left_right_price, two_price):
        self.left_right_price = left_right_price
        self.two_price = two_price
        self.dictionary = defaultdict(list)
        self.list = []

    def prepare_table(self, budget):
        """ initializes the table """
        dx0, dy0 = 0, 1
        for path, (x, y, dx, dy) in self.correct_paths(0, 0, dx0, dy0, budget):
            self.list.append((path, x, y, dx, dy))
            self.dictionary[x, y, dx, dy].append(path)

    def cached_paths(self, dx, dy, xn, yn, dxn, dyn):
        """ returns cached paths starting at (0,0) with direction (dx,dy)
            and ending at (xn,yn) with direction (dxn,dyn) """
        x, y = Utils.inverse(xn, yn, dx, dy)
        dxk, dyk = Utils.inverse(dxn, dyn, dx, dy)
        return self.dictionary[x, y, dxk, dyk]

    def correct_paths(self, x, y, dx, dy, budget, init_set=None):
        """ gives correct paths """
        if init_set is None:
            init_set = set()
        if budget >= 0:
            yield (), (x, y, dx, dy)
        if budget <= 0:
            return

        init_set.add((x, y))
        x1, y1 = x + dx, y + dy

        if (x1, y1) not in init_set:
            for path, end in self.correct_paths(
                    x1, y1, -dy, dx, budget - self.left_right_price, init_set):
                yield (Utils.LEFT,) + path, end
            for path, end in self.correct_paths(
                    x1, y1, dy, -dx, budget - self.left_right_price, init_set):
                yield (Utils.RIGHT,) + path, end
            init_set.add((x1, y1))
            x2, y2 = x1 + dx, y1 + dy
            if (x2, y2) not in init_set:
                for path, end in self.correct_paths(
                        x2, y2, dx, dy, budget - self.two_price, init_set):
                    yield (Utils.TWO,) + path, end
            init_set.remove((x1, y1))
        init_set.remove((x, y))

    def random_loop(self, clock=0):
        """ return path with overlap """
        while True:
            path, x, y, dx, dy = choice(self.list)
            path2s = self.cached_paths(dx, dy, -x, -y, 0, 1)
            if path2s:
                path2 = choice(path2s)
                joined_path = Path(path + path2)

                if clock and (joined_path.positions.count(Utils.RIGHT) -
                              joined_path.positions.count(Utils.LEFT) !=
                              clock * 4):
                    continue
                if joined_path.check_path_loop():
                    return joined_path

    def random_path(self, xn, yn, dxn, dyn):
        """ returns a path starting at (0,0) with (dx,dy) = (0,1)
            and ending at (xn,yn) with direction (dxn, dyn) """
        init_set = set()
        path = []

        while True:
            init_set.clear()
            del path[:]
            x, y, dx, dy = 0, 0, 0, 1
            init_set.add((x, y))

            for _ in range(2 * (abs(xn) + abs(yn))):
                position, = choices([Utils.LEFT, Utils.RIGHT, Utils.TWO],
                                    [1 / self.left_right_price,
                                     1 / self.left_right_price,
                                     2 / self.two_price])
                path.append(position)
                x, y = x + dx, y + dy

                if (x, y) in init_set:
                    break

                init_set.add((x, y))

                if position == Utils.LEFT:
                    dx, dy = -dy, dx
                if position == Utils.RIGHT:
                    dx, dy = dy, -dx
                elif position == Utils.TWO:
                    x, y = x + dx, y + dy
                    if (x, y) in init_set:
                        break
                    init_set.add((x, y))

                if (x, y) == (xn, yn):
                    return Path(path)

                ends = self.cached_paths(dx, dy, xn - x, yn - y, dxn, dyn)
                if ends:
                    return Path(tuple(path) + choice(ends))

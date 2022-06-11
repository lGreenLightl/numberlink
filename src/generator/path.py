from src.utils import Utils


class Path:
    def __init__(self, positions):
        self.positions = positions

    def __repr__(self):
        return ''.join({Utils.T: '2', Utils.R: 'R', Utils.L: 'L'}[position] for position in self.positions)

    def get_positions(self, dx=0, dy=1):
        x, y = 0, 0
        yield x, y

        for position in self.positions:
            x, y = x + dx, y + dy
            yield x, y

            if position == Utils.L:
                dx, dy = -dy, dx
            if position == Utils.R:
                dx, dy = dy, -dx
            elif position == Utils.T:
                x, y = x + dx, y + dy
                yield x, y

    def taping(self):
        return self.positions.count(Utils.R) - self.positions.count(Utils.L)

    def check_path(self):
        ps = list(self.get_positions())
        return len(set(ps)) == len(ps)

    def check_path_loop(self):
        ps = list(self.get_positions())
        seen = set(ps)
        return len(ps) == len(seen) or len(ps) == len(seen) + 1 and ps[0] == ps[-1]

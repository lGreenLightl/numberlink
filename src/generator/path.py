from src.utils import Utils


class Path:
    def __init__(self, positions):
        self.positions = positions

    def __repr__(self):
        return ''.join({Utils.T: '2',
                        Utils.R: 'R',
                        Utils.L: 'L'}[position] for position in self.positions)

    def get_positions(self, dx=0, dy=1):
        """ gives all positions on the path """
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

    def check_path(self):
        """ checking for a path without overlaps """
        path_list = list(self.get_positions())
        return len(set(path_list)) == len(path_list)

    def check_path_loop(self):
        """ checking for a path without overlaps, except for first and last """
        path_list = list(self.get_positions())
        return (len(path_list) == len(set(path_list)) or
                len(path_list) == len(set(path_list)) + 1 and
                path_list[0] == path_list[-1])

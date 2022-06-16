from re import split
from unittest import main, TestCase

from src.generator.grid import Grid
from src.utils import Utils


class SolverTest(TestCase):
    def test_solve_xsmall_puzzle(self):
        xsmall_field = SolverTest.load_field('xsmall_field.txt')
        xsmall_grid = Grid(5, 5)
        self.check_grid(xsmall_field, xsmall_grid)

    def test_solve_small_puzzle(self):
        small_field = SolverTest.load_field('small_field.txt')
        small_grid = Grid(10, 10)
        self.check_grid(small_field, small_grid)

    def test_solve_medium_puzzle(self):
        medium_field = SolverTest.load_field('medium_field.txt')
        medium_grid = Grid(15, 15)
        self.check_grid(medium_field, medium_grid)

    def test_solve_big_puzzle(self):
        big_field = SolverTest.load_field('big_field.txt')
        big_grid = Grid(20, 20)
        self.check_grid(big_field, big_grid)

    def test_solve_xbig_puzzle(self):
        xbig_field = SolverTest.load_field('xbig_field.txt')
        xbig_grid = Grid(30, 30)
        self.check_grid(xbig_field, xbig_grid)

    def check_grid(self, field, grid):
        finished_grid = self.solve_puzzle(field, grid)
        self.assertTrue(finished_grid[0] is not None)

    @staticmethod
    def load_field(path):
        with open(f'resource/{path}', 'r', encoding='utf-8') as file:
            return file.read()

    @staticmethod
    def solve_puzzle(field, grid):
        finished_field = split('.\n', field)

        for y in range(grid.height):
            for x in range(grid.width):
                grid[x, y] = finished_field[y][x]

        return Utils.get_correct_field(grid)


if __name__ == '__main__':
    main()

import re
import unittest

from src.generator.grid import Grid
from src.utils import Utils


class SolverTest(unittest.TestCase):
    def setUp(self):
        self.x_small_field = SolverTest.load('x_small_field.txt')
        self.small_field = SolverTest.load('small_field.txt')
        self.medium_field = SolverTest.load('medium_field.txt')
        self.big_field = SolverTest.load('big_field.txt')
        self.x_big_field = SolverTest.load('x_big_field.txt')
        self.x_small_grid = Grid(5, 5)
        self.small_grid = Grid(10, 10)
        self.medium_grid = Grid(15, 15)
        self.big_grid = Grid(20, 20)
        self.x_big_grid = Grid(30, 30)

    def test_solver(self):
        x_small_grid = self.solve(self.x_small_field, self.x_small_grid)
        small_grid = self.solve(self.small_field, self.small_grid)
        medium_grid = self.solve(self.medium_field, self.medium_grid)
        big_grid = self.solve(self.big_field, self.big_grid)
        x_big_grid = self.solve(self.x_big_field, self.x_big_grid)

        self.assertTrue(x_small_grid[0] is not None)
        self.assertTrue(small_grid[0] is not None)
        self.assertTrue(medium_grid[0] is not None)
        self.assertTrue(big_grid[0] is not None)
        self.assertTrue(x_big_grid[0] is not None)

    @staticmethod
    def solve(field, grid):
        ready_field = re.split('.\n', field)
        for y in range(grid.height):
            for x in range(grid.width):
                grid[x, y] = ready_field[y][x]

        return Utils.color_tubes(grid)

    @staticmethod
    def load(path):
        with open(f'../resource/{path}', 'r', encoding='utf-8') as file:
            return file.read()


if __name__ == '__main__':
    unittest.main()

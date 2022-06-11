from math import sqrt

from src.generator.generator import create_grid
from src.generator.table import Table
from src.generator.size import Size
from src.utils import Utils


class Field:
    def __init__(self, size: Size, form: str) -> None:
        self.form = form
        self.size = size
        self.field = self.generate_field()

    def generate_field(self):
        numbers_amount = int(sqrt(self.size.width * self.size.height))
        min_amount = numbers_amount * 2 // 3
        max_amount = numbers_amount * 3 // 2
        table = Table(2, 1)
        table.prepare_table(min(20, max(self.size.height, 6)))

        grid = create_grid(self.size.width, self.size.height, table, min_amount, max_amount)
        color_grid, mapping = Utils.color_tubes(grid)

        field = [['.'] * self.size.width for _ in range(self.size.height)]
        for y in range(self.size.height):
            for x in range(self.size.width):
                if grid[x, y] in 'v^<>':
                    field[y][x] = color_grid[x, y]

        print(repr(color_grid).replace('-', '─').replace('|', '│'))

        return field

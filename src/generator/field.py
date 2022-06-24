from src.generator.generator import create_raw_grid
from src.generator.table import Table
from src.generator.size import Size
from src.utils import Utils


class Field:
    def __init__(self, size: Size, form: str, field=None) -> None:
        self.form = form
        self.size = size
        if field is None:
            self.field = self.generate_field()
        else:
            self.field = field

    def generate_field(self):
        """ generates the correct field """

        # if you use a long path in the table,
        # then the complexity of the puzzle may increase,
        # but 8 - 10 pairs of numbers
        # is the best solution for small fields, such as 4x4
        table = Table(2, 1)
        table.prepare_table(min(20, max(self.size.height, 6)))

        grid = create_raw_grid(self.size.width, self.size.height, table)
        finished_field, mapping = Utils.get_correct_field(grid)

        # generates correct field
        field = [['.'] * self.size.width for _ in range(self.size.height)]
        for y in range(self.size.height):
            for x in range(self.size.width):
                if grid[x, y] in 'v^<>':
                    field[y][x] = finished_field[x, y]

        # prints solved puzzle
        print(repr(finished_field).replace('-', '─').replace('|', '│'))

        return field

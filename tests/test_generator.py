from unittest import main, TestCase

from src.generator.field import Field
from src.generator.size import Size


class GeneratorTest(TestCase):
    def test_correct_xsmall_field(self):
        xsmall_field = Field(Size(5, 5), 'Квадрат')
        self.check_field(xsmall_field)

    def test_correct_small_field(self):
        small_field = Field(Size(10, 10), 'Квадрат')
        self.check_field(small_field)

    def test_correct_medium_field(self):
        medium_field = Field(Size(15, 15), 'Квадрат')
        self.check_field(medium_field)

    def test_correct_big_field(self):
        big_field = Field(Size(20, 20), 'Квадрат')
        self.check_field(big_field)

    def test_correct_xbig_field(self):
        xbig_field = Field(Size(30, 30), 'Квадрат')
        self.check_field(xbig_field)

    def check_field(self, field):
        dictionary = self.count_pairs(field)
        for item in dictionary.items():
            self.assertEqual(item[1], 2)

    @staticmethod
    def count_pairs(field):
        pairs_dictionary = {}

        for y in range(field.size.height):
            for x in range(field.size.width):
                if (field.field[x][y] not in pairs_dictionary
                        and field.field[x][y] != '.'):
                    pairs_dictionary[field.field[x][y]] = 1
                elif field.field[x][y] != '.':
                    pairs_dictionary[field.field[x][y]] += 1

        return pairs_dictionary


if __name__ == '__main__':
    main()

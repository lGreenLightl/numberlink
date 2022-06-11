import unittest

from src.field import Field
from src.size import Size


class GeneratorTest(unittest.TestCase):
    def setUp(self):
        self.x_small_field = Field(Size(5, 5), 'Квадрат')
        self.small_field = Field(Size(10, 10), 'Квадрат')
        self.medium_field = Field(Size(15, 15), 'Квадрат')
        self.big_field = Field(Size(20, 20), 'Квадрат')
        self.x_big_field = Field(Size(30, 30), 'Квадрат')

    def test_correct_pairs_amount(self):
        first_dictionary = self.pairs_counter(self.x_small_field)
        second_dictionary = self.pairs_counter(self.small_field)
        third_dictionary = self.pairs_counter(self.medium_field)
        fourth_dictionary = self.pairs_counter(self.big_field)
        fifth_dictionary = self.pairs_counter(self.x_big_field)

        for item in first_dictionary.items():
            self.assertEqual(item[1], 2)
        for item in second_dictionary.items():
            self.assertEqual(item[1], 2)
        for item in third_dictionary.items():
            self.assertEqual(item[1], 2)
        for item in fourth_dictionary.items():
            self.assertEqual(item[1], 2)
        for item in fifth_dictionary.items():
            self.assertEqual(item[1], 2)

    @staticmethod
    def pairs_counter(field):
        pairs_dictionary = {}
        for y in range(field.size.height):
            for x in range(field.size.width):
                if field.field[x][y] not in pairs_dictionary and field.field[x][y] != '.':
                    pairs_dictionary[field.field[x][y]] = 1
                elif field.field[x][y] != '.':
                    pairs_dictionary[field.field[x][y]] += 1

        return pairs_dictionary


if __name__ == '__main__':
    unittest.main()

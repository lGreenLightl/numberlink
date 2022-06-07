from dataclasses import dataclass


@dataclass
class Color:
    red: int
    green: int
    blue: int

    def __eq__(self, other):
        return self.red == other.red and self.green == other.green and self.blue == other.blue

from dataclasses import dataclass


@dataclass
class Color:
    red: int
    green: int
    blue: int

    def __eq__(self, other):
        """compare current color with another"""
        return (self.red == other.red and
                self.green == other.green and
                self.blue == other.blue)

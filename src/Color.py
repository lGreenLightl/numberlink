class Color:
    def __init__(self, r, g, b):
        self.Red = r
        self.Green = g
        self.Blue = b

    def __eq__(self, other):
        return self.Red == other.Red and self.Green == other.Green and self.Blue == other.Blue

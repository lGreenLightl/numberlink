from src.size import Size


class Field:
    def __init__(self, size: Size, form: str) -> None:
        self.form = form
        self.size = size
        self.field = self.generate_field()

    def generate_field(self):
        field = [['.'] * self.size.width for _ in range(self.size.height)]
        return field

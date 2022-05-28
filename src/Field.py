class Field:
    def __init__(self, size, form) -> None:
        self.Form = form
        self.Size = size
        self.Field = self.generate_field()

    def generate_field(self):
        field = [['.'] * self.Size.Weight for _ in range(self.Size.Height)]
        return field


class Field:
    def __init__(self, size, form):
        self.Form = form
        self.Size = size
        self.Field = self.generate_field()

    def generate_field(self):
        if self.Form == "SQUARE" or "RECTANGLE":
            field = [['.'] * self.Size.Weight for _ in range(self.Size.Height)]
        return field


class Field:
    def __init__(self, size, form) -> None:
        self.Form = form  # TODO: от Дани: название файлов с маленькой буквы, название полей тоже.
        self.Size = size  # TODO: от Дани: где тайпинг??))))
        self.Field = self.generate_field()

    def generate_field(self):
        field = None
        if self.Form == "SQUARE" or "RECTANGLE":
            field = [['.'] * self.Size.Weight for _ in range(self.Size.Height)]
        return field


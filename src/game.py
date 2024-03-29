from src.generator.field import Field
from src.generator.size import Size


class Game:
    def __init__(self, user_name: str, complexity: str,
                 field_form: str, field_width: int,
                 field_height: int, field=None) -> None:
        self.user_name = user_name
        self.complexity = complexity
        if field is None:
            self.field = Field(Size(field_height, field_width), field_form)
        else:
            self.field = Field(Size(field_height, field_width), field_form, field)

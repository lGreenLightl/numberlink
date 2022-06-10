from src.field import Field
from src.size import Size


class Game:
    def __init__(self, user_name: str, complexity: str,
                 field_form: str, field_weight: int, field_height: int) -> None:
        self.user_name = user_name
        self.complexity = complexity
        self.field = Field(Size(field_weight, field_height), field_form)

    def start(self):
        pass

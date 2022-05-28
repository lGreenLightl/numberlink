from Field import Field
from Size import Size


class Game:
    def __init__(
            self, user_name: str, complexity: str,
            field_form: str,
            field_weight: int, field_height: int
    ) -> None:
        self.User_name = user_name
        self.Complexity = complexity
        self.Field = Field(Size(field_weight, field_height), field_form,)

    def start(self):
        pass

from json import dump, load

from src.game import Game
from src.utils import Utils


class Saver:
    def __init__(self, file_path):
        self.file_path = file_path

    def save(self, game: Game, text):
        data = {'user_name': game.user_name,
                'complexity': game.complexity,
                'field_form': game.field.form,
                'field_width': game.field.size.width,
                'field_height': game.field.size.height,
                'field': game.field.field,
                'score': Utils.best_score[game.field.size.height],
                'clicks': text}

        with open(self.file_path, 'w') as file:
            dump(data, file)

    def load(self):
        try:
            with open(self.file_path, 'r') as file:
                data = load(file)
        except FileNotFoundError:
            return None

        user_name = data['user_name']
        complexity = data['complexity']
        field_form = data['field_form']
        field_width: int = data['field_width']
        field_height: int = data['field_height']
        field: list[list[str]] = data['field']
        Utils.best_score[field_height] = data['score']
        clicks: str = data['clicks']

        game = Game(user_name, complexity,
                    field_form, field_width, field_height, field)
        return game, clicks

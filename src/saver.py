from json import dump, load

from src.game import Game
from src.utils import Utils


class Saver:
    def __init__(self, file_path):
        self.file_path = file_path

    def save(self, game: Game, text, colors):
        data = {'user_name': game.user_name,
                'complexity': game.complexity,
                'field_form': game.field.form,
                'field_width': game.field.size.width,
                'field_height': game.field.size.height,
                'field': game.field.field,
                'score': Utils.best_score[game.field.size.height],
                'clicks': text,
                'colors': colors,
                'numbers': Utils.numbers_in_field}

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
        colors = data['colors']
        Utils.numbers_in_field = data['numbers']

        game = Game(user_name, complexity,
                    field_form, field_width, field_height, field)
        return game, clicks, colors

    def save_score(self, user_name, size, score):
        try:
            with open(self.file_path, 'r') as file:
                data = load(file)
            if f'{size}' in data:
                if (user_name in data[f'{size}'] and
                        int(data[f'{size}'][user_name]) > int(score) or
                        user_name not in data[f'{size}']):
                    data[f'{size}'][user_name] = score
            else:
                data[f'{size}'] = {user_name: score}
            with open(self.file_path, 'w') as file:
                dump(data, file)
        except FileNotFoundError:
            data = {f'{size}': {user_name: score}}
            with open(self.file_path, 'x') as file:
                dump(data, file)

    def load_score(self, user_name, size):
        try:
            with open(self.file_path, 'r') as file:
                data = load(file)
            return data[f'{size}'][user_name]
        except FileNotFoundError:
            return None
        except KeyError:
            return None

    def load_top(self, size):
        try:
            with open(self.file_path, 'r') as file:
                data = load(file)
            return data[f'{size}']
        except FileNotFoundError:
            return None
        except KeyError:
            return None

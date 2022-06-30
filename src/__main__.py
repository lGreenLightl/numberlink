from argparse import ArgumentParser, RawTextHelpFormatter
from sys import argv, exit

from PyQt6.uic import loadUi
from PyQt6.QtWidgets import *

from src.cell import Cell
from src.color import Color
from src.game import Game
from src.saver import Saver
from src.utils import Utils


class GameScreen(QMainWindow):
    def __init__(self, game, clicks=None, colors=None) -> None:
        super(GameScreen, self).__init__()
        self.GameWidget = None
        self.ClicksLabel = None
        self.SaveButton = None
        self.ResetButton = None
        self.NameLabel = None
        self.ExitButton = None
        loadUi("src/ui/GameScreen.ui", self)
        self.ExitButton.clicked.connect(self.exit_game)
        self.NameLabel.setText(game.user_name)
        self.SaveButton.clicked.connect(self.save)
        self.ResetButton.clicked.connect(self.reset_game)
        self.top_saver = Saver('src/resource/top').load_score(
            game.user_name, game.field.size.height)
        self.colors = colors

        if clicks is None:
            self.ClicksLabel.setText('0')
        else:
            self.ClicksLabel.setText(clicks)
        self.Game = game

        if self.top_saver is None:
            self.ScoreLabel.setText("пока нет")
            Utils.best_current_size_score = "0"
            Utils.current_name = game.user_name
        else:
            self.ScoreLabel.setText(str(self.top_saver))
            Utils.best_current_size_score = str(self.top_saver)
            Utils.current_name = game.user_name

        self.GameGrid = QGridLayout()

        Utils.current_color = Color(255, 255, 255)
        Utils.current_cell[0] = -1
        Utils.current_cell[1] = -1
        Utils.cells.clear()
        Utils.start = ""
        Utils.color_collection.clear()
        Utils.current_size = game.field.size.height
        if clicks is None:
            self.get_field_numbers()
        self.create_cells()
        self.create_layout()

    def get_field_numbers(self):
        """get dictionary with numbers from field"""
        Utils.numbers_in_field.clear()
        for i in range(self.Game.field.size.height):
            for j in range(self.Game.field.size.width):
                if Utils.is_digit(self.Game.field.field[i][j]):
                    Utils.numbers_in_field[str(self.Game.field.field[i][j])] = False

    def create_layout(self):
        """create new Game grid"""
        grid_layout = QGridLayout()
        for i in range(self.Game.field.size.height):
            for j in range(self.Game.field.size.width):
                grid_layout.addWidget(Utils.cells[i][j], i, j)

        self.GameGrid = grid_layout
        self.GameWidget.setLayout(grid_layout)

    def create_cells(self):
        """create cells for fixed size game grid"""
        for i in range(0, self.Game.field.size.height):
            c = []
            for j in range(0, self.Game.field.size.width):
                if self.colors is None:
                    c.append(Cell(self.Game.field.field[i][j],
                                  self.ClicksLabel, j, i, self, widget))
                else:
                    c.append(Cell(self.Game.field.field[i][j],
                                  self.ClicksLabel, j, i, self, widget,
                                  self.colors[i][j][0],
                                  self.colors[i][j][1],
                                  self.colors[i][j][2]))
            Utils.cells.append(c)

    def save(self):
        self.colors = []
        for i in range(0, self.Game.field.size.height):
            current_colors = []
            for j in range(0, self.Game.field.size.width):
                current_colors.append((Utils.cells[i][j].color.red,
                                       Utils.cells[i][j].color.green,
                                       Utils.cells[i][j].color.blue))
            self.colors.append(current_colors)
        return Saver('src/resource/data').save(self.Game,
                                               self.ClicksLabel.text(),
                                               self.colors)

    @staticmethod
    def exit_game() -> None:
        """exit from the Game"""
        widget.close()

    def reset_game(self) -> None:
        """clean all cells and reset clicks count"""
        self.ClicksLabel.setText('0')
        self.get_field_numbers()
        Utils.start = ""
        Utils.finish = "empty"
        Utils.current_color = Color(255, 255, 255)
        for i in range(0, self.Game.field.size.height):
            for j in range(0, self.Game.field.size.width):
                Utils.cells[i][j].clean_label()


class WelcomeScreen(QDialog):
    def __init__(self) -> None:
        super(WelcomeScreen, self).__init__()
        self.ContinueButton = None
        self.ExitButton = None
        self.NewGameButton = None
        self.TopButton = None
        loadUi("src/ui/WelcomeScreen.ui", self)
        self.NewGameButton.clicked.connect(self.go_to_new_game)
        self.ExitButton.clicked.connect(self.exit_game)
        self.ContinueButton.clicked.connect(self.continue_game)
        self.TopButton.clicked.connect(self.show_top_players)

    @staticmethod
    def go_to_new_game() -> None:
        """go to new Game creating"""
        new_game = NewGameScreen()
        widget.addWidget(new_game)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    @staticmethod
    def exit_game() -> None:
        """exit from the Game"""
        widget.close()

    @staticmethod
    def continue_game() -> None:
        """go to selecting Game from saved Games"""
        saver = Saver('src/resource/data').load()
        if saver is None:
            mess = QMessageBox()
            mess.setWindowTitle("Сохраненная игра")
            mess.setText("Нет последней сохраненной игры")
            mess.setIcon(QMessageBox.Icon.Warning)
            mess.setStandardButtons(QMessageBox.StandardButton.Ok)
            mess.exec()
        else:
            game = GameScreen(saver[0], saver[1], saver[2])
            widget.addWidget(game)
            widget.setCurrentIndex(widget.currentIndex() + 1)

    def show_top_players(self) -> None:
        result, ok = QInputDialog().getInt(self, 'Топ для поля NxN',
                                           'Введите длину стороны поля (одно число)',
                                           0, 3)

        data = Saver('src/resource/top').load_top(result)
        if data is None and ok:
            mess = QMessageBox()
            mess.setWindowTitle("Размер поля")
            mess.setText("Для данного размера нет топа")
            mess.setIcon(QMessageBox.Icon.Warning)
            mess.setStandardButtons(QMessageBox.StandardButton.Ok)
            mess.exec()
        elif data is not None and ok:
            game = PlayersTopScreen(data)
            widget.addWidget(game)
            widget.setCurrentIndex(widget.currentIndex() + 1)


class NewGameScreen(QDialog):
    def __init__(self) -> None:
        super(NewGameScreen, self).__init__()

        self.WidthLabel = None
        self.HeightLabel = None
        self.FormComboBox = None
        self.LevelComboBox = None
        self.ErrorSizeLabel = None
        self.NameLineEdit = None
        self.BackButton = None
        self.StartNewGameButton = None
        loadUi("src/ui/NewGameScreen.ui", self)
        self.StartNewGameButton.clicked.connect(self.start_new_game)
        self.BackButton.clicked.connect(self.back)

    def start_new_game(self):
        """start new Game with selected parameters"""
        if not self.NameLineEdit.text():
            self.ErrorSizeLabel.setText("")
            Utils.create_message("Не хватает данных",
                                 "Пожалуйста, укажите свое имя")

        elif self.LevelComboBox.currentText() == "":
            self.ErrorSizeLabel.setText("")
            Utils.create_message("Не хватает данных",
                                 "Пожалуйста, выберите уровень сложности")

        elif self.FormComboBox.currentText() == "":
            self.ErrorSizeLabel.setText("")
            Utils.create_message("Не хватает данных",
                                 "Пожалуйста, выберите форму поля")
        elif self.HeightLabel.text() == "" or self.WidthLabel.text() == "":
            self.ErrorSizeLabel.setText("")
            Utils.create_message("Не хватает данных",
                                 "Пожалуйста, введите размеры поля")
        elif (self.FormComboBox.currentText() == "Квадрат" and
              self.HeightLabel.text() != self.WidthLabel.text()):
            self.ErrorSizeLabel.setText("")
            Utils.create_message("Ошибка ввода данных",
                                 f"Ваша форма поля - "
                                 f"{self.FormComboBox.currentText()}"
                                 f",\nВысота "
                                 f"и ширина поля должны быть одинаковыми!")

        elif (not Utils.is_digit(self.HeightLabel.text()) or
              not Utils.is_digit(self.WidthLabel.text()) or
              int(self.HeightLabel.text()) <= 2 or
              int(self.WidthLabel.text()) <= 2):

            self.ErrorSizeLabel.setText("Некорректный ввод")

        else:
            if widget.count() == 3:
                widget.removeWidget(GameScreen)
            game = GameScreen(Game(
                self.NameLineEdit.text(),
                self.LevelComboBox.currentText(),
                self.FormComboBox.currentText(),
                int(self.WidthLabel.text()),
                int(self.HeightLabel.text())))
            widget.addWidget(game)
            widget.setCurrentIndex(widget.currentIndex() + 1)

    def back(self):
        """go back to start window"""
        self.close()
        widget.removeWidget(self)


class PlayersTopScreen(QDialog):
    def __init__(self, data) -> None:
        super(PlayersTopScreen, self).__init__()

        self.BackButton = None
        self.tableWidget = None
        self.data = data
        loadUi("src/ui/PlayersTopScreen.ui", self)
        self.add_top_players()
        self.BackButton.clicked.connect(self.back)

    def add_top_players(self):
        for keys, values in self.data.items():
            self.data[keys] = int(values)

        sorted_values = sorted(self.data.values())
        sorted_dict = {}

        for value in sorted_values:
            for keys in self.data.keys():
                if self.data[keys] == value:
                    sorted_dict[keys] = self.data[keys]

        counter = 0
        for keys, values in sorted_dict.items():
            self.tableWidget.setItem(counter, 0, QTableWidgetItem(keys))
            self.tableWidget.setItem(counter, 1, QTableWidgetItem(str(values)))
            counter += 1
            if counter == 10:
                break

    def back(self):
        """go back to start window"""
        self.close()
        widget.removeWidget(self)


args_parser = ArgumentParser(description=Utils.loading(),
                             formatter_class=RawTextHelpFormatter)
args_parser.parse_args()

app = QApplication(argv)
welcome = WelcomeScreen()
widget = QStackedWidget()
widget.addWidget(welcome)
widget.setFixedWidth(1200)
widget.setFixedHeight(800)
widget.setWindowTitle('Numberlink')

widget.show()

try:
    exit(app.exec())
except SystemExit:
    print("Exiting")

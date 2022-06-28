from argparse import ArgumentParser, RawTextHelpFormatter
from sys import argv, exit

from PyQt6.uic import loadUi
from PyQt6.QtWidgets import *

from src.cell import Cell
from src.color import Color
from src.game import Game
from src.utils import Utils


class GameScreen(QMainWindow):
    def __init__(self, game) -> None:
        super(GameScreen, self).__init__()
        self.GameWidget = None
        self.ClicksLabel = None
        self.ResetButton = None
        self.NameLabel = None
        self.ExitButton = None
        loadUi("src/ui/GameScreen.ui", self)
        self.ExitButton.clicked.connect(self.exit_game)
        self.NameLabel.setText(game.user_name)

        self.ResetButton.clicked.connect(self.reset_game)
        self.ClicksLabel.setText('0')
        self.Game = game

        if Utils.best_score[game.field.size.height] == 1000000000000000000000000:
            self.ScoreLabel.setText("пока нет")
            Utils.best_current_size_score = "0"
        else:
            self.ScoreLabel.setText(str(Utils.best_score[game.field.size.height]))
            Utils.best_current_size_score = str(Utils.best_score[game.field.size.height])

        self.GameGrid = QGridLayout()

        Utils.current_color = Color(255, 255, 255)
        Utils.current_cell[0] = -1
        Utils.current_cell[1] = -1
        Utils.cells.clear()
        Utils.numbers_in_field.clear()
        Utils.start = ""
        Utils.color_collection.clear()
        Utils.curren_size = game.field.size.height
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
                c.append(Cell(self.Game.field.field[i][j],
                              self.ClicksLabel, j, i, self, widget))
            Utils.cells.append(c)

    @staticmethod
    def exit_game() -> None:
        """exit from the Game"""
        widget.close()

    def reset_game(self) -> None:
        """clean all cells and reset clicks count"""
        self.ClicksLabel.setText('0')
        Utils.start = ""
        Utils.finish = ""
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
        loadUi("src/ui/WelcomeScreen.ui", self)
        self.NewGameButton.clicked.connect(self.go_to_new_game)
        self.ExitButton.clicked.connect(self.exit_game)
        self.ContinueButton.clicked.connect(self.continue_game)

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
        mess = QMessageBox()
        mess.setWindowTitle("Недоступно")
        mess.setText("Сохранение и загрузка игр пока недоступны")
        mess.setIcon(QMessageBox.Icon.Information)
        mess.setStandardButtons(QMessageBox.StandardButton.Ok)
        mess.exec()


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


args_parser = ArgumentParser(description=Utils.loading(),
                             formatter_class=RawTextHelpFormatter)
args_parser.parse_args()

app = QApplication(argv)
welcome = WelcomeScreen()
widget = QStackedWidget()
widget.addWidget(welcome)
widget.setFixedWidth(1200)
widget.setFixedHeight(800)

widget.show()

try:
    exit(app.exec())
except SystemExit:
    print("Exiting")

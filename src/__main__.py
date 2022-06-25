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
    def __init__(self, game) -> None:
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
        self.ClicksLabel.setText('0')
        self.Game = game
        self.GameGrid = QGridLayout()

        self.CurrentColor = Color(255, 255, 255)
        self.create_cells()
        self.create_layout()

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
                              self.ClicksLabel))
            Utils.cells.append(c)

    def save(self):
        return Saver('src/resource/data').save(self.Game)

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
        saver = Saver('src/resource/data').load()
        if saver is None:
            mess = QMessageBox()
            mess.setWindowTitle("Сохраненная игра")
            mess.setText("Нет последней сохраненной игры")
            mess.setIcon(QMessageBox.Icon.Warning)
            mess.setStandardButtons(QMessageBox.StandardButton.Ok)
            mess.exec()
        else:
            game = GameScreen(saver)
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

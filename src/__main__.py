import sys

from PyQt6.uic import loadUi
from PyQt6.QtWidgets import (QDialog, QApplication, QStackedWidget,
                             QMessageBox, QMainWindow, QGridLayout)

from src.cell import Cell
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
        loadUi("ui/GameScreen.ui", self)
        self.ExitButton.clicked.connect(self.exit_game)
        self.NameLabel.setText(game.user_name)
        self.ResetButton.clicked.connect(self.reset_game)
        self.ClicksLabel.setText('0')
        self.Game = game
        self.GameGrid = QGridLayout()
        self.Cells = []
        self.create_cells()
        self.create_layout()

    def create_layout(self):
        grid_layout = QGridLayout()
        for i in range(0, self.Game.field.size.height):
            for j in range(0, self.Game.field.size.width):
                grid_layout.addWidget(self.Cells[i][j], i, j)

        self.GameGrid = grid_layout
        self.GameWidget.setLayout(grid_layout)

    def create_cells(self):
        for i in range(0, self.Game.field.size.height):
            c = []
            for j in range(0, self.Game.field.size.width):
                c.append(Cell(self.Game.field.field[i][j], self.ClicksLabel))
            self.Cells.append(c)

    @staticmethod
    def exit_game() -> None:
        widget.close()

    def reset_game(self) -> None:
        self.ClicksLabel.setText('0')

        # придумать, как адекватно сделать зачистку клеток
        for i in range(0, self.Game.field.size.height):
            for j in range(0, self.Game.field.size.width):
                self.Cells[i][j].clean_label()


class WelcomeScreen(QDialog):
    def __init__(self) -> None:
        super(WelcomeScreen, self).__init__()
        self.ContinueButton = None
        self.ExitButton = None
        self.NewGameButton = None
        loadUi("ui/WelcomeScreen.ui", self)
        self.NewGameButton.clicked.connect(self.go_to_new_game)
        self.ExitButton.clicked.connect(self.exit_game)
        self.ContinueButton.clicked.connect(self.continue_game)

    @staticmethod
    def go_to_new_game() -> None:
        new_game = NewGameScreen()
        widget.addWidget(new_game)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    @staticmethod
    def exit_game() -> None:
        widget.close()

    @staticmethod
    def continue_game() -> None:
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
        loadUi("ui/NewGameScreen.ui", self)
        self.StartNewGameButton.clicked.connect(self.start_new_game)
        self.BackButton.clicked.connect(self.back)

    def start_new_game(self):
        if self.NameLineEdit.text() == "":
            self.ErrorSizeLabel.setText("")
            Utils.create_message("Нехватает данных", "Пожалуйста, укажите свое имя")

        elif self.LevelComboBox.currentText() == "":
            self.ErrorSizeLabel.setText("")
            Utils.create_message("Нехватает данных", "Пожалуйста, выберите уровень сложности")

        elif self.FormComboBox.currentText() == "":
            self.ErrorSizeLabel.setText("")
            Utils.create_message("Нехватает данных", "Пожалуйста, выберите форму поля")
        elif self.HeightLabel.text() == "" or self.WidthLabel.text() == "":
            self.ErrorSizeLabel.setText("")
            Utils.create_message("Нехватает данных", "Пожалуйста, введите размеры поля")
        elif self.FormComboBox.currentText() == "Квадрат" and self.HeightLabel.text() != self.WidthLabel.text():
            self.ErrorSizeLabel.setText("")
            Utils.create_message("Ошибка ввода данных", f"Ваша форма поля - {self.FormComboBox.currentText()},\nВысота "
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
        self.close()
        widget.removeWidget(self)


app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QStackedWidget()
widget.addWidget(welcome)
widget.setFixedWidth(1200)
widget.setFixedHeight(800)

widget.show()

try:
    sys.exit(app.exec())
except SystemExit:
    print("Exiting")

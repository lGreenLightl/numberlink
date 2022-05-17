import sys
from PyQt6.uic import loadUi
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget, QMessageBox


class WelcomeScreen(QDialog):
    def __init__(self) -> None:
        super(WelcomeScreen, self).__init__()
        loadUi("../resource/WelcomeScreen.ui", self)
        self.NewGameButton.clicked.connect(self.go_to_new_game)
        self.ExitButton.clicked.connect(self.exit_game)
        self.ContinueButton.clicked.connect(self.continue_game)

    def go_to_new_game(self) -> None:
        new_game = NewGameScreen()
        widget.addWidget(new_game)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def exit_game(self) -> None:
        widget.close()

    def continue_game(self) -> None:
        mess = QMessageBox()
        mess.setWindowTitle("Недоступно")
        mess.setText("Сохранение и загрузка игр пока недоступны")
        mess.setIcon(QMessageBox.Icon.Information)
        mess.setStandardButtons(QMessageBox.StandardButton.Ok)
        mess.exec()


class NewGameScreen(QDialog):
    def __init__(self) -> None:
        super(NewGameScreen, self).__init__()
        loadUi("../resource/NewGameScreen.ui", self)


app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(800)
widget.setFixedWidth(1200)
widget.show()

try:
    sys.exit(app.exec())
except:
    print("Exiting")

# TODO: от Дани - добавить метод main и if __name__ == "__main__"

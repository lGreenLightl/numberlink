import random

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QLabel, QSizePolicy

from src.Color import Color


class Cell(QWidget):
    clicked = QtCore.pyqtSignal()

    def mousePressEvent(self, QMouseEvent):
        self.clicked.emit()

    def __init__(self, text, click_label):
        super(Cell, self).__init__()

        self.Color = Color(255, 255, 255)
        self.setStyleSheet(
            f"background-color:rgb({self.Color.Red}, {self.Color.Green}, {self.Color.Blue}); "
            f"border-radius: 20px;")
        #if text == ".":
        #    self.setText("")
        #else:
        #    self.setText(text)
        #self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ClickLabel = click_label
        self.clicked.connect(self.click_widget)





    def click_widget(self) -> None:
        self.increase_click_count()
        self.set_color()

    def clean_widget(self) -> None:
        self.Color = Color(255, 255, 255)
        self.setStyleSheet(
            f"background-color:rgb({self.Color.Red}, {self.Color.Green}, {self.Color.Blue}); "
            f"border-radius: 20px;")

    def increase_click_count(self) -> None:
        self.ClickLabel.setText(str(int(self.ClickLabel.text()) + 1))

    def set_color(self) -> None:
        #if self.text() == "":
            if self.Color == Color(255, 255, 255):
                color = self.random_choose_color()
            else:
                color = Color(255, 255, 255)
            self.Color = color
            self.setStyleSheet(
                f"background-color:rgb({self.Color.Red}, {self.Color.Green}, {self.Color.Blue}); "
                f"border-radius: 20px;")

    def random_choose_color(self) -> Color:
        red = random.randint(0, 254)
        green = random.randint(0, 254)
        blue = random.randint(0, 254)
        return Color(red, green, blue)

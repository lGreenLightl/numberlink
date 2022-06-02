import random

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QLabel, QSizePolicy

from src.Color import Color
from src.ColorCollection import in_collection, color_collection


class Cell(QLabel):
    clicked = QtCore.pyqtSignal()

    def mousePressEvent(self, QMouseEvent):
        self.clicked.emit()

    def __init__(self, text, click_label):
        super(Cell, self).__init__()

        self.Color = Color(255, 255, 255)
        self.setStyleSheet(
            f"background-color:rgb({self.Color.Red}, {self.Color.Green}, {self.Color.Blue}); "
            f"border-radius: 20px; font: 75 20pt \"MS Shell Dlg 2\";color:rgb(67, 65, 49);")
        if text == ".":
            self.setText("")
        else:
            self.setText(text)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ClickLabel = click_label
        self.clicked.connect(self.click_label)


    def click_label(self) -> None:
        self.increase_click_count()
        self.set_color()

    def clean_label(self) -> None:
        self.Color = Color(255, 255, 255)
        self.setStyleSheet(
            f"background-color:rgb({self.Color.Red}, {self.Color.Green}, {self.Color.Blue}); "
            f"border-radius: 20px; font: 75 20pt \"MS Shell Dlg 2\";color:rgb(67, 65, 49);")

    def increase_click_count(self) -> None:
        self.ClickLabel.setText(str(int(self.ClickLabel.text()) + 1))

    def set_color(self) -> None:
        if self.text() == "":
            if self.Color == Color(255, 255, 255):
                color = self.random_choose_color()
                if in_collection(color):
                    color = self.random_choose_color()
            else:
                color_collection.remove(self.Color)
                color = Color(255, 255, 255)
            self.Color = color
            self.setStyleSheet(
                f"background-color:rgb({self.Color.Red}, {self.Color.Green}, {self.Color.Blue}); "
                f"border-radius: 20px; font: 75 20pt \"MS Shell Dlg 2\";color:rgb(67, 65, 49);")

    def random_choose_color(self) -> Color:
        red = random.randint(0, 254)
        green = random.randint(0, 254)
        blue = random.randint(0, 254)
        return Color(red, green, blue)
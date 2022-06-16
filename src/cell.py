from random import randint

from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel

from src.color import Color
from src.utils import Utils


class Cell(QLabel):
    clicked = QtCore.pyqtSignal()

    def mousePressEvent(self, q_mouse_event):
        """extension for the label to track clicks on it"""
        self.clicked.emit()

    def __init__(self, text, click_label):
        super(Cell, self).__init__()

        self.color = Color(255, 255, 255)
        self.setStyleSheet(
            f"background-color:rgb"
            f"({self.color.red}, {self.color.green}, {self.color.blue}); "
            f"border-radius: 20px; font: 75 20pt "
            f"\"MS Shell Dlg 2\";color:rgb(67, 65, 49);")
        if text == ".":
            self.setText("")
        else:
            self.setText(text)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ClickLabel = click_label
        self.clicked.connect(self.click_label)

    def click_label(self) -> None:
        """increase click count and change label color"""
        self.increase_click_count()
        self.set_color()

    def clean_label(self) -> None:
        """remove label color"""
        self.color = Color(255, 255, 255)
        self.setStyleSheet(
            f"background-color:rgb"
            f"({self.color.red}, {self.color.green}, {self.color.blue}); "
            f"border-radius: 20px; font: 75 20pt "
            f"\"MS Shell Dlg 2\";color:rgb(67, 65, 49);")

    def increase_click_count(self) -> None:
        """increase click count"""
        self.ClickLabel.setText(str(int(self.ClickLabel.text()) + 1))

    def set_color(self) -> None:
        """set color to label"""
        if self.color == Color(255, 255, 255):
            color = self.random_choose_color()
            if Utils.in_collection(color):
                color = self.random_choose_color()
        else:
            Utils.color_collection.remove(self.color)
            color = Color(255, 255, 255)
        self.color = color
        self.setStyleSheet(
            f"background-color:rgb"
            f"({self.color.red}, {self.color.green}, {self.color.blue}); "
            f"border-radius: 20px; font: 75 20pt "
            f"\"MS Shell Dlg 2\";color:rgb(67, 65, 49);")

    @staticmethod
    def random_choose_color() -> Color:
        """generate random color for label"""
        red = randint(0, 254)
        green = randint(0, 254)
        blue = randint(0, 254)
        return Color(red, green, blue)

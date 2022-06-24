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
        if self.text() != "":
            if Utils.start == "" and self.color == Color(255, 255, 255):
                Utils.start = self.text()

            self.set_color()

        else:
            self.cancel_choice(self.color)

    @staticmethod
    def cancel_choice(c) -> None:
        Utils.start = ""
        if c != Color(255, 255, 255):
            Utils.current_color = Color(255, 255, 255)
            for i in range(0, len(Utils.cells)):
                for j in range(0, len(Utils.cells[i])):
                    if Utils.cells[i][j].color == c:
                        Utils.cells[i][j].color = Color(255, 255, 255)
                        Utils.cells[i][j].setStyleSheet(
                            f"background-color:rgb"
                            f"(255, 255, 255); "
                            f"border-radius: 20px; font: 75 20pt "
                            f"\"MS Shell Dlg 2\";color:rgb(67, 65, 49);")

    def enterEvent(self, e):
        if Utils.current_color != Color(255, 255, 255) \
                and self.color == Color(255, 255, 255) \
                and (self.text() == "" or self.text() == Utils.start):
            self.color = Color(Utils.current_color.red,
                               Utils.current_color.green,
                               Utils.current_color.blue)
            self.setStyleSheet(
                f"background-color:rgb"
                f"({Utils.current_color.red}, "
                f"{Utils.current_color.green}, "
                f"{Utils.current_color.blue}); "
                f"border-radius: 20px; font: 75 20pt "
                f"\"MS Shell Dlg 2\";color:rgb(67, 65, 49);")
            if self.text() == Utils.start:
                Utils.current_color = Color(255, 255, 255)
                Utils.start = ""

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
            if Utils.is_in_collection(color):
                color = self.random_choose_color()
            self.color = color
            Utils.current_color = color
            self.setStyleSheet(
                f"background-color:rgb"
                f"({self.color.red}, {self.color.green}, {self.color.blue}); "
                f"border-radius: 20px; font: 75 20pt "
                f"\"MS Shell Dlg 2\";color:rgb(67, 65, 49);")

        else:
            self.cancel_choice(self.color)

    @staticmethod
    def random_choose_color() -> Color:
        """generate random color for label"""
        red = randint(0, 254)
        green = randint(0, 254)
        blue = randint(0, 254)
        return Color(red, green, blue)

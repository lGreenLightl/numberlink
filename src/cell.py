from random import randint

from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QMessageBox

from src.color import Color
from src.saver import Saver
from src.utils import Utils


class Cell(QLabel):
    clicked = QtCore.pyqtSignal()

    def mousePressEvent(self, q_mouse_event):
        """extension for the label to track clicks on it"""
        self.clicked.emit()

    def __init__(self, text, click_label, x, y, screen, w,
                 red=255, green=255, blue=255):
        super(Cell, self).__init__()

        self.color = Color(red, green, blue)
        self.X = x
        self.Y = y
        self.start = False
        self.screen = screen
        self.widget = w

        self.setStyleSheet(
            f"background-color:rgb"
            f"({self.color.red}, {self.color.green}, {self.color.blue}); "
            f"border-radius: 20px; font: 75 20pt "
            f"\"MS Shell Dlg 2\";color:rgb(67, 65, 49);")
        if not Utils.is_digit(text):
            self.setText("")
        else:
            self.setText(text)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ClickLabel = click_label
        self.clicked.connect(self.click_label)

    def click_label(self) -> None:
        """increase click count, change label color, set start, if it as possible"""
        self.increase_click_count()

        if self.text() != "":
            if Utils.current_color == self.color and \
                    self.text() == Utils.start and not self.start:
                if Utils.finish == "true":
                    Utils.current_color = Color(255, 255, 255)
                    Utils.start = ""
                    Utils.finish = "empty"
                    Utils.current_cell[0] = -1
                    Utils.current_cell[1] = -1
                    Utils.numbers_in_field[self.text()] = True
                    for i in range(0, len(Utils.cells)):
                        for j in range(0, len(Utils.cells[i])):
                            Utils.cells[i][j].start = False
                    ok = True
                    for num in Utils.numbers_in_field:
                        if not Utils.numbers_in_field[num]:
                            ok = False
                            break

                    if ok:
                        self.preparing_for_new_game()
                else:
                    self.cancel_choice(self.color)

            else:
                if Utils.start != "":
                    self.cancel_choice(Utils.current_color)

                if Utils.start == "" and self.color == Color(255, 255, 255):
                    Utils.start = self.text()
                    self.start = True

                    Utils.current_cell[0] = self.X
                    Utils.current_cell[1] = self.Y

                if Utils.current_color == Color(255, 255, 255):
                    self.set_color()

        else:
            color = Utils.current_color
            self.cancel_choice(self.color)
            self.cancel_choice(color)

    @staticmethod
    def cancel_choice(c) -> None:
        """end color session"""
        Utils.start = ""
        Utils.finish = "empty"
        Utils.current_cell[0] = -1
        Utils.current_cell[1] = -1

        if c != Color(255, 255, 255):
            Utils.current_color = Color(255, 255, 255)
            for i in range(0, len(Utils.cells)):
                for j in range(0, len(Utils.cells[i])):
                    if Utils.cells[i][j].color == c:
                        Utils.cells[i][j].color = Color(255, 255, 255)
                        Utils.cells[i][j].start = False
                        Utils.cells[i][j].setStyleSheet(
                            f"background-color:rgb"
                            f"(255, 255, 255); "
                            f"border-radius: 20px; font: 75 20pt "
                            f"\"MS Shell Dlg 2\";color:rgb(67, 65, 49);")

                        if Utils.cells[i][j].text() != "":
                            Utils.numbers_in_field[Utils.cells[i][j].text()] = False

    def check_cell(self) -> bool:
        """check, if this cell can be pained"""
        cur_x = Utils.current_cell[0]
        cur_y = Utils.current_cell[1]
        x = self.X
        y = self.Y
        length = len(Utils.cells) - 1

        if y == 0:
            if x == 0:
                if ((cur_x == x + 1 and cur_y == y)
                        or (cur_x == x and cur_y == y + 1)):
                    return True
                return False

            elif x == length:
                if ((cur_x == x - 1 and cur_y == y)
                        or (cur_x == x and cur_y == y + 1)):
                    return True
                return False

            else:
                if ((cur_x == x + 1 and cur_y == y)
                        or (cur_x == x and cur_y == y + 1)
                        or (cur_x == x - 1 and cur_y == y)):
                    return True
                return False

        elif y == length:
            if x == 0:
                if ((cur_x == x + 1 and cur_y == y)
                        or (cur_x == x and cur_y == y - 1)):
                    return True
                return False

            elif x == length:
                if ((cur_x == x - 1 and cur_y == y)
                        or (cur_x == x and cur_y == y - 1)):
                    return True
                return False

            else:
                if ((cur_x == x + 1 and cur_y == y)
                        or (cur_x == x and cur_y == y - 1)
                        or (cur_x == x - 1 and cur_y == y)):
                    return True
                return False
        else:

            if x == 0:
                if ((cur_x == x + 1 and cur_y == y)
                        or (cur_x == x and cur_y == y - 1)
                        or (cur_x == x and cur_y == y + 1)):
                    return True
                return False
            elif x == length:
                if ((cur_x == x - 1 and cur_y == y)
                        or (cur_x == x and cur_y == y - 1)
                        or (cur_x == x and cur_y == y + 1)):
                    return True
                return False
            else:
                if ((cur_x == x - 1 and cur_y == y)
                        or (cur_x == x + 1 and cur_y == y)
                        or (cur_x == x and cur_y == y - 1)
                        or (cur_x == x and cur_y == y + 1)):
                    return True
                return False

    def enterEvent(self, e):
        """set color to label, when pointing the mouse"""
        if Utils.current_color != Color(255, 255, 255) \
                and self.color == Color(255, 255, 255) \
                and (self.text() == "" or self.text() == Utils.start) \
                and self.check_cell():

            if Utils.finish == "true":
                Utils.finish = "false"

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

            Utils.current_cell[0] = self.X
            Utils.current_cell[1] = self.Y

        if self.text() == Utils.start and not self.start and \
                self.color == Utils.current_color \
                and Utils.finish == "empty" \
                and Utils.current_color != Color(255, 255, 255):
            Utils.finish = "true"

    def preparing_for_new_game(self):
        Saver('src/resource/top').save_score(Utils.current_name,
                                             Utils.current_size,
                                             self.ClickLabel.text())

        mess = QMessageBox()
        mess.setWindowTitle("ПОБЕДА!")
        m = ""

        if Utils.best_current_size_score == "0" or \
                int(Utils.best_current_size_score) > int(self.ClickLabel.text()):
            m = "У вас новый лучший счет для текущего размера!\n"
            Utils.best_score[Utils.current_size] = int(self.ClickLabel.text())

        mess.setText("Поздравляю с победой!\n" + m + "Хотите сыграть снова?")
        mess.setIcon(QMessageBox.Icon.Question)
        mess.setStandardButtons(QMessageBox.StandardButton.Yes |
                                QMessageBox.StandardButton.No)
        button = mess.exec()

        if button == QMessageBox.StandardButton.Yes:
            self.screen.close()
            self.widget.removeWidget(self.screen)

        else:
            self.widget.close()

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

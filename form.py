import sys

import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit
from PyQt5.QtCore import QSize, Qt

import sudoku


class MainWindow(QMainWindow):
    def __init__(self):

        QMainWindow.__init__(self)

        self.setFixedSize(QSize(210, 230))
        self.setWindowTitle("Судоку")

        self.button_calculate = QPushButton('Calculate', self)
        self.button_calculate.clicked.connect(self.solver)

        self.elements = []
        for _ in range(81):
            self.elements.append(QLineEdit(self))
            self.elements[-1].setAlignment(Qt.AlignCenter)
            self.elements[-1].setMaxLength(1)

        self.placement_of_elements()

    def placement_of_elements(self):
        for i, item in enumerate(self.elements):
            x = i % 9
            y = i // 9
            item.move(20*x + 10 + 5 * int(x // 3), 20*y + 10 + 5 * int(y // 3))
            item.resize(20, 20)

        self.button_calculate.move(10, 205)
        self.button_calculate.resize(190, 20)

    def solver(self):
        data = [element.text() for element in self.elements]
        data = np.array([(int(val) if val else 0) for val in data]).reshape((9, 9))

        answer, err = sudoku.rec_sudoku(data)
        if not err:
            for i in range(9):
                for j in range(9):
                    element = self.elements[i * 9 + j]
                    if not element.text():
                        element.setText(str(answer[i, j]))

    def keyPressEvent(self, e):
        if int(e.modifiers()) == (Qt.AltModifier + Qt.ControlModifier):
            for item in self.elements:
                item.setText('')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    start_form = MainWindow()
    start_form.show()
    sys.exit(app.exec())

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QWidget


class GoBoard(QWidget):
    def __init__(self, size=7):
        super().__init__()
        self.size = size
        self.setFixedSize(600, 600)
        self.setWindowTitle('Go Board')

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw_board(qp)
        qp.end()

    def draw_board(self, qp):
        cell_size = self.width() // self.size
        for row in range(self.size):
            for col in range(self.size):
                qp.drawRect(col * cell_size, row * cell_size,
                            cell_size, cell_size)
                if (row + col) % 2 == 0:
                    qp.fillRect(col * cell_size, row * cell_size,
                                cell_size, cell_size, Qt.GlobalColor.white)
                else:
                    qp.fillRect(col * cell_size, row * cell_size,
                                cell_size, cell_size, Qt.GlobalColor.black)

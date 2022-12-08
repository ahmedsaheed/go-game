from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QApplication, QWidget


class GoBall(QWidget):
    def __init__(self, x=10, y=10):
        super().__init__()
        self.x = x
        self.y = y

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw_balls(qp)
        qp.end()

    def draw(self, qp):
        qp.drawEllipse(self.x, self.y, 20, 20)

    def draw_balls(self, qp):
        for i in range(40):
            self.draw(qp)



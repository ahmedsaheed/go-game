from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QApplication, QWidget

from code.go_board import GoBoard


# create a class to draw the balls

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

    # draw 40 balls
    def draw_balls(self, qp):
        for i in range(40):
            self.draw(qp)


if __name__ == '__main__':
    app = QApplication([])
    board = GoBoard()
    board.show()
    balls = GoBall()
    balls.show()
    app.exec()

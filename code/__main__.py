from PyQt6.QtWidgets import QApplication
from go_board import GoBoard
from go_balls import GoBall
import sys

app = QApplication([])
newBoard = GoBoard()
newBoard.show()
balls = GoBall()
#balls.show()
sys.exit(app.exec())

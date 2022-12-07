from PyQt6.QtWidgets import QApplication
from go import Go
from go_board import GoBoard
import sys

app = QApplication([])
#myGo = Go()
newBoard = GoBoard()
sys.exit(app.exec())

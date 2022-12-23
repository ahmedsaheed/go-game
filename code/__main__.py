from PyQt6.QtWidgets import QApplication
from go import Go
import sys

app = QApplication([])
go = Go()
go.show()
sys.exit(app.exec())

from PyQt6 import QtCore
from PyQt6.QtWidgets import QMainWindow, QStatusBar
from PyQt6.QtCore import Qt
from board import Board
from score_board import ScoreBoard


class Go(QMainWindow):

    def __init__(self):
        super().__init__()
        self.statusBar = None
        self.board = None
        self.scoreBoard = None
        self.initUI()

    def getBoard(self):
        return self.board


    def getScoreBoard(self):
        return self.scoreBoard

    def initUI(self):
        self.board = Board(self)
        self.setCentralWidget(self.board)
        self.board.setContentsMargins(10, 10, 10, 10)   # pad the board
        self.scoreBoard = ScoreBoard()
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.scoreBoard)
        self.scoreBoard.make_connection(self.board)
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.minimumHeight()
        self.resize(850, 850)
        self.setMinimumWidth(750)
        self.setMinimumHeight(650)
        self.center()
        self.setWindowTitle('Go')
        self.show()

    def center(self):
        '''centers the window on the screen'''
        gr = self.frameGeometry()
        screen = self.screen().availableGeometry().center()

        gr.moveCenter(screen)
        self.move(gr.topLeft())
        size = self.geometry()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_R:
            self.getBoard().resetGame()
            self.update()
        if event.key() == QtCore.Qt.Key.Key_P:
            if self.getBoard().skipTurn():
                self.close()
            self.update()

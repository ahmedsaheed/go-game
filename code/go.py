from PyQt6 import QtCore
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QMainWindow, QStatusBar, QMessageBox
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
        self.board.setStyleSheet(
            """
               
                 padding:0px;
                 
                
            """
        )
       # self.board.setContentsMargins(10, 10, 10, 10)  # pad the board
        self.scoreBoard = ScoreBoard()
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.scoreBoard)
        # self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.scoreBoard)
        self.scoreBoard.make_connection(self.board)
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.resize(850, 850)
        self.setMinimumWidth(750)
        self.setMinimumHeight(650)
        self.center()
        self.setWindowTitle('Go')
        self.menu()
        self.show()

    def center(self):
        '''centers the window on the screen'''
        gr = self.frameGeometry()
        screen = self.screen().availableGeometry().center()

        gr.moveCenter(screen)
        self.move(gr.topLeft())
        size = self.geometry()

    def menu(self):
        # set up menus
        mainMenu = self.menuBar()  # create and a menu bar
        # main menu stylesheet
        mainMenu.setStyleSheet(
            """
                 width: 100%; 
                 padding:10px;
                 padding-left:130px;
                 text-align: center; 
                 font-size: 15px;
                 font-family:Lucida Sans;
                 background: #f5f3f0;
                
               } 
               helpMenu
            """
        )
        # skip menu
        skipAction = QAction("Skip Turn", self)
        skipAction.setShortcut("Ctrl+S")  # set shortcut
        passMenu = mainMenu.addAction(skipAction)
        skipAction.triggered.connect(self.click)

        # reset
        resetAction = QAction("Reset", self)
        resetAction.setShortcut("Ctrl+R")  # set shortcut
        resetAction.triggered.connect(self.board.resetGame)
        resetMenu = mainMenu.addAction(resetAction)

        # help menu
        helpAction = QAction("Help", self)
        helpAction.setShortcut("Ctrl+H")  # set shortcut
        helpMenu = mainMenu.addAction(helpAction)
        helpAction.triggered.connect(self.help)

        # About Menu
        aboutAction = QAction(QIcon("./icons/about.png"), "About", self)
        aboutAction.setShortcut("Ctrl+A")
        aboutMenu = mainMenu.addAction(aboutAction)  # connect the action to the function below
        aboutAction.triggered.connect(self.about)

        # exit menu
        exitAction = QAction("Exit", self)
        exitAction.setShortcut("Ctrl+E")  # set shortcut
        exitMenu = mainMenu.addAction(exitAction)
        exitAction.triggered.connect(self.exit)

        # help message display rules

    def help(self):
        msg = QMessageBox()
        msg.setText(
            "<p><strong>How to play go</strong></p> "
            "<p><strong>Rules: </strong></p>"
            "<p>A game of Go starts with an empty board. Each player has an effectively unlimited supply of pieces ("
            "called balls), one taking the black piece, the other taking white. The main object of the game is to "
            "use your pieces to form territories by surrounding vacant areas of the board. It is also possible to "
            "capture your opponent's pieces by completely surrounding them..</p> "

            "<p>Players take turns, placing one of their pieces on a vacant point at each turn, with Black playing "
            "first. Note that piece are placed on the intersections of the lines rather than in the squares and once "
            "played pieces are not moved. However they may be captured, in which case they are removed from the "
            "board, and kept by the capturing player as prisoners.</p> "

            "<br><strong> press ( Ctrl + E ) to Exit <br>"
            "<br><strong> press ( Ctrl + S ) to Skip Turn <br>"
            "<br><strong> press ( Ctrl + R ) or Reset <br>"

        )
        msg.setWindowTitle("Help")
        msg.exec()

    def about(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("About")
        msg.setText("ABOUT GO game")
        msg.setText("Go game v1.0\n\n@2022 ApexPlayground, SaheedCodes. All rights reserved")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.show()

        # exit function

    def exit(self):
        QtCore.QCoreApplication.quit()

    # click method for pass
    def click(self):
        if self.getBoard().changeturn():  # link to board to change turn
            self.close()
        self.update()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_R:
            self.getBoard().resetGame()
            self.update()
        if event.key() == QtCore.Qt.Key.Key_P:
            if self.getBoard().skipTurn():
                self.close()
            self.update()

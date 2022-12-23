from PyQt6 import QtCore
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QDockWidget, QWidget
from PyQt6.QtCore import Qt
from code.board import Board
from score_board import ScoreBoard


class Go(QMainWindow):

    def __init__(self):
        super().__init__()
        self.board = None
        self.scoreBoard = None
        self.initUI()

    def getBoard(self):
        return self.board

    def getScoreBoard(self):
        return self.scoreBoard

    def initUI(self):
        '''initiates application UI'''
        self.board = Board(self)
        # add padding to the board
        self.board.setContentsMargins(10, 10, 10, 10)
        self.setCentralWidget(self.board)
        self.scoreBoard = ScoreBoard()
        self.scoreBoard.setContentsMargins(10, 10, 10, 10)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.scoreBoard)
        # remove the dock title bar
        self.scoreBoard.setTitleBarWidget(QWidget())
        # make the dock widget unmovable
        self.scoreBoard.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.scoreBoard.setMaximumWidth(150)
        self.scoreBoard.make_connection(self.board)
        self.resize(800, 800)
        self.setMinimumSize(800, 700)
        self.center()
        self.setWindowTitle('Go')

        self.show()

    def center(self):
        '''centers the window on the screen'''
        gr = self.frameGeometry()
        screen = self.screen().availableGeometry().center()

        gr.moveCenter(screen)
        self.move(gr.topLeft())
        # size = self.geometry()
        # self.move((screen.width() - size.width()) / 2,(screen.height() - size.height()) / 2)

    def menu(self):
        # set up menus
        mainMenu = self.menuBar()  # create and a menu bar
        # main menu stylesheet
        mainMenu.setStyleSheet(
            """
                 width: 100%; 
                 padding:10px;
                 text-align: center; 
                 font-size: 15px;
                 font-family:Lucida Sans;
                 background: #D3D3D3;
                 border: 1px solid
               } 
               helpMenu
            """
        )
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
        mainMenu.show()

        # help message display rules

    def help(self):
        msg = QMessageBox()
        msg.setText(
            "<p><strong>How to play go</strong></p> "
            "<p><strong>Rules: </strong></p>"
            "<p>A game of Go starts with an empty board. Each player has an effectively unlimited supply of pieces ("
            "called stones), one taking the black stones, the other taking white. The main object of the game is to "
            "use your stones to form territories by surrounding vacant areas of the board. It is also possible to "
            "capture your opponent's stones by completely surrounding them..</p> "

            "<p>Players take turns, placing one of their stones on a vacant point at each turn, with Black playing "
            "first. Note that stones are placed on the intersections of the lines rather than in the squares and once "
            "played stones are not moved. However they may be captured, in which case they are removed from the "
            "board, and kept by the capturing player as prisoners.</p> "

            "<br><strong> press ( Ctrl + E ) or Exit <br>"

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
        if self.getBoard().passEvent():  # link to board to count passcount and change turn
            self.close()
        self.update()

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QLabel, QDialog, QFrame
from PyQt6.QtCore import pyqtSlot
from piece import Piece


class ScoreBoard(QDockWidget):

    def __init__(self):
        super().__init__()
        self.modal = None
        self.label_PrisonersBlack = None
        self.timerLeft = None
        self.player_turn = None
        self.clicker = None
        self.instructions = None
        self.mainLayout = None
        self.mainWidget = None
        self.initUI()

    def initUI(self):
        # Score board init
        self.resize(200, 200)
        self.setFixedWidth(200)
        self.center()
        self.setWindowTitle('ScoreBoard')
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()

        # create two labels which will be updated by signals
        self.instructions = QLabel("Instructions\n 1. Click any where to place"
                                   "\n a stone \n 2. Press P to pass a turn \n 3. Press R to reset the Game")

        self.player_turn = QLabel("Current Turn: ")
        self.clicker = QLabel("Click Location: ")
        self.timerLeft = QLabel("Time remaining: ")
        self.label_PrisonersBlack = QLabel("Prisoners Taken by Black: ")
        self.label_PrisonersWhite = QLabel("Prisoners Taken by White: ")
        self.label_TerritoriesBlack = QLabel("Territories Taken by Black: ")
        self.label_TerritoriesWhite = QLabel("Territories Taken by White: ")
        col = QColor(Qt.GlobalColor.white)
        self.frm = QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: %s }"
                               % col.name())
        self.frm.setGeometry(20, 20, 100, 100)

        self.mainWidget.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.instructions)
        self.mainLayout.addWidget(self.player_turn)
        self.mainLayout.addWidget(self.frm)
        # self.mainLayout.addWidget(self.passbutton)
        self.mainLayout.addWidget(self.clicker)
        self.mainLayout.addWidget(self.timerLeft)
        self.mainLayout.addWidget(self.label_PrisonersBlack)
        self.mainLayout.addWidget(self.label_PrisonersWhite)
        self.mainLayout.addWidget(self.label_TerritoriesBlack)
        self.mainLayout.addWidget(self.label_TerritoriesWhite)

        self.setWidget(self.mainWidget)
        self.show()

    def center(self):
        '''centers the window on the screen, you do not need to implement this method'''

    def make_connection(self, board):
        '''this handles a signal sent from the board class'''
        # when the clickLocationSignal is emitted in board the setClickLocation slot receives it
        board.listenToClick.connect(self.setClickLocation)
        # when the updateTimerSignal is emitted in the board the setTimeRemaining slot receives it
        board.listenToTime.connect(self.setTimeRemaining)
        # when the updatePrionersSignal is emitted in the board the updatePrisoners slot receives it
        board.captives.connect(self.updatePrisoners)
        board.territories.connect(self.updateTerritories)
        board.notifier.connect(self.displaynotification)
        board.playerTurn.connect(self.updateturn)

    @pyqtSlot(str)  # checks to make sure that the following slot is receiving an argument of the type 'int'
    def setClickLocation(self, clickLoc):
        '''updates the label to show the click location'''
        self.clicker.setText("Click Location:\n" + clickLoc)
        # print('slot ' + clickLoc)

    @pyqtSlot(int)
    def setTimeRemaining(self, timeRemainng):
        '''updates the time remaining label to show the time remaining'''
        update = "Time Remaining:" + str(timeRemainng)
        self.timerLeft.setText(update)

    # print('slot '+update)
    # self.redraw()


    def updateturn(self, Piece):
        if (Piece == 1):
            self.player_turn.setText("Current Turn: White")
            self.frm.setStyleSheet("QWidget { background-color: %s }"
                                   % QColor(Qt.GlobalColor.white).name())
        elif (Piece == 2):
            self.player_turn.setText("Current Turn: Black")
            self.frm.setStyleSheet("QWidget { background-color: %s }"
                                   % QColor(Qt.GlobalColor.black).name())


    def updatePrisoners(self, n, Player):
        if (Player == Piece.Black):
            update = "Prisoners Taken by Black: " + n
            self.label_PrisonersBlack.setText(update)

        elif (Player == Piece.White):
            update = "Prisoners Taken by White: " + n
            self.label_PrisonersWhite.setText(update)


    def updateTerritories(self, n, Player):
        if (Player == Piece.Black):
            update = "Territories Taken by Black: " + n
            self.label_TerritoriesBlack.setText(update)

        elif (Player == Piece.White):
            update = "Territories Taken by White: " + n
            self.label_TerritoriesWhite.setText(update)


    def passevent(self):
        print("Pass clicked")


    def displaynotification(self, message):
        dialog = QDialog(self)
        dialog.setFixedWidth(300)

        dialog.setWindowTitle("Notification")
        self.modal = QVBoxLayout()
        self.modal.addWidget(QLabel(message))
        dialog.setLayout(self.modal)
        dialog.exec()


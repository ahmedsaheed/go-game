from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import Qt, QBasicTimer, pyqtSignal, QPointF, QPoint
from PyQt6.QtGui import QPainter, QBrush, QColor
from PyQt6.QtTest import QTest
from piece import Piece


class Board(QFrame):  # base the board on a QFrame widget
    updateTimerSignal = pyqtSignal(int)  # signal sent when timer is updated
    clickLocationSignal = pyqtSignal(str)  # signal sent when there is a new click location

    # TODO set the board width and height to be square
    boardWidth = 7  # board width set to 7
    boardHeight = 7  # board height set to 7
    timerSpeed = 1000  # the timer updates every 1 second
    counter = 90 # countdown set to 90 seconds

    def __init__(self, parent):
        super().__init__(parent)
        self.isStarted = None
        self.timer = None
        self.boardArray = None
        self.initBoard()

    def initBoard(self):
        """initiates board"""
        self.timer = QBasicTimer()  # create a timer for the game
        self.isStarted = False  # game is not currently started
        self.start()  # start the game which will start the timer

        self.boardArray = [[Piece(Piece.NoPiece,i,j) for i in range(self.boardWidth)] for j in range(self.boardHeight)]  #2d array that stores the state of the game
        self.printBoardArray()  # TODO - uncomment this method after creating the array above

    def printBoardArray(self):
        """prints the boardArray in an attractive way"""
        print("boardArray:")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.boardArray]))

    def mousePosToColRow(self, event):
        """convert the mouse click event to a row and column"""

    def squareWidth(self):
        """returns the width of one square in the board"""
        return self.contentsRect().width() / self.boardWidth

    def squareHeight(self):
        """returns the height of one square of the board"""
        return self.contentsRect().height() / self.boardHeight

    def start(self):
        """starts game"""
        self.isStarted = True  # set the boolean which determines if the game has started to TRUE
        self.resetGame()  # reset the game
        self.timer.start(self.timerSpeed, self)  # start the timer with the correct speed
        print("start () - timer is started")

    def timerEvent(self, event):
        """this event is automatically called when the timer is updated. based on the timerSpeed variable """
        # TODO adapt this code to handle your timers
        if event.timerId() == self.timer.timerId():  # if the timer that has 'ticked' is the one in this class
            if Board.counter == 0:
                print("Game over")
            self.counter -= 1
            print('timerEvent()', self.counter)
            self.updateTimerSignal.emit(self.counter)
        else:
            super(Board, self).timerEvent(event)  # if we do not handle an event we should pass it to the super
            # class for handling

    def paintEvent(self, event):
        """paints the board and the pieces of the game"""
        painter = QPainter(self)
        self.drawBoardSquares(painter)
        # self.drawPieces(painter)

    def mousePressEvent(self, event):
        """this event is automatically called when the mouse is pressed"""
        clickLoc = "click location [" + str(event.position().x()) + "," + str(
            event.position().y()) + "]"  # the location where a mouse click was registered
        print("mousePressEvent() - " + clickLoc)
        # TODO you could call some game logic here
        self.clickLocationSignal.emit(clickLoc)

    def resetGame(self):
        """clears pieces from the board"""
        # TODO write code to reset game

    def tryMove(self, newX, newY):
        """tries to move a piece"""

    def drawBoardSquares(self, painter):
        """draw all the square on the board"""
        # setting the default colour of the brush
        color1 = QColor(209, 179, 141)  # yellowish brown
        color2 = QColor(196, 164, 132)  # light brown color
        brush = QBrush(Qt.BrushStyle.SolidPattern)  # calling SolidPattern to a variable
        brush.setColor(color1)  # setting color to black
        painter.setBrush(brush)
        for row in range(0, Board.boardHeight):
            for col in range(0, Board.boardWidth):
                painter.save()
                colTransformation = self.squareWidth() * col  # setting this value equal the transformation in the
                # column direction
                rowTransformation = self.squareHeight() * row  # setting this value equal the transformation in the
                # row direction
                painter.translate(colTransformation, rowTransformation)
                painter.fillRect(col, row, round(self.squareWidth()), round(self.squareHeight()), brush) # passing
                # the above variables and methods as a parameter
                painter.restore()

                # changing the colour of the brush so that a checkered board is drawn
                if brush.color() == color1:  # if the brush color of square is color1
                    brush.setColor(color2)  # set the next color of the square to color2
                else:  # if the brush color of square is color2
                    brush.setColor(color1)  # set the next color of the square to color1

    def drawPieces(self, painter):
        """draw the prices on the board"""
        colour = Qt.GlobalColor.transparent  # empty square could be modeled with transparent pieces
        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                painter.save()
                ''' the string translate() method returns a string where each row and col is mapped to 
                its corresponding character in the translation table '''
                painter.translate(((self.squareWidth()) * row) + self.squareWidth() / 2,
                                  (self.squareHeight()) * col + self.squareHeight() / 2)
                color = QColor(0, 0, 0)  #  color set to unspecified

                if self.boardArray[col][row].Piece == Piece.NoPiece:  # if piece in array == 0
                    color = QColor(Qt.GlobalColor.transparent)  # color is transparent

                elif self.boardArray[col][row].Piece == Piece.Black:  # if piece in array == 1
                    color = QColor(Qt.GlobalColor.black)  # set color to black

                elif self.boardArray[col][row].Piece == Piece.White:  # if piece in array == 2
                    color = QColor(Qt.GlobalColor.white)  # set color to white

                painter.setPen(color)  # set pen color to painter
                painter.setBrush(color)  # set brush color to painter
                radius = (self.squareWidth()) / 2
                center = QPoint(radius, radius)
                painter.drawEllipse(center, radius, radius)
                painter.restore()
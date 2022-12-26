from collections import namedtuple
from copy import copy

from PyQt6.QtWidgets import QFrame, QStatusBar, QMessageBox
from PyQt6.QtCore import Qt, QBasicTimer, pyqtSignal, QPoint
from PyQt6.QtGui import QPainter, QBrush, QColor
from piece import Piece
from balls import Balls
from game_logic import GameLogic


class Board(QFrame):
    boardWidth = 7  # board width
    boardHeight = 7  # board height
    timerSpeed = 1000  # timer set to 1 sec
    counter = 120  # countdown
    gamelogic = GameLogic()  # getting game logic class
    passcount = 0
    listenToTime = pyqtSignal(int)
    listenToClick = pyqtSignal(str)
    captives = pyqtSignal(str, int)
    territories = pyqtSignal(str, int)
    notifier = pyqtSignal(str)
    playerTurn = pyqtSignal(int)

    def __init__(self, parent):
        super().__init__(parent)
        self.boardArray = None
        self.isStarted = None
        self.timer = None
        self.initBoard()
        self.__gameState__ = []  # array to store state of the game

    def initBoard(self):
        self.timer = QBasicTimer()
        self.isStarted = False
        self.start()
        self.boardArray = [[Balls(Piece.NoPiece, i, j) for i in range(self.boardWidth)] for j in
                           range(self.boardHeight)]
        self.gamelogic = GameLogic()
        self.printBoardArray()

    def printBoardArray(self):
        '''prints the boardArray in an attractive way'''
        print("boardArray:")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.boardArray]))

    def squareWidth(self):
        return self.contentsRect().width() / self.boardWidth

    def squareHeight(self):
        return self.contentsRect().height() / self.boardHeight

    def start(self):
        # Start the game
        self.isStarted = True
        self.resetGame()
        self.timer.start(self.timerSpeed, self)
        print("start () - timer is started")

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():  # if the timer that has 'ticked' is the one in this class
            if self.counter == 0:
                self.notifyUser("Timer Ran out : Game over")  # notifiers user when counter get to zero
                if self.gamelogic.turn == Piece.Black:
                    self.notifyUser("White Player Wins")  # white wins if they capture more territories
                else:
                    self.notifyUser("Black Player Wins")  # else black wins
                self.close()
            self.counter -= 1
            self.listenToTime.emit(self.counter)
        else:
            super(Board, self).timerEvent(event)

    def paintEvent(self, event):
        '''paints the board and the pieces of the game'''
        painter = QPainter(self)
        self.drawBoardSquares(painter)
        self.drawPieces(painter)

    def mousePressEvent(self, event):
        '''this event is automatically called when the mouse is pressed'''
        clickLoc = "click location [" + str(event.position().x()) + "," + str(
            event.position().y()) + "]"  # the location where a mouse click was registered
        print("mousePressEvent() - " + clickLoc)
        # TODO you could call some game logic here
        self.mousePosToColRow(event)  # calls mousePosToColRow
        self.listenToClick.emit(clickLoc)

    def mousePosToColRow(self, event):
        '''convert the mouse click event to a row and column'''
        xPosition = event.position().x()  # assigning mouse click x & y event to variables
        yPosition = event.position().y()
        xCoordinate = xPosition / self.squareWidth()  # setting up x & y coordinates
        yCoordinate = yPosition / self.squareHeight()

        x = round(xCoordinate) - 1
        y = round(yCoordinate) - 1

        self.gamelogic.updateparams(self.boardArray, x, y)  # passing parameters to update current variables.
        if self.canWePlaceBallAtChosenPosition():  # checks to see if move is not illegal
            self.placeBall()  # place the pieces on the board
            self.updateTerritoriesAndCaptives()  # update prisoner & territory if any
        self.update()

    def drawBoardSquares(self, painter):
        """draw all the square on the board"""
        # setting the default colour of the brush
        color = QColor(209, 179, 141)
        color2 = QColor(196, 164, 132)
        brush = QBrush(Qt.BrushStyle.SolidPattern)  # calling SolidPattern to a variable
        brush.setColor(color)  # setting color to yellowish brown
        painter.setBrush(brush)
        for row in range(0, Board.boardHeight):
            for col in range(0, Board.boardWidth):
                painter.save()
                colTransformation = self.squareWidth() * col  # setting this value equal the transformation in the
                # column direction
                rowTransformation = self.squareHeight() * row  # setting this value equal the transformation in the
                # row direction
                painter.translate(colTransformation, rowTransformation)
                painter.fillRect(col, row, round(self.squareWidth()), round(self.squareHeight()), brush)  # passing
                # the above variables and methods as a parameter
                painter.restore()

                # changing the colour of the brush so that a checkered board is drawn
                if brush.color() == color:  # if the brush color of square is color
                    brush.setColor(color2)  # set the next color of the square to color2
                else:  # if the brush color of square is color2
                    brush.setColor(color)  # set the next color of the square to color

    def drawPieces(self, painter):
        # Draw the pieces
        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                painter.save()
                painter.translate(((self.squareWidth()) * row) + self.squareWidth() * 0.70,  # get width location
                                  (self.squareHeight()) * col + self.squareHeight() * 0.70)  # get height location

                color = QColor(0, 0, 0)  # set the color is unspecified

                if self.boardArray[col][row].Piece == Piece.NoPiece:  # if no piece change unspecified color is
                    # transparent
                    color = QColor(Qt.GlobalColor.transparent)

                elif self.boardArray[col][row].Piece == Piece.White:  # if white change unspecified colour to white
                    color = QColor(Qt.GlobalColor.white)

                elif self.boardArray[col][row].Piece == Piece.Black:  # if black, change unspecified colour to black
                    color = QColor(Qt.GlobalColor.black)

                painter.setPen(color)
                painter.setBrush(color)

                radius = self.squareWidth() / 3  # size of the piece
                center = QPoint(round(radius), round(radius))

                painter.drawEllipse(center, round(radius), round(radius))
                painter.restore()

    def canWePlaceBallAtChosenPosition(self):
        # check if it's safe to place a ball at the chosen position
        if self.gamelogic.postionNotOccupied():
            if self.gamelogic.isBadMove():
                self.notifyUser("Move not Allowed")
                return False
            else:
                return True
        else:
            self.notifyUser("Spot Occupied")
            return False

    def placeBall(self):
        self.gamelogic.plotTheBalls()  # place the piece on the board
        self.gamelogic.updateLiberty()  # update the liberties
        message = self.gamelogic.updateCaptivesTheSecond()
        if message is not None:
            self.notifyUser(message)  # notify piece was captured
            print("Stone captured")
            self.gamelogic.updateLiberty()  # update the liberties again in case of capture

        self.gamelogic.updateTeritories()  # update territories
        self.__addCurrentStateToGlobalState__()  # push it to the global state
        if not self._check_for_ko():
            self.passcount = 0
            self.changeturn()
        else:

            if self.gamelogic.turn == Piece.White:  # change to White prisoner count
                self.gamelogic.captiveIsWhite = self.gamelogic.captiveIsWhite - 1
            else:  # change to black prisoner count
                self.gamelogic.captiveIsBlack = self.gamelogic.captiveIsBlack - 1

            self.__removeFromGlobalState__(self.__gameState__[-2])
            # update the liberties and territories
            self.gamelogic.updateLiberty()
            self.gamelogic.updateTeritories()
            # push this state to history
            self.__addCurrentStateToGlobalState__()

    def __addCurrentStateToGlobalState__(self):
        # Add the current board state to the state array
        self.__gameState__.append(self.copyThisBoard())  # adds it to the end of the list
        try:
            print("Last move")  # prints the last element of the list
            print('\n'.join(['\t'.join([str(cell.Piece) for cell in row]) for row in self.__gameState__[-1]]))
            print("Second Last")  # prints the second last element of the list
            print('\n'.join(['\t'.join([str(cell.Piece) for cell in row]) for row in self.__gameState__[-2]]))
            print("3rd Last")  # prints the third last element of the list
            print('\n'.join(['\t'.join([str(cell.Piece) for cell in row]) for row in self.__gameState__[-3]]))
        except IndexError:
            return None

    def __removeFromGlobalState__(self, previousstate):
        """
        Pops and loads game state from history.
        """
        print("Removed from global state stack")
        rowIndex = 0
        for row in previousstate:
            colIndex = 0
            for cell in row:
                if cell.Piece == 1:  # if piece is 1, assign white stone to the row and col index of boardArray
                    self.boardArray[rowIndex][colIndex] = Balls(Piece.White, colIndex, rowIndex)
                elif cell.Piece == 2:  # if piece is 2, assign black stone to the row and col index of boardArray
                    self.boardArray[rowIndex][colIndex] = Balls(Piece.Black, colIndex, rowIndex)
                elif cell.Piece == 0:  # if piece is 0, assign null to the row and col index of boardArray
                    self.boardArray[rowIndex][colIndex] = Balls(Piece.NoPiece, colIndex, rowIndex)
                colIndex = colIndex + 1  # move to the next col index position
            rowIndex = rowIndex + 1  # move to the next row index position
        print('\n'.join(['\t'.join([str(cell.Piece) for cell in row]) for row in self.boardArray]))

    def copyThisBoard(self):

        # store and return the current state of the board
        copyofboard = [[Balls(Piece.NoPiece, i, j) for i in range(7)] for j in
                       range(7)]
        rowIndex = 0
        for row in self.boardArray:
            colIndex = 0
            for cell in row:
                if cell.Piece == Piece.White:
                    copyofboard[rowIndex][colIndex] = Balls(Piece.White, colIndex, rowIndex)
                elif cell.Piece == Piece.Black:
                    copyofboard[rowIndex][colIndex] = Balls(Piece.Black, colIndex, rowIndex)
                elif cell.Piece == Piece.NoPiece:
                    copyofboard[rowIndex][colIndex] = Balls(Piece.NoPiece, colIndex, rowIndex)
                colIndex = colIndex + 1
            rowIndex = rowIndex + 1

        return copyofboard

    def _check_for_ko(self):
        # Checks for KO.
        try:
            if self.assertBoardsAreEqual(self.__gameState__[-1], self.__gameState__[-3]):
                self.notifyUser('KO. Revert back now')
                return True
        except IndexError:
            pass
        return False

    def assertBoardsAreEqual(self, current, previous):
        # Check for equality of two boards returns boolean
        rowindex = 0
        for row in previous:
            colindex = 0
            for cell in row:
                if cell.Piece != current[rowindex][colindex].Piece:
                    return False
                colindex = colindex + 1
            rowindex = rowindex + 1

        return True

    def changeturn(self):
        # Change the turn to next player and send update interface
        self.gamelogic.toggleTurns()
        self.counter = 120
        self.playerTurn.emit(self.gamelogic.turn)

    def updateTerritoriesAndCaptives(self):
        self.captives.emit(self.gamelogic.getBlackPrisoner(), Piece.Black)
        self.captives.emit(str(self.gamelogic.getWhitePrisoner()), Piece.White)
        self.territories.emit(str(self.gamelogic.getWhiteTerritories()), Piece.White)
        self.territories.emit(str(self.gamelogic.getBlackTerritories()), Piece.Black)

    def whoIsTheWinner(self):
        # Compare both players score
        # Is game a draw or is there a winner ?
        blackscore = self.gamelogic.returnTheScores(Piece.Black)
        whitescore = self.gamelogic.returnTheScores(Piece.White)
        self.notifyUser("Scores : \n Black :" + str(blackscore) + "\n White : " + str(
            whitescore))  # a notification for Black and White score
        if blackscore > whitescore:
            self.notifyUser("Black Wins")
        elif blackscore < whitescore:
            self.notifyUser("White Wins")
        else:
            self.notifyUser("Game is a Draw")

    def getScore(self, Piece):
        return self.gamelogic.returnTheScores(Piece)

    def notifyUser(self, message):
        self.notifier.emit(message)

    def resetGame(self):
        '''clears pieces from the board'''
        print("Game Reset")
        self.notifyUser("Game Reset")
        '''clears pieces from the board'''
        print("Game Reseted")
        self.boardArray = [[Balls(Piece.NoPiece, i, j) for i in range(self.boardWidth)] for j in
                           range(self.boardHeight)]
        self.gamelogic.blackprisoners = 0
        self.gamelogic.whiteprisoners = 0
        self.gamelogic.turn = Piece.White





    def skipTurn(self):
        self.notifyUser("Move Passed")
        self.passcount = self.passcount + 1
        self.gamelogic.toggleTurns()
        if self.passcount == 2:
            self.notifyUser("Double turn skipped, game over")
            self.whoIsTheWinner()
            return True
        return False

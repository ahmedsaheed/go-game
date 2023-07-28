from collections import namedtuple
from copy import copy

from PyQt6.QtWidgets import QFrame, QStatusBar, QMessageBox
from PyQt6.QtCore import Qt, QBasicTimer, pyqtSignal, QPoint
from PyQt6.QtGui import QPainter, QBrush, QColor
from piece import Piece
from balls import Balls
from game_logic import GameLogic


class Board(QFrame):
    boardWidth = 7   
    boardHeight = 7  
    timerSpeed = 1000  
    counter = 120 
    gamelogic = GameLogic() 
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
        self.__gameState__ = []  

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
        if event.timerId() == self.timer.timerId():  
            if self.counter == 0:
                self.notifyUser("Timer Ran out : Game over")  
                if self.gamelogic.turn == Piece.Black:
                    self.notifyUser("White Player Wins")  
                else:
                    self.notifyUser("Black Player Wins")  
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
            event.position().y()) + "]"  
        print("mousePressEvent() - " + clickLoc)
        self.mousePosToColRow(event)  
        self.listenToClick.emit(clickLoc)

    def mousePosToColRow(self, event):
        '''convert the mouse click event to a row and column'''
        xPosition = event.position().x() 
        yPosition = event.position().y()
        xCoordinate = xPosition / self.squareWidth() 
        yCoordinate = yPosition / self.squareHeight()
        x = round(xCoordinate) - 1
        y = round(yCoordinate) - 1

        self.gamelogic.updateparams(self.boardArray, x, y)  
        if self.canWePlaceBallAtChosenPosition():  
            self.placeBall() 
            self.updateTerritoriesAndCaptives()  
        self.update()

    def drawBoardSquares(self, painter):
        """draw all the square on the board"""
        color = QColor(209, 179, 141)
        color2 = QColor(196, 164, 132)
        brush = QBrush(Qt.BrushStyle.SolidPattern)  
        brush.setColor(color)  
        painter.setBrush(brush)
        for row in range(0, Board.boardHeight):
            for col in range(0, Board.boardWidth):
                painter.save()
                colTransformation = self.squareWidth() * col  
                rowTransformation = self.squareHeight() * row  
                painter.translate(colTransformation, rowTransformation)
                painter.fillRect(col, row, round(self.squareWidth()), round(self.squareHeight()), brush)  # passing
                painter.restore()

                if brush.color() == color: 
                    brush.setColor(color2) 
                else:  
                    brush.setColor(color)  

    def drawPieces(self, painter):
        # Draw the pieces
        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                painter.save()
                painter.translate(((self.squareWidth()) * row) + self.squareWidth() * 0.70, 
                                  (self.squareHeight()) * col + self.squareHeight() * 0.70) 

                color = QColor(0, 0, 0)  

                if self.boardArray[col][row].Piece == Piece.NoPiece:  
                    color = QColor(Qt.GlobalColor.transparent)

                elif self.boardArray[col][row].Piece == Piece.White:  
                    color = QColor(Qt.GlobalColor.white)

                elif self.boardArray[col][row].Piece == Piece.Black:  
                    color = QColor(Qt.GlobalColor.black)

                painter.setPen(color)
                painter.setBrush(color)

                radius = self.squareWidth() / 3 
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
        self.gamelogic.plotTheBalls()  
        self.gamelogic.updateLiberty()  
        message = self.gamelogic.updateCaptivesTheSecond()
        if message is not None:
            self.notifyUser(message)  
            print("Stone captured")
            self.gamelogic.updateLiberty() 
        self.gamelogic.updateTeritories()  
        self.__addCurrentStateToGlobalState__() 
        if not self._check_for_ko():
            self.passcount = 0
            self.changeturn()
        else:
            if self.gamelogic.turn == Piece.White: 
                self.gamelogic.captiveIsWhite = self.gamelogic.captiveIsWhite - 1
            else: 
                self.gamelogic.captiveIsBlack = self.gamelogic.captiveIsBlack - 1

            self.__removeFromGlobalState__(self.__gameState__[-2])
            self.gamelogic.updateLiberty()
            self.gamelogic.updateTeritories()
            self.__addCurrentStateToGlobalState__()

    def __addCurrentStateToGlobalState__(self):
        self.__gameState__.append(self.copyThisBoard())  
        try:
            print("Last move")  
            print('\n'.join(['\t'.join([str(cell.Piece) for cell in row]) for row in self.__gameState__[-1]]))
            print("Second Last")  
            print('\n'.join(['\t'.join([str(cell.Piece) for cell in row]) for row in self.__gameState__[-2]]))
            print("3rd Last")  
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
                if cell.Piece == 1:  
                    self.boardArray[rowIndex][colIndex] = Balls(Piece.White, colIndex, rowIndex)
                elif cell.Piece == 2:  
                    self.boardArray[rowIndex][colIndex] = Balls(Piece.Black, colIndex, rowIndex)
                elif cell.Piece == 0:  
                    self.boardArray[rowIndex][colIndex] = Balls(Piece.NoPiece, colIndex, rowIndex)
                colIndex = colIndex + 1  
            rowIndex = rowIndex + 1  
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
        blackscore = self.gamelogic.returnTheScores(Piece.Black)
        whitescore = self.gamelogic.returnTheScores(Piece.White)
        self.notifyUser("Scores : \n Black :" + str(blackscore) + "\n White : " + str(
            whitescore))  
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

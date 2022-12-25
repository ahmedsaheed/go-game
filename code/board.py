from collections import namedtuple
from copy import copy

from PyQt6.QtWidgets import QFrame, QStatusBar
from PyQt6.QtCore import Qt, QBasicTimer, pyqtSignal, QPoint
from PyQt6.QtGui import QPainter, QBrush, QColor
from piece import Piece
from balls import Balls
from game_logic import GameLogic

class Board(QFrame):  # base the board on a QFrame widget
    updateTimerSignal = pyqtSignal(int)  # signal sent when timer is updated
    clickLocationSignal = pyqtSignal(str)  # signal sent when there is a new click location
    updatePrionersSignal = pyqtSignal(str, int) # signal sent when prisoner is updated.
    updateTerritoriesSignal = pyqtSignal(str, int) # signal sent territory is updated.
    showNotificationSignal = pyqtSignal(str)    # signal sent for notification message.
    displaychangeturnSignal = pyqtSignal(int)   # signal sent when swap player is updated.


    boardWidth = 7  # board width is set to 7
    boardHeight = 7  # board height is set to 7
    timerSpeed = 1000  # the timer updates ever 1 second
    counter = 120  # countdown is set to two minutes

    gamelogic = GameLogic()
    passcount = 0

    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()
        self._history = [] # create a list of game history

    def initBoard(self):
        '''initiates board'''
        self.timer = QBasicTimer()  # create a timer for the game
        self.isStarted = False  # game is not currently started
        self.start()  # start the game which will start the timer
        self.boardArray = [[Balls(Piece.NoPiece,i,j) for i in range(self.boardWidth)] for j in range(self.boardHeight)]
        self.gamelogic = GameLogic()
        self.printBoardArray()

    def printBoardArray(self):
        '''prints the boardArray in an attractive way'''

        print("boardArray:")
        for row in self.boardArray: # running double loop of boardArray
            for cell in row:
                if cell.Piece == Piece.NoPiece: # if NoPiece then print *
                    print(" * ", end=" ")
                if cell.Piece == Piece.Black:   # if Black then print 0
                    print(" 0 ", end=" ")
                if cell.Piece == Piece.White:   # if White then print 1
                    print(" 1 ", end=" ")
        print('\n')
        # print('\n'.join(['\t'.join([ str(cell ) for cell in row]) for row in self.boardArray]))


    def squareWidth(self):
        '''returns the width of one square in the board'''
        return self.contentsRect().width() / self.boardWidth

    def squareHeight(self):
        '''returns the height of one square of the board'''
        return self.contentsRect().height() / self.boardHeight

    def start(self):
        '''starts game'''
        self.isStarted = True  # set the boolean which determines if the game has started to TRUE
        self.resetGame()  # reset the game
        self.timer.start(self.timerSpeed, self)  # start the timer with the correct speed
        print("start () - timer is started")


    def timerEvent(self, event):
        '''this event is automatically called when the timer is updated. based on the timerSpeed variable '''
        # TODO adapter this code to handle your timers
        if event.timerId() == self.timer.timerId():  # if the timer that has 'ticked' is the one in this class
            # print("got in timer")
            if self.counter == 0:   # if time is up
                self.shownotification("Timer Ran out : Game over")  # show this message
                if self.gamelogic.turn == Piece.Black:  # if next turn is black
                    self.shownotification("White Player Wins")  # white wins, capturing more territories
                else:
                    self.shownotification("Black Player Wins") # else black wins
                self.close()
            self.counter -= 1
            # print('timerEvent()', self.counter)
            self.updateTimerSignal.emit(self.counter)
        else:
            super(Board, self).timerEvent(event)  # if we do not handle an event we should pass it to the super
            # class for handelingother wise pass it to the super class for handling


    def paintEvent(self, event):
        '''paints the board and the pieces of the game'''
        painter = QPainter(self)    # initialising painter and passing it as a parameter
        self.drawBoardSquares(painter)
        self.drawPieces(painter)

    #     def mousePressEvent(self, event):
    #         """this event is automatically called when the mouse is pressed"""
    #         clickLoc = "click location [" + str(event.position().x()) + "," + str(
    #             event.position().y()) + "]"  # the location where a mouse click was registered
    #         print("mousePressEvent() - " + clickLoc)
    #         # TODO you could call some game logic here
    #         self.clickLocationSignal.emit(clickLoc)
    def mousePressEvent(self, event):
        '''this event is automatically called when the mouse is pressed'''
        clickLoc = "click location [" + str(event.position().x()) + "," + str(event.position().y()) + "]"  # the location where a mouse click was registered
        print("mousePressEvent() - " + clickLoc)
        # TODO you could call some game logic here
        self.mousePosToColRow(event)    # a method that converts the mouse click to a row and col.
        self.clickLocationSignal.emit(clickLoc)


    def mousePosToColRow(self, event):
        '''convert the mouse click event to a row and column'''
        xpos = event.position().x()    # assigning mouse click x & y event to variables
        ypos = event.position().y()
        xcoordinate = xpos / self.squareWidth() # setting up x & y coordinates
        ycoordinate = ypos / self.squareHeight()
        ''' The round() method returns the floating point number rounded off to the given ndigits
         digits after the decimal point. If no ndigits is provided, it rounds off the number to the 
         nearest integer.'''
        xp = round(xcoordinate) - 1
        yp = round(ycoordinate) - 1

        self.gamelogic.updateparams(self.boardArray, xp, yp) # passing parameters to update current variables.
        if (self.setBall()):    # if move is not suicide
            self.placeStone()   # place the stone on the board
            self.updatePrisonersandTerritories() # update prisoner & territory if any
        self.update()


    def drawBoardSquares(self, painter):
        '''draw all the square on the board'''
        # setting the default colour of the brush
        brush = QBrush(Qt.BrushStyle.SolidPattern)  # calling SolidPattern to a variable
        brush.setColor(QColor(209, 179, 141))  # setting color to orange
        painter.setBrush(brush)  # setting brush color to painter

        for row in range(0, Board.boardHeight):
            for col in range(0, Board.boardWidth):
                painter.save()
                colTransformation = self.squareWidth() * col  # setting this value equal the transformation in the column direction
                rowTransformation = self.squareHeight() * row  # setting this value equal the transformation in the row direction

                painter.translate(colTransformation, rowTransformation)
                painter.fillRect(col, row, round(self.squareWidth()), round(self.squareHeight()),
                                 brush)  # passing the above variables and methods as a parameter
                painter.restore()

                # changing the colour of the brush so that a checkered board is drawn
                # color1 = QColor(209, 179, 141)  # yellowish brown
                # #         color2 = QColor(196, 164, 132)  # light brown color
                if brush.color() == QColor(209, 179, 141):  # if the brush color of square is orange
                    brush.setColor(QColor(196, 164, 132))  # set the nex color of the square to black
                else:  # if its black, then set the next square to orange
                    brush.setColor(QColor(209, 179, 141))


    def drawPieces(self, painter):
        '''draw the prices on the board'''
        color = Qt.GlobalColor.transparent  # empty square could be modeled with transparent pieces
        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                painter.save()

                ''' the string translate() method returns a string where each row and col is mapped to 
                its corresponding character in the translation table '''
                painter.translate(((self.squareWidth()) * row) + self.squareWidth() / 2,
                                  (self.squareHeight()) * col + self.squareHeight() / 2)
                color = QColor(0, 0, 0)  # set the color is unspecified

                if self.boardArray[col][row].Piece == Piece.NoPiece:  # if piece in array == 0
                    color = QColor(Qt.GlobalColor.transparent)  # color is transparent

                elif self.boardArray[col][row].Piece == Piece.White:  # if piece in array == 1
                    color = QColor(Qt.GlobalColor.white)  # set color to white

                elif self.boardArray[col][row].Piece == Piece.Black:  # if piece in array == 2
                    color = QColor(Qt.GlobalColor.black)  # set color to black

                painter.setPen(color)  # set pen color to painter
                painter.setBrush(color)  # set brush color to painter

                radius = (self.squareWidth() - 2) / 2
                center = QPoint(round(radius), round(radius))
                painter.drawEllipse(center, round(radius), round(radius))
                painter.restore()



    def setBall(self):
        '''  a methoad for checking rules before placing stone  '''
        if self.gamelogic.checkvacant():    # check if the position is vacant or not
            if self.gamelogic.checkforSuicide():  # if the move is suicide
                self.shownotification("Suicide Move not Allowed")   # show message
                return False
            else:
                return True
        else:
            self.shownotification("Spot Occupied")
            return False


    def placeStone(self):
        self.gamelogic.placestone()  # place the stone on the board
        self.gamelogic.updateLiberties()  # update the liberties
        message = self.gamelogic.updatecaptures2()
        if (message != None):   # if no liberties left of the neighbouring stones
            self.shownotification(message)
            print("Stone captured")
            self.gamelogic.updateLiberties()  # update the liberties again in case of capture

        self.gamelogic.updateTeritories()   # update territories
        self._push_history()    # push it to the history list
        if not self._check_for_ko():    # if board state is not in KO
            self.passcount = 0  # change the pass count to reflect that any one of the player has taken a turn
            self.changeturn()  # change the turn to next player in case of successful position of piece

        else:

            if self.gamelogic.turn == Piece.White:  # revert back the White prisoner count
                self.gamelogic.whiteprisoners = self.gamelogic.whiteprisoners - 1

            else:   # # revert back the Black prisoner count
                self.gamelogic.blackprisoners = self.gamelogic.blackprisoners - 1
            # revert back the board to previous state
            self._pop_history(self._history[-2])
            # uodate the liberties and territories
            self.gamelogic.updateLiberties()
            self.gamelogic.updateTeritories()
            # push this state to history
            self._push_history()


    def _push_history(self):
        """
        Pushes game state onto history.
        """
        self._history.append(self.copyboard())  # adds it to the end of the list
        try:
            print("Last move") # prints the last element of the list
            print('\n'.join(['\t'.join([str(cell.Piece) for cell in row]) for row in self._history[-1]]))
            print("Second Last")  # prints the second last element of the list
            print('\n'.join(['\t'.join([str(cell.Piece) for cell in row]) for row in self._history[-2]]))
            print("3rd Last")   # prints the third last element of the list
            print('\n'.join(['\t'.join([str(cell.Piece) for cell in row]) for row in self._history[-3]]))
        except IndexError:
            return None


    def _pop_history(self, previousstate):
        """
        Pops and loads game state from history.
        """
        print("popping history")
        print("Current array before popping")
        print('\n'.join(['\t'.join([str(cell.Piece) for cell in row]) for row in self.boardArray])) # nested for loop of boardArray
        print("Previous state")
        print('\n'.join(['\t'.join([str(cell.Piece) for cell in row]) for row in previousstate])) # nested for loop of prevoisstate
        rowindex = 0
        for row in previousstate:
            colindex = 0
            for cell in row:
                if cell.Piece == 1: # if piece is 1, assign white stone to the row and col index of boardArray
                    self.boardArray[rowindex][colindex] = Balls(Piece.White, colindex, rowindex)
                elif cell.Piece == 2: # if piece is 2, assign black stone to the row and col index of boardArray
                    self.boardArray[rowindex][colindex] = Balls(Piece.Black, colindex, rowindex)
                elif cell.Piece == 0: # if piece is 0, assign null to the row and col index of boardArray
                    self.boardArray[rowindex][colindex] = Balls(Piece.NoPiece, colindex, rowindex)
                colindex = colindex + 1 # move to the next col index position
            rowindex = rowindex + 1 # move to the next row index position

        print("Current array after popping")
        print('\n'.join(['\t'.join([str(cell.Piece) for cell in row]) for row in self.boardArray]))
        # converting the value of col and row in boardArray to string before printing

    def copyboard(self):
        ''' A method to store and return the current state of the board '''
        copyofboard = [[Balls(Piece.NoPiece, i, j) for i in range(7)] for j in range(7)] # nested loop of Stone class to the size of board range.
        rowindex = 0
        for row in self.boardArray:
            colindex = 0
            for cell in row:
                if cell.Piece == Piece.White:
                    copyofboard[rowindex][colindex] = Balls(Piece.White, colindex, rowindex) # places the current value of white stone to the copyofboard row and col index
                elif cell.Piece == Piece.Black:
                    copyofboard[rowindex][colindex] = Balls(Piece.Black, colindex, rowindex) # places the current value of black stone to the copyofboard row and col index
                elif cell.Piece == Piece.NoPiece:
                    copyofboard[rowindex][colindex] = Balls(Piece.NoPiece, colindex, rowindex) # places the current value of Stone to the copyofboard row and col index
                colindex = colindex + 1 # increment col index
            rowindex = rowindex + 1 # increment row index

        return copyofboard


    def _check_for_ko(self):
        # Checks if board state is in KO.
        try:
            if self.compareboards(self._history[-1], self._history[-3]):
                self.shownotification('Cannot make a move this is KO!, Reverting back now')
                return True  # return true if move is KO
        except IndexError:
            # Insufficient history...let this one slide
            pass
        return False  # return false incase its not KO


    def compareboards(self, current, previous):
        rowindex = 0
        for row in previous:
            colindex = 0
            for cell in row:
                if cell.Piece != current[rowindex][colindex].Piece:
                    return False  # return false if found a single position different
                colindex = colindex + 1
            rowindex = rowindex + 1

        return True  # else return true


    def changeturn(self):
        self.gamelogic.changeturn()  # function to swap turns
        self.counter = 120  # reset the timer for the next player
        self.displaychangeturnSignal.emit(self.gamelogic.turn)  # signal sent to display Current Turn message


    def updatePrisonersandTerritories(self):
        self.updatePrionersSignal.emit(self.gamelogic.getBlackPrisoner(), Piece.Black)
        self.updatePrionersSignal.emit(str(self.gamelogic.getWhitePrisoner()), Piece.White)
        self.updateTerritoriesSignal.emit(str(self.gamelogic.getWhiteTerritories()), Piece.White)
        self.updateTerritoriesSignal.emit(str(self.gamelogic.getBlackTerritories()), Piece.Black)


    def declarewinner(self):
        blackscore = self.gamelogic.getScore(Piece.Black)   # gets the current score of Black
        whitescore = self.gamelogic.getScore(Piece.White)    # gets the current score of White
        self.shownotification("Scores : \n Black :" + str(blackscore) + "\n White : " + str(whitescore)) # a notification for Black and White score
        if blackscore > whitescore:
            self.shownotification("Black Wins")
        elif blackscore < whitescore:
            self.shownotification("White Wins")
        else:
            self.shownotification("Game is a Draw")


    def getScore(self, Piece):
        return self.gamelogic.getScore(Piece) # passing Piece class in a getScore method from a gamelogic class
                                            # to retrieve the sum of territories and prisoners

    def shownotification(self, message):
        self.showNotificationSignal.emit(message)


    def keyPressEvent(self, e):
        ''' A method to detect to escape key '''
        print("geting here")
        if e.key() == Qt.Key.Key_Escape:
            print("Escape pressed")


    def resetGame(self):
        '''clears pieces from the board'''
        print("Game Reseted")
        self.boardArray = [[Balls(Piece.NoPiece, i, j) for i in range(self.boardWidth)] for j in
                           range(self.boardHeight)]
        self.gamelogic.blackprisoners = 0
        self.gamelogic.whiteprisoners = 0
        self.gamelogic.turn = Piece.White


    def passEvent(self):
        self.shownotification("Move Passed")
        self.passcount = self.passcount + 1
        self.gamelogic.changeturn()
        if self.passcount == 2:
            self.shownotification("Double turn skipped, game over")
            self.declarewinner()
            return True
        return False






# from PyQt6.QtWidgets import QFrame
# from PyQt6.QtCore import Qt, QBasicTimer, pyqtSignal, QPointF, QPoint
# from PyQt6.QtGui import QPainter, QBrush, QColor
# from piece import Piece
#
#
# class Board(QFrame):
#     updateTimerSignal = pyqtSignal(int)
#     clickLocationSignal = pyqtSignal(str)
#
#     # TODO set the board width and height to be square
#     boardWidth = 7
#     boardHeight = 7
#     timerSpeed = 1000
#     counter = 90
#
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.isStarted = None
#         self.timer = None
#         self.boardArray = None
#         self.initBoard()
#
#     def initBoard(self):
#         """initiates board"""
#         self.timer = QBasicTimer()
#         self.isStarted = False
#         self.start()
#         self.boardArray = [[Piece(Piece.NoPiece, i, j) for i in range(self.boardWidth)] for j in
#                            range(self.boardHeight)]
#
#     def printBoardArray(self):
#         """prints the boardArray in an attractive way"""
#         print("boardArray:")
#         print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.boardArray]))
#
#     def mousePosToColRow(self, event):
#         """convert the mouse click event to a row and column"""
#
#     def squareWidth(self):
#         """returns the width of one square in the board"""
#         return self.contentsRect().width() / self.boardWidth
#
#     def squareHeight(self):
#         """returns the height of one square of the board"""
#         return self.contentsRect().height() / self.boardHeight
#
#     def start(self):
#         """starts game"""
#         self.isStarted = True
#         self.resetGame()  # reset the game
#         self.timer.start(self.timerSpeed, self)  # start the timer with the correct speed
#         print("start () - timer is started")
#
#     def timerEvent(self, event):
#         """this event is automatically called when the timer is updated. based on the timerSpeed variable """
#         # TODO adapt this code to handle your timers
#         if event.timerId() == self.timer.timerId():  # if the timer that has 'ticked' is the one in this class
#             if Board.counter == 0:
#                 print("Game over")
#             self.counter -= 1
#             print('timerEvent()', self.counter)
#             self.updateTimerSignal.emit(self.counter)
#         else:
#             super(Board, self).timerEvent(event)  # if we do not handle an event we should pass it to the super
#             # class for handling
#
#     def mousePressEvent(self, event):
#         """this event is automatically called when the mouse is pressed"""
#         clickLoc = "click location [" + str(event.position().x()) + "," + str(
#             event.position().y()) + "]"  # the location where a mouse click was registered
#         print("mousePressEvent() - " + clickLoc)
#         # TODO you could call some game logic here
#         self.clickLocationSignal.emit(clickLoc)
#
#     def resetGame(self):
#         """clears pieces from the board"""
#         # TODO write code to reset game
#
#     def tryMove(self, newX, newY):
#         """tries to move a piece"""
#
#     def drawBoardSquares(self, painter):
#         """draw all the square on the board"""
#         # setting the default colour of the brush
#         color1 = QColor(209, 179, 141)  # yellowish brown
#         color2 = QColor(196, 164, 132)  # light brown color
#         brush = QBrush(Qt.BrushStyle.SolidPattern)  # calling SolidPattern to a variable
#         brush.setColor(color1)  # setting color to black
#         painter.setBrush(brush)
#         # add padding to the board
#         padding = 20  # padding size in pixels
#         for row in range(0, Board.boardHeight):
#             for col in range(0, Board.boardWidth):
#                 painter.save()
#                 colTransformation = self.squareWidth() * col + padding
#                 rowTransformation = self.squareHeight() * row + padding
#                 painter.translate(colTransformation, rowTransformation)
#                 # draw the square with the padding
#                 painter.fillRect(col, row, round(self.squareWidth()), round(self.squareHeight()), brush)
#                 painter.restore()
#                 if brush.color() == color1:
#                     brush.setColor(color2)
#                 else:
#                     brush.setColor(color1)
#
#     def drawPieces(self, painter):
#         # on each line intersection, draw a circle
#         radius_w = self.squareWidth() / 2 - 32  # width radius
#         radius_h = self.squareHeight() / 2 - 32  # height radius
#         for row in range(0, Board.boardHeight):
#             for col in range(0, Board.boardWidth):
#                 painter.save()
#                 # calculate the position of the piece on the board
#                 colTransformation = self.squareWidth() * col
#                 rowTransformation = self.squareHeight() * row
#                 # offset the piece to the intersection
#                 colTransformation += self.squareWidth() / 4
#                 rowTransformation += self.squareHeight() / 4
#                 painter.translate(colTransformation, rowTransformation)
#                 # draw the circle at the border of the square
#                 if Piece.Status == Piece.Black:
#                     painter.setBrush(QBrush(Qt.BrushStyle.SolidPattern))
#                     painter.setPen(Qt.GlobalColor.black)
#                     painter.drawEllipse(QPointF(0, 0), radius_w, radius_h)
#                 elif Piece.Status == Piece.White:
#                     painter.setBrush(QBrush(Qt.BrushStyle.SolidPattern))
#                     painter.setPen(Qt.GlobalColor.white)
#                     painter.drawEllipse(QPointF(0, 0), radius_w, radius_h)
#                 else:
#                     painter.setBrush(QBrush(Qt.BrushStyle.SolidPattern))
#                     painter.setPen(Qt.GlobalColor.white)
#                     painter.drawEllipse(QPointF(0, 0), radius_w, radius_h)
#                 painter.restore()
#
#     def paintEvent(self, event):
#         """paints the board and the pieces of the game"""
#         painter = QPainter(self)
#         self.drawBoardSquares(painter)
#         self.drawPieces(painter)
#
#     # def drawPieces(self, painter):
#     #     """draw the prices on the board"""
#     #     colour = Qt.GlobalColor.red  # empty square could be modeled with transparent pieces
#     #     for row in range(0, len(self.boardArray)):
#     #         for col in range(0, len(self.boardArray[0])):
#     #             painter.save()
#     #             ''' the string translate() method returns a string where each row and col is mapped to
#     #             its corresponding character in the translation table '''
#     #             painter.translate(((self.squareWidth()) * row) + self.squareWidth() / 2,
#     #                               (self.squareHeight()) * col + self.squareHeight() / 2)
#     #             color = QColor(0, 0, 0)  #  color set to unspecified
#     #
#     #             if self.boardArray[col][row].Piece == Piece.NoPiece:  # if piece in array == 0
#     #                 color = QColor(Qt.GlobalColor.transparent)  # color is transparent
#     #
#     #             elif self.boardArray[col][row].Piece == Piece.Black:  # if piece in array == 1
#     #                 color = QColor(Qt.GlobalColor.black)  # set color to black
#     #
#     #             elif self.boardArray[col][row].Piece == Piece.White:  # if piece in array == 2
#     #                 color = QColor(Qt.GlobalColor.white)  # set color to white
#     #
#     #             painter.setPen(color)  # set pen color to painter
#     #             painter.setBrush(color)  # set brush color to painter
#     #             radius = (self.squareWidth()) / 2
#     #             center = QPoint(radius, radius)
#     #             painter.drawEllipse(center, radius, radius)
#     #             painter.restore()

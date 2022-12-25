# TODO: Add more functions as needed for your Pieces
class Piece(object):
    NoPiece = 0
    White = 1
    Black = 2
    Piece = NoPiece  # default to nopiece
    liberties = 0  # default no liberties
    x = -1
    y = -1

    def __init__(self, Piece, x, y):  # constructor
        self.Piece = Piece
        self.liberties = 0
        self.x = x
        self.y = y

    def getPiece(self):  # return PieceType
        return self.Piece

    def getLiberties(self):  # return Liberties
        return self.liberties

    def setLiberties(self, liberties):  # set Liberties
        self.liberties = liberties

    def getTop(self, boardArray):
        if self.y == 0:
            return None
        else:
            return boardArray[self.y - 1][self.x]  # move y coordinate upwards

    def getRight(self, boardArray):
        if self.x == 6:
            return None
        else:
            return boardArray[self.y][self.x + 1]  # move x coordinate to the right

    def getLeft(self, boardArray):
        if self.x == 0:
            return None
        else:
            return boardArray[self.y][self.x - 1]  # move x coordinate to the left

    def getBottom(self, boardArray):
        if self.y == 6:
            return None
        else:
            return boardArray[self.y + 1][self.x]  # move y coordinate to downwards

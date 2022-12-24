from piece import Piece


class GameLogic:
    print("Game Logic Object Created")
    # TODO add code here to manage the logic of your game
    turn = Piece.Black
    xPosition = 0
    yPosition = 0
    boardArray = 0
    blackPrisoners = 0
    whitePrisoners = 0
    blackTerritories = 0
    whiteTerritories = 0

    def updateVariables(self, boardArray, xPosition, yPosition):
        # update current variables
        self.xPosition = xPosition
        self.yPosition = yPosition
        self.boardArray = boardArray

    def checkLogic(self, boardArray, xPosition, yPosition):
        # update current variables
        self.xPosition = xPosition
        self.yPosition = yPosition
        self.boardArray = boardArray

    def checkVacant(self):
        # check if the position is vacant
        if self.boardArray[self.yPosition][self.xPosition].Piece == Piece.NoPiece:
            return True
        else:
            return False

    def changeTurn(self):
        # Change player ture
        print("Turn Changed")
        if self.turn == Piece.White:
            self.turn = Piece.Black
        else:
            self.turn = Piece.White

    def placePiece(self):
        # function to place the piece on the board
        if self.turn == Piece.White:
            self.boardArray[self.yPosition][self.xPosition].Piece = Piece.White

        else:
            self.boardArray[self.yPosition][self.xPosition].Piece = Piece.Black

        print("Liberties = " + str(self.boardArray[self.yPosition][self.xPosition].liberties) + "x pos = " + str(
            self.boardArray[self.yPosition][self.xPosition].x) + "y pos = " + str(self.boardArray[self.yPosition][self.xPosition].y))

    def updateLiberties(self):
        # update the liberties of all the available stones
        count = 0
        for row in self.boardArray:
            for cell in row:
                count = 0
                if cell.Piece != Piece.NoPiece:
                    pieceColor = cell.Piece

                    if cell.getTop(self.boardArray) is not None and (
                            cell.getup(self.boardArray).Piece == pieceColor or cell.getTop(
                            self.boardArray).Piece == Piece.NoPiece):
                        count = count + 1
                    if cell.getRight(self.boardArray) is not None and (
                            cell.getright(self.boardArray).Piece == pieceColor or cell.getRight(
                            self.boardArray).Piece == Piece.NoPiece):
                        count = count + 1
                    if cell.getLeft(self.boardArray) is not None and (
                            cell.getleft(self.boardArray).Piece == pieceColor or cell.getLeft(
                            self.boardArray).Piece == Piece.NoPiece):
                        count = count + 1
                    if cell.getBottom(self.boardArray) is not None and (
                            cell.getdown(self.boardArray).Piece == pieceColor or cell.getBottom(
                            self.boardArray).Piece == Piece.NoPiece):
                        count = count + 1
                    cell.setLiberties(count)


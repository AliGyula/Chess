from PIL import Image, ImageTk
from pathFinding import pathFinding

class Piece:
    def __init__(self, x, y, color, type):
        self.x = x
        self.y = y
        self.color = color
        self.type = type
        self.tile = None
        self.player = None
        self.canvasElement = None
        self.hasMoved = False
        if color == 'black':
            self.xOff = 75
        else:
            self.xOff = 0

        if self.type == 'king':
            self.yOff = 0
        if self.type == 'queen':
            self.yOff = 75
        if self.type == 'bishop':
            self.yOff = 150
        if self.type == 'knight':
            self.yOff = 225
        if self.type == 'rook':
            self.yOff = 300
        if self.type == 'pawn':
            self.yOff = 375
        self.img = ImageTk.PhotoImage(self.setupImg())

    def setupImg(self):
        im = Image.open("chessPieces.png")
        crop_rectangle = (self.yOff, self.xOff, self.yOff + 75, self.xOff + 75)
        img = im.crop(crop_rectangle)
        return img

    def calculateValidMoves(self, board, ize = True, lastMoved = None):
        validMoves = []
        offSet = -1 if self.color == 'white' else 1

        if self.player.checkedBy != None and ize:
            checkLine = self.player.calculateCheckLine()
            moves = self.calculateValidMoves(board, False)
            for j in range(0, len(moves)):
                if moves[j] not in checkLine:
                    if self.type == 'king':
                        validMoves.append(moves[j])
                elif self.type != 'king':
                    validMoves.append(moves[j])
            return validMoves

        if self.type == 'pawn':
            if board.tiles[self.x][self.y + (1 * offSet)].piece == None:
                validMoves.append(board.tiles[self.x][self.y + (1 * offSet)])
            if board.tiles[self.x][self.y + (2 * offSet)].piece == None and self.hasMoved == False:
                validMoves.append(board.tiles[self.x][self.y + (2 * offSet)])
            if self.validateCoordinates(self.x + 1, self.y + (1 * offSet)):
                if board.tiles[self.x + 1][self.y + (1 * offSet)].piece != None:
                    if board.tiles[self.x + 1][self.y + (1 * offSet)].piece.color != self.color:
                        validMoves.append(board.tiles[self.x + 1][self.y + (1 * offSet)])
            if self.validateCoordinates(self.x - 1, self.y + (1 * offSet)):
                if board.tiles[self.x - 1][self.y + (1 * offSet)].piece != None:
                    if board.tiles[self.x - 1][self.y + (1 * offSet)].piece.color != self.color:
                        validMoves.append(board.tiles[self.x - 1][self.y + (1 * offSet)])

        if self.type == 'rook' or self.type == 'queen':
            for i in range(self.y + 1, len(board.tiles), 1):
                if board.tiles[self.x][i].piece == None:
                    validMoves.append(board.tiles[self.x][i])
                else:
                    if board.tiles[self.x][i].piece.color != self.color:
                        validMoves.append(board.tiles[self.x][i])
                    break
            for i in range(self.y - 1, -1, -1):
                if board.tiles[self.x][i].piece == None:
                    validMoves.append(board.tiles[self.x][i])
                else:
                    if board.tiles[self.x][i].piece.color != self.color:
                        validMoves.append(board.tiles[self.x][i])
                    break
            for i in range(self.x + 1, len(board.tiles), 1):
                if board.tiles[i][self.y].piece == None:
                    validMoves.append(board.tiles[i][self.y])
                else:
                    if board.tiles[i][self.y].piece.color != self.color:
                        validMoves.append(board.tiles[i][self.y])
                    break
            for i in range(self.x - 1, -1, -1):
                if board.tiles[i][self.y].piece == None:
                    validMoves.append(board.tiles[i][self.y])
                else:
                    if board.tiles[i][self.y].piece.color != self.color:
                        validMoves.append(board.tiles[i][self.y])
                    break

        if self.type == 'knight':
            for i in range(self.y - 2, self.y + 3, 4):
                if self.validateCoordinates(self.x + 1, i):
                    if board.tiles[self.x + 1][i].piece == None or board.tiles[self.x + 1][i].piece.color != self.color:
                        validMoves.append(board.tiles[self.x + 1][i])
                if self.validateCoordinates(self.x - 1, i):
                    if board.tiles[self.x - 1][i].piece == None or board.tiles[self.x - 1][i].piece.color != self.color:
                        validMoves.append(board.tiles[self.x - 1][i])

            for i in range(self.x - 2, self.x + 3, 4):
                if self.validateCoordinates(i, self.y + 1):
                    if board.tiles[i][self.y + 1].piece == None or board.tiles[i][self.y + 1].piece.color != self.color:
                        validMoves.append(board.tiles[i][self.y + 1])
                if self.validateCoordinates(i, self.y - 1):
                    if board.tiles[i][self.y - 1].piece == None or board.tiles[i][self.y - 1].piece.color != self.color:
                        validMoves.append(board.tiles[i][self.y - 1])


        if self.type == 'bishop' or self.type == 'queen':
            checkUpLeft = True
            checkUpRight = True
            checkDownLeft = True
            checkDownRight = True
            for i in range(1, self.y + 1):
                if self.validateCoordinates(self.x - i, self.y - i) and checkUpLeft:
                    if board.tiles[self.x - i][self.y - i].piece == None:
                        validMoves.append(board.tiles[self.x - i][self.y - i])
                    else:
                        if board.tiles[self.x - i][self.y - i].piece.color != self.color:
                            validMoves.append(board.tiles[self.x - i][self.y - i])
                        checkUpLeft = False
                if self.validateCoordinates(self.x + i, self.y - i) and checkUpRight:
                    if board.tiles[self.x + i][self.y - i].piece == None:
                        validMoves.append(board.tiles[self.x + i][self.y - i])
                    else:
                        if board.tiles[self.x + i][self.y - i].piece.color != self.color:
                            validMoves.append(board.tiles[self.x + i][self.y - i])
                        checkUpRight = False
            for i in range(1, (len(board.tiles) - self.y)):
                if self.validateCoordinates(self.x + i, self.y + i) and checkDownRight:
                    if board.tiles[self.x + i][self.y + i].piece == None:
                        validMoves.append(board.tiles[self.x + i][self.y + i])
                    else:
                        if board.tiles[self.x + i][self.y + i].piece.color != self.color:
                            validMoves.append(board.tiles[self.x + i][self.y + i])
                        checkDownRight = False
                if self.validateCoordinates(self.x - i, self.y + i) and checkDownLeft:
                    if board.tiles[self.x - i][self.y + i].piece == None:
                        validMoves.append(board.tiles[self.x - i][self.y + i])
                    else:
                        if board.tiles[self.x - i][self.y + i].piece.color != self.color:
                            validMoves.append(board.tiles[self.x - i][self.y + i])
                        checkDownLeft = False

        if self.type == 'king':
            for i in range(self.x - 1, self.x + 2):
                for j in range(self.y - 1, self.y + 2):
                    if self.validateCoordinates(i, j):
                        if board.tiles[i][j].piece == None or board.tiles[i][j].piece.color != self.color:
                            validMoves.append(board.tiles[i][j])
        

        return validMoves


    def validateCoordinates(self, x, y):
        return (x > -1 and x < 8 and y > -1 and y < 8)

    def __str__(self):
        return f"x: {self.x}, y: {self.y}, color: {self.color}, type: {self.type}"

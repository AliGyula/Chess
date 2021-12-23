from board import Board

class Player:
    def __init__(self, name, color, enemy, board):
        self.name = name
        self.color = color
        self.board = board
        self.enemy = enemy
        self.pieces = []
        self.knockedPieces = []
        self.checkedBy = None

        self.setupPieces()

    def isChecked(self):
        x, y = self.kingPosition()
        for i in range(len(self.enemy.pieces)):
            if self.board.tiles[x][y] in self.enemy.pieces[i].calculateValidMoves(self.board, False):
                self.checkedBy = self.enemy.pieces[i]
                return True
        self.checkedBy = None
        return False

    def isInMate(self):
        if self.checkedBy == None:
            return False

        checkLine = self.calculateCheckLine()
        
        for i in range(len(self.pieces)):
            moves = self.pieces[i].calculateValidMoves(self.board, False)
            for j in range(len(moves)):
                if moves[j] in checkLine and self.pieces[i].type != 'king':
                    return False

        return True

    def kingPosition(self):
        for i in range(len(self.pieces)):
            if self.pieces[i].type == 'king':
                return (self.pieces[i].x, self.pieces[i].y)

    def setupPieces(self):
        for i in range(len(self.board.tiles)):
            for j in range(len(self.board.tiles[i])):
                if self.board.tiles[i][j].piece != None:
                    if self.board.tiles[i][j].piece.color == self.color:
                        self.board.tiles[i][j].piece.player = self
                        self.pieces.append(self.board.tiles[i][j].piece)

    def deletePiece(self, piece):
        self.knockedPieces.append(self.pieces.remove(piece))

    def calculateCheckLine(self):
        line = []
        """
        for i in range(self.checkedBy.y, -1, -1):
            if self.board.tiles[self.checkedBy.x][i].piece.type == 'king':
                return line
            line.append(self.board.tiles[self.checkedBy.x][i])
            """
        for i in range(self.checkedBy.y, 8, 1):
            if self.board.tiles[self.checkedBy.x][i].piece != None:
                if self.board.tiles[self.checkedBy.x][i].piece.type == 'king':
                    return line
            line.append(self.board.tiles[self.checkedBy.x][i])
        """
        for i in range(self.checkedBy.x, -1, -1):
            if self.board.tiles[i][self.checkedBy.y].piece.type == 'king':
                return line
            line.append(self.board.tiles[i][self.checkedBy.y])

        for i in range(self.checkedBy.x, 8, 1):
            if self.board.tiles[i][self.checkedBy.y].piece.type == 'king':
                return line
            line.append(self.board.tiles[i][self.checkedBy.y])
        """
        return line
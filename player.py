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

    def isChecked(self, pos = None):
        if pos == None:
            x, y = self.kingPosition()
        else:
            x, y = pos

        for i in range(len(self.enemy.pieces)):
            if self.board.tiles[x][y] in self.enemy.pieces[i].calculateValidMoves(self.board, None, False):
                self.checkedBy = self.enemy.pieces[i]
                return True
        self.checkedBy = None
        return False

    def isInMate(self):
        if self.checkedBy == None:
            return False

        checkLine = self.calculateCheckLine()
        
        for i in range(len(self.pieces)):
            moves = self.pieces[i].calculateValidMoves(self.board, None, False)
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

    def calculateCheckLine(self, piece = None):
        line = []
        if piece == None:
            piece = self.checkedBy

        for i in range(piece.y, -1, -1):
            if self.validateCoordinates(piece.x, i):
                if self.board.tiles[piece.x][i].piece != None:
                    if self.board.tiles[piece.x][i].piece.type == 'king' and self.board.tiles[piece.x][i].piece.color != piece.color:
                        return line
                line.append(self.board.tiles[piece.x][i])
        line = []
        for i in range(piece.y, 8, 1):
            if self.validateCoordinates(piece.x, i):
                if self.board.tiles[piece.x][i].piece != None:
                    if self.board.tiles[piece.x][i].piece.type == 'king' and self.board.tiles[piece.x][i].piece.color != piece.color:
                        return line
                line.append(self.board.tiles[piece.x][i])
        line = []
        for i in range(piece.x, -1, -1):
            if self.validateCoordinates(i, piece.y):
                if self.board.tiles[i][piece.y].piece != None and self.board.tiles[i][piece.y].piece.color != piece.color:
                    if self.board.tiles[i][piece.y].piece.type == 'king':
                        return line
                line.append(self.board.tiles[i][piece.y])
        line = []
        for i in range(piece.x, 8, 1):
            if self.validateCoordinates(i, piece.y):
                if self.board.tiles[i][piece.y].piece != None and self.board.tiles[i][piece.y].piece.color != piece.color:
                    if self.board.tiles[i][piece.y].piece.type == 'king':
                        return line
                line.append(self.board.tiles[i][piece.y])
        line = []

        for i in range(0, piece.y + 1):
            if self.validateCoordinates(piece.x - i, piece.y - i):
                if self.board.tiles[piece.x - i][piece.y - i].piece != None:
                    if self.board.tiles[piece.x - i][piece.y - i].piece.type == 'king' and self.board.tiles[piece.x - i][piece.y - i].piece.color != piece.color:
                        return line
                line.append(self.board.tiles[piece.x - i][piece.y - i])
        line = []

        for i in range(0, piece.y + 1):
            if self.validateCoordinates(piece.x + i, piece.y - i):
                if self.board.tiles[piece.x + i][piece.y - i].piece != None:
                    if self.board.tiles[piece.x + i][piece.y - i].piece.type == 'king' and self.board.tiles[piece.x + i][piece.y - i].piece.color != piece.color:
                        return line
                line.append(self.board.tiles[piece.x + i][piece.y - i])
        line = []
        
        for i in range(0, (len(self.board.tiles) - piece.y)):
            if self.validateCoordinates(piece.x + i, piece.y + i):
                if self.board.tiles[piece.x + i][piece.y + i].piece != None:
                    if self.board.tiles[piece.x + i][piece.y + i].piece.type == 'king' and self.board.tiles[piece.x + i][piece.y + i].piece.color != piece.color:
                        return line
                line.append(self.board.tiles[piece.x + i][piece.y + i])
        line = []
        
        for i in range(0, (len(self.board.tiles) - piece.y)):
            if self.validateCoordinates(piece.x - i, piece.y + i):
                if self.board.tiles[piece.x - i][piece.y + i].piece != None:
                    if self.board.tiles[piece.x - i][piece.y + i].piece.type == 'king' and self.board.tiles[piece.x - i][piece.y + i].piece.color != piece.color:
                        return line
                line.append(self.board.tiles[piece.x - i][piece.y + i])

        
        if piece.type == 'knight':
            return [self.board.tiles[piece.x][piece.y]]

        return []

    def getPieceByType(self, type):
        for i in range(len(self.pieces)):
            if self.pieces[i].type == type:
                return self.pieces[i]
        return None

    def validateCoordinates(self, x, y):
        return (x > -1 and x < 8 and y > -1 and y < 8)
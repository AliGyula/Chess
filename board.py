from tile import Tile
from piece import Piece

class Board:
    def __init__(self):
        self.tiles = []
        self.setupTiles()

    def setupTiles(self):
        type = ''
        color = ''
        i = 0
        j = 0
        for x in range(0, 600, 75):
            self.tiles.append([])
            for y in range(0, 600, 75):
                color = ''
                if j == 0 or j == 1:
                    color = 'black'
                if j == 6 or j == 7:
                    color = 'white'
                if j == 1 or j == 6:
                    type = 'pawn'
                elif i == 0 or i == 7:
                    type = 'rook'
                elif i == 1 or i == 6:
                    type = 'knight'
                elif i == 2 or i == 5:
                    type = 'bishop'
                elif i == 3:
                    type = 'queen'
                elif i == 4:
                    type = 'king'
                if color == '':
                    self.tiles[-1].append(Tile(x, y))
                else:
                    self.tiles[-1].append(Tile(x, y, Piece(i, j, color, type)))
                    self.tiles[-1][-1].piece.tile = self.tiles[-1][-1]
                j += 1
            i += 1
            j = 0


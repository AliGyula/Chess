from piece import Piece

class Tile:
    def __init__(self, x, y, piece = None):
        self.x = x
        self.y = y
        self.piece = piece

    def deletePiece(self):
        self.piece = None

    def __str__(self):
        return f"x: {self.x}, y: {self.y}"
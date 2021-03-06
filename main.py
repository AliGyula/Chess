# 0.1 version: Matyi:1, Gyula:1
# 0.2 version: Matyi:0, Gyula:1

#bugok: tudunk sakkba lepni

from window import gui
from board import Board
import time
from tkinter import Tk, messagebox
from player import Player

width = 600
height = 600
handFull = False
pieceInHand = None
highlights = []

currentPlayer = 'white'
lastMovedPiece = None

def getItemfromCoordinates(x, y):
    return (x // 76, y // 76)

def onMouseDown(event, board):
    global handFull, pieceInHand, highlights, currentPlayer, lastMovedPiece
    moves = []
    index = getItemfromCoordinates(event.x, event.y)

    if handFull == False and board.tiles[index[0]][index[1]].piece != None and board.tiles[index[0]][index[1]].piece.color == currentPlayer:
        handFull = True
        pieceInHand = board.tiles[index[0]][index[1]].piece
        gui.canvas.tag_raise(pieceInHand.canvasElement)
    if pieceInHand != None:
        gui.canvas.coords(pieceInHand.canvasElement, event.x - 37, event.y - 37)
        gui.canvas.itemconfig(pieceInHand.canvasElement, image=pieceInHand.img)
        moves = pieceInHand.calculateValidMoves(board, lastMovedPiece)
    for i in range(len(moves)):
        if moves[i].piece == None or moves[i].piece.type != 'king':
            highlights.append(gui.canvas.create_rectangle(moves[i].x, moves[i].y, moves[i].x + 75, moves[i].y + 75, fill = "green", stipple='gray50'))

def onMouseUp(event, board):
    global handFull, pieceInHand, highlights, currentPlayer, lastMovedPiece, player1, player2

    if pieceInHand != None:
        moved = False

        index = getItemfromCoordinates(event.x, event.y)
        moves = pieceInHand.calculateValidMoves(board, lastMovedPiece)

        if board.tiles[index[0]][index[1]] in moves and (board.tiles[index[0]][index[1]].piece == None or board.tiles[index[0]][index[1]].piece.type != 'king'):
            board.tiles[pieceInHand.x][pieceInHand.y].deletePiece()
            pieceInHand.tile = board.tiles[index[0]][index[1]]
            pieceInHand.x = index[0]
            pieceInHand.y = index[1]

            if pieceInHand.type == 'king':
                if pieceInHand.isCastling:
                    if pieceInHand.x < 4:
                        rook = board.tiles[0][pieceInHand.y].piece
                        board.tiles[0][pieceInHand.y].deletePiece()
                        gui.canvas.coords(rook.canvasElement, board.tiles[index[0] + 1][index[1]].x, board.tiles[index[0] + 1][index[1]].y)
                        gui.canvas.itemconfig(rook.canvasElement, image=rook.img)
                        rook.hasMoved = True
                        rook.moveCount += 1
                        rook.x = index[0] + 1
                        rook.y = index[1]
                        board.tiles[index[0] + 1][index[1]].piece = rook
                    elif pieceInHand.x > 5:
                        rook = board.tiles[7][pieceInHand.y].piece
                        board.tiles[7][pieceInHand.y].deletePiece()
                        gui.canvas.coords(rook.canvasElement, board.tiles[index[0] - 1][index[1]].x, board.tiles[index[0] - 1][index[1]].y)
                        gui.canvas.itemconfig(rook.canvasElement, image=rook.img)
                        rook.hasMoved = True
                        rook.moveCount += 1
                        rook.x = index[0] - 1
                        rook.y = index[1]
                        board.tiles[index[0] - 1][index[1]].piece = rook

            if board.tiles[index[0]][index[1]].piece != None:
                if currentPlayer == 'black':
                    player1.deletePiece(board.tiles[index[0]][index[1]].piece)
                else:
                    player2.deletePiece(board.tiles[index[0]][index[1]].piece)
            elif pieceInHand.type == 'pawn' and lastMovedPiece!= None and lastMovedPiece.type == 'pawn' and lastMovedPiece.moveCount == 1:
                if currentPlayer == 'black' and board.tiles[index[0]][index[1] - 1].piece != None:
                    player1.deletePiece(board.tiles[index[0]][index[1] - 1].piece)
                    board.tiles[index[0]][index[1] - 1].deletePiece()
                elif currentPlayer == 'white' and board.tiles[index[0]][index[1] + 1].piece != None:
                    player2.deletePiece(board.tiles[index[0]][index[1] + 1].piece)
                    board.tiles[index[0]][index[1] + 1].deletePiece()

            board.tiles[index[0]][index[1]].piece = pieceInHand
            gui.canvas.coords(pieceInHand.canvasElement, board.tiles[index[0]][index[1]].x, board.tiles[index[0]][index[1]].y)
            gui.canvas.itemconfig(pieceInHand.canvasElement, image=pieceInHand.img)
            pieceInHand.hasMoved = True
            pieceInHand.moveCount += 1
            moved = True
            lastMovedPiece = pieceInHand
            currentPlayer = 'black' if currentPlayer == 'white' else 'white'
        else:
            gui.canvas.coords(pieceInHand.canvasElement, pieceInHand.tile.x, pieceInHand.tile.y)
            gui.canvas.itemconfig(pieceInHand.canvasElement, image=pieceInHand.img)

        for i in range(len(highlights)):
            gui.canvas.delete(highlights[i])
        pieceInHand = None
        handFull = False
        highlights = []
    player1.isChecked()
    player2.isChecked()

if __name__ == '__main__':
    window = Tk()
    board = Board()
    player1 = Player('player1', 'white', None, board)
    player2 = Player('player2', 'black', player1, board)
    player1.enemy = player2
    gui = gui(width, height, board, "Chess")
    gui.canvas.bind("<B1-Motion>", lambda event: onMouseDown(event, board))
    gui.canvas.bind("<ButtonRelease-1>", lambda event: onMouseUp(event, board))
    while 1:
        gui.update()
        gui.update_idletasks()
        time.sleep(0.01)
        """
        if player1.isInMate():
            messagebox.showinfo("Window", "fekete nyert")
            break
        if player2.isInMate():
            messagebox.showinfo("Window", "feher nyert")
            break
        """

gui.mainloop()
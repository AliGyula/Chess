import tkinter as tk
from tkinter import Canvas

from PIL import ImageTk
import os

class gui(tk.Frame):

    def __init__(self, width, height, board, title, master=None):
        self.width = width
        self.height = height
        self.title = title
        self.board = board.tiles
        tk.Frame.__init__(self, master)
        self.master.title(self.title)
        self.master.wm_iconbitmap('pawn.ico')
        self.master.geometry(str(self.width) + 'x' + str(self.height))
        self.master.resizable(0, 0)
        self.createCanvas()
        self.pack()
        self.updateIndexes()

        def onClose():
            os._exit(0)

        self.master.protocol("WM_DELETE_WINDOW", onClose)

    def createCanvas(self):
        color = 'black'
        self.canvas = Canvas(self.master, width=self.width, height=self.height, background='white')
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if (i % 2 == 1 and j % 2 == 1) or (i % 2 == 0 and j % 2 == 0):
                    color = 'white'
                else:
                    color = 'grey'
                self.canvas.create_rectangle(self.board[i][j].x, self.board[i][j].y, self.board[i][j].x + 75, self.board[i][j].y + 75, fill = color)
                if self.board[i][j].piece != None:
                    self.board[i][j].piece.canvasElement = self.canvas.create_image(self.board[i][j].x, self.board[i][j].y, image=self.board[i][j].piece.img, anchor='nw')
        self.canvas.pack()

    def updateIndexes(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j].piece != None:
                    self.canvas.tag_raise(self.board[i][j].piece.canvasElement)
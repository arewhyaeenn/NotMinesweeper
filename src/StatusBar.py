'''
    The StatusBar class will display the number of unflagged bombs (assuming all flags are correct).
    It will interact with the GameBoard to keep itself up to date.
'''

from Tkinter import *


class StatusBar:

    def __init__(self, master):

        # hierarchy
        self.master = master  # master is BombMopper instance
        self.board = master.board  # board is GameBoard instance

        # bomb image reference from board
        self.bombImage = self.board.bombImage

        # text display label for (bombs - flags)
        self.bombTextLabel = Label(self.master.statusFrame, text='')

        # image display label for bomb, next to text display
        self.bombImageLabel = Label(self.master.statusFrame, image=self.bombImage)

        # set reference to this StatusBar in the GameBoard
        self.board.setStatusBar(self)

        # pack and unpack to resize frame
        self.bombImageLabel.pack(side=RIGHT)
        self.bombTextLabel.pack(side=RIGHT)

    # update the text denoting number of unmarked bombs
    def updateText(self):
        self.bombTextLabel.config(text=str(self.board.nBombs - self.board.nFlags))

    # update text, pack bomb and text labels
    def activate(self):
        self.updateText()
        self.packContents()

    # pack both the text and bomb labels
    def packContents(self):
        self.bombImageLabel.pack(side=RIGHT)
        self.bombTextLabel.pack(side=RIGHT)

    # stop displaying
    def deactivate(self):
        self.bombImageLabel.pack_forget()
        self.bombTextLabel.pack_forget()

from Tkinter import *
import tkMessageBox
from PlayButton import PlayButton
from GameBoard import GameBoard
from DifficultyButton import DifficultyButton


class BombMopper:

    def __init__(self):

        # settings
        self.buttonSize = 25
        self.defaultWidth = 500
        self.defaultHeight = 500
        self.padding = 20
        self.buttonImagePadding = 10
        self.adjBombTextSize = 25

        # window
        self.tk = Tk()
        self.tk.title("BOMBMOPPER")

        # frames
        self.statusFrame = Frame(self.tk)
        self.statusFrame.pack(side=TOP)

        self.gameFrame = Frame(self.tk)
        self.gameFrame.pack(side=BOTTOM)

        # canvas
        self.canvasWidth = self.defaultWidth
        self.canvasHeight = self.defaultHeight
        self.canvas = Canvas(self.gameFrame)
        self.canvas.config(
            width=self.canvasWidth,
            height=self.canvasHeight,
            background='gray',
            highlightthickness=0
        )
        self.canvas.grid(column=0, row=0, sticky=(N, W, E, S))

        # play button
        self.playButton = PlayButton(self)

        # difficulty buttons
        self.easyButton = DifficultyButton(self, 'easy')
        self.intermediateButton = DifficultyButton(self, 'intermediate')
        self.hardButton = DifficultyButton(self, 'hard')

        # initialize board
        self.board = GameBoard(self)

        self.isActive = True

    def selectDifficulty(self):

        # turn off play button
        self.playButton.deactivate()

        # turn on difficulty selection buttons
        self.easyButton.activate()
        self.intermediateButton.activate()
        self.hardButton.activate()
        self.resizeCanvasToDefault()

    def playGame(self, gridSize, nBombs):

        # turn off difficulty selection buttons
        self.easyButton.deactivate()
        self.intermediateButton.deactivate()
        self.hardButton.deactivate()

        # start game board
        self.board.activate(gridSize, nBombs)

    def resizeCanvasToDefault(self):
        self.canvasWidth = self.defaultWidth
        self.canvasHeight = self.defaultHeight
        self.canvas.config(
            width=self.canvasWidth,
            height=self.canvasHeight
        )

    def resizeCanvas(self, width, height):
        self.canvasWidth = width
        self.canvasHeight = height
        self.canvas.config(
            width=self.canvasWidth,
            height=self.canvasHeight
        )

    def mainloop(self):
        while self.isActive:
            self.tk.update()
            self.canvas.update()
        self.tk.destroy()

    def winGame(self):
        self.winLose("YOU WIN!")

    def loseGame(self):
        self.winLose("YOU LOSE!\nand you smell")

    def winLose(self, message):
        self.tk.after(100, lambda: self.winLosePopup(message))

    def winLosePopup(self, message):
        result = tkMessageBox.askquestion(message, "Keep Playing?")
        if result == "yes":
            self.board.reset()
            self.resizeCanvasToDefault()
            self.canvas.delete('all')
            self.playButton.activate()
        else:
            self.isActive = False


if __name__ == '__main__':
    game = BombMopper()
    game.mainloop()

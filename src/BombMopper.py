'''
    The BombMopper class is the top layer; it will:
        - run the Tkinter window that the game is in
        - run the Canvas on which buttons, pictures etc will be drawn
        - run the Frames containing the game components
        - run the PlayButton, DifficultyButtons, and GameBoard
'''

from Tkinter import *
import tkMessageBox
from PlayButton import PlayButton
from GameBoard import GameBoard
from DifficultyButton import DifficultyButton


class BombMopper:

    # initialize game window
    def __init__(self):

        # settings
        self.buttonSize = 25
        self.defaultCanvasWidth = 500
        self.defaultCanvasHeight = 500
        self.padding = 20
        self.buttonImagePadding = 10
        self.adjBombTextSize = 25

        # window
        self.window = Tk()
        self.window.title("BOMBMOPPER")

        # frames
        self.statusFrame = Frame(self.window)
        self.statusFrame.pack(side=TOP)

        self.gameFrame = Frame(self.window)
        self.gameFrame.pack(side=BOTTOM)

        # canvas
        self.canvasWidth = self.defaultCanvasWidth
        self.canvasHeight = self.defaultCanvasHeight
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

    # transition from opening screen (with play button) to difficulty selection
    def selectDifficulty(self):

        # turn off play button
        self.playButton.deactivate()

        # turn on difficulty selection buttons
        self.easyButton.activate()
        self.intermediateButton.activate()
        self.hardButton.activate()
        self.resizeCanvasToDefault()

    # transition from difficulty selection to playing game
    def playGame(self, gridSize, nBombs):

        # turn off difficulty selection buttons
        self.easyButton.deactivate()
        self.intermediateButton.deactivate()
        self.hardButton.deactivate()

        # start game board
        self.board.activate(gridSize, nBombs)

    # reset size of canvas (for use after game a game ends)
    def resizeCanvasToDefault(self):
        self.resizeCanvas(self.defaultCanvasHeight, self.defaultCanvasWidth)

    # resize canvas; width and height are calculated in GameBoard based on selected difficulty
    def resizeCanvas(self, width, height):
        self.canvasWidth = width
        self.canvasHeight = height
        self.canvas.config(
            width=self.canvasWidth,
            height=self.canvasHeight
        )

    # keep displays up to date; run continuously
    # buttons run callbacks which update parameters of window / canvas
    # display is updated to match parameters when mainloop runs
    def mainloop(self):
        while self.isActive:
            self.window.update()
            self.canvas.update()
        self.window.destroy()

    # run win/lose dialogue with win message
    def winGame(self):
        self.winLose("YOU WIN!")

    # run win/lose dialogue with lose message
    def loseGame(self):
        self.winLose("YOU LOSE!\nand you smell")

    # wait a short time (100ms), then open the win/lose dialogue with input message
    def winLose(self, message):
        self.window.after(100, lambda: self.winLosePopup(message))

    # open win/lose dialogue with input message
    # essentially says "<message>, Keep Playing?" and user selects yes or no
    def winLosePopup(self, message):
        result = tkMessageBox.askquestion(message, "Keep Playing?")
        if result == "yes":
            self.board.reset()
            self.resizeCanvasToDefault()
            self.canvas.delete('all')
            self.playButton.activate()
        else:
            self.isActive = False


# main method (i.e. entry point when run)
# when we run this project, this method is what is run
# it references the BombMopper class, which references the other classes...
if __name__ == '__main__':
    game = BombMopper()
    game.mainloop()

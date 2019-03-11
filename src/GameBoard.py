'''
    The GameBoard class will run the core of the MineSweeper (er... BombMopper) game.
    It will:
        - import and store all assets (images) and colors
        - set up and control a grid of BombButtons
        - track win/lose conditions
'''

from Tkinter import *
from PIL import Image, ImageTk
from BombButton import BombButton
from random import randrange


class GameBoard:

    def __init__(self, master):

        # hierarchy
        self.master = master  # master is BombMopper instance

        # board fields
        self.gridSize = None
        self.nBombs = None
        self.nFlags = 0
        self.board = None
        self.safeCoords = None
        self.nSafeCoords = 0

        # import button images
        self.flagImage = self.importButtonImage('../images/flag.jpg')
        self.questionImage = self.importButtonImage('../images/question.jpg')
        self.buttonImages = [  # list of button images for easy state switching
            '',  # index 0 (empty string denotes "no image")
            self.flagImage,  # index 1 - flag
            self.questionImage  # index 2 - question mark
        ]

        # import bomb image... we're good at minesweeper so we'll never see this :)
        self.bombImage = self.importBackgroundImage('../images/bomb.jpg')

        # colors for adjacent mine number displays (using Tkinter's preset colors because lazy))
        self.numberColors = [
            None,  # we don't draw 0's... placeholder for easy indexing because future me is lazy
            'blue2',  # 1...
            'green2',
            'red',
            'blue4',
            'firebrick4',
            'cyan',
            'mightnight blue',
            'black'
        ]

    # sets up grid, does not place mines
    def activate(self, gridSize, nBombs):

        # set fields
        self.gridSize = gridSize
        self.nBombs = nBombs

        # resize canvas
        canvasSize = self.master.buttonSize * self.gridSize + self.master.padding
        self.master.resizeCanvas(canvasSize, canvasSize)

        # create board (wow this is so ugly but its too long in one line)
        self.board = [
            [
                BombButton(self, x, y) for y in range(gridSize)
            ] for x in range(gridSize)
        ]

        # make safe coords (no bombs yet, everywhere is safe)
        self.safeCoords = [(x, y) for x in range(gridSize) for y in range(gridSize)]

    # import image specified by path and resize for use on button
    def importButtonImage(self, path):
        buttonImageSize = self.master.buttonSize - self.master.buttonImagePadding
        return ImageTk.PhotoImage(
            Image.open(path).resize(
                (buttonImageSize, buttonImageSize),
                Image.ANTIALIAS
            )
        )

    # import image specified by path and resize for use on canvas
    def importBackgroundImage(self, path):
        buttonImageSize = self.master.buttonSize
        return ImageTk.PhotoImage(
            Image.open(path).resize(
                (buttonImageSize, buttonImageSize),
                Image.ANTIALIAS
            )
        )

    # place bombs; x,y are coords of first click, do not place bombs on or adjacent to x,y
    def startGame(self, x, y):

        # create bombs
        nBombs = 0
        while nBombs < self.nBombs:
            bombCoordIndex = randrange(len(self.safeCoords))
            bx, by = self.safeCoords.pop(bombCoordIndex)  # get coords for random space with no mine
            if abs(bx - x) > 1 or abs(by - y) > 1:  # make sure it's not the start spot or adjacent...
                self.board[bx][by].isBomb = True  # place a bomb
                nBombs += 1
            else:
                self.safeCoords.append((bx, by))  # put it back if it was adjacent to first click...

        self.nSafeCoords = len(self.safeCoords)

        # update grid
        for x in range(self.gridSize):
            for y in range(self.gridSize):
                self.board[x][y].onStartGame()

    # called when player clears a safe space
    def removeSafeNode(self, coords):

        # decrement number of remaining safe spaces
        self.nSafeCoords -= 1

        # if player has cleared all safe spaces, win game
        if self.nSafeCoords == 0:
            self.master.winGame()

    # remove keybinds on all buttons
    def unbindButtons(self):
        for x in range(self.gridSize):
            for y in range(self.gridSize):
                self.board[x][y].unbind()

    def reset(self):

        # delete buttons
        for x in range(self.gridSize):
            for y in range(self.gridSize):
                self.board[x][y].delete()

        # reset fields to init
        self.gridSize = None
        self.nBombs = None
        self.nFlags = 0
        self.board = None
        self.safeCoords = None
        self.nSafeCoords = 0

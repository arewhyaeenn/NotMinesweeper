from Tkinter import *
from PIL import Image, ImageTk
from BombButton import BombButton
from random import randrange


class GameBoard:

    def __init__(self, master):

        # hierarchy
        self.master = master

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
        self.buttonImages = [
            '',  # I guess Tkinter uses the empty string as "No Image" but not None or 0 -_-
            self.flagImage,
            self.questionImage
        ]

        # import bomb image...
        self.bombImage = self.importBackgroundImage('../images/bomb.jpg')

        # colors for number displays (using preset colors)
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

    def importButtonImage(self, path):
        buttonImageSize = self.master.buttonSize - self.master.buttonImagePadding
        return ImageTk.PhotoImage(
            Image.open(path).resize(
                (buttonImageSize, buttonImageSize),
                Image.ANTIALIAS
            )
        )

    def importBackgroundImage(self, path):
        buttonImageSize = self.master.buttonSize
        return ImageTk.PhotoImage(
            Image.open(path).resize(
                (buttonImageSize, buttonImageSize),
                Image.ANTIALIAS
            )
        )

    def startGame(self, x, y):

        # create bombs
        nBombs = 0
        while nBombs < self.nBombs:
            bombCoordIndex = randrange(len(self.safeCoords))
            bx, by = self.safeCoords.pop(bombCoordIndex)  # get random pair of safe coords
            if (bx != x or by != y):  # make sure it's not the start spot
                self.board[bx][by].isBomb = True
                nBombs += 1
            else:
                self.safeCoords.append((bx, by))  # put it back if it was the start spot...

        self.nSafeCoords = len(self.safeCoords)

        # update grid
        for x in range(self.gridSize):
            for y in range(self.gridSize):
                self.board[x][y].onStartGame()

    def removeSafeNode(self, coords):
        # self.safeCoords.remove(coords)
        # if len(self.safeCoords) == 0:
        #     self.master.winGame()

        # actually just track how many...
        self.nSafeCoords -= 1
        if self.nSafeCoords == 0:
            self.master.winGame()

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

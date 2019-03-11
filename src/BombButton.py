'''
    The BombButton class will occupy a single space on the GameBoard.
    It will:
        - track its own status (cleared, flagged, unknown (question mark), blank)
        - bind to user inputs, perform appropriate action(s) when clicked
        - access and display images stored in GameBoard as appropriate
'''

from Tkinter import *


class BombButton:

    def __init__(self, board, x, y):

        # hierarchy
        self.board = board  # GameBoard instance running buttons
        self.master = board.master  # BombMopper instance running GameBoard
        self.canvas = self.master.canvas  # Canvas on which buttons are drawn

        # button position
        self.x = x
        self.xPosition = float(x) / self.board.gridSize

        self.y = y
        self.yPosition = float(y) / self.board.gridSize

        # create button
        self.button = Button(
            self.canvas,
            bg='blue',
            fg='blue',
            # activebackground='black',
            # activeforeground='black'
            highlightbackground='gray'
        )

        # bind button clicks to start the game
        self.button.bind('<Button-1>', self.startGame)  # will change to self.onLeftClick once game starts
        self.buttonState = 0  # 0 for blank, 1 for flag, 2 for question mark

        # local bombs
        self.nAdjBombs = 0
        self.isBomb = False
        self.background = None  # for text or bomb image

        # place button on canvas
        self.isActive = True  # isActive is a flag boolean for "this button hasn't been clicked yet"
        self.activate()

    # turn on button display, set status to active
    def activate(self):
        self.button.place(
            relx=self.xPosition,
            rely=self.yPosition,
            anchor=NW
        )
        self.isActive = True

    # turn off button display, set status to inactive
    def deactivate(self):
        self.button.place_forget()
        self.isActive = False

    # remove keybinds (for use when deleting board after game ends)
    def unbind(self):
        self.button.unbind('<Button-1>')
        self.button.unbind('<Shift-Button-1>')

    # deactivate and delete; for use when game ends
    def delete(self):
        self.unbind()
        self.deactivate()
        del self

    # when left clicked
    def onLeftClick(self, event):  # event is passed in automatically by bind, stores click location etc

        # does nothing if flagged or question marked
        if self.buttonState == 0:  # if not flagged or question marked

            # if it's a bomb, blow up
            if self.isBomb:
                self.kaboom()

            # if it's not a bomb, reveal the space
            else:
                self.reveal()

    # when a bomb is clicked...
    def kaboom(self):
        self.deactivate()
        self.background = self.canvas.create_image(
            self.canvas.winfo_width() * self.xPosition + self.master.buttonSize / 2,
            self.canvas.winfo_height() * self.yPosition + self.master.buttonSize / 2,
            image=self.board.bombImage,
            anchor=CENTER
        )
        self.master.loseGame()

    # when a safe space is clicked...
    def reveal(self):
        if self.isActive:
            self.deactivate()
            if self.nAdjBombs == 0:
                for neighbor in self.getNeighbors():
                    neighbor.reveal()
            else:
                self.background = self.canvas.create_text(
                    self.canvas.winfo_width() * self.xPosition + self.master.buttonSize / 2,
                    self.canvas.winfo_height() * self.yPosition + self.master.buttonSize / 2,
                    text=str(self.nAdjBombs),
                    font=("Times", self.master.adjBombTextSize),
                    anchor=CENTER,
                    fill=self.board.numberColors[self.nAdjBombs]
                )
            self.board.removeSafeNode((self.x, self.y))

    # shift button state; 0 for blank, 1 for flag, 2 for question mark
    def onRightClick(self, event):
        self.buttonState = (self.buttonState + 1) % 3
        self.button.config(
            image=self.board.buttonImages[self.buttonState]
        )
        if self.buttonState == 1:
            self.board.incrementFlags()
        elif self.buttonState == 2:
            self.board.decrementFlags()

    # when a button is clicked initially, tell GameBoard instance to start the game
    # then, reveal the spot that was clicked
    def startGame(self, event):
        self.board.startGame(self.x, self.y)
        self.reveal()

    # when the game is started, rebind buttons for gameplay and count adjacent bombs
    # called on all buttons by GameBoard when the game starts
    def onStartGame(self):

        # rebind keys for gameplay
        self.button.bind('<Button-1>', self.onLeftClick)
        self.button.bind('<Button-3>', self.onRightClick)
        self.button.bind('<Shift-Button-1>', self.onRightClick)  # for those of us with 1-button mice

        # iterate adjacent mine counts (er... bomb counts <.< >.>) if necessary
        if self.isBomb:
            for neighbor in self.getNeighbors():
                neighbor.nAdjBombs += 1  # Python please give me ++

    # get list of adjacent BombButtons on grid
    def getNeighbors(self):

        # list of neighbors
        neighbors = []
        gridSize = self.board.gridSize

        # theres probably a way more efficient way to do this
        for i in range(-1, 2):  # -1, 0, 1
            for j in range(-1, 2):  # -1, 0, 1

                # store coords of adjacent space
                x = self.x + i
                y = self.y + j

                # check that space is both in the grid and not the button calling getNeighbors
                if x >= 0 and y >= 0 and x < gridSize and y < gridSize and (x != self.x or y != self.y):
                    neighbors.append(self.board.board[x][y])  # add neighbor to list

        return neighbors

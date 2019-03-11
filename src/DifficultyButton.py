'''
    The DifficultyButton class will run a Button for difficulty selection.
    The BombMopper class will use three of these (for easy, medium and hard) for difficulty selection.
    The Button will pass parameters (grid size, bumber of bombs, ...) to the GameBoard
'''

from Tkinter import *

class DifficultyButton:

    # initialize difficulty selection button based on input difficulty
    def __init__(self, master, difficulty):

        # hierarchy
        self.master = master  # master is BombMopper instance

        # difficulty settings
        self.nBombs = None  # number of bombs corresponding to difficulty
        self.gridSize = None  # size of (presumed square) grid corresponding to difficulty

        # canvas placement settings
        self.y = None  # where to place button; proportion of canvas size

        # button settings
        color = None
        text = None

        # assign settings
        if difficulty == 'easy':
            color = 'green'
            text = 'EASY'
            self.gridSize = 8
            self.nBombs = 10
            self.y = 0.25
        elif difficulty == 'intermediate':
            color = 'orange'
            text = 'INTERMEDIATE'
            self.gridSize = 16
            self.nBombs = 40
            self.y = 0.5
        else:
            color = 'red'
            text = 'HARD'
            self.gridSize = 24
            self.nBombs = 99
            self.y = 0.75

        # create button
        self.button = Button(
            self.master.canvas,
            text=text,
            bg=color,
            command=self.onClick
        )

    # turn on (i.e. display) button
    def activate(self):
        self.button.place(relx=0.5, rely=self.y, anchor=CENTER)

    # turn off button display
    def deactivate(self):
        self.button.place_forget()

    # when button is clicked...
    def onClick(self):
        self.master.playGame(self.gridSize, self.nBombs)

from Tkinter import *

class DifficultyButton:

    def __init__(self, master, difficulty):

        # hierarchy
        self.master = master

        # difficulty settings
        self.nBombs = None
        self.gridSize = None

        # canvas placement settings
        self.y = None

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

    def activate(self):
        self.button.place(relx=0.5, rely=self.y, anchor=CENTER)

    def deactivate(self):
        self.button.place_forget()

    def onClick(self):
        self.master.playGame(self.gridSize, self.nBombs)

'''
    The PlayButton class is runs a simple Tkinter Button.
    The Button will tell the BombMopper instance to transition to the Difficulty Selection screen.
'''

from Tkinter import *

class PlayButton:

    # initialize play button
    def __init__(self, master):

        # hierarchy
        self.master = master  # master is BombMopper instance

        # button
        self.button = Button(master.canvas, text="Play", command=self.onClick)
        self.activate()

    # what happens when button is clicked
    def onClick(self):
        self.master.selectDifficulty()

    # turn off button (i.e. stop it from being displayed / clicked)
    def deactivate(self):
        self.button.place_forget()

    # turn on button (display it so it can be clicked)
    def activate(self):
        self.button.place(relx=0.5, rely=0.5, anchor=CENTER)

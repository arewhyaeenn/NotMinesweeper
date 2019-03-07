from Tkinter import *

class PlayButton:

    def __init__(self, master):

        # hierarchy
        self.master = master

        # button
        self.button = Button(master.canvas, text="Play", command=self.onClick)
        self.activate()

    def onClick(self):
        self.master.selectDifficulty()

    def deactivate(self):
        self.button.place_forget()

    def activate(self):
        self.button.place(relx=0.5, rely=0.5, anchor=CENTER)

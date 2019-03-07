from Tkinter import *


class BombButton:

    def __init__(self, master, x, y):

        # hierarchy
        self.master = master
        self.canvas = master.master.canvas

        # button position
        self.x = x
        self.xPosition = float(x) / self.master.gridSize

        self.y = y
        self.yPosition = float(y) / self.master.gridSize

        # create button
        self.button = Button(
            self.canvas,
            #command=self.onClick
        )

        # bind button clicks
        self.button.bind('<Button-1>', self.startGame)  # will change to self.onLeftClick once game starts
        self.buttonState = 0  # 0 for blank, 1 for flag, 2 for question mark

        # local bombs
        self.nAdjBombs = 0
        self.isBomb = False
        self.background = None  # for text or bomb image

        # place button on canvas
        self.isActive = True
        self.activate()

    def activate(self):
        self.button.place(
            relx=self.xPosition,
            rely=self.yPosition,
            anchor=NW
        )
        self.isActive = True

    def deactivate(self):
        self.button.place_forget()
        self.isActive = False

    def delete(self):
        self.deactivate()
        del self

    def onLeftClick(self, event):  # event is passed in automatically by bind, stores click location etc
        if self.buttonState == 0:  # if not flagged or question marked
            if self.isBomb:
                self.kaboom()
            else:
                self.reveal()

    def onRightClick(self, event):
        self.buttonState = (self.buttonState + 1) % 3
        self.button.config(
            image=self.master.buttonImages[self.buttonState]
        )

    def startGame(self, event):
        self.master.startGame(self.x, self.y)
        self.reveal()

    def onStartGame(self):

        # rebind keys for gameplay
        self.button.bind('<Button-1>', self.onLeftClick)
        #self.button.bind('<Button-3>', self.onRightClick)
        self.button.bind('<Shift-Button-1>', self.onRightClick)  # lazy workaround for 1 button mouse

        # iterate adjacent mine counts (er... bomb counts <.< >.>) if necessary
        if self.isBomb:
            for neighbor in self.getNeighbors():
                neighbor.nAdjBombs += 1  # wow I forgot ++ doesn't exist -_-

    def getNeighbors(self):
        neighbors = []
        gridSize = self.master.gridSize
        # theres probably a way more efficient way to do this
        for i in range(-1, 2):
            for j in range(-1, 2):
                x = self.x + i
                y = self.y + j
                if (x >= 0 and y >= 0 and x < gridSize and y < gridSize and (x != self.x or y != self.y)):
                    neighbors.append(self.master.board[x][y])
        return neighbors

    def kaboom(self):
        self.deactivate()
        #self.button.config(image=self.master.bombImage)
        self.background = self.canvas.create_image(
            self.canvas.winfo_width() * self.xPosition + self.master.master.buttonSize / 2,
            self.canvas.winfo_height() * self.yPosition + self.master.master.buttonSize / 2,
            image=self.master.bombImage,
            anchor=CENTER
        )
        self.master.master.loseGame()

    def reveal(self):
        if self.isActive:
            self.deactivate()
            if self.nAdjBombs == 0:
                for neighbor in self.getNeighbors():
                    neighbor.reveal()
            else:
                self.background = self.canvas.create_text(
                    self.canvas.winfo_width() * self.xPosition + self.master.master.buttonSize / 2,
                    self.canvas.winfo_height() * self.yPosition + self.master.master.buttonSize / 2,
                    text=str(self.nAdjBombs),
                    font=("Times", self.master.master.adjBombTextSize),
                    anchor=CENTER,
                    fill=self.master.numberColors[self.nAdjBombs]
                )
            self.master.removeSafeNode((self.x, self.y))

    def unbind(self):
        self.button.unbind('<Button-1>')
        self.button.unbind('<Shift-Button-1>')



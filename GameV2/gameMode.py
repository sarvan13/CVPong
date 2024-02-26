from abc import ABC, abstractmethod 

class GameMode(ABC):
    def __init__(self, screen, cap, mp_hands, hands):
        self.screen = screen
        self.cap = cap
        self.mp_hands = mp_hands
        self.hands = hands
        self.running = True
        self.useCV = -1
        self.paused = False
        self.fadeIn = True
        self.returnMenu = False
    
    def runGame(self):
        while self.useCV == -1:
            self.getInput()
        
        if self.fadeIn:
            self.countDown()

        while(self.running):
            while self.paused:
                self.pauseScreen()
            if self.fadeIn:
                self.countDown()
            self.interruptGame()
            self.updateScore()
            self.calculateFrame()
            self.drawFrame()
            self.displayPygame()
    
    @abstractmethod
    def pauseScreen(self):
        pass

    @abstractmethod
    def getInput(self):
        pass

    @abstractmethod
    def calculateFrame(self):
        pass

    @abstractmethod
    def updateScore(self):
        pass

    @abstractmethod
    def drawFrame(self):
        pass
    
    @abstractmethod
    def displayPygame():
        pass

    @abstractmethod
    def interruptGame(self):
        pass

    @abstractmethod
    def gameOver(self):
        pass

    @abstractmethod
    def resetGame(self):
        pass

    @abstractmethod
    def countDown(self):
        pass
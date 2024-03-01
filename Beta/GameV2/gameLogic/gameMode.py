from abc import ABC, abstractmethod 

# This abstract class defines what all game modes should look like as well as defining
# the overarching workflow of the game
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
        self.gameOver = False
        self.endText = ""
        self.right_score = 0
        self.left_score = 0
        self.score = 0
    
    # Outlines the workflow for all game modes
    def runGame(self):
        while self.useCV == -1:
            self.getInput()
        
        if self.fadeIn and self.running:
            self.countDown()

        while(self.running):
            while self.paused:
                self.pauseScreen()
                self.fadeIn = True
            if self.fadeIn and self.running:
                self.countDown()
            self.interruptGame()
            self.updateScore()
            self.calculateFrame()
            self.drawFrame()
            self.displayPygame()
            self.checkGameOver()
    
    # This method is where the work of the game is done. It is where we calculate what the next
    # frame should look like. All vision and physics should be done within this method
    @abstractmethod
    def calculateFrame(self):
        pass

    # Calculate/update the score for each game
    @abstractmethod
    def updateScore(self):
        pass

    # Draw the shapes on the pygame surface
    @abstractmethod
    def drawFrame(self):
        pass
    
    # Display the surface to the users screen
    @abstractmethod
    def displayPygame():
        pass

    # Handles any interrupts ie quitting the game and setting the state to paused
    @abstractmethod
    def interruptGame(self):
        pass

    # Check and enforce the game over requirement 
    @abstractmethod
    def checkGameOver(self):
        pass

    # Reset the game state - should be called within checkGameOver when the game is over
    @abstractmethod
    def resetGame(self):
        pass

    # Handle displaying the pause screen and setting the game state afterwards
    # displays a menu selection screen
    @abstractmethod
    def pauseScreen(self):
        pass

    # Gets the players desired input method (KB or CV)
    # displays a menu selection screen
    @abstractmethod
    def getInput(self):
        pass

    # 3 second count down on beginning of game
    @abstractmethod
    def countDown(self):
        pass
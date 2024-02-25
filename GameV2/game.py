from abc import ABC, abstractmethod 
class Game(ABC):
    def __init__(self, screen, cap, mp_hands, hands):
        self.screen = screen
        self.cap = cap
        self.mp_hands = mp_hands
        self.hands = hands
        self.running = True
    
    @abstractmethod
    def runGame(self):
        pass

    @abstractmethod
    def calculateFrame():
        pass
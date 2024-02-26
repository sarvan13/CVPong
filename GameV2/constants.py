from enum import Enum 

WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALL_SPEED = 5
PADDLE_SPEED = 8
COMP_SPEED = 6
COUNTDOWN_NUM_WIDTH = 21

DEFAULT_FONT_SIZE = 36
SELECTED_FONT_SIZE = 46
TITLE_FONT_SIZE = 56

options = ["Classic", "Infinite", "Two Player", "Exit"]

class State(Enum):
    MENU = 0
    CLASSIC = 1
    INFINITE = 2
    PVP = 3
    EXIT = 4
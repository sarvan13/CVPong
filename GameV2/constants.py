from enum import Enum 

WIDTH, HEIGHT = 800, 600
FPS = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (252,70,236)
BALL_SPEED = 12
PADDLE_SPEED = 17
COMP_SPEED = 10
MAX_SPEED_INC = 6
SPEED_MULT = 0.5
MIN_ANGLE = 20
COUNTDOWN_NUM_WIDTH = 21
FRAME_SCALE = 0.7
WIN_SCORE = 1

DEFAULT_FONT_SIZE = 36
SELECTED_FONT_SIZE = 46
TITLE_FONT_SIZE = 56
BAYSHORE_ADJ = 20

options = ["Classic", "Infinite", "Two Player", "Exit"]

class State(Enum):
    MENU = 0
    CLASSIC = 1
    INFINITE = 2
    PVP = 3
    EXIT = 4
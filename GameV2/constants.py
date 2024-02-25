from enum import Enum 
import pygame

WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALL_SPEED = 5
PADDLE_SPEED = 8
COMP_SPEED = 6

options = ["Classic", "Infinite", "2 Player", "Exit"]

class State(Enum):
    MENU = 0
    CLASSIC = 1
    INFINITE = 2
    PVP = 3
import pygame

def loadPongSound():
    return pygame.mixer.Sound("sounds/pong-noise.wav")

def loadGameOverSound():
    return pygame.mixer.Sound("sounds/game-over.wav")

def loadScoreSound():
    return pygame.mixer.Sound("sounds/point-noise.mp3")

def loadWinSound():
    return pygame.mixer.Sound("sounds/win-noise.mp3")
def loadConcedeSound():
    return pygame.mixer.Sound("sounds/bad-noise.mp3")
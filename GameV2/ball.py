import constants
from paddle import Paddle
import pygame

class Ball:
    def __init__(self, pygame_rect, spin):
        self.pygame_rect = pygame_rect
        self.vx = constants.BALL_SPEED
        self.vy = constants.BALL_SPEED
        self.spin = spin
        self.score_left = 0
        self.score_right = 0

    def moveBall(self, left_paddle, right_paddle):
        self.pygame_rect.x += self.vx
        self.pygame_rect.y += self.vy

        if self.pygame_rect.top <= 0 or self.pygame_rect.bottom >= constants.HEIGHT:
            self.vy = -self.vy

        if self.pygame_rect.colliderect(left_paddle.pygame_rect) \
              or self.pygame_rect.colliderect(right_paddle.pygame_rect):
            self.vx = -self.vx

        if self.pygame_rect.left <= 0:
            self.score_right += 1
            self.pygame_rect.x = constants.WIDTH // 2 - self.pygame_rect.width // 2
            self.vx = constants.BALL_SPEED

        if self.pygame_rect.right >= constants.WIDTH:
            self.score_left += 1
            self.pygame_rect.x = constants.WIDTH // 2 - self.pygame_rect.width // 2
            self.vx = -constants.BALL_SPEED

import pygame
import constants
import cv2
import mediapipe as mp

class Paddle:
    def __init__(self, pygame_rect, speed):
        self.pygame_rect = pygame_rect
        self.speed = speed
    
    def movePlayerCV(self, frame, mp_hands, hands):
        return
    
    def movePlayerKey(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.pygame_rect.top > 0:
            self.pygame_rect.y -= constants.PADDLE_SPEED
        if keys[pygame.K_DOWN] and self.pygame_rect.bottom < constants.HEIGHT:
            self.pygame_rect.y += constants.PADDLE_SPEED
    
    def moveComp(self, movespeed, ball):
        paddle_x = self.pygame_rect.right
        ball_x_curr = ball.pygame_rect.left
        if ball_x_curr > paddle_x and ball.vx < 0:
            # Calculate where the ball will be going
            ball_traj_y = ((paddle_x - ball_x_curr) / ball.vx) * ball.vy \
            + ball.pygame_rect.centery

            diff = ball_traj_y - self.pygame_rect.centery 

            if abs(diff) > movespeed:
                self.pygame_rect.centery = (diff/abs(diff))*movespeed + self.pygame_rect.centery
            else:
                self.pygame_rect.centery = ball_traj_y
            
            if self.pygame_rect.top < 0:
                self.pygame_rect.top = 0
            if self.pygame_rect.bottom > constants.HEIGHT:
                self.pygame_rect.bottom = constants.HEIGHT

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

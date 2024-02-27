import pygame
import GameV2.constants as constants
import cv2
import mediapipe as mp
import numpy as np
from time import time

class Paddle:
    def __init__(self, pygame_rect, speed):
        self.pygame_rect = pygame_rect
        self.speed = speed
        self.time_last_hit = -1
    
    # Draw
    def movePlayerCV(self, frame, mp_hands, hands):
        results = hands.process(frame)
        frame_height = frame.shape[0]
        frame_edge = (1 - constants.FRAME_SCALE) / 2

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Get the coordinates of the center of the hand
                cx, cy = int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].x * frame.shape[1]), \
                         int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y * frame.shape[0])
                
                game_y = np.clip(cy, frame_height * frame_edge, frame_height * (1-frame_edge)) - (frame_height * frame_edge)
                game_y = game_y * (constants.HEIGHT/ (frame_height *constants.FRAME_SCALE))
                game_y = np.clip(game_y, self.pygame_rect.height // 2, constants.HEIGHT - self.pygame_rect.height // 2)
                self.speed = game_y - self.pygame_rect.centery
                self.pygame_rect.centery = game_y

                # Draw a circle at the center of the hand
                cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)
        
        cv2.imshow('Hand Tracking', frame)
    
    def movePlayerKey(self, key_up, key_down):
        keys = pygame.key.get_pressed()
        if keys[key_up] and self.pygame_rect.top > 0:
            self.pygame_rect.y -= constants.PADDLE_SPEED
        if keys[key_down] and self.pygame_rect.bottom < constants.HEIGHT:
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
        self.past_left = 0
        self.past_right = 0
        self.time = time()

    def moveBall(self, left_paddle, right_paddle):
        self.time = time()
        self.pygame_rect.x += self.vx
        self.pygame_rect.y += self.vy

        self.checkPaddleCollision(left_paddle)
        self.checkPaddleCollision(right_paddle)

        if self.pygame_rect.top <= 0:
            self.vy = abs(self.vy)
        if self.pygame_rect.bottom >= constants.HEIGHT:
            self.vy = -1 * abs(self.vy)

        if self.pygame_rect.left <= 0:
            self.past_left += 1
            self.pygame_rect.x = constants.WIDTH // 2 - self.pygame_rect.width // 2
            self.vx = constants.BALL_SPEED
            self.vy = constants.BALL_SPEED

        if self.pygame_rect.right >= constants.WIDTH:
            self.past_right += 1
            self.pygame_rect.x = constants.WIDTH // 2 - self.pygame_rect.width // 2
            self.vx = -constants.BALL_SPEED
            self.vy = constants.BALL_SPEED
    
    def checkPaddleCollision(self, paddle):
        # We dont want to keep checking the same paddle if we already collided with it otherwise it leads
        # to unwanted edge case behaviour so we put the paddle on a collision cool down of 200 ms
        if self.pygame_rect.colliderect(paddle.pygame_rect) and (self.time - paddle.time_last_hit) > 0.2:
            paddle.time_last_hit = self.time
            if self.pygame_rect.bottom > paddle.pygame_rect.bottom:
                # This means the ball is either on the corner or bottom of the paddle
                self.vy = abs(self.vy) # force the ball to bounce down

                # If its a corner bounce it back to the playing field but with a potentially changed y
                if self.pygame_rect.right > (paddle.pygame_rect.right + self.pygame_rect.width // 2) \
                    or self.pygame_rect.left < (paddle.pygame_rect.left - self.pygame_rect.width // 2):
                    self.vx = -self.vx
                    self.vx = self.vx / abs(self.vx) + self.vx
                    self.vy = self.vy / abs(self.vy) + self.vy

            elif self.pygame_rect.top < paddle.pygame_rect.top:
                # ball is either on corner or top of paddle
                self.vy = -1 * abs(self.vy) # force ball up

                if self.pygame_rect.right > (paddle.pygame_rect.right + self.pygame_rect.width // 2) \
                    or self.pygame_rect.left < (paddle.pygame_rect.left - self.pygame_rect.width // 2):
                    self.vx = -self.vx
                    self.vx = self.vx / abs(self.vx) + self.vx
                    self.vy = self.vy / abs(self.vy) + self.vy
            else:
                self.vx = -self.vx
                self.vx = self.vx / abs(self.vx) + self.vx
                self.vy = self.vy / abs(self.vy) + self.vy
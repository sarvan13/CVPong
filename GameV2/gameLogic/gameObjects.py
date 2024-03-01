import pygame
import GameV2.constants as constants
import GameV2.sounds.sounds as sounds
import cv2
import mediapipe as mp
import numpy as np
import random
from time import time

class Paddle:
    def __init__(self, pygame_rect):
        self.pygame_rect = pygame_rect
        self.speed = 0
        self.time_last_hit = -1
    
    # Moves a player controlled paddle using computer vision detecting hand position
    def movePlayerCV(self, frame, results, mp_hands, use_left=False):
        frame_height = frame.shape[0]
        frame_edge = (1 - constants.FRAME_SCALE) / 2

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                is_left = self.isLeftHand(mp_hands, hand_landmarks)
                if use_left and not is_left:
                    continue
                elif not use_left and is_left:
                    continue
                # Get the coordinates of the center of the hand
                cx, cy = int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].x * frame.shape[1]), \
                         int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y * frame.shape[0])
                
                game_y = np.clip(cy, frame_height * frame_edge, frame_height * (1-frame_edge)) - (frame_height * frame_edge)
                game_y = game_y * (constants.HEIGHT/ (frame_height *constants.FRAME_SCALE))
                game_y = np.clip(game_y, self.pygame_rect.height // 2, constants.HEIGHT - self.pygame_rect.height // 2) + constants.TOP_SCREEN_OFFSET
                self.speed = game_y - self.pygame_rect.centery
                self.pygame_rect.centery = game_y

    
    # This method should only be called on the right paddle and is used only in 2 player modes
    # If I have time - combine this function with the other CV function - its doable but not priority
    def moveRightLeftPaddleCV(self, frame, results, mp_hands, left_paddle):
        frame_height = frame.shape[0]
        frame_edge = (1 - constants.FRAME_SCALE) / 2

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                is_left = self.isLeftHand(mp_hands, hand_landmarks)
                # Get the coordinates of the center of the hand
                cx, cy = int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].x * frame.shape[1]), \
                         int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y * frame.shape[0])
                
                game_y = np.clip(cy, frame_height * frame_edge, frame_height * (1-frame_edge)) - (frame_height * frame_edge)
                game_y = game_y * (constants.HEIGHT/ (frame_height *constants.FRAME_SCALE))
                game_y = np.clip(game_y, self.pygame_rect.height // 2, constants.HEIGHT - self.pygame_rect.height // 2) + constants.TOP_SCREEN_OFFSET
                
                if is_left:
                    left_paddle.speed = game_y - self.pygame_rect.centery
                    left_paddle.pygame_rect.centery = game_y 
                else:
                    self.speed = game_y - self.pygame_rect.centery
                    self.pygame_rect.centery = game_y

    # Moves a player controlled paddle using the keyboard and specified keys for up and down
    def movePlayerKey(self, key_up, key_down):
        keys = pygame.key.get_pressed()
        prevy = self.pygame_rect.y
        if keys[key_up] and self.pygame_rect.top > constants.TOP_SCREEN_OFFSET:
            self.pygame_rect.y -= constants.PADDLE_SPEED
        if keys[key_down] and self.pygame_rect.bottom < constants.HEIGHT + constants.TOP_SCREEN_OFFSET:
            self.pygame_rect.y += constants.PADDLE_SPEED
        self.speed = self.pygame_rect.y - prevy

        # Check bounds and correct
        if self.pygame_rect.top < constants.TOP_SCREEN_OFFSET:
                self.pygame_rect.top = constants.TOP_SCREEN_OFFSET
        if self.pygame_rect.bottom > constants.TOP_SCREEN_OFFSET + constants.HEIGHT:
            self.pygame_rect.bottom = constants.HEIGHT + constants.TOP_SCREEN_OFFSET
    
    # Moves a computer controlled paddle vertically based on ball trajectory
    def moveComp(self, movespeed, ball):
        paddle_x = self.pygame_rect.right
        ball_x_curr = ball.pygame_rect.left
        # We only move the paddle when its going towards the AI and is on the right side of it
        if ball_x_curr > paddle_x and ball.vx < 0:
            # Calculate where the ball will be going
            ball_traj_y = ((paddle_x - ball_x_curr) / ball.vx) * ball.vy \
            + ball.pygame_rect.centery

            diff = ball_traj_y - self.pygame_rect.centery 

            if abs(diff) > movespeed:
                self.pygame_rect.centery = (diff/abs(diff))*movespeed + self.pygame_rect.centery
                self.speed = (diff/abs(diff))*movespeed
            else:
                self.pygame_rect.centery = ball_traj_y
                self.speed = diff
            
            # Check bounds and correct
            if self.pygame_rect.top < constants.TOP_SCREEN_OFFSET:
                self.pygame_rect.top = constants.TOP_SCREEN_OFFSET
            if self.pygame_rect.bottom > constants.TOP_SCREEN_OFFSET + constants.HEIGHT:
                self.pygame_rect.bottom = constants.HEIGHT + constants.TOP_SCREEN_OFFSET

    # Checks if the hand is a left hand 
    def isLeftHand(self, mp_hands, landmarks):
        if landmarks:
            thumb_tip_x = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
            pinky_tip_x = landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x

            return thumb_tip_x < pinky_tip_x
        return False

class Ball:
    def __init__(self, pygame_rect, speed_inc):
        self.pygame_rect = pygame_rect
        self.vx = constants.BALL_SPEED
        self.vy = 0.5*constants.BALL_SPEED
        self.past_left = 0
        self.past_right = 0
        self.time = time()
        self.pong_sound = sounds.loadPongSound()
        self.max_speed_inc = speed_inc

    # Progresses the ball one frame
    def moveBall(self, left_paddle, right_paddle, particles):
        self.time = time()
        self.pygame_rect.x += self.vx
        self.pygame_rect.y += self.vy

        self.checkPaddleCollision(left_paddle, particles)
        self.checkPaddleCollision(right_paddle, particles)

        if self.pygame_rect.top <= constants.TOP_SCREEN_OFFSET:
            self.vy = abs(self.vy)
        if self.pygame_rect.bottom >= constants.HEIGHT + constants.TOP_SCREEN_OFFSET:
            self.vy = -1 * abs(self.vy)

        # Check bounds and if past the bounds move back to center, add a count of which side for scoring,
        # and then redirect it to the opposite paddle for the next point
        if self.pygame_rect.left <= constants.LEFT_SCREEN_OFFSET:
            self.past_left += 1
            self.pygame_rect.x = constants.LEFT_SCREEN_OFFSET + constants.WIDTH // 2 - self.pygame_rect.width // 2
            self.pygame_rect.y = constants.TOP_SCREEN_OFFSET + constants.HEIGHT // 2 - self.pygame_rect.height // 2
            self.vx = constants.BALL_SPEED
            self.vy = (self.pygame_rect.y - right_paddle.pygame_rect.y) / (self.pygame_rect.x - right_paddle.pygame_rect.x) \
                        * self.vx

        if self.pygame_rect.right >= constants.WIDTH + constants.LEFT_SCREEN_OFFSET:
            self.past_right += 1
            self.pygame_rect.x =constants.LEFT_SCREEN_OFFSET + constants.WIDTH // 2 - self.pygame_rect.width // 2
            self.pygame_rect.y = constants.TOP_SCREEN_OFFSET + constants.HEIGHT // 2 - self.pygame_rect.height // 2
            self.vx = -constants.BALL_SPEED
            self.vy = (self.pygame_rect.y - left_paddle.pygame_rect.y) / (self.pygame_rect.x - left_paddle.pygame_rect.x) \
                        * self.vx
    
    # Check if there are any collisions between the ball and a given paddle
    def checkPaddleCollision(self, paddle, particles):
        # We dont want to keep checking the same paddle if we already collided with it otherwise it leads
        # to unwanted edge case behaviour so we put the paddle on a collision cool down of 200 ms
        if self.pygame_rect.colliderect(paddle.pygame_rect) and (self.time - paddle.time_last_hit) > 0.2:
            paddle.time_last_hit = self.time
            particle_sourcex = paddle.pygame_rect.left # assume it collided with right paddle and correct after
            particle_sourcey = self.pygame_rect.centery
            self.pong_sound.play()
            # This means the ball is either on the corner or bottom of the paddle
            if self.pygame_rect.bottom > paddle.pygame_rect.bottom:
                self.vy = abs(self.vy) # force the ball to bounce down
                particle_sourcey = paddle.pygame_rect.bottom
                # If its a corner bounce it back to the playing field but with a potentially changed y
                if self.pygame_rect.right > (paddle.pygame_rect.right + self.pygame_rect.width // 2) \
                    or self.pygame_rect.left < (paddle.pygame_rect.left - self.pygame_rect.width // 2):
                    self.vx = -self.vx
                    self.vx = (self.vx / abs(self.vx))*constants.SPEED_MULT + self.vx
                    # Need to check for vy = 0 for divide by 0, vx will never be 0 so no need to check
                    if self.vy != 0:
                        self.vy = (self.vy / abs(self.vy))*constants.SPEED_MULT + self.vy
            elif self.pygame_rect.top < paddle.pygame_rect.top:
                # ball is either on corner or top of paddle
                self.vy = -1 * abs(self.vy) # force ball up
                particle_sourcey = paddle.pygame_rect.top

                if self.pygame_rect.right > (paddle.pygame_rect.right + self.pygame_rect.width // 2) \
                    or self.pygame_rect.left < (paddle.pygame_rect.left - self.pygame_rect.width // 2):
                    self.vx = -self.vx
                    self.vx = (self.vx / abs(self.vx))*constants.SPEED_MULT + self.vx
                    if self.vy != 0:
                        self.vy = (self.vy / abs(self.vy))*constants.SPEED_MULT + self.vy
            else:
                self.vx = -self.vx
                self.vx = (self.vx / abs(self.vx))*constants.SPEED_MULT + self.vx
                self.vx = (self.vx / abs(self.vx))*constants.SPEED_MULT + self.vx
                if self.vy != 0:
                    self.vy = (self.vy / abs(self.vy))*constants.SPEED_MULT + self.vy
            
            # Now we add in the speed from the paddle - this is the PHYSICS
            curr_energy = self.vy**2 + self.vx**2
            max_energy = curr_energy + self.max_speed_inc**2
            new_y_speed = self.vy + paddle.speed
            new_x_speed = self.vx
            new_energy = new_y_speed**2 + new_x_speed**2
            if (max_energy > constants.MAX_ENERGY):
                max_energy = constants.MAX_ENERGY
            if (new_energy > max_energy):
                new_energy = max_energy
            elif (new_energy < curr_energy):
                new_energy = curr_energy
            
            theta = np.arctan2(new_y_speed, new_x_speed)
            if abs(abs(theta) - (np.pi / 2)) < np.radians(constants.MIN_ANGLE):
                # Too close to vertical push it past min angle
                # Theta wont be 0 ever so no need to check for divide by 0
                if abs(theta) < np.pi / 2:
                    theta = theta / abs(theta) * ((np.pi / 2) - constants.MIN_ANGLE)
                else:
                    theta = theta / abs(theta) * ((np.pi / 2) + constants.MIN_ANGLE)
            self.vy = np.sqrt(new_energy) * np.sin(theta)
            self.vx = np.sqrt(new_energy) * np.cos(theta)

            # Finally add particles at collision source
            if (self.pygame_rect.right > paddle.pygame_rect.right):
                particle_sourcex = paddle.pygame_rect.right

            particles.extend([Particle((particle_sourcex, particle_sourcey), \
                                       [random.uniform(-3, 3), random.uniform(-3, 3)]) for _ in range(constants.NUM_PARTICLES)])
    
# Simple class used for particle effects upon ball impacting paddles
class Particle:
    def __init__(self, position, speed):
        self.position = list(position)
        self.speed = list(speed)
        self.lifetime = random.randint(10, 25)

    def move(self):
        self.position[0] += self.speed[0]
        self.position[1] += self.speed[1]
        self.lifetime -= 1

# Describes the physical container of the power ups, ie how the power up is shaped, size, lifetime, consumption
class PowerUp:
    def __init__(self, dest_x, dest_y):
        self.pygame_rect = pygame.Rect(constants.LEFT_SCREEN_OFFSET + constants.WIDTH // 2 - constants.POWER_UP_RAD, \
                                         constants.TOP_SCREEN_OFFSET  + constants.HEIGHT // 2 - constants.POWER_UP_RAD, \
                                            2*constants.POWER_UP_RAD, 2*constants.POWER_UP_RAD)
        self.type = constants.PowerUpType(random.randint(1,3))
        self.dest_x = dest_x
        self.dest_y = dest_y
        self.speed = constants.POWER_UP_SPEED
        self.destroy = False

        diff_x = self.dest_x - self.pygame_rect.x
        diff_y = self.dest_y - self.pygame_rect.y
        theta = np.arctan2(diff_y, diff_x)
        self.vy = self.speed * np.sin(theta)
        self.vx = self.speed * np.cos(theta)
    
    def move(self):
        self.pygame_rect.x += self.vx
        self.pygame_rect.y += self.vy

        if self.pygame_rect.x <= constants.LEFT_SCREEN_OFFSET or \
            self.pygame_rect.x >= constants.LEFT_SCREEN_OFFSET + constants.WIDTH:
            self.destroy = True

        if self.pygame_rect.y <= constants.TOP_SCREEN_OFFSET or \
        self.pygame_rect.y >= constants.SCREEN_HEIGHT - constants.BOTTOM_SCREEN_OFFSET:
            self.destroy = True
    
    # detects if the power up hits a paddle and if it does it returns the type of power up 
    # that the paddle consumed
    def detectCollision(self, paddle):
        if self.pygame_rect.colliderect(paddle.pygame_rect):
            self.destroy = True
            return self.type
        else:
            return constants.PowerUpType.NONE
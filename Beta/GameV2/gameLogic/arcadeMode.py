from GameV2.gameLogic.classicGame import ClassicGame
import pygame
import cv2
import GameV2.constants as constants
import mediapipe as mp
import random
import numpy as np
from GameV2.gameLogic.gameObjects import PowerUp

class ArcadeGame(ClassicGame):
    def __init__(self, screen, cap, mp_hands, hands):
        super().__init__(screen, cap, mp_hands, hands)
        self.last_pup_time = pygame.time.get_ticks() + 2000
        self.power_up = None
        self.power_up_state = constants.PowerUpType.NONE
        self.ball_prev_velocity = 0
        self.pup_start_time = pygame.time.get_ticks()
        self.stuck = False
        self.stuck_phi = constants.PHI_MIN
        self.stuck_line = None
        self.stuck_flip = 1
        self.hand_open = True
    
    def calculateFrame(self):
        if self.useCV: # Computer Vision as input
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame")
                self.running = False
            # Convert the BGR image to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)
            self.right_paddle.movePlayerCV(rgb_frame, results, self.mp_hands)
            self.analyzeCVFrame(results, rgb_frame)
            self.hand_open = self.isHandOpen(results)
        else: # Keyboard as input
            self.right_paddle.movePlayerKey(pygame.K_UP, pygame.K_DOWN)
        # Handle the game logic depending on the power up state
        if self.power_up_state == constants.PowerUpType.SLOW:
            self.handleSlow()
        elif self.power_up_state == constants.PowerUpType.FREEZE:
            self.handleFreeze()
        elif self.power_up_state == constants.PowerUpType.GRAB:
            self.handleGrab(self.hand_open)
        else:
            self.ball.moveBall(self.left_paddle, self.right_paddle, self.particles)
            self.left_paddle.moveComp(constants.COMP_SPEED, self.ball)

        # Progress and kill particles
        for particle in self.particles:
            particle.move()
        self.particles = [particle for particle in self.particles if particle.lifetime > 0]

        # Check if we hit a power up
        if self.power_up:
            collided = self.power_up.detectCollision(self.right_paddle)
            if self.power_up_state == constants.PowerUpType.NONE and collided != constants.PowerUpType.NONE:
                self.power_up_state = collided
                self.pup_start_time = pygame.time.get_ticks()
                self.ball_prev_velocity = (self.ball.vx, self.ball.vy)

        # destroy or move the actual power up
        if self.power_up:
            if self.power_up.destroy:
                self.power_up = None
            else:
                self.power_up.move()

        # spawn power ups
        if pygame.time.get_ticks() > self.last_pup_time + random.randint(5, 10)*1000 and \
            self.power_up_state == constants.PowerUpType.NONE:
            self.last_pup_time = pygame.time.get_ticks()
            dest_x = self.right_paddle.pygame_rect.centerx
            dest_y = random.randint(constants.GAME_TOP + constants.PADDLE_HEIGHT,  \
                                    constants.GAME_BOTTOM - constants.PADDLE_HEIGHT)
            self.power_up = PowerUp(dest_x, dest_y)
    
    def drawFrame(self):
        super().drawFrame()
        # Show the colours for the powerups!
        if self.power_up:
            pygame.draw.ellipse(self.screen, constants.PowerUpColour[self.power_up.type], self.power_up.pygame_rect)
        if self.power_up_state == constants.PowerUpType.SLOW:
            pygame.draw.ellipse(self.screen, constants.LIGHT_GREY, self.ball.pygame_rect)
        if self.power_up_state == constants.PowerUpType.FREEZE:
            pygame.draw.rect(self.screen, constants.ICE_BLUE, self.left_paddle.pygame_rect)
        if self.power_up_state == constants.PowerUpType.GRAB:
            if self.stuck:
                pygame.draw.line(self.screen, constants.WHITE, self.stuck_line[0], self.stuck_line[1], 2)
            if self.useCV and self.hand_open:
                # If our hand is open dont show that the paddle is sticky
                return
            pygame.draw.rect(self.screen, constants.SLIME_GREEN, self.right_paddle.pygame_rect)
    
    def updateScore(self):
        # Reset the power up state on a point scored
        if self.ball.past_left > self.right_score:
            self.right_score = self.ball.past_left
            self.power_up_state == constants.PowerUpType.NONE
            self.score_sound.play()
        elif self.ball.past_right > self.left_score:
            self.left_score = self.ball.past_right
            self.power_up_state == constants.PowerUpType.NONE
            self.concede_sound.play()
    
    # Handles the Slow power up state. Slows the ball for a brief period or until the ball makes
    # contact with another paddle or wall at which point it returns to its original velocity.
    def handleSlow(self):
        if pygame.time.get_ticks() - self.pup_start_time < constants.SLOW_TIME:
            # Slow the ball down and then move it
            self.ball.vx = self.ball_prev_velocity[0] * constants.SLOW_FACTOR
            self.ball.vy = self.ball_prev_velocity[1]  * constants.SLOW_FACTOR
            self.ball.moveBall(self.left_paddle, self.right_paddle, self.particles)
            self.left_paddle.moveComp(constants.COMP_SPEED, self.ball)

            # If the ball hits anything during its slow return to the original speed and reset the state
            if self.checkSlowCollisions():
                self.ball.vx = self.ball.vx / constants.SLOW_FACTOR
                self.ball.vy = self.ball.vy / constants.SLOW_FACTOR
                self.power_up_state = constants.PowerUpType.NONE
                self.ball.moveBall(self.left_paddle, self.right_paddle, self.particles)
                self.left_paddle.moveComp(constants.COMP_SPEED, self.ball)
                self.last_pup_time = pygame.time.get_ticks()
        else:
            # Time has elapsed so return ball to the original speed and reset the state
            self.ball.vx = self.ball.vx / constants.SLOW_FACTOR
            self.ball.vy = self.ball.vy / constants.SLOW_FACTOR
            self.power_up_state = constants.PowerUpType.NONE
            self.ball.moveBall(self.left_paddle, self.right_paddle, self.particles)
            self.left_paddle.moveComp(constants.COMP_SPEED, self.ball)
            self.last_pup_time = pygame.time.get_ticks()
    
    # Handles the Freeze power up state. Freezes the computers paddle for a short period.
    def handleFreeze(self):
        if pygame.time.get_ticks() - self.pup_start_time < constants.FREEZE_TIME:
            # Just dont move the computer 
            self.ball.moveBall(self.left_paddle, self.right_paddle, self.particles)
        else:
            # Back to normal and reset the state
            self.ball.moveBall(self.left_paddle, self.right_paddle, self.particles)
            self.left_paddle.moveComp(constants.COMP_SPEED, self.ball)
            self.power_up_state = constants.PowerUpType.NONE
            self.last_pup_time = pygame.time.get_ticks()
    
    # Handles the Grab power up state. When a user hits a green power up they can grab the ball 
    # and release it at an angle that is shown by a sweeping line. The user can do this by either
    # pressing space or closing and opening their hand (depends on specified input method)
    def handleGrab(self, hand_open):
        if self.ball.pygame_rect.colliderect(self.right_paddle.pygame_rect):
            # We have to wait until the ball collides with the paddle to start the timer here
            # Once the ball collides with the paddle, snap to center and stop it
            if self.useCV and hand_open:
                # only stop is hand is closed, so just do normal procedures
                self.ball.moveBall(self.left_paddle, self.right_paddle, self.particles)
                self.left_paddle.moveComp(constants.COMP_SPEED, self.ball)
                return
            
            self.pup_start_time = pygame.time.get_ticks()
            self.stuck = True
            self.ball_prev_velocity = (self.ball.vx, self.ball.vy)
            self.ball.vx = 0
            self.ball.vy = 0
            self.ball.pygame_rect.right = self.right_paddle.pygame_rect.left
            self.ball.pygame_rect.centery = self.right_paddle.pygame_rect.centery
            self.stuck_phi = constants.PHI_MIN
        if self.stuck and pygame.time.get_ticks() - self.pup_start_time < constants.GRAB_TIME:
            # Ball is stuck to the paddle
            self.ball.vx = 0
            self.ball.vy = 0
            self.ball.pygame_rect.right = self.right_paddle.pygame_rect.left
            self.ball.pygame_rect.centery = self.right_paddle.pygame_rect.centery

            # Create a line based on phi 
            ball_point = (self.ball.pygame_rect.left, self.ball.pygame_rect.centery)
            line_x = ball_point[0] - constants.STUCK_LINE_LENGTH * np.sin(np.radians(self.stuck_phi))
            line_y = ball_point[1] - constants.STUCK_LINE_LENGTH * np.cos(np.radians(self.stuck_phi))

            self.stuck_line = (ball_point, (line_x, line_y))

            # Check for input
            if self.useCV:
                if hand_open:
                    self.releaseBall()
                    return
            else:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    # Release ball
                    self.releaseBall()
                    return

            # increment phi
            self.stuck_phi = self.stuck_phi + self.stuck_flip * constants.DEGREE_INC

            if self.stuck_phi >= 160:
                self.stuck_phi = 160
                self.stuck_flip = -1
            elif self.stuck_phi <= 20:
                self.stuck_phi = 20
                self.stuck_flip = 1
            
        elif self.stuck:
            # Time has elapsed and ball is still stuck so we release the ball
            self.releaseBall()
        else:
            # Ball has yet to reach the paddle so just move as normal
            self.ball.moveBall(self.left_paddle, self.right_paddle, self.particles)
            self.left_paddle.moveComp(constants.COMP_SPEED, self.ball)

    # Releases a stuck ball from a paddle and sends it off with the previous speed but along a new
    # specified angle. Resets the power up state.
    def releaseBall(self):
        ball_speed = np.sqrt(self.ball_prev_velocity[0]**2 + self.ball_prev_velocity[1]**2)
        self.ball.vx = -1 * ball_speed * np.sin(np.radians(self.stuck_phi))
        self.ball.vy = -1 * ball_speed * np.cos(np.radians(self.stuck_phi))
        self.ball.pygame_rect.x += self.ball.vx
        self.ball.pygame_rect.y += self.ball.vy

        self.power_up_state = constants.PowerUpType.NONE
        self.stuck = False
        self.last_pup_time = pygame.time.get_ticks()

    # Checks if users hand is open and returns a bool
    def isHandOpen(self, results):
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                if self.right_paddle.isLeftHand(self.mp_hands, hand_landmarks):
                    pass
                # Define the landmarks for fingers
                index_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
                thumb_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]
                middle_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP]
                ring_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.RING_FINGER_TIP]
                pinky_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.PINKY_TIP]

                # Define thresholds for open hand
                threshold_distance = constants.HAND_OPEN_THRESH

                # Check if fingers are open based on distance between tips
                is_open = (
                    self.calculateDistance(index_tip, middle_tip) > threshold_distance and
                    self.calculateDistance(middle_tip, ring_tip) > threshold_distance and
                    self.calculateDistance(ring_tip, pinky_tip) > threshold_distance and
                    self.calculateDistance(thumb_tip, index_tip) > threshold_distance
                )

                return is_open

        return False
    
    def calculateDistance(self, point1, point2):
        return np.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)
    
    # Checks if the ball collided with anything
    def checkSlowCollisions(self):
        if self.ball.pygame_rect.top <= constants.TOP_SCREEN_OFFSET:
            return True
        if self.ball.pygame_rect.bottom >= constants.HEIGHT + constants.TOP_SCREEN_OFFSET:
            return True
        if self.ball.pygame_rect.left <= constants.LEFT_SCREEN_OFFSET:
            return True
        if self.ball.pygame_rect.right >= constants.WIDTH + constants.LEFT_SCREEN_OFFSET:
            return True
        if self.ball.pygame_rect.colliderect(self.left_paddle.pygame_rect):
            return True
        if self.ball.pygame_rect.colliderect(self.right_paddle.pygame_rect):
            return True
        else:
            return False

from game import Game
from gameObjects import Paddle, Ball
import pygame
import constants
import cv2
import mediapipe as mp

class ClassicGame(Game):
    def __init__(self, screen, cap, mp_hands, hands):
        super().__init__(screen, cap, mp_hands, hands)
        self.right_paddle = Paddle(pygame.Rect(constants.WIDTH - 70, constants.HEIGHT // 2 - 50,\
                                   20, 100), 0)
        self.left_paddle = Paddle(pygame.Rect(50, constants.HEIGHT // 2 - 50, 20, 100), 0)
        self.ball = Ball(pygame.Rect(constants.WIDTH // 2 - 15, constants.HEIGHT // 2 - 15, 30, 30), 0)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.running = True

    def runGame(self):
        while (self.running):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                self.running = False
            
            self.calculateFrame()

            # Draw Frame
            self.screen.fill(constants.BLACK)
            pygame.draw.rect(self.screen, constants.WHITE, self.left_paddle.pygame_rect)
            pygame.draw.rect(self.screen, constants.WHITE, self.right_paddle.pygame_rect)
            pygame.draw.ellipse(self.screen, constants.WHITE, self.ball.pygame_rect)

            # Score display
            score_display = self.font.render(f"{self.ball.score_left} - {self.ball.score_right}", True, constants.WHITE)
            self.screen.blit(score_display, (constants.WIDTH // 2 - score_display.get_width() // 2, 20))

            # Update display
            pygame.display.flip()

            # Set the frames per second
            self.clock.tick(constants.FPS)

    def calculateFrame(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to grab frame")
            self.running = False
        # Game logic

        # Flip the frame horizontally for a later selfie-view display
        frame = cv2.flip(frame, 1)
        # Convert the BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        self.right_paddle.movePlayerCV(rgb_frame, self.mp_hands, self.hands)
        self.ball.moveBall(self.left_paddle, self.right_paddle)
        self.left_paddle.moveComp(constants.PADDLE_SPEED, self.ball)

import pygame
import sys
import cv2
import mediapipe as mp
import constants
from gameObjects import Paddle, Ball

def run_classic(screen, cap, mp_hands, hands):
    font = pygame.font.Font(None, 36)
    right_paddle = Paddle(pygame.Rect(constants.WIDTH - 70, constants.HEIGHT // 2 - 50,\
                                   20, 100), 0)
    left_paddle = Paddle(pygame.Rect(50, constants.HEIGHT // 2 - 50, 20, 100), 0)

    ball = Ball(pygame.Rect(constants.WIDTH // 2 - 15, constants.HEIGHT // 2 - 15, 30, 30), 0)
    clock = pygame.time.Clock()
    running = True

    while (running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False

        ret, frame = cap.read()
        # if not ret:
        #     print("Failed to grab frame")
        #     break

        # Game logic

        # Flip the frame horizontally for a later selfie-view display
        frame = cv2.flip(frame, 1)
        # Convert the BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        right_paddle.movePlayerKey()
        ball.moveBall(left_paddle, right_paddle)
        left_paddle.moveComp(constants.PADDLE_SPEED, ball)

        # Drawing
        screen.fill(constants.BLACK)
        pygame.draw.rect(screen, constants.WHITE, left_paddle.pygame_rect)
        pygame.draw.rect(screen, constants.WHITE, right_paddle.pygame_rect)
        pygame.draw.ellipse(screen, constants.WHITE, ball.pygame_rect)

        # Score display
        score_display = font.render(f"{ball.score_left} - {ball.score_right}", True, constants.WHITE)
        screen.blit(score_display, (constants.WIDTH // 2 - score_display.get_width() // 2, 20))

        # Update display
        pygame.display.flip()

        # Set the frames per second
        clock.tick(constants.FPS)
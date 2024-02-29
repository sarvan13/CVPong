from GameV2.gameLogic.classicGame import ClassicGame
from GameV2.gameLogic.gameObjects import DoublePaddle
import GameV2.constants as constants
import pygame
import cv2

class DoublePaddleGame(ClassicGame):
    def __init__(self, screen, cap, mp_hands, hands):
        super().__init__(screen, cap, mp_hands, hands)
        self.right_paddle = DoublePaddle(pygame.Rect(constants.LEFT_SCREEN_OFFSET + constants.WIDTH - constants.HORIZ_PADDLE_OFFSET - constants.PADDLE_WIDTH, \
                                               constants.TOP_SCREEN_OFFSET + constants.HEIGHT // 2 - constants.HORIZ_PADDLE_OFFSET, 20, 100))
        self.left_paddle = DoublePaddle(pygame.Rect(constants.LEFT_SCREEN_OFFSET + 50, constants.TOP_SCREEN_OFFSET + \
                                              constants.HEIGHT // 2 - 50, 20, 100))
        self.top_paddle = DoublePaddle(pygame.Rect(constants.LEFT_SCREEN_OFFSET + constants.WIDTH //2, \
                                             constants.TOP_SCREEN_OFFSET + constants.TOP_PADDLE_OFFSET + constants.PADDLE_WIDTH // 2, \
                                            constants.PADDLE_HEIGHT, constants.PADDLE_WIDTH))
        self.bottom_paddle = DoublePaddle(pygame.Rect(constants.LEFT_SCREEN_OFFSET + constants.WIDTH //2, \
                                             constants.SCREEN_HEIGHT - constants.BOTTOM_SCREEN_OFFSET - constants.TOP_PADDLE_OFFSET
                                             - constants.PADDLE_WIDTH // 2, constants.PADDLE_HEIGHT, constants.PADDLE_WIDTH))
        self.past_top = 0
        self.past_bottom = 0
        
    def calculateFrame(self):
        # Override to move top and side panels
        if self.useCV:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame")
                self.running = False
            # Convert the BGR image to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)
            self.right_paddle.movePlayerCV(rgb_frame, results, self.mp_hands)
            self.top_paddle.moveTopPlayerCV(rgb_frame, results, self.mp_hands)
            self.analyzeCVFrame(results, rgb_frame)
        else:
            self.right_paddle.movePlayerKey(pygame.K_UP, pygame.K_DOWN)
            self.top_paddle.moveTopPlayer(self.right_paddle)
        
        self.ball.moveBall(self.left_paddle, self.right_paddle, self.particles)
        self.ball.checkHorizPaddleCollisions(self.bottom_paddle, self.particles)
        self.ball.checkHorizPaddleCollisions(self.top_paddle, self.particles)

        self.bottom_paddle.moveBotComp(constants.COMP_SPEED, self.ball)
        self.left_paddle.moveComp(constants.COMP_SPEED, self.ball)

        # Progress and kill particles
        for particle in self.particles:
            particle.move()
        self.particles = [particle for particle in self.particles if particle.lifetime > 0]

    def drawFrame(self):
        super().drawFrame()
        pygame.draw.rect(self.screen, constants.PINK, self.top_paddle.pygame_rect)
        pygame.draw.rect(self.screen, constants.PINK, self.bottom_paddle.pygame_rect)
    
    def updateScore(self):
        if self.ball.pygame_rect.centery < self.top_paddle.pygame_rect.centery:
            self.past_top += 1
            self.ball.pygame_rect.x = constants.LEFT_SCREEN_OFFSET + constants.WIDTH // 2 - self.ball.pygame_rect.width // 2
            self.ball.pygame_rect.y = constants.TOP_SCREEN_OFFSET + constants.HEIGHT // 2 - self.ball.pygame_rect.height // 2
            self.ball.vx = constants.BALL_SPEED
            self.ball.vy = constants.BALL_SPEED
        elif self.ball.pygame_rect.centery > self.bottom_paddle.pygame_rect.centery:
            self.past_bottom += 1
            self.ball.pygame_rect.x = constants.LEFT_SCREEN_OFFSET + constants.WIDTH // 2 - self.ball.pygame_rect.width // 2
            self.ball.pygame_rect.y = constants.TOP_SCREEN_OFFSET + constants.HEIGHT // 2 - self.ball.pygame_rect.height // 2
            self.ball.vx = -constants.BALL_SPEED
            self.ball.vy = constants.BALL_SPEED

        self.left_score = self.ball.past_right + self.past_top
        self.right_score = self.ball.past_left + self.past_bottom

    def resetGame(self):
        super().resetGame()
        self.past_top = 0
        self.past_bottom = 0

from GameV2.gameLogic.classicGame import ClassicGame
import pygame
import GameV2.constants as constants
import cv2

class InfiniteGame(ClassicGame):
    def __init__(self, screen, cap, mp_hands, hands):
        super().__init__(screen, cap, mp_hands, hands)
        # Override left paddle to extend across entire screen height
        self.left_paddle.pygame_rect = pygame.Rect(constants.LEFT_SCREEN_OFFSET, constants.TOP_SCREEN_OFFSET - 1\
                                                   , 50, constants.HEIGHT + 2)
        self.score = 0
        self.endText = self.score
        self.paddle_last_hit = pygame.time.get_ticks()
    
    def runGame(self):
        return super().runGame()

    def calculateFrame(self):
        # Override to only move the right paddle
        if self.useCV:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame")
                self.running = False
            # Convert the BGR image to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.camera_frame = self.right_paddle.movePlayerCV(rgb_frame, self.mp_hands, self.hands)
        else:
            self.right_paddle.movePlayerKey(pygame.K_UP, pygame.K_DOWN)
        
        self.ball.moveBall(self.left_paddle, self.right_paddle)
    
    def updateScore(self):
        # Override to calculate score based on number of returns 
        if self.ball.pygame_rect.colliderect(self.right_paddle.pygame_rect) and \
            pygame.time.get_ticks() - self.paddle_last_hit > 100:
            self.score += 1

    def drawScore(self):
        # Override to show only a single score
        score_display = self.font.render(f"{self.score}", True, constants.WHITE)
        self.screen.blit(score_display, (constants.LEFT_SCREEN_OFFSET + constants.WIDTH // 2 \
                                         - score_display.get_width() // 2, constants.TOP_SCREEN_OFFSET + 20))
    def checkGameOver(self):
        if self.ball.past_right:
            self.endText = str(self.score)
            self.gameOver = True
            self.paused = True
            self.resetGame()


    def resetGame(self):
        super().resetGame()
        self.score = 0

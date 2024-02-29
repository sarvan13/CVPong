from GameV2.gameLogic.classicGame import ClassicGame
import cv2
import mediapipe as mp
import pygame
import GameV2.constants as constants

class TwoPlayerGame(ClassicGame):
    def __init__(self, screen, cap, mp_hands, hands):
        super().__init__(screen, cap, mp_hands, hands)
    
    def runGame(self):
        return super().runGame()
    def interruptGame(self):
        return super().interruptGame()
    
    def calculateFrame(self):
        if self.useCV:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame")
                self.running = False
            # Convert the BGR image to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)
            self.right_paddle.moveRightLeftPaddleCV(frame, results, self.mp_hands, self.left_paddle)
            self.analyzeCVFrame(results, rgb_frame)
        else:   
            self.right_paddle.movePlayerKey(pygame.K_UP, pygame.K_DOWN)
            self.left_paddle.movePlayerKey(pygame.K_w, pygame.K_s)
            
        self.ball.moveBall(self.left_paddle, self.right_paddle, self.particles)

        # Progress and kill particles
        for particle in self.particles:
            particle.move()
        self.particles = [particle for particle in self.particles if particle.lifetime > 0]
        
    def checkGameOver(self):
        if (self.right_score == constants.WIN_SCORE):
            self.paused = True
            self.gameOver = True
            self.endText = "Right Player Wins!"
            self.resetGame()
        elif (self.left_score == constants.WIN_SCORE):
            self.paused = True
            self.gameOver = True
            self.endText = "Left Player Wins!"
            self.resetGame()

    
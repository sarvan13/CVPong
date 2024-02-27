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
            # Flip the frame horizontally for a later selfie-view display
            frame = cv2.flip(frame, 1)
            # Convert the BGR image to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.right_paddle.movePlayerCV(rgb_frame, self.mp_hands, self.hands, False)
            self.left_paddle.movePlayerCV(rgb_frame, self.mp_hands, self.hands, True)
        else:   
            self.right_paddle.movePlayerKey(pygame.K_UP, pygame.K_DOWN)
            self.left_paddle.movePlayerKey(pygame.K_w, pygame.K_s)
            
        self.ball.moveBall(self.left_paddle, self.right_paddle)
        
    def updateScore(self):
        return super().updateScore()
    def drawFrame(self):
        return super().drawFrame()

    
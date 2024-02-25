from classicGame import ClassicGame
import pygame
import constants
import cv2

class InfiniteGame(ClassicGame):
    def __init__(self, screen, cap, mp_hands, hands):
        super().__init__(screen, cap, mp_hands, hands)
        self.left_paddle.pygame_rect = pygame.Rect(50, 0, 20, constants.HEIGHT)
    
    def runGame(self):
        return super().runGame()

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

        self.right_paddle.movePlayerKey()
        self.ball.moveBall(self.left_paddle, self.right_paddle)
from GameV2.gameLogic.gameMode import GameMode
from GameV2.gameLogic.gameObjects import Paddle, Ball
from GameV2.graphics import Graphics
import pygame
import GameV2.constants as constants
import cv2
import mediapipe as mp
from time import sleep

class ClassicGame(GameMode):
    def __init__(self, screen, cap, mp_hands, hands):
        super().__init__(screen, cap, mp_hands, hands)
        self.right_paddle = Paddle(pygame.Rect(constants.WIDTH - 70, constants.HEIGHT // 2 - 50,\
                                   20, 100), 0)
        self.left_paddle = Paddle(pygame.Rect(50, constants.HEIGHT // 2 - 50, 20, 100), 0)
        self.ball = Ball(pygame.Rect(constants.WIDTH // 2 - 15, constants.HEIGHT // 2 - 15, 30, 30), 0)
        self.clock = pygame.time.Clock()
        self.graphics = Graphics(screen)
        self.font = pygame.font.Font(None, constants.DEFAULT_FONT_SIZE)
        self.selected_font = pygame.font.Font(None, constants.SELECTED_FONT_SIZE)
        self.title_font = pygame.font.Font(None, constants.TITLE_FONT_SIZE)
        self.input_text = ["Motion Capture", "Keyboard"]
        self.selected_input = 0
        self.right_score = 0
        self.left_score = 0

    def runGame(self):
        return super().runGame()
    
    def interruptGame(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = True
                    self.selected_input = 0
            

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
            self.right_paddle.movePlayerCV(rgb_frame, self.mp_hands, self.hands)
        else:
            self.right_paddle.movePlayerKey(pygame.K_UP, pygame.K_DOWN)

        self.ball.moveBall(self.left_paddle, self.right_paddle)
        self.left_paddle.moveComp(constants.PADDLE_SPEED, self.ball)
    
    def updateScore(self):
        self.right_score = self.ball.past_left
        self.left_score = self.ball.past_right

    def drawFrame(self):
         # Draw Frame
        #self.screen.fill(constants.BLACK)
        self.graphics.drawBackgroundImage(self.screen, self.graphics.game_background_image)
        pygame.draw.rect(self.screen, constants.PINK, self.left_paddle.pygame_rect)
        pygame.draw.rect(self.screen, constants.PINK, self.right_paddle.pygame_rect)
        pygame.draw.ellipse(self.screen, constants.WHITE, self.ball.pygame_rect)
        
        # Display Score
        self.drawScore()
    
    def drawScore(self):
        score_display = self.font.render(f"{self.left_score} - {self.right_score}", True, constants.WHITE)
        self.screen.blit(score_display, (constants.WIDTH // 2 - score_display.get_width() // 2, 20))

    def displayPygame(self):
        # Update display
        pygame.display.flip()
        # Set the frames per second
        self.clock.tick(constants.FPS)
        print(self.clock.get_fps())
    
    def getInput(self):
        #self.screen.fill(constants.WHITE)
        self.graphics.drawBackgroundImage(self.screen, self.graphics.title_background_image)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.useCV = 0
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected_input = (self.selected_input + 1) % len(self.input_text)
                elif event.key == pygame.K_UP:
                    self.selected_input = (self.selected_input - 1) % len(self.input_text)
                elif event.key == pygame.K_RETURN:
                    self.useCV =  not self.selected_input
            
        text = self.title_font.render("Select Control Option", True, constants.BLACK)
        self.screen.blit(text, (constants.WIDTH // 2 - text.get_width() // 2, 100))

        if self.selected_input == 0:
            text = self.selected_font.render(self.input_text[0], True, constants.BLACK)
            self.screen.blit(text, (constants.WIDTH // 2 - text.get_width() // 2, 176))
            text = self.font.render(self.input_text[1], True, constants.BLACK)
            self.screen.blit(text, (constants.WIDTH // 2 - text.get_width() // 2, 176 + 56))
        else:
            text = self.font.render(self.input_text[0], True, constants.BLACK)
            self.screen.blit(text, (constants.WIDTH // 2 - text.get_width() // 2, 176))
            text = self.selected_font.render(self.input_text[1], True, constants.BLACK)
            self.screen.blit(text, (constants.WIDTH // 2 - text.get_width() // 2, 176 + 46))
        
        pygame.display.flip()

    def pauseScreen(self):
        self.screen.fill(constants.WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.paused = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected_input = (self.selected_input + 1) % 3
                elif event.key == pygame.K_UP:
                    self.selected_input = (self.selected_input - 1) % 3
                elif event.key == pygame.K_RETURN:
                    if self.selected_input == 2:
                        self.running = False
                    elif self.selected_input == 1:
                        self.returnMenu = True
                        self.running = False
                    self.paused = False
                    self.gameOver = False
                elif event.key == pygame.K_ESCAPE:
                    self.paused = False
                    self.gameOver = False

        to_game_text = "Return to Game"
        if self.gameOver:
            to_game_text = "Play Again"
            text = self.font.render("GAME OVER", True, constants.BLACK)
            self.screen.blit(text, (constants.WIDTH // 2 - text.get_width() // 2, 100))

        if self.selected_input == 0:
            text = self.selected_font.render(to_game_text, True, constants.BLACK)
            self.screen.blit(text, (constants.WIDTH // 2 - text.get_width() // 2, constants.HEIGHT // 2 - (constants.SELECTED_FONT_SIZE + 10)))
            text = self.font.render("Return to Menu", True, constants.BLACK)
            self.screen.blit(text, (constants.WIDTH // 2 - text.get_width() // 2, constants.HEIGHT // 2))
            text = self.font.render("Exit Game", True, constants.BLACK)
            self.screen.blit(text, (constants.WIDTH // 2 - text.get_width() // 2, constants.HEIGHT // 2 + (constants.DEFAULT_FONT_SIZE + 10)))
        elif self.selected_input == 1:
            text = self.font.render(to_game_text, True, constants.BLACK)
            self.screen.blit(text, (constants.WIDTH // 2 - text.get_width() // 2, constants.HEIGHT // 2 - (constants.DEFAULT_FONT_SIZE + 10)))
            text = self.selected_font.render("Return to Menu", True, constants.BLACK)
            self.screen.blit(text, (constants.WIDTH // 2 - text.get_width() // 2, constants.HEIGHT // 2))
            text = self.font.render("Exit Game", True, constants.BLACK)
            self.screen.blit(text, (constants.WIDTH // 2 - text.get_width() // 2, constants.HEIGHT // 2 + (constants.SELECTED_FONT_SIZE + 10)))
        else:
            text = self.font.render(to_game_text, True, constants.BLACK)
            self.screen.blit(text, (constants.WIDTH // 2 - text.get_width() // 2, constants.HEIGHT // 2 - (constants.DEFAULT_FONT_SIZE + 10)))
            text = self.font.render("Return to Menu", True, constants.BLACK)
            self.screen.blit(text, (constants.WIDTH // 2 - text.get_width() // 2, constants.HEIGHT // 2))
            text = self.selected_font.render("Exit Game", True, constants.BLACK)
            self.screen.blit(text, (constants.WIDTH // 2 - text.get_width() // 2, constants.HEIGHT // 2 + (constants.SELECTED_FONT_SIZE + 10)))

        pygame.display.flip()
    
    def countDown(self):
        # Dont want numbers covering the ball so we offset the counter up if this is going to happen
        offset = 0
        text_y = constants.HEIGHT // 2
        text_x = constants.WIDTH // 2 - constants.COUNTDOWN_NUM_WIDTH // 2
        if self.ball.pygame_rect.centery <= text_y + constants.TITLE_FONT_SIZE // 2 \
            and self.ball.pygame_rect.centery >= text_y - constants.TITLE_FONT_SIZE // 2 :
            offset = constants.TITLE_FONT_SIZE

        for i in range(3,0, -1):
            self.drawFrame()
            text = self.title_font.render(str(i), True, constants.WHITE)
            self.screen.blit(text, (text_x, text_y - offset))
            pygame.display.flip()
            sleep(1)

        self.fadeIn = False

    def gameOver(self):
        return super().gameOver()
    
    def resetGame(self):
        return super().resetGame()
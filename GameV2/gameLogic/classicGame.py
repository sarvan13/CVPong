from GameV2.gameLogic.gameMode import GameMode
from GameV2.gameLogic.gameObjects import Paddle, Ball
from GameV2.gameLogic.gameMenus import GameMenus
import GameV2.sounds.sounds as sounds
import GameV2.constants as constants
import pygame
import cv2
import mediapipe as mp
import numpy as np

class ClassicGame(GameMode):
    def __init__(self, screen, cap, mp_hands, hands):
        super().__init__(screen, cap, mp_hands, hands)
        self.clock = pygame.time.Clock()
        self.right_paddle = Paddle(pygame.Rect(constants.LEFT_SCREEN_OFFSET + constants.WIDTH - 70, \
                                               constants.TOP_SCREEN_OFFSET + constants.HEIGHT // 2 - 50, 20, 100))
        self.left_paddle = Paddle(pygame.Rect(constants.LEFT_SCREEN_OFFSET + 50, constants.TOP_SCREEN_OFFSET + \
                                              constants.HEIGHT // 2 - 50, 20, 100))
        self.ball = Ball(pygame.Rect(constants.LEFT_SCREEN_OFFSET + constants.WIDTH // 2 - 15, constants.TOP_SCREEN_OFFSET \
                                      + constants.HEIGHT // 2 - 15, 30, 30), constants.MAX_SPEED_INC)
        self.border_surface = pygame.Surface((constants.WIDTH + 2*constants.BORDER_THICKNESS,\
                                               constants.HEIGHT + 2*constants.BORDER_THICKNESS), pygame.SRCALPHA)
        self.border_surface.fill((0,0,0,0))
        self.border_rect = pygame.Rect(0, 0, constants.WIDTH + 2*constants.BORDER_THICKNESS, \
                                  constants.HEIGHT + 2*constants.BORDER_THICKNESS)
        self.camera_frame = None
        self.camera_pos = (constants.LEFT_SCREEN_OFFSET + constants.WIDTH//2 - constants.CAMERA_WIDTH//2, \
                          constants.SCREEN_HEIGHT - constants.BOTTOM_SCREEN_OFFSET //2 \
                            - constants.CAMERA_HEIGHT //2)
        self.game_over_sound = sounds.loadGameOverSound()
        self.win_sound = sounds.loadWinSound()
        self.score_sound = sounds.loadScoreSound()
        self.concede_sound = sounds.loadConcedeSound()
        self.particles = []
        self.menu = GameMenus(screen)

    def runGame(self):
        return super().runGame()
    
    def interruptGame(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = True
                    self.menu.selected_input = 0
            
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

        else: # Keyboard as input
            self.right_paddle.movePlayerKey(pygame.K_UP, pygame.K_DOWN)

        self.ball.moveBall(self.left_paddle, self.right_paddle, self.particles)
        self.left_paddle.moveComp(constants.COMP_SPEED, self.ball)

        # Progress and kill particles
        for particle in self.particles:
            particle.move()
        self.particles = [particle for particle in self.particles if particle.lifetime > 0]
    
    # This does CV analysis for the game state - use the hand to pause the frame by moving it to the other side
    # Also gets the frame to display 
    def analyzeCVFrame(self, results, frame):
        frame_height = frame.shape[0]
        frame_edge = (1 - constants.FRAME_SCALE) / 2
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Get the coordinates of the center of the hand
                cx, cy = int(hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_MCP].x * frame.shape[1]), \
                         int(hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_MCP].y * frame.shape[0])
                cv2.circle(frame, (cx, cy), 10, constants.PINK, -1)

                is_left = self.right_paddle.isLeftHand(self.mp_hands, hand_landmarks)

                # Moving right hand to lfhs of screen will pause
                if not is_left:
                    if cx > frame.shape[1] * (1 - constants.PAUSE_DIST):
                        self.paused = True
            # Get frame with rectangles for displaying on game
            cv2.rectangle(frame, (0, int(frame_height * frame_edge)), (frame.shape[1], int(frame_height * (1-frame_edge))), constants.PINK, 3)
            pygame_frame = cv2.resize(frame, (constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT))
            pygame_frame = np.rot90(pygame_frame)
            pygame_frame = pygame.surfarray.make_surface(pygame_frame)
            self.camera_frame = pygame_frame
    
    def updateScore(self):
        if self.ball.past_left > self.right_score:
            self.right_score = self.ball.past_left
            self.score_sound.play()
        elif self.ball.past_right > self.left_score:
            self.left_score = self.ball.past_right
            self.concede_sound.play()

    def drawFrame(self):
         # Draw Frame
        self.screen.fill(constants.BLACK)
        #self.graphics.drawBackgroundImage(self.screen, self.graphics.game_background_image)
        
        # Draw border
        pygame.draw.rect(self.border_surface, constants.WHITE, self.border_rect, width=constants.BORDER_THICKNESS)
        self.screen.blit(self.border_surface, (constants.LEFT_SCREEN_OFFSET - constants.BORDER_THICKNESS \
                                               , constants.TOP_SCREEN_OFFSET - constants.BORDER_THICKNESS))
        if self.camera_frame:
            self.screen.blit(self.camera_frame, self.camera_pos)
        pygame.draw.rect(self.screen, constants.PINK, self.left_paddle.pygame_rect)
        pygame.draw.rect(self.screen, constants.PINK, self.right_paddle.pygame_rect)
        pygame.draw.ellipse(self.screen, constants.WHITE, self.ball.pygame_rect)

        for particle in self.particles:
            pygame.draw.circle(self.screen, (255,255,255, 100), (int(particle.position[0]), int(particle.position[1])), 3)
        
        # Display Score
        self.drawScore()

    
    def drawScore(self):
        score_display = self.menu.font.render(f"{self.left_score} - {self.right_score}", True, constants.WHITE)
        self.screen.blit(score_display, (constants.LEFT_SCREEN_OFFSET + constants.WIDTH // 2 \
                                          - score_display.get_width() // 2, constants.TOP_SCREEN_OFFSET + 20))

    def displayPygame(self):
        # Update display
        pygame.display.flip()
        # Set the frames per second
        self.clock.tick(constants.FPS)
        #print(self.clock.get_fps())
    
    def checkGameOver(self):
        if (self.right_score == constants.WIN_SCORE):
            self.paused = True
            self.gameOver = True
            self.endText = "You Win!"
            self.win_sound.play()
            self.resetGame()
        elif (self.left_score == constants.WIN_SCORE):
            self.paused = True
            self.gameOver = True
            self.endText = "You Lose"
            self.game_over_sound.play()
            self.resetGame()
    
    def resetGame(self):
        self.left_score = 0
        self.right_score = 0
        self.ball.vx = constants.BALL_SPEED
        self.ball.vy = constants.BALL_SPEED
        self.ball.pygame_rect.x = constants.LEFT_SCREEN_OFFSET + constants.WIDTH // 2 - self.ball.pygame_rect.width // 2
        self.ball.pygame_rect.y = constants.LEFT_SCREEN_OFFSET + constants.HEIGHT // 2 - self.ball.pygame_rect.height // 2
        self.left_paddle.pygame_rect.y = constants.TOP_SCREEN_OFFSET + constants.HEIGHT // 2 \
              - self.left_paddle.pygame_rect.height //2
        self.right_paddle.pygame_rect.y = constants.TOP_SCREEN_OFFSET + constants.HEIGHT // 2 \
            - self.right_paddle.pygame_rect.height //2
        self.ball.past_left = 0
        self.ball.past_right = 0
        self.particles = []
    
    def countDown(self):
        # Dont want numbers covering the ball so we offset the counter up if this is going to happen
        offset = 0
        text_y = constants.HEIGHT // 2
        text_x = constants.SCREEN_WIDTH // 2 - constants.COUNTDOWN_NUM_WIDTH // 2
        if self.ball.pygame_rect.centery <= text_y + constants.TITLE_FONT_SIZE // 2 \
            and self.ball.pygame_rect.centery >= text_y - constants.TITLE_FONT_SIZE // 2 :
            offset = constants.TITLE_FONT_SIZE
        startTime = pygame.time.get_ticks()

        k = 1
        for i in range(3,0, -1):
            self.drawFrame()
            text = self.menu.title_font.render(str(i), True, constants.WHITE)
            self.screen.blit(text, (text_x, text_y - offset))
            pygame.display.flip()
            while (pygame.time.get_ticks() - startTime < k * 1000):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        self.paused = False
            k = k + 1
        self.fadeIn = False
    
    # Hand off to menu class and offload the job
    def pauseScreen(self):
        self.menu.running = self.running
        self.menu.fadeIn = self.useCV
        self.menu.gameOver = self.gameOver
        self.menu.paused = self.paused
        self.menu.returnMenu = self.returnMenu
        self.menu.endText = self.endText

        self.menu.pauseScreen()

        self.running = self.menu.running
        self.fadeIn = self.menu.useCV
        self.gameOver = self.menu.gameOver
        self.returnMenu = self.menu.returnMenu
        self.paused = self.menu.paused
        self.endText = self.menu.endText

    # Hand off to menu class and offload the job
    def getInput(self):
        self.menu.running = self.running
        self.menu.useCV = self.useCV
        self.menu.fadeIn = self.fadeIn

        self.menu.getInput()

        self.running = self.menu.running
        self.useCV = self.menu.useCV
        self.fadeIn = self.menu.fadeIn
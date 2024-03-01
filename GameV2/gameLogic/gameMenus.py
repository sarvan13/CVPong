import pygame
from GameV2.gameLogic.gameMode import GameMode
from GameV2.graphics import Graphics
import constants

# This class handles all menu screens that occur during the game - a game mode will use an 
# instance of this class to show any menu
class GameMenus():
    def __init__(self, screen):
        self.screen = screen
        self.input_text = ["Motion Capture", "Keyboard"]
        self.selected_input = 0
        self.graphics = Graphics(screen)
        self.font = pygame.font.Font(None, constants.DEFAULT_FONT_SIZE)
        self.title_font = pygame.font.Font(None, constants.TITLE_FONT_SIZE)
        self.running = True
        self.fadeIn = True
        self.gameOver = False
        self.useCV = -1
        self.returnMenu = False
        self.paused = False
        self.endText = ""
    
    def getInput(self):
        #self.screen.fill(constants.WHITE)
        self.graphics.drawBackgroundImage(self.screen, self.graphics.title_background_image)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.useCV = 0
                self.fadeIn = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected_input = (self.selected_input + 1) % len(self.input_text)
                elif event.key == pygame.K_UP:
                    self.selected_input = (self.selected_input - 1) % len(self.input_text)
                elif event.key == pygame.K_RETURN:
                    self.useCV =  not self.selected_input
            
        text = self.graphics.font_thor_title.render("Select Control Option", True, constants.WHITE)
        self.screen.blit(text, (constants.SCREEN_WIDTH // 2 - text.get_width() // 2, 100))

        if self.selected_input == 0:
            text = self.graphics.font_bayshore_selected.render(self.input_text[0], True, constants.BLACK)
            self.screen.blit(text, (constants.SCREEN_WIDTH // 2 - text.get_width() // 2, 176))
            text = self.graphics.font_bayshore.render(self.input_text[1], True, constants.BLACK)
            self.screen.blit(text, (constants.SCREEN_WIDTH // 2 - text.get_width() // 2, 176 + constants.SELECTED_FONT_SIZE \
                                    + constants.BAYSHORE_ADJ + 10))
        else:
            text = self.graphics.font_bayshore.render(self.input_text[0], True, constants.BLACK)
            self.screen.blit(text, (constants.SCREEN_WIDTH // 2 - text.get_width() // 2, 176))
            text = self.graphics.font_bayshore_selected.render(self.input_text[1], True, constants.BLACK)
            self.screen.blit(text, (constants.SCREEN_WIDTH // 2 - text.get_width() // 2, 176 + constants.DEFAULT_FONT_SIZE \
                                    + constants.BAYSHORE_ADJ + 10))
        
        pygame.display.flip()

    def pauseScreen(self):
        self.graphics.drawBackgroundImage(self.screen, self.graphics.title_background_image)

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
            text = self.graphics.font_thor_title.render("GAME OVER", True, constants.BLACK)
            self.screen.blit(text, (constants.SCREEN_WIDTH // 2 - text.get_width() // 2, 100))
            text = self.graphics.font_thor.render(self.endText, True, constants.BLACK)
            self.screen.blit(text, (constants.SCREEN_WIDTH // 2 - text.get_width() // 2, 175))
        if self.selected_input == 0:
            text = self.graphics.font_bayshore_selected.render(to_game_text, True, constants.WHITE)
            self.screen.blit(text, (constants.SCREEN_WIDTH // 2 - text.get_width() // 2, constants.HEIGHT // 2 \
                                    - (constants.DEFAULT_FONT_SIZE + constants.BAYSHORE_ADJ + 10)))
            text = self.graphics.font_bayshore.render("Return to Menu", True, constants.WHITE)
            self.screen.blit(text, (constants.SCREEN_WIDTH // 2 - text.get_width() // 2, constants.HEIGHT // 2))
            text = self.graphics.font_bayshore.render("Exit Game", True, constants.WHITE)
            self.screen.blit(text, (constants.SCREEN_WIDTH // 2 - text.get_width() // 2, constants.HEIGHT // 2 + \
                                    (constants.DEFAULT_FONT_SIZE + constants.BAYSHORE_ADJ + 10)))
        elif self.selected_input == 1:
            text = self.graphics.font_bayshore.render(to_game_text, True, constants.WHITE)
            self.screen.blit(text, (constants.SCREEN_WIDTH // 2 - text.get_width() // 2, constants.HEIGHT // 2  \
                                    - (constants.DEFAULT_FONT_SIZE + constants.BAYSHORE_ADJ + 10)))
            text = self.graphics.font_bayshore_selected.render("Return to Menu", True, constants.WHITE)
            self.screen.blit(text, (constants.SCREEN_WIDTH // 2 - text.get_width() // 2, constants.HEIGHT // 2))
            text = self.graphics.font_bayshore.render("Exit Game", True, constants.WHITE)
            self.screen.blit(text, (constants.SCREEN_WIDTH // 2 - text.get_width() // 2, constants.HEIGHT // 2 +  \
                                    (constants.DEFAULT_FONT_SIZE + constants.BAYSHORE_ADJ + 10)))
        else:
            text = self.graphics.font_bayshore.render(to_game_text, True, constants.WHITE)
            self.screen.blit(text, (constants.SCREEN_WIDTH // 2 - text.get_width() // 2, constants.HEIGHT // 2  \
                                    - (constants.DEFAULT_FONT_SIZE + constants.BAYSHORE_ADJ + 10)))
            text = self.graphics.font_bayshore.render("Return to Menu", True, constants.WHITE)
            self.screen.blit(text, (constants.SCREEN_WIDTH // 2 - text.get_width() // 2, constants.HEIGHT // 2))
            text = self.graphics.font_bayshore_selected.render("Exit Game", True, constants.WHITE)
            self.screen.blit(text, (constants.SCREEN_WIDTH // 2 - text.get_width() // 2, constants.HEIGHT // 2 + \
                                    (constants.DEFAULT_FONT_SIZE + constants.BAYSHORE_ADJ + 10)))

        pygame.display.flip()
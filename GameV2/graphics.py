import pygame
import constants

class Graphics:
    def __init__(self, screen):
        self.screen = screen
        self.game_background_image = pygame.image.load("images/grid_ref.png")
        self.game_background_image = pygame.transform.scale(self.game_background_image, (constants.WIDTH, constants.HEIGHT))
        self.game_background_image = self.game_background_image.convert()

        self.title_background_image = pygame.image.load("images/menu_bckg.png")
        self.title_background_image = pygame.transform.scale(self.title_background_image, (constants.WIDTH, constants.HEIGHT))
        self.title_background_image = self.title_background_image.convert()

    def drawTitleBackground(self, screen):
        self.screen.blit(self.title_background_image, (0,0))

        font = pygame.font.Font("fonts/miami.ttf", constants.TITLE_FONT_SIZE + 40)
        text = font.render("PONG", True, constants.WHITE)
        screen.blit(text, (constants.WIDTH // 2 - text.get_width() //2, 150))

        font = pygame.font.Font("fonts/miami.ttf", constants.TITLE_FONT_SIZE + 35)
        text = font.render("PONG", True, constants.BLACK)
        screen.blit(text, (constants.WIDTH // 2 - text.get_width() //2, 145))

    def drawBackgroundImage(self, screen, image):
        screen.blit(image, (0,0))
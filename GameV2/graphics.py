import pygame
import constants

def drawBackground(screen):
    background_image = pygame.image.load("images/menu_bckg.png")
    background_image = pygame.transform.scale(background_image, (constants.WIDTH, constants.HEIGHT))

    screen.blit(background_image, (0,0))

    font = pygame.font.Font("fonts/miami.ttf", constants.TITLE_FONT_SIZE + 40)
    text = font.render("PONG", True, constants.WHITE)
    screen.blit(text, (constants.WIDTH // 2 - text.get_width() //2, 150))

    font = pygame.font.Font("fonts/miami.ttf", constants.TITLE_FONT_SIZE + 35)
    text = font.render("PONG", True, constants.BLACK)
    screen.blit(text, (constants.WIDTH // 2 - text.get_width() //2, 145))
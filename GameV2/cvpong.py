import pygame
import sys
import cv2
import mediapipe as mp
from classicGame import ClassicGame
from infiniteGame import InfiniteGame
from twoPlayer import TwoPlayerGame
from gameMode import GameMode
import constants
import graphics

# Initialize Pygame
pygame.init()

# Create the game window
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("Pong Game")

# Menu Options
selected_option = 0

# Fonts
font = pygame.font.Font("fonts/miami.ttf", constants.DEFAULT_FONT_SIZE)
selected_font = pygame.font.Font("fonts/miami.ttf", constants.SELECTED_FONT_SIZE)

#initialized camera and hand model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
cap = cv2.VideoCapture(0)

# Game loop
clock = pygame.time.Clock()
gameState = constants.State.MENU
game = None

while gameState != constants.State.EXIT:
    if gameState == constants.State.MENU:
        graphics.drawBackground(screen)
        for i, option in enumerate (constants.options):
            if i == selected_option:
                text = selected_font.render(option, True, constants.BLACK)
            else:
                text = font.render(option, True, constants.BLACK)
            screen.blit(text, (constants.WIDTH // 2 - text.get_width() // 2, constants.HEIGHT // 2 + i * (constants.DEFAULT_FONT_SIZE + 20)))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameState = constants.State.EXIT
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(constants.options)
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(constants.options)
                elif event.key == pygame.K_RETURN:
                    gameState = constants.State(selected_option + 1)
                    print (f"{gameState}")
        # Update display
        pygame.display.flip()

        # Set the frames per second
        clock.tick(constants.FPS)

    if gameState == constants.State.CLASSIC:
        game = ClassicGame(screen, cap, mp_hands, hands)
    elif gameState == constants.State.INFINITE:
        game = InfiniteGame(screen, cap, mp_hands, hands)
    elif gameState == constants.State.PVP:
        game = TwoPlayerGame(screen, cap, mp_hands, hands)

    if game and gameState != constants.State.EXIT:
        game.runGame()
        if game.returnMenu:
            gameState = constants.State.MENU
        else:
            gameState = constants.State.EXIT
# Quit Pygame
pygame.quit()
cap.release()
cv2.destroyAllWindows()
sys.exit()
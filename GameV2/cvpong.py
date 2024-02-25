import pygame
import sys
import cv2
import mediapipe as mp
from classicGame import ClassicGame
from infiniteGame import InfiniteGame
from game import Game
import constants

# Initialize Pygame
pygame.init()

# Create the game window
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("Pong Game")

# Menu Options
selected_option = 0

# Fonts
font = pygame.font.Font(None, 36)
selected_font = pygame.font.Font(None, 46)

#initialized camera and hand model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
cap = cv2.VideoCapture(0)

# Game loop
clock = pygame.time.Clock()
gameState = constants.State.MENU

while (gameState == constants.State.MENU):
    screen.fill(constants.WHITE)
    for i, option in enumerate (constants.options):
        if i == selected_option:
            text = selected_font.render(option, True, constants.BLACK)
        else:
            text = font.render(option, True, constants.BLACK)
        screen.blit(text, (constants.WIDTH // 2 - text.get_width() // 2, 100 + i * (36 + 20)))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                selected_option = (selected_option + 1) % len(constants.options)
            elif event.key == pygame.K_UP:
                selected_option = (selected_option - 1) % len(constants.options)
            elif event.key == pygame.K_RETURN:
                if (selected_option == (len(constants.options) - 1)):
                    running = False
                else:
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

game.runGame()
# Quit Pygame
pygame.quit()
cap.release()
cv2.destroyAllWindows()
sys.exit()
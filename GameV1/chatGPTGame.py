import pygame
import sys
import cv2
import mediapipe as mp
from Paddle import Paddle

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALL_SPEED = 5
PADDLE_SPEED = 8

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Fonts
font = pygame.font.Font(None, 36)
selected_font = pygame.font.Font(None, 46)

# Menu Options
options = ["Classic", "Infinite", "2 Player", "Exit"]
selected_option = 0

# Game variables
ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
ball_speed_x = BALL_SPEED
ball_speed_y = BALL_SPEED
paddle_left = pygame.Rect(50, HEIGHT // 2 - 50, 20, 100)
paddle_right = pygame.Rect(WIDTH - 70, HEIGHT // 2 - 50, 20, 100)
rightP = Paddle(paddle_right.centery, 0)
score_left = 0
score_right = 0

#initialized camera and hand model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
cap = cv2.VideoCapture(0)

# Game loop
clock = pygame.time.Clock()
running = True
menu = True

while (running and cap.isOpened()):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False

    if menu:
        screen.fill(BLACK)

        for i, option in enumerate(options):
            if i == selected_option:
                text = selected_font.render(option, True, BLACK)
            else:
                text = font.render(option, True, BLACK)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 100 + i * (FONT_SIZE + 20)))
                    
        start_text = font.render("Press SPACE to start", True, WHITE)
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()

        if keys[pygame.K_SPACE]:
            menu = False

    else:

        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        
        # Flip the frame horizontally for a later selfie-view display
        frame = cv2.flip(frame, 1)
        # Convert the BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        rightP.getPlayerPaddle(rgb_frame, mp_hands, hands)
        paddle_right.y = rightP.y

        # Game logic
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y = -ball_speed_y

        if ball.colliderect(paddle_left) or ball.colliderect(paddle_right):
            ball_speed_x = -ball_speed_x

        if ball.left <= 0:
            score_right += 1
            ball.x = WIDTH // 2 - ball.width // 2
            ball_speed_x = BALL_SPEED

        if ball.right >= WIDTH:
            score_left += 1
            ball.x = WIDTH // 2 - ball.width // 2
            ball_speed_x = -BALL_SPEED

        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_UP] and paddle_right.top > 0:
        #     paddle_right.y -= PADDLE_SPEED
        # if keys[pygame.K_DOWN] and paddle_right.bottom < HEIGHT:
        #     paddle_right.y += PADDLE_SPEED
        

        # Drawing
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, paddle_left)
        pygame.draw.rect(screen, WHITE, paddle_right)
        pygame.draw.ellipse(screen, WHITE, ball)

        # Score display
        score_display = font.render(f"{score_left} - {score_right}", True, WHITE)
        screen.blit(score_display, (WIDTH // 2 - score_display.get_width() // 2, 20))

        # Update display
        pygame.display.flip()

        # Set the frames per second
        clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
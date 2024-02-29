import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BALL_RADIUS = 15
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PARTICLE_COLOR = (255, 255, 255)  # White for particles

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Miami Vice Pong")

# Create paddles and ball
player_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
computer_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)

# Initial ball speed
ball_speed = [5, 5]

# Particle class
class Particle:
    def __init__(self, position, speed):
        self.position = list(position)
        self.speed = list(speed)
        self.lifetime = random.randint(10, 25)

    def move(self):
        self.position[0] += self.speed[0]
        self.position[1] += self.speed[1]
        self.lifetime -= 1

# Particle system
particles = []

# Game loop
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Move paddles
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_paddle.top > 0:
        player_paddle.y -= 5
    if keys[pygame.K_DOWN] and player_paddle.bottom < HEIGHT:
        player_paddle.y += 5

    # AI for computer paddle
    if computer_paddle.centery < ball.centery and computer_paddle.bottom < HEIGHT:
        computer_paddle.y += 5
    elif computer_paddle.centery > ball.centery and computer_paddle.top > 0:
        computer_paddle.y -= 5

    # Move ball
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # Ball collision with walls
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed[1] = -ball_speed[1]

    # Ball collision with paddles
    if ball.colliderect(player_paddle):
        ball_speed[0] = -ball_speed[0]
        particles.extend([Particle(ball.center, [random.uniform(-2, 2), random.uniform(-2, 2)]) for _ in range(10)])

    elif ball.colliderect(computer_paddle):
        ball_speed[0] = -ball_speed[0]
        particles.extend([Particle(ball.center, [random.uniform(-2, 2), random.uniform(-2, 2)]) for _ in range(10)])

    # Check for scoring
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed = [5, 5] if random.choice([True, False]) else [-5, -5]
        ball.x = WIDTH // 2 - BALL_RADIUS
        ball.y = HEIGHT // 2 - BALL_RADIUS

    # Update particles
    for particle in particles:
        particle.move()

    # Remove expired particles
    particles = [particle for particle in particles if particle.lifetime > 0]

    # Add particles that follow the ball
    particles.extend([Particle(ball.center, [random.uniform(-2, 2), random.uniform(-2, 2)]) for _ in range(2)])

    # Draw background
    screen.fill(BLACK)

    # Draw paddles and ball
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, computer_paddle)
    pygame.draw.circle(screen, WHITE, ball.center, BALL_RADIUS)

    # Draw particles
    for particle in particles:
        pygame.draw.circle(screen, PARTICLE_COLOR, (int(particle.position[0]), int(particle.position[1])), 3)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong")

# Colors
green = (0, 128, 0)
white = (255, 255, 255)

# Paddle settings
paddle_width = 10
paddle_height = 100
paddle_speed = 10

# Ball settings
ball_size = 20
ball_speed_x = 5 * random.choice((1, -1))
ball_speed_y = 5 * random.choice((1, -1))

# Initialize paddles and ball
paddle_a = pygame.Rect(50, (height // 2) - (paddle_height // 2), paddle_width, paddle_height)
paddle_b = pygame.Rect(width - 50 - paddle_width, (height // 2) - (paddle_height // 2), paddle_width, paddle_height)
ball = pygame.Rect(width // 2 - ball_size // 2, height // 2 - ball_size // 2, ball_size, ball_size)

# Score
score_a = 0
score_b = 0
font = pygame.font.SysFont("Courier", 24)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and paddle_a.top > 0:
        paddle_a.y -= paddle_speed
    if keys[pygame.K_s] and paddle_a.bottom < height:
        paddle_a.y += paddle_speed
    if keys[pygame.K_UP] and paddle_b.top > 0:
        paddle_b.y -= paddle_speed
    if keys[pygame.K_DOWN] and paddle_b.bottom < height:
        paddle_b.y += paddle_speed

    # Move the ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with top and bottom
    if ball.top <= 0 or ball.bottom >= height:
        ball_speed_y *= -1

    # Ball collision with paddles
    if ball.colliderect(paddle_a) or ball.colliderect(paddle_b):
        ball_speed_x *= -1

    # Scoring
    if ball.left <= 0:
        score_b += 1
        ball.x, ball.y = width // 2 - ball_size // 2, height // 2 - ball_size // 2
        ball_speed_x *= -1
    if ball.right >= width:
        score_a += 1
        ball.x, ball.y = width // 2 - ball_size // 2, height // 2 - ball_size // 2
        ball_speed_x *= -1

    # Drawing
    screen.fill(green)
    pygame.draw.rect(screen, white, paddle_a)
    pygame.draw.rect(screen, white, paddle_b)
    pygame.draw.ellipse(screen, white, ball)

    # Display scores
    score_display = font.render(f"Jugador A: {score_a}  Jugador B: {score_b}", True, white)
    screen.blit(score_display, (width // 2 - score_display.get_width() // 2, 20))

    pygame.display.flip()
    pygame.time.Clock().tick(60)  # Frame rate

import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Configurar pantalla
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong con Poderes")

# Cargar imagen de fondo
background_image = pygame.image.load("fondo_pong.jpg").convert()
background_image = pygame.transform.scale(background_image, (width, height))

# Colores
white = (255, 255, 255)

# Paletas
paddle_width, paddle_height = 10, 100
paddle_speed = 10

# Pelota
ball_size = 20
ball_speed_x = 5 * random.choice((1, -1))
ball_speed_y = 5 * random.choice((1, -1))

# Objetos
paddle_a = pygame.Rect(50, height//2 - paddle_height//2, paddle_width, paddle_height)
paddle_b = pygame.Rect(width - 50 - paddle_width, height//2 - paddle_height//2, paddle_width, paddle_height)
ball = pygame.Rect(width//2 - ball_size//2, height//2 - ball_size//2, ball_size, ball_size)

# Poderes (gadgets)
power_active = False
power_timer = 0
power = pygame.Rect(random.randint(200, 600), random.randint(100, 500), 20, 20)
power_type = random.choice(["speed", "big_paddle", "big_ball", "reverse"])

# Puntuación
score_a, score_b = 0, 0
font = pygame.font.SysFont("Courier", 24)

clock = pygame.time.Clock()

# Bucle principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movimiento paletas
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and paddle_a.top > 0:
        paddle_a.y -= paddle_speed
    if keys[pygame.K_s] and paddle_a.bottom < height:
        paddle_a.y += paddle_speed
    if keys[pygame.K_UP] and paddle_b.top > 0:
        paddle_b.y -= paddle_speed
    if keys[pygame.K_DOWN] and paddle_b.bottom < height:
        paddle_b.y += paddle_speed

    # Mover pelota
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Colisiones
    if ball.top <= 0 or ball.bottom >= height:
        ball_speed_y *= -1

    if ball.colliderect(paddle_a) or ball.colliderect(paddle_b):
        ball_speed_x *= -1

    # Goles
    if ball.left <= 0:
        score_b += 1
        ball.x, ball.y = width//2 - ball_size//2, height//2 - ball_size//2
        ball_speed_x = 5 * random.choice((1, -1))
        ball_speed_y = 5 * random.choice((1, -1))
    if ball.right >= width:
        score_a += 1
        ball.x, ball.y = width//2 - ball_size//2, height//2 - ball_size//2
        ball_speed_x = 5 * random.choice((1, -1))
        ball_speed_y = 5 * random.choice((1, -1))

    # Poderes
    if not power_active and random.randint(0, 500) == 1:  # Aparece aleatoriamente
        power_active = True
        power.x, power.y = random.randint(100, width - 100), random.randint(50, height - 50)
        power_type = random.choice(["speed", "big_paddle", "big_ball", "reverse"])

    if power_active and ball.colliderect(power):
        if power_type == "speed":
            ball_speed_x *= 1.5
            ball_speed_y *= 1.5
        elif power_type == "big_paddle":
            paddle_a.height = 200  # jugador A se agranda
        elif power_type == "big_ball":
            ball.width = ball.height = 40
        elif power_type == "reverse":
            ball_speed_x *= -1
        power_active = False
        power_timer = pygame.time.get_ticks()

    # Restaurar paleta después de 5 segundos
    if pygame.time.get_ticks() - power_timer > 5000:
        paddle_a.height = 100
        ball.width = ball.height = 20

    # Dibujar
    screen.blit(background_image, (0, 0))
    pygame.draw.rect(screen, white, paddle_a)
    pygame.draw.rect(screen, white, paddle_b)
    pygame.draw.ellipse(screen, white, ball)

    if power_active:
        pygame.draw.rect(screen, (255, 0, 0), power)  # Color rojo para el gadget

    score_display = font.render(f"Jugador A: {score_a}  Jugador B: {score_b}", True, white)
    screen.blit(score_display, (width // 2 - score_display.get_width() // 2, 20))

    pygame.display.flip()
    clock.tick(60)

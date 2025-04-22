import pygame
import sys
import random

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong con Poderes")

# Cargar fondo
background_image = pygame.image.load("fondo_pong.jpg").convert()
background_image = pygame.transform.scale(background_image, (width, height))

# Colores
white = (255, 255, 255)

# Configuración
paddle_width, paddle_height = 10, 100
paddle_speed = 10
ball_size = 20

# Pelota principal
ball = pygame.Rect(width // 2, height // 2, ball_size, ball_size)
ball_speed = [5 * random.choice((1, -1)), 5 * random.choice((1, -1))]

# Pelota secundaria
extra_ball = None
extra_speed = [0, 0]

# Paletas
paddle_a = pygame.Rect(50, height // 2 - paddle_height // 2, paddle_width, paddle_height)
paddle_b = pygame.Rect(width - 50 - paddle_width, height // 2 - paddle_height // 2, paddle_width, paddle_height)

# Poderes
power_rect = pygame.Rect(0, 0, 40, 40)
power_type = None
power_timer = 0
power_active = False
power_visible = True
active_effects = {}

# Cargar íconos
power_icons = {
    "speed": pygame.image.load("speed.png"),
    "big_paddle": pygame.image.load("big_paddle.png"),
    "big_ball": pygame.image.load("big_ball.png"),
    "reverse": pygame.image.load("reverse.png"),
    "invisible": pygame.image.load("invisible.png"),
    "double": pygame.image.load("double.png")
}

# Escalar íconos
for key in power_icons:
    power_icons[key] = pygame.transform.scale(power_icons[key], (40, 40))

# Puntuación
score_a = 0
score_b = 0
font = pygame.font.SysFont("Courier", 24)

clock = pygame.time.Clock()

# Función para reiniciar pelota
def reset_ball():
    ball.x, ball.y = width // 2, height // 2
    ball_speed[0] = 5 * random.choice((1, -1))
    ball_speed[1] = 5 * random.choice((1, -1))

# Loop
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

    # Movimiento pelota principal
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # Movimiento pelota extra
    if extra_ball:
        extra_ball.x += extra_speed[0]
        extra_ball.y += extra_speed[1]

    # Colisiones pelota
    for b, speed in [(ball, ball_speed), (extra_ball, extra_speed) if extra_ball else (None, None)]:
        if not b: continue
        if b.top <= 0 or b.bottom >= height:
            speed[1] *= -1
        if b.colliderect(paddle_a) or b.colliderect(paddle_b):
            speed[0] *= -1

    # Goles
    for b, speed in [(ball, ball_speed), (extra_ball, extra_speed) if extra_ball else (None, None)]:
        if not b: continue
        if b.left <= 0:
            score_b += 1
            b.x, b.y = width // 2, height // 2
            speed[0] *= -1
        if b.right >= width:
            score_a += 1
            b.x, b.y = width // 2, height // 2
            speed[0] *= -1

    # Poder aparece
    if not power_active and random.randint(0, 400) == 1:
        power_type = random.choice(list(power_icons.keys()))
        power_rect.topleft = (random.randint(100, width - 140), random.randint(100, height - 140))
        power_active = True
        power_visible = True

    # Activar poder
    if power_active and ball.colliderect(power_rect):
        active_effects[power_type] = pygame.time.get_ticks()
        if power_type == "speed":
            ball_speed[0] *= 1.5
            ball_speed[1] *= 1.5
        elif power_type == "big_paddle":
            paddle_a.height = 200
        elif power_type == "big_ball":
            ball.width = ball.height = 40
        elif power_type == "reverse":
            ball_speed[0] *= -1
        elif power_type == "invisible":
            power_visible = False
        elif power_type == "double":
            extra_ball = ball.copy()
            extra_speed = [ball_speed[0], -ball_speed[1]]

        power_active = False
        power_timer = pygame.time.get_ticks()

    # Restaurar efectos después de 5 segundos
    for p in list(active_effects):
        if pygame.time.get_ticks() - active_effects[p] > 5000:
            if p == "big_paddle":
                paddle_a.height = 100
            elif p == "big_ball":
                ball.width = ball.height = 20
            elif p == "invisible":
                power_visible = True
            elif p == "double":
                extra_ball = None
            del active_effects[p]

    # Dibujar
    screen.blit(background_image, (0, 0))
    pygame.draw.rect(screen, white, paddle_a)
    pygame.draw.rect(screen, white, paddle_b)

    if power_visible:
        pygame.draw.ellipse(screen, white, ball)
        if extra_ball:
            pygame.draw.ellipse(screen, white, extra_ball)

    if power_active:
        screen.blit(power_icons[power_type], power_rect)

    score_display = font.render(f"Jugador A: {score_a}  Jugador B: {score_b}", True, white)
    screen.blit(score_display, (width // 2 - score_display.get_width() // 2, 20))

    pygame.display.flip()
    clock.tick(60)
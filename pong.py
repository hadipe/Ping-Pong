import pygame
import sys
import random

# Inicializar Pygame y audio
pygame.init()
pygame.mixer.init()

# Lista de canciones (playlist)
playlist = [
    "musica_fondo1.mp3",
    "musica_fondo2.mp3",
    "musica_fondo3.mp3"
]
current_song = 0

# Evento para detectar fin de canción
pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)

def play_next_song():
    global current_song
    pygame.mixer.music.load(playlist[current_song])
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play()
    current_song = (current_song + 1) % len(playlist)

play_next_song()  # Reproducir la primera canción

# Cargar sonidos
hit_sound = pygame.mixer.Sound("hit.wav.mp3")
score_sound = pygame.mixer.Sound("score.wav.mp3")
power_sound = pygame.mixer.Sound("power.wav.mp3")

# Configurar pantalla
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong con Poderes")

# Imagen de fondo
background_image = pygame.image.load("fondo_pong.jpg").convert()
background_image = pygame.transform.scale(background_image, (width, height))

# Imágenes de poderes
power_images = {
    "speed": pygame.image.load("power_speed.png"),
    "big_paddle": pygame.image.load("power_big_paddle.png"),
    "big_ball": pygame.image.load("power_big_ball.png"),
    "reverse": pygame.image.load("power_reverse.png"),
    "freeze": pygame.image.load("power_freeze.png"),
    "multi_ball": pygame.image.load("power_multi_ball.png"),
    "invisible": pygame.image.load("power_invisible.png"),
}
for key in power_images:
    power_images[key] = pygame.transform.scale(power_images[key], (20, 20))

# Colores
white = (255, 255, 255)

# Paletas y pelota
paddle_width, paddle_height = 10, 100
paddle_speed = 10

ball_size = 20
ball_speed_x = 5 * random.choice((1, -1))
ball_speed_y = 5 * random.choice((1, -1))

paddle_a = pygame.Rect(50, height//2 - paddle_height//2, paddle_width, paddle_height)
paddle_b = pygame.Rect(width - 50 - paddle_width, height//2 - paddle_height//2, paddle_width, paddle_height)
ball = pygame.Rect(width//2 - ball_size//2, height//2 - ball_size//2, ball_size, ball_size)
second_ball = None

# Poderes
power_active = False
power_timer = 0
power = pygame.Rect(random.randint(200, 600), random.randint(100, 500), 20, 20)
power_type = ""
frozen = False
frozen_timer = 0
invisible = False
invisible_timer = 0

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
        elif event.type == pygame.USEREVENT + 1:
            play_next_song()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_n:
            play_next_song()  # Cambio manual de canción

    # Movimiento paletas
    keys = pygame.key.get_pressed()
    if not frozen:
        if keys[pygame.K_w] and paddle_a.top > 0:
            paddle_a.y -= paddle_speed
        if keys[pygame.K_s] and paddle_a.bottom < height:
            paddle_a.y += paddle_speed
    if keys[pygame.K_UP] and paddle_b.top > 0:
        paddle_b.y -= paddle_speed
    if keys[pygame.K_DOWN] and paddle_b.bottom < height:
        paddle_b.y += paddle_speed

    # Movimiento pelota(s)
    ball.x += int(ball_speed_x)
    ball.y += int(ball_speed_y)
    if second_ball:
        second_ball.x += int(ball_speed_x)
        second_ball.y += int(ball_speed_y)

    # Colisiones
    for b in [ball] + ([second_ball] if second_ball else []):
        if b.top <= 0 or b.bottom >= height:
            ball_speed_y *= -1
        if b.colliderect(paddle_a) or b.colliderect(paddle_b):
            ball_speed_x *= -1
            hit_sound.play()

    # Goles
    for b in [ball] + ([second_ball] if second_ball else []):
        if b.left <= 0:
            score_b += 1
            b.x, b.y = width//2 - ball_size//2, height//2 - ball_size//2
            ball_speed_x = 5 * random.choice((1, -1))
            ball_speed_y = 5 * random.choice((1, -1))
            score_sound.play()
        if b.right >= width:
            score_a += 1
            b.x, b.y = width//2 - ball_size//2, height//2 - ball_size//2
            ball_speed_x = 5 * random.choice((1, -1))
            ball_speed_y = 5 * random.choice((1, -1))
            score_sound.play()

    # Activar poderes
    if not power_active and random.randint(0, 500) == 1:
        power_active = True
        power.x, power.y = random.randint(100, width - 100), random.randint(50, height - 50)
        power_type = random.choice([
            "speed", "big_paddle", "big_ball", "reverse",
            "freeze", "multi_ball", "invisible"
        ])

    if power_active and ball.colliderect(power):
        power_sound.play()
        if power_type == "speed":
            ball_speed_x *= 1.5
            ball_speed_y *= 1.5
        elif power_type == "big_paddle":
            paddle_a.height = 200
        elif power_type == "big_ball":
            ball.width = ball.height = 40
        elif power_type == "reverse":
            ball_speed_x *= -1
        elif power_type == "freeze":
            frozen = True
            frozen_timer = pygame.time.get_ticks()
        elif power_type == "multi_ball":
            second_ball = pygame.Rect(ball.x, ball.y, 20, 20)
        elif power_type == "invisible":
            invisible = True
            invisible_timer = pygame.time.get_ticks()
        power_active = False
        power_timer = pygame.time.get_ticks()

    # Restaurar efectos
    if pygame.time.get_ticks() - power_timer > 5000:
        paddle_a.height = 100
        ball.width = ball.height = 20
        second_ball = None
        invisible = False
    if frozen and pygame.time.get_ticks() - frozen_timer > 3000:
        frozen = False

    # Dibujar
    screen.blit(background_image, (0, 0))
    pygame.draw.rect(screen, white, paddle_a)
    pygame.draw.rect(screen, white, paddle_b)
    if not invisible:
        pygame.draw.ellipse(screen, white, ball)
    if second_ball:
        pygame.draw.ellipse(screen, white, second_ball)
    if power_active:
        screen.blit(power_images[power_type], (power.x, power.y))
    score_display = font.render(f"Jugador A: {score_a}  Jugador B: {score_b}", True, white)
    screen.blit(score_display, (width // 2 - score_display.get_width() // 2, 20))
    pygame.display.flip()
    clock.tick(60)
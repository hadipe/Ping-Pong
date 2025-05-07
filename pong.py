import pygame
import sys
import random
import time
import math

# Inicialización
pygame.init()
pygame.mixer.init()

# Pantalla
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong con Poderes y Pelota Circular")

# Colores
white = (255, 255, 255)
gray = (180, 180, 180)

# Fuente
font = pygame.font.SysFont("Courier", 24)

# Variables de volumen
music_volume = 0.5
sfx_volume = 0.5

# Musica
playlist = ["cancion1.mp3", "cancion3.mp3", "cancion2.mp3"]
song_lengths = {"cancion1.mp3": 120, "cancion3.mp3": 140, "cancion2.mp3": 160}
current_song = 0
song_start_time = time.time()
pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)

# Sonidos
hit_sound = pygame.mixer.Sound("hit.wav.mp3")
score_sound = pygame.mixer.Sound("score.wav.mp3")
power_sound = pygame.mixer.Sound("power.wav.mp3")

# Imágenes
background_image = pygame.image.load("fondo_pong.jpg").convert()
background_image = pygame.transform.scale(background_image, (width, height))
pause_menu_image = pygame.image.load("menu_pausa.png").convert_alpha()
pause_menu_image = pygame.transform.scale(pause_menu_image, (400, 300))

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
    power_images[key] = pygame.transform.scale(power_images[key], (40, 40))

# Funciones musicales
def play_next_song():
    global current_song, song_start_time
    pygame.mixer.music.load(playlist[current_song])
    pygame.mixer.music.set_volume(music_volume)
    pygame.mixer.music.play()
    song_start_time = time.time()
    current_song = (current_song + 1) % len(playlist)

def play_previous_song():
    global current_song, song_start_time
    current_song = (current_song - 2) % len(playlist)
    pygame.mixer.music.load(playlist[current_song])
    pygame.mixer.music.set_volume(music_volume)
    pygame.mixer.music.play()
    song_start_time = time.time()
    current_song = (current_song + 1) % len(playlist)

play_next_song()

# Paletas
paddle_width, paddle_height = 10, 100
paddle_speed = 10
paddle_a = pygame.Rect(50, height//2 - paddle_height//2, paddle_width, paddle_height)
paddle_b = pygame.Rect(width - 50 - paddle_width, height//2 - paddle_height//2, paddle_width, paddle_height)

# Pelota circular
ball_radius = 10
ball_pos = [width//2, height//2]
ball_speed = [5 * random.choice((1, -1)), 5 * random.choice((1, -1))]
second_ball = None

# Puntuación
score_a, score_b = 0, 0

# Poderes
power_active = False
power_timer = 0
power = pygame.Rect(random.randint(200, 600), random.randint(100, 500), 20, 20)
power_type = ""
frozen = False
frozen_timer = 0
invisible = False
invisible_timer = 0

# Pausa
paused = False
clock = pygame.time.Clock()

# Colisión círculo-rectángulo
def circle_rect_collision(circle_pos, circle_radius, rect):
    cx, cy = circle_pos
    closest_x = max(rect.left, min(cx, rect.right))
    closest_y = max(rect.top, min(cy, rect.bottom))
    distance = math.hypot(cx - closest_x, cy - closest_y)
    return distance < circle_radius

# Bucle principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.USEREVENT + 1:
            play_next_song()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                paused = not paused
            elif event.key == pygame.K_n:
                play_next_song()
            elif event.key == pygame.K_b:
                play_previous_song()
            elif paused:
                if event.key == pygame.K_LEFT:
                    music_volume = max(0, music_volume - 0.1)
                    pygame.mixer.music.set_volume(music_volume)
                elif event.key == pygame.K_RIGHT:
                    music_volume = min(1, music_volume + 0.1)
                    pygame.mixer.music.set_volume(music_volume)
                elif event.key == pygame.K_DOWN:
                    sfx_volume = max(0, sfx_volume - 0.1)
                elif event.key == pygame.K_UP:
                    sfx_volume = min(1, sfx_volume + 0.1)
                hit_sound.set_volume(sfx_volume)
                score_sound.set_volume(sfx_volume)
                power_sound.set_volume(sfx_volume)

    if paused:
        screen.blit(background_image, (0, 0))
        screen.blit(pause_menu_image, (width // 2 - 200, height // 2 - 150))
        screen.blit(font.render("JUEGO EN PAUSA", True, white), (width//2 - 100, 180))
        screen.blit(font.render(f"Musica: {int(music_volume * 100)}%", True, white), (width//2 - 100, 240))
        screen.blit(font.render(f"Sonidos: {int(sfx_volume * 100)}%", True, white), (width//2 - 100, 270))
        screen.blit(font.render("Pulsa ESC o P para continuar", True, white), (width//2 - 140, 320))
        pygame.display.flip()
        clock.tick(15)
        continue

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

    # Movimiento pelota
    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]

    # Segundo balón
    if second_ball:
        second_ball[0] += ball_speed[0]
        second_ball[1] += ball_speed[1]

    # Rebote arriba/abajo
    if ball_pos[1] - ball_radius <= 0 or ball_pos[1] + ball_radius >= height:
        ball_speed[1] *= -1

    if second_ball:
        if second_ball[1] - ball_radius <= 0 or second_ball[1] + ball_radius >= height:
            ball_speed[1] *= -1

    # Colisiones con paletas
    if circle_rect_collision(ball_pos, ball_radius, paddle_a) and ball_speed[0] < 0:
        ball_speed[0] *= -1
        hit_sound.play()
    if circle_rect_collision(ball_pos, ball_radius, paddle_b) and ball_speed[0] > 0:
        ball_speed[0] *= -1
        hit_sound.play()

    if second_ball:
        if circle_rect_collision(second_ball, ball_radius, paddle_a) and ball_speed[0] < 0:
            ball_speed[0] *= -1
            hit_sound.play()
        if circle_rect_collision(second_ball, ball_radius, paddle_b) and ball_speed[0] > 0:
            ball_speed[0] *= -1
            hit_sound.play()

    # Goles
    if ball_pos[0] - ball_radius <= 0:
        score_b += 1
        ball_pos = [width//2, height//2]
        ball_speed = [5 * random.choice((1, -1)), 5 * random.choice((1, -1))]
        score_sound.play()
    if ball_pos[0] + ball_radius >= width:
        score_a += 1
        ball_pos = [width//2, height//2]
        ball_speed = [5 * random.choice((1, -1)), 5 * random.choice((1, -1))]
        score_sound.play()

    # Poderes
    if not power_active and random.randint(0, 500) == 1:
        power_active = True
        power.x, power.y = random.randint(100, width - 100), random.randint(50, height - 50)
        power_type = random.choice(["speed", "big_paddle", "big_ball", "reverse", "freeze", "multi_ball", "invisible"])

    if power_active and math.hypot(ball_pos[0] - power.centerx, ball_pos[1] - power.centery) < ball_radius + 20:
        power_sound.play()
        if power_type == "speed":
            ball_speed[0] *= 1.5
            ball_speed[1] *= 1.5
        elif power_type == "big_paddle":
            paddle_a.height = 200
        elif power_type == "big_ball":
            ball_radius = 20
        elif power_type == "reverse":
            ball_speed[0] *= -1
        elif power_type == "freeze":
            frozen = True
            frozen_timer = pygame.time.get_ticks()
        elif power_type == "multi_ball":
            second_ball = list(ball_pos)
        elif power_type == "invisible":
            invisible = True
            invisible_timer = pygame.time.get_ticks()
        power_active = False
        power_timer = pygame.time.get_ticks()

    # Restaurar efectos
    if pygame.time.get_ticks() - power_timer > 5000:
        paddle_a.height = 100
        ball_radius = 10
        second_ball = None
        invisible = False
    if frozen and pygame.time.get_ticks() - frozen_timer > 3000:
        frozen = False

    # Dibujos
    screen.blit(background_image, (0, 0))
    pygame.draw.rect(screen, white, paddle_a)
    pygame.draw.rect(screen, white, paddle_b)
    if not invisible:
        pygame.draw.circle(screen, white, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)
    if second_ball:
        pygame.draw.circle(screen, white, (int(second_ball[0]), int(second_ball[1])), ball_radius)
    if power_active:
        screen.blit(power_images[power_type], (power.x, power.y))

    # Puntuación
    score_display = font.render(f"Jugador A: {score_a}  Jugador B: {score_b}", True, white)
    screen.blit(score_display, (width // 2 - score_display.get_width() // 2, 20))

    # Barra de progreso de la canción
    current_filename = playlist[(current_song - 1) % len(playlist)]
    song_duration = song_lengths[current_filename]
    elapsed = time.time() - song_start_time
    progress = min(1, elapsed / song_duration)
    bar_width = int(progress * 300)
    pygame.draw.rect(screen, gray, (width // 2 - 150, height - 40, 300, 10))
    pygame.draw.rect(screen, white, (width // 2 - 150, height - 40, bar_width, 10))
    song_name_text = font.render(current_filename, True, white)
    screen.blit(song_name_text, (width // 2 - song_name_text.get_width() // 2, height - 60))

    pygame.display.flip()
    clock.tick(60)

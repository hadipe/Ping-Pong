import turtle
import os

h = turtle.Screen()
h.title("Pong")
h.bgcolor("Green")
h.setup(width=800, height=600)
h.tracer(0)

# Los Puntos
puntuacion_a = 0
puntuacion_b = 0

# Cosas de la paleta A
paleta_a = turtle.Turtle()
paleta_a.speed(0)
paleta_a.shape("square")
paleta_a.color("white")
paleta_a.shapesize(stretch_wid=5, stretch_len=1)
paleta_a.penup()
paleta_a.goto(-350, 0)

# Cosas de la paleta B
paleta_b = turtle.Turtle()
paleta_b.speed(0)
paleta_b.shape("square")
paleta_b.color("white")
paleta_b.shapesize(stretch_wid=5, stretch_len=1)
paleta_b.penup()
paleta_b.goto(350, 0)

# Cosas de la pelota
pelota = turtle.Turtle()
pelota.speed(0)
pelota.shape("square")
pelota.color("white")
pelota.penup()
pelota.goto(0, 0)
pelota.dx = 0.09  # Velocidad inicial más baja
pelota.dy = 0.09  # Velocidad inicial más baja


# Marcador
marcador = turtle.Turtle()
marcador.speed(0)
marcador.shape("circle")
marcador.color("white")
marcador.penup()
marcador.hideturtle()
marcador.goto(0, 260)
marcador.write("Jugador A: 0  Jugador B: 0", align="center", font=("Courier", 24, "normal"))

# no se
def paleta_a_arriba():
    y = paleta_a.ycor()
    y += 20
    paleta_a.sety(y)

def paleta_a_abajo():
    y = paleta_a.ycor()
    y -= 20
    paleta_a.sety(y)

def paleta_b_arriba():
    y = paleta_b.ycor()
    y += 20
    paleta_b.sety(y)

def paleta_b_abajo():
    y = paleta_b.ycor()
    y -= 20
    paleta_b.sety(y)

# Movimiento con el teclado
h.listen()
h.onkeypress(paleta_a_arriba, "w")
h.onkeypress(paleta_a_abajo, "s")
h.onkeypress(paleta_b_arriba, "Up")
h.onkeypress(paleta_b_abajo, "Down")

# Bucle del juego
while True:
    h.update()
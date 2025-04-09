import turtle
import os

wn = turtle.Screen()
wn.title("Pong")
wn.bgcolor("Green")
wn.setup(width=800, height=600)
wn.tracer(0)

# Puntuación
puntuacion_a = 0
puntuacion_b = 0

# Paleta A
paleta_a = turtle.Turtle()
paleta_a.speed(0)
paleta_a.shape("square")
paleta_a.color("white")
paleta_a.shapesize(stretch_wid=5, stretch_len=1)
paleta_a.penup()
paleta_a.goto(-350, 0)

# Paleta B
paleta_b = turtle.Turtle()
paleta_b.speed(0)
paleta_b.shape("square")
paleta_b.color("white")
paleta_b.shapesize(stretch_wid=5, stretch_len=1)
paleta_b.penup()
paleta_b.goto(350, 0)

# Pelota
pelota = turtle.Turtle()
pelota.speed(0)
pelota.shape("square")
pelota.color("white")
pelota.penup()
pelota.goto(0, 0)
pelota.dx = 0.09  # Velocidad inicial más baja
pelota.dy = 0.09  # Velocidad inicial más baja


# Lápiz 
lapiz = turtle.Turtle()
lapiz.speed(0)
lapiz.shape("square")
lapiz.color("white")
lapiz.penup()
lapiz.hideturtle()
lapiz.goto(0, 260)
lapiz.write("Jugador A: 0  Jugador B: 0", align="center", font=("Courier", 24, "normal"))

# Funciones
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

# Configuración del teclado
wn.listen()
wn.onkeypress(paleta_a_arriba, "w")
wn.onkeypress(paleta_a_abajo, "s")
wn.onkeypress(paleta_b_arriba, "Up")
wn.onkeypress(paleta_b_abajo, "Down")

# Bucle principal del juego
while True:
    wn.update()
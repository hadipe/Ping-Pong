import random

options = ("Piedra", "Papel", "Tijeras")
running = True

while running:

    player = None
    computer = random.choice(options)

    while player not in options:
        player = input("Selecciona tu opcion (Piedra, Papel, Tijeras): ")

    print(f"Player: {player}")
    print(f"Computer: {computer}")

    if player == computer:
        print("ES UN EMPATE!")
    elif player == "Piedra" and computer == "Tijeras":
        print("GANASTE!")
    elif player == "Papel" and computer == "Piedra":
        print("GANAS!")
    elif player == "scissors" and computer == "paper":
        print("VICTORIA!")
    #else:
       # print("MALA SUERTE PIERDES!")
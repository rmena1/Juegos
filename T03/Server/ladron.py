import random

def ladron(parent):
    for jugador in parent.jugadores:
        cantidad_materia = jugador.madera + jugador.arcilla + jugador.trigo
        if cantidad_materia > 7:
            contador = 0
            while contador < cantidad_materia // 2:
                materia = random.randint(0, 2)
                if materia == 0:
                    if jugador.madera > 0:
                        jugador.madera -= 1
                    else:
                        contador -= 1
                elif materia == 1:
                    if jugador.arcilla > 0:
                        jugador.arcilla -= 1
                    else:
                        contador -= 1
                elif materia == 2:
                    if jugador.trigo > 0:
                        jugador.trigo -= 1
                    else:
                        contador -= 1
                contador += 1
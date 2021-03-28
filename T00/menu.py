import tablero as tabl
import os 
import random
import parametros

def menu_principal():
    while True:
        print('*** MENU DE INICIO ***\n')
        entrada = input('[1] -> Iniciar partida \n[2] -> Rankings \n[3] -> Salir \nIngresa una acción: ')
        print('')

        if entrada in '123':
            return entrada

        else:
            print('Acción inválida, intenta nuevamente.')
            input('Presiona Enter para continuar.')
            print('')


def apodo():
    print('*** CREACIÓN DE APODO ***')
    while True:
        nombre_jugador = input('Ingresa tu nombre: ')
        print('')
        if len(nombre_jugador) >= 5 and nombre_jugador.isalnum():
            return nombre_jugador
        
        else:
            print('Nombre inválido. Tu nombre debe tener como mínimo cinco carácteres y estar compuesto sólo de letras y números.')
            input('Presiona Enter para continuar.')
            print('')
            entrada = input('[1] -> Volver a ingresar nombre \n[2] -> Volver al menú \nIngresa una acción: ')
            print('')
            
            if entrada == '2':
                return 'menu_'
            
            elif not entrada == '1':
                print('Opción inválida.')
                input('Presiona Enter para volver a intentar.')

            print('')


def tamaño_tablero():
    print('*** CREACIÓN DE TABLERO ***')
    while True:
        print('Creación del tablero. Alto y ancho deben ser números entre 3 y 15 (inclusive).')
        alto = input('Ingrese el alto del tablero: ').strip(' ')
        ancho = input('Ingrese el ancho del tablero: ').strip(' ')
        print('')

        if alto in '101121314156789' and ancho in '1011213141567890':
            alto = int(alto)
            ancho = int(ancho)
            if ancho >= 3 and ancho <= 15 and alto >= 3 and alto <= 15:
                break

        print('Valores incorrectos. Intentar nuevamente?')
        entrada = input('[1] -> Si. \n[2] -> No, salir del programa. \nIngresa una acción: ')
        print('')

        if entrada != '1' and entrada != '2':
            print('Entrada incorrecta, intente nuevamente.')
            input('Presiona Enter para continuar.')
            print('')
            return 'menu_'

        if entrada == '2':
            exit()

    tablero_propio = []
    tablero_rival = []

    for fila in range(alto):
        tablero_propio.append([])
        tablero_rival.append([])

        for columna in range(ancho):
            tablero_propio[fila].append(' ')
            tablero_rival[fila].append(' ')
    
    return tablero_propio, tablero_rival        


def rankings():
    print('*** RANKING DE PUNTAJES ***\n')
    with open(os.path.join('puntajes.txt'), 'rt') as archivo:
        ranking = archivo.readlines()
    
    for indice in range(len(ranking)):
        ranking[indice] = ranking[indice].strip('\n').split(',')
        ranking[indice][1] = int(ranking[indice][1])
    
    puntaje_maximo = -1
    mejores_puntajes = []

    for puesto in range(5):
        for jugador in ranking:
            if jugador[1] > puntaje_maximo:
                mejor_jugador = jugador
                puntaje_maximo = jugador[1]
        mejores_puntajes.append(mejor_jugador)
        ranking.remove(mejor_jugador)
        puntaje_maximo = -1
        if len(ranking) == 0:
            break

    lugar = 1
    for jugador in mejores_puntajes:
        print(f'{lugar}) {jugador[0]}: {jugador[1]} Pts.')
        lugar += 1
    print('')
    
    input('Presiona Enter para volver.')
    print('')
    return

def ubicar_flota(tablero):
    tablero_propio = tablero[0]
    tablero_rival = tablero[1]

    numero_de_barcos = 0
    while True:
        fila = random.randint(0, len(tablero_propio) - 1)
        columna = random.randint(0, len(tablero_propio[0]) - 1)

        if tablero_propio[fila][columna] != 'B':
            tablero_propio[fila][columna] = 'B'
            numero_de_barcos += 1


        if numero_de_barcos == parametros.NUM_BARCOS:
            break
    
    numero_de_barcos = 0
    while True:
        fila = random.randint(0, len(tablero_rival) - 1)
        columna = random.randint(0, len(tablero_rival[0]) - 1)

        if tablero_rival[fila][columna] != 'B':
            tablero_rival[fila][columna] = 'B'
            numero_de_barcos += 1

        if numero_de_barcos == parametros.NUM_BARCOS:
            return tablero_propio, tablero_rival


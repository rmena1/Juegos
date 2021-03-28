import menu
import parametros
import tablero
import random
import os


def menu_juego(juego):
    print('*** MENU DE JUEGO *** \n')

    while True:
        tablero.print_tablero(juego.tablero_rival, juego.tablero_propio)
        print('')
        print('[1] -> Salir \n[2] -> Rendirse \n[3] -> Lanzar una bomba')
        entrada = input('Elige una opción: ')
        print('')
        
        if entrada == '1':
            exit()

        elif entrada == '2':
            return 'menu_'

        elif entrada == '3':
            return 'bomba!'

        else:
            print('Opción inválida, intente nuevamente.')
            input('Presiona Enter para continuar.')
            print('')


def seleccionar_bomba():
    print('*** SELECCIONAR BOMBA *** \n')

    print('Capitán! Enemigo a la vista! ¿Con que bomba debemos atacar?')
    input('Presiona Enter para continuar.')
    print('')
    while True:
        entrada = input('[1] -> Bomba normal \n[2] -> Super Bomba! \nElige tu bomba Capitán: ')
        print('')

        if entrada == '1':
            return 'normal'

        elif entrada == '2':
            return 'super'
        
        else:
            print('Lo siento, no entendí tu respuesta :( \nIntenta nuevamente.')
            input('Presiona Enter para continuar.')
            print('')


def seleccionar_coordenadas(juego):
    while True:
        fila_ataque = input('Ingresa un número para registrar la FILA: ')
        columna_ataque = input('Ingresa una letra para registrar la COLUMNA: ')
        print('')
        columna_ataque = columna_ataque.lower()

        if fila_ataque in '101121314156789':
            fila_ataque = int(fila_ataque)

        else:
            print('No logré entender tus coordenadas, intenta nuevamente!')
            input('Presiona Enter para continuar.')
            print('')
            continue

        if columna_ataque in 'abcdefghijklmno':
            columna_ataque = 'abcdefghijklmno'.index(columna_ataque)

        else:
            print('No logré entender tus coordenadas, intenta nuevamente!')
            input('Presiona Enter para continuar.')
            print('')
            continue

        if fila_ataque >= len(juego.tablero_rival) or columna_ataque >= len(juego.tablero_rival[0]):
            print('No logré entender tus coordenadas, intenta nuevamente!')
            input('Presiona Enter para continuar.')
            print('')
            continue

        return fila_ataque, columna_ataque


def resultado_bomba_normal(juego, fila_ataque, columna_ataque):
    if juego.tablero_rival[fila_ataque][columna_ataque] == ' ':
        juego.tablero_rival[fila_ataque][columna_ataque] = 'x'
        print('Demonios! Hemos fallado!')
        input('Presiona Enter para continuar.')
        print('')
        return 'x'

    elif juego.tablero_rival[fila_ataque][columna_ataque] == 'B':
        juego.tablero_rival[fila_ataque][columna_ataque] = 'F'
        print('Fuego a la vista! Hemos acertado!')
        input('Presiona Enter para continuar.')
        print('')
        juego.hundidos_enemigo += 1
        if juego.fin_juego():
            print('Enemigo derrotado! Has ganado!')
            input('Presiona Enter para continuar.')
            print('')
        else:
            print('Repites turno por acertar!')
            input('Presiona Enter para continuar.')
            print('')
        return 'F'

    elif juego.tablero_rival[fila_ataque][columna_ataque] == 'x' or juego.tablero_rival[fila_ataque][columna_ataque] == 'F':
        print('Ya hemos disparado en esa dirección, elige una coordenada distinta!')
        input('Presiona Enter para continuar.')
        print('')
        return 'denuevo'


def resultado_bomba_especial(juego, fila_ataque, columna_ataque):
    if fila_ataque >= len(juego.tablero_rival) or columna_ataque >= len(juego.tablero_rival[0]) or fila_ataque < 0 or columna_ataque < 0:
        return False

    if juego.tablero_rival[fila_ataque][columna_ataque] == ' ' or juego.tablero_rival[fila_ataque][columna_ataque] == 'x':
        juego.tablero_rival[fila_ataque][columna_ataque] = 'x'

    elif juego.tablero_rival[fila_ataque][columna_ataque] == 'B':
        juego.tablero_rival[fila_ataque][columna_ataque] = 'F'
        return True

    elif juego.tablero_rival[fila_ataque][columna_ataque] == 'F':
        juego.tablero_rival[fila_ataque][columna_ataque] = 'F'

    return False


def bomba(radio, juego):
    if radio == 0:
        print('Bomba normal seleccionada!')
        input('Presiona Enter para continuar.')
        print('')
        tablero.print_tablero(juego.tablero_rival, juego.tablero_propio)
        print('Ingresa las coordenadas de ataque!')

        while True:
            fila_ataque, columna_ataque = seleccionar_coordenadas(juego)
            resultado = resultado_bomba_normal(juego, fila_ataque, columna_ataque)
            tablero.print_tablero(juego.tablero_rival, juego.tablero_propio)
            print('')
            if resultado == 'F':
                return True
            elif resultado == 'x':
                return False

    else:
        if juego.bomba_especial:
            print('No tenemos más disponibilidad de bombas especiales! \nIntenta con una bomba normal.')
            input('Presiona Enter para continuar.')
            print('')
            return True
        
        else:
            print('Selecciona una Bomba Especial de nuestro catálogo de Super Bombas!')
            input('Presiona Enter para continuar.')
            print('')
            while True:
                print('[1] -> Bomba Cruz \n[2] -> Bomba X \n[3] -> Bomba Diamante')
                entrada = input('Elige tu bomba!: ')
                print('')

                if entrada == '1':
                    if bomba_cruz(radio, juego):
                        return True
                    else:
                        return False 

                elif entrada == '2':
                    if bomba_x(radio, juego):
                        return True
                    else:
                        return False

                elif entrada == '3':
                    if bomba_diamante(radio, juego):
                        return True
                    else:
                        return False

                else:
                    print('No entendí tu selección :( intenta nuevamente!')
                    input('Presiona Enter para continuar.')
                    print('')

        pass


def bomba_cruz(radio, juego):
    print('Has elegido Bomba Cruz, Acabemos con estos malditos!')
    input('Presiona Enter para continuar.')
    print('')
    tablero.print_tablero(juego.tablero_rival, juego.tablero_propio)
    print('')
    print('Ingresa las coordenadas del centro de la explosión!')
    fila_centro, columna_centro = seleccionar_coordenadas(juego)
    explosiones = 0

    for i in range(radio):
        if resultado_bomba_especial(juego, fila_centro + i, columna_centro):
            explosiones += 1
        if resultado_bomba_especial(juego, fila_centro - i, columna_centro):
            explosiones += 1
        if resultado_bomba_especial(juego, fila_centro, columna_centro + i):
            explosiones += 1
        if resultado_bomba_especial(juego, fila_centro, columna_centro - i):
            explosiones += 1
    
    if explosiones != 0:
        print(f'Hemos derribado {explosiones} flota(s) enemigas con la Bomba Especial!')
        juego.hundidos_enemigo += explosiones
        if juego.fin_juego():
            print('Enemigo derrotado! Has ganado!')
            input('Presiona Enter para continuar.')
            print('')
        else:
            print('Repites turno por acertar!')
            input('Presiona Enter para continuar.')
            print('')
        return True

    else:
        print('Linda explosión, pero no logramos derribar ninguna flota enemiga :(')
        input('Presiona Enter para continuar.')
        print('')
        return False




def bomba_x(radio, juego):
    print('Has elegido Bomba X, Acabemos con estos malditos!')
    input('Presiona Enter para continuar.')
    print('')
    tablero.print_tablero(juego.tablero_rival, juego.tablero_propio)
    print('')
    print('Ingresa las coordenadas del centro de la explosión!')
    fila_centro, columna_centro = seleccionar_coordenadas(juego)
    explosiones = 0

    for i in range(radio):
        if resultado_bomba_especial(juego, fila_centro + i, columna_centro + i):
            explosiones += 1
        if resultado_bomba_especial(juego, fila_centro - i, columna_centro - i):
            explosiones += 1
        if resultado_bomba_especial(juego, fila_centro - i, columna_centro + i):
            explosiones += 1
        if resultado_bomba_especial(juego, fila_centro + i, columna_centro - i):
            explosiones += 1
    
    if explosiones != 0:
        print(f'Hemos derribado {explosiones} flota(s) enemigas con la Bomba Especial!')
        input('Presiona Enter para continuar.')
        print('')
        juego.hundidos_enemigo += explosiones
        if juego.fin_juego():
            print('Enemigo derrotado! Has ganado!')
            input('Presiona Enter para continuar.')
            print('')
        else:
            print('Repites turno por acertar!')
            input('Presiona Enter para continuar.')
            print('')
        return True

    else:
        print('Linda explosión, pero no logramos derribar ninguna flota enemiga :(')
        input('Presiona Enter para continuar.')
        print('')
        return False


def bomba_diamante(radio, juego):
    print('Has elegido Bomba Diamante, Acabemos con estos malditos!')
    input('Presiona Enter para continuar.')
    print('')
    tablero.print_tablero(juego.tablero_rival, juego.tablero_propio)
    print('')
    print('Ingresa las coordenadas del centro de la explosión!')
    fila_centro, columna_centro = seleccionar_coordenadas(juego)
    explosiones = 0

    if resultado_bomba_especial(juego, fila_centro, columna_centro):
        explosiones += 1
    for i in range(radio):
        for j in range(i):
            if resultado_bomba_especial(juego, fila_centro + i - j, columna_centro + j):
                explosiones += 1
            if resultado_bomba_especial(juego, fila_centro - i + j, columna_centro - j):
                explosiones += 1
            if resultado_bomba_especial(juego, fila_centro - j, columna_centro + i - j):
                explosiones += 1
            if resultado_bomba_especial(juego, fila_centro + j, columna_centro - i + j):
                explosiones += 1
    
    if explosiones != 0:
        print(f'Hemos derribado {explosiones} flota(s) enemigas con la Bomba Especial!')
        input('Presiona Enter para continuar.')
        print('')
        juego.hundidos_enemigo += explosiones
        if juego.fin_juego():
            print('Enemigo derrotado! Has ganado!')
            input('Presiona Enter para continuar.')
            print('')
        else:
            print('Repites turno por acertar!')
            input('Presiona Enter para continuar.')
            print('')
        return True

    else:
        print('Linda explosión, pero no logramos derribar ninguna flota enemiga :(')
        input('Presiona Enter para continuar.')
        print('')
        return False


def puntaje(juego):
    puntaje = max(0, (len(juego.tablero_propio) * len(juego.tablero_propio[0]) * parametros.NUM_BARCOS * (juego.hundidos_enemigo - juego.hundidos_propio)))
    print(f'PUNTAJE: {puntaje}')
    input('Presiona Enter para continuar.')
    print('')
    with open(os.path.join('puntajes.txt'), 'a') as archivo: #https://stackoverflow.com/questions/45198007/write-to-the-last-line-of-a-text-file
        linea = juego.jugador.nombre + ',' + str(puntaje)
        archivo.write('\n')
        archivo.write(linea)




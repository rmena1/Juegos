import menu
import batalla_naval as bnav
import parametros
import tablero
import random

class Jugador:

    def __init__(self, nombre_jugador):
        self.nombre = nombre_jugador

    def __str__(self):
        return f'Hola! soy {self.nombre}'

class Juego:

    def __init__(self, tablero_propio, tablero_rival, jugador):
        self.jugador = jugador
        self.tablero_propio = tablero_propio
        self.tablero_rival = tablero_rival
        self.bomba_especial = False
        self.hundidos_enemigo = 0
        self.hundidos_propio = 0
        self.juego_finalizado = False

    def turno_maquina(self):
        while True:
            atacar_fila = random.randint(0, len(self.tablero_propio) - 1)
            atacar_columna = random.randint(0, len(self.tablero_propio[0]) - 1)
            if self.tablero_propio[atacar_fila][atacar_columna] == ' ':
                self.tablero_propio[atacar_fila][atacar_columna] = 'x'
                abecedario = 'ABCDEFGHIJKLMNOPQ'
                print(f'El enemigo ha atacado la coordenada {atacar_fila}, {abecedario[atacar_columna]}')
                return False
            elif self.tablero_propio[atacar_fila][atacar_columna] == 'B':
                self.tablero_propio[atacar_fila][atacar_columna] = 'F'
                self.hundidos_propio += 1
                abecedario = 'ABCDEFGHIJKLMNOPQ'
                print(f'El enemigo ha atacado la coordenada ({atacar_fila}, {abecedario[atacar_columna]})')
                return True

    def fin_juego(self):
        if self.hundidos_enemigo == parametros.NUM_BARCOS:
            self.juego_finalizado = True
            return True

        elif self.hundidos_propio == parametros.NUM_BARCOS:
            self.juego_finalizado = True
            return True

        else:
            return False

            
            
# Codigo principal
while True:
    entrada = menu.menu_principal()

    if entrada == '1':
        apodo = menu.apodo()
        if apodo == 'menu_':
            continue

        jugador = Jugador(apodo)
        tablero_sin_barcos = menu.tamaño_tablero()
        if tablero_sin_barcos == 'menu_':
            continue

        tablero_con_barcos = menu.ubicar_flota(tablero_sin_barcos)
        juego = Juego(tablero_con_barcos[0], tablero_con_barcos[1], jugador)

        ### Desde aquí se considera que estamos dentro del juego, por lo tanto utilizamos modulo batalla_naval ###

        jugando = True
        turno = 1
        while jugando:
            if turno % 2:
                entrada = bnav.menu_juego(juego)
                if entrada == 'menu_':
                    print('Icen las banderas blancas. Nos rendimos!')
                    input('Presiona Enter para continuar.')
                    print('')
                    juego.juego_finalizado = True
                    jugando = False
                    continue

                elif entrada == 'bomba!':
                    entrada = bnav.seleccionar_bomba()
                    if entrada == 'normal':
                        if not bnav.bomba(0, juego):
                            turno += 1
                        elif juego.fin_juego():
                                jugando = False
                        continue        
                    else:
                        if not bnav.bomba(parametros.RADIO_EXP, juego):
                            turno += 1
                            juego.bomba_especial = True
                        elif juego.fin_juego():
                            juego.bomba_especial = True
                            jugando = False
                        else:
                            juego.bomba_especial = True
                        continue
            
            else:
                while True:
                    print('Turno del enemigo!')
                    input('Presiona Enter para continuar.')
                    print('')
                    if juego.turno_maquina():
                        print('Oh no! Han destruido una de nuestrar embarcaciones!')
                        input('Presiona Enter para continuar.')
                        print('')
                        if juego.fin_juego():
                            jugando = False
                    else:
                        print('Hurra! el enemigo no ha acertado!')
                        input('Presiona Enter para continuar.')
                        print('')
                    turno += 1
                    break

        if juego.juego_finalizado:
            bnav.puntaje(juego)

    elif entrada == '2':
        menu.rankings()

    elif entrada == '3':
        exit()


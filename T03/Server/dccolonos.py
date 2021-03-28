import random
import os
import json
from grafo_dccolonos import Choza, Carretera
from generador_de_cartas import sacar_cartas
from ladron import ladron

path = os.path.join("parametros.json")
with open(path, "rb") as archivo:
    parametros = json.load(archivo)

class Juego:
    def __init__(self, parent, jugadores, dic_materias, dic_hexagonos):
        self.parent = parent
        self.jugadores = jugadores
        self.dic_materias_hexagonos = dic_materias
        self.dic_hexagonos_vertices = dic_hexagonos
        self.vertices = None
        self.adyacencia_nodos = None
        self.adyacencia_hexagonos = None
        self.hexagonos = None
        self.numero_materia = None
        self.aristas_ocupados = []
        self.vertices_ocupados = []
        self.adyacencia_aristas = None
        self.orden = []
        self.jugando = True
        self.carreteras_recorridas = []
        self.jugador_carretera_larga = None

    def lanzar_dados(self):
        dado_1 = random.randint(1, 6)
        dado_2 = random.randint(1, 6)
        self.parent.server.log(f"{self.orden[-1].nombre} lanzó los dados y obtuvo {dado_1 + dado_2}")
        self.otorgar_materia(dado_1 + dado_2)
        if dado_1 + dado_2 == 7:
            self.ladron()
        return dado_1, dado_2

    def empezar(self, vertices, 
        adyacencia_nodos, adyacencia_hexagonos, hexagonos, numero_materia, adyacencia_aristas):
        self.vertices = vertices
        self.adyacencia_nodos = adyacencia_nodos
        self.adyacencia_hexagonos = adyacencia_hexagonos
        self.hexagonos = hexagonos
        self.numero_materia = numero_materia
        self.adyacencia_aristas = adyacencia_aristas
        self.ubicar_fichas_aleatorias()

        for jugador in self.jugadores:
            self.orden.append(jugador)
        for numero in [2, 3, 4, 5, 6, 8, 9, 10, 11, 12]:
            self.otorgar_materia(numero)
        self.pasar_turno()

    def ubicar_fichas_aleatorias(self):
        diccionario_fichas_iniciales = dict()
        for jugador in self.jugadores:
            vertices_validos = False
            aristas_validas = False
            vertices = []
            aristas = []
            while not vertices_validos:
                continuar = False
                vertice = random.randint(0, 32)
                for vertice1 in self.vertices_ocupados:
                    if str(vertice) in self.adyacencia_nodos[str(vertice1)]:
                        continuar = True
                if continuar:
                    continue
                if vertice not in self.vertices_ocupados:
                    self.vertices_ocupados.append(vertice)
                    jugador.chozas.append(Choza(jugador.indice_choza, vertice))
                    jugador.indice_choza += 1
                    vertices.append(vertice)
                    if len(vertices) == 2:
                        vertices_validos = True
            posibles_aristas = []
            for choza in jugador.chozas:
                    for arista in self.adyacencia_aristas:
                        if str(choza.posicion) in self.adyacencia_aristas[arista]:
                            posibles_aristas.append(arista)
            while not aristas_validas:
                arista = random.randint(0, len(posibles_aristas) - 1)
                arista = posibles_aristas[arista]
                if arista not in self.aristas_ocupados:
                    aristas.append(arista)
                    self.ubicar_carretera(jugador, arista)
                    self.aristas_ocupados.append(arista)
                    if len(aristas) == 2:
                        aristas_validas = True
            diccionario_fichas_iniciales[jugador] = [vertices, aristas]
        self.ubicar_fichas_iniciales(diccionario_fichas_iniciales)

    def ubicar_fichas_iniciales(self, fichas_iniciales):
        for jugador in fichas_iniciales:
            chozas = fichas_iniciales[jugador][0]
            carreteras = fichas_iniciales[jugador][1]
            for choza in chozas:
                self.parent.enviar_chozas(choza, jugador)
            for carretera in carreteras:
                self.parent.enviar_carreteras(carretera, jugador)

    def pasar_turno(self):
        self.definir_carretera_mas_larga()
        juego_terminado, ganador = self.checkear_puntos()
        if juego_terminado:
            self.parent.server.log(f"{ganador} ha ganado la partida.")
            self.parent.server.enviar_mensaje_todos(f"juego_terminado:{ganador}")
            self.jugando = False
        if self.jugando:
            turno_jugador = self.orden.pop(0)
            self.parent.server.log(f"Turno de: {turno_jugador.nombre}")
            self.orden.append(turno_jugador)
            turno_jugador.en_turno = True
            self.parent.comenzar_turno(turno_jugador)

    def checkear_puntos(self):
        for jugador in self.jugadores:
            puntos = jugador.contar_puntos()
            self.parent.server.enviar_mensaje_todos(f"puntos:{jugador.nombre}:{puntos}")
            if puntos >= int(parametros["PUNTOS_VICTORIA_FINALES"]):
                return True, jugador.nombre
        return False, None

    def terminar_turno(self):
        jugador = self.orden[-1]
        jugador.en_turno = False
        self.pasar_turno()

    def otorgar_materia(self, numero):
        ganancia = parametros["GANANCIA_MATERIA_PRIMA"]
        for jugador in self.jugadores:
            for choza in jugador.chozas:
                choza = choza.posicion
                for hexagono in self.numero_materia:
                    if self.numero_materia[hexagono][1] == numero:
                        for vertice in self.adyacencia_hexagonos[str(hexagono)]:
                            if vertice == str(choza):
                                if self.numero_materia[hexagono][0] == 0:
                                    jugador.arcilla += ganancia
                                    self.parent.server.log(f"{jugador.nombre} recibió {ganancia} de arcilla por numero de dados")
                                    self.parent.server.enviar_mensaje_especifico(f"recibir:arcilla:{str(jugador.arcilla)}", jugador)
                                    self.parent.server.enviar_mensaje_todos(f"recibio:arcilla:{jugador.nombre}:{jugador.arcilla}")
                                elif self.numero_materia[hexagono][0] == 1:
                                    jugador.madera += ganancia
                                    self.parent.server.log(f"{jugador.nombre} recibió {ganancia} de madera por numero de dados")
                                    self.parent.server.enviar_mensaje_especifico(f"recibir:madera:{str(jugador.madera)}", jugador)
                                    self.parent.server.enviar_mensaje_todos(f"recibio:madera:{jugador.nombre}:{jugador.madera}")
                                else:
                                    jugador.trigo += ganancia
                                    self.parent.server.log(f"{jugador.nombre} recibió {ganancia} de trigo por numero de dados")
                                    self.parent.server.enviar_mensaje_especifico(f"recibir:trigo:{str(jugador.trigo)}", jugador)
                                    self.parent.server.enviar_mensaje_todos(f"recibio:trigo:{jugador.nombre}:{jugador.trigo}")
    
    def solicitar_choza(self, nombre, indice):
        jugador = self.orden[-1]
        if jugador.arcilla < parametros["CANTIDAD_ARCILLA_CHOZA"]:
            self.parent.choza_invalida(jugador)
            return
        elif jugador.madera < parametros["CANTIDAD_MADERA_CHOZA"]:
            self.parent.choza_invalida(jugador)
            return
        elif jugador.trigo < parametros["CANTIDAD_TRIGO_CHOZA"]:
            self.parent.choza_invalida(jugador)
            return
        for vertice in self.vertices_ocupados:
            if indice in self.adyacencia_nodos[str(vertice)]:
                self.parent.choza_invalida(jugador)
                return
        for carretera in jugador.carreteras:
            if indice in self.adyacencia_aristas[int(carretera.posicion)]:
                if len(carretera.chozas_adyacentes) != 0:
                    self.parent.choza_invalida(jugador)
                    return
                else:
                    jugador.arcilla -= parametros["CANTIDAD_ARCILLA_CHOZA"]
                    jugador.madera -= parametros["CANTIDAD_MADERA_CHOZA"]
                    jugador.trigo -= parametros["CANTIDAD_TRIGO_CHOZA"]
                    self.actualizar_cant_materia()
                    self.parent.enviar_chozas(int(indice), jugador)
                    self.ubicar_choza(jugador, indice)
                    return
        self.parent.choza_invalida(jugador)

    def solicitar_carretera(self, nombre, indice):
        jugador = self.orden[-1]
        if jugador.arcilla < parametros["CANTIDAD_ARCILLA_CARRETERA"]:
            self.parent.carretera_invalida(jugador)
            return
        elif jugador.madera < parametros["CANTIDAD_MADERA_CARRETERA"]:
            self.parent.carretera_invalida(jugador)
            return
        for carretera_ubicada in jugador.carreteras:
            for vertice1 in self.adyacencia_aristas[int(carretera_ubicada.posicion)]:
                for vertice2 in self.adyacencia_aristas[int(indice)]:
                    if vertice1 == vertice2:
                        jugador.arcilla -= parametros["CANTIDAD_ARCILLA_CARRETERA"]
                        jugador.madera -= parametros["CANTIDAD_MADERA_CARRETERA"]
                        self.actualizar_cant_materia()
                        self.parent.enviar_carreteras(int(indice), jugador)
                        self.ubicar_carretera(jugador, indice)
                        return
        for choza in jugador.chozas:
            if str(choza.posicion) in self.adyacencia_aristas[int(indice)]:
                jugador.arcilla -= parametros["CANTIDAD_ARCILLA_CARRETERA"]
                jugador.madera -= parametros["CANTIDAD_MADERA_CARRETERA"]
                self.actualizar_cant_materia()
                self.parent.enviar_carreteras(int(indice), jugador)
                self.ubicar_carretera(jugador, indice)
                return
        self.parent.carretera_invalida(jugador)

    def ubicar_carretera(self, jugador, posicion):
        carretera = Carretera(jugador.indice_carretera, posicion)
        jugador.indice_carretera += 1
        for choza in jugador.chozas:
            if str(choza.posicion) in self.adyacencia_aristas[int(carretera.posicion)]:
                if choza not in carretera.chozas_adyacentes:
                    carretera.chozas_adyacentes.append(choza)
                if carretera not in choza.carreteras_adyacentes:
                    choza.carreteras_adyacentes.append(carretera)
        for carretera_ubicada in jugador.carreteras:
            for vertice1 in self.adyacencia_aristas[int(carretera_ubicada.posicion)]:
                for vertice2 in self.adyacencia_aristas[int(posicion)]:
                    if vertice1 == vertice2:
                        if carretera not in carretera_ubicada.carreteras_adyacentes:
                            carretera_ubicada.carreteras_adyacentes.append(carretera)
                        if carretera_ubicada not in carretera.carreteras_adyacentes:
                            carretera.carreteras_adyacentes.append(carretera_ubicada)
        self.parent.server.log(f"{jugador.nombre} construyó una carretera en arista {posicion}.")
        jugador.carreteras.append(carretera)

    def ubicar_choza(self, jugador, indice):
        self.vertices_ocupados.append(indice)
        choza = Choza(jugador.indice_choza, indice)
        jugador.chozas.append(choza)
        self.parent.server.log(f"{jugador.nombre} construyó una choza en vertice {indice}.")
        jugador.indice_choza += 1
        for carretera in jugador.carreteras:
            if indice in self.adyacencia_aristas[int(carretera.posicion)]:
                choza.carreteras_adyacentes.append(carretera)
                carretera.chozas_adyacentes.append(choza)

    def actualizar_cant_materia(self):
        for jugador in self.orden:
            self.parent.server.enviar_mensaje_especifico(f"recibir:arcilla:{str(jugador.arcilla)}", jugador)
            self.parent.server.enviar_mensaje_todos(f"recibio:arcilla:{jugador.nombre}:{jugador.arcilla}")
            self.parent.server.enviar_mensaje_especifico(f"recibir:madera:{str(jugador.madera)}", jugador)
            self.parent.server.enviar_mensaje_todos(f"recibio:madera:{jugador.nombre}:{jugador.madera}")
            self.parent.server.enviar_mensaje_especifico(f"recibir:trigo:{str(jugador.trigo)}", jugador)
            self.parent.server.enviar_mensaje_todos(f"recibio:trigo:{jugador.nombre}:{jugador.trigo}")

    def procesar_intercambio(self, emisario, destinatario, ofrece, cant_o, pide, cant_p):
        self.parent.server.log(
            f"{emisario} solicita intercambio con {destinatario}. Ofrece {cant_o} de {ofrece} y pide {cant_p} de {pide}")
        jugador_ofrece = self.orden[-1]
        for jugador in self.jugadores:
            if jugador.nombre == destinatario:
                jugador_dest = jugador
        if ofrece == "Arcilla":
            if jugador_ofrece.arcilla < cant_o:
                self.parent.server.enviar_mensaje_especifico("transacc_inv:None", jugador_ofrece)
                return
        elif ofrece == "Madera":
            if jugador_ofrece.madera < cant_o:
                self.parent.server.enviar_mensaje_especifico("transacc_inv:None", jugador_ofrece)
                return
        elif ofrece == "Trigo":
            if jugador_ofrece.trigo < cant_o:
                self.parent.server.enviar_mensaje_especifico("transacc_inv:None", jugador_ofrece)
                return
        if pide == "Arcilla":
            if jugador_dest.arcilla < cant_p:
                self.parent.server.enviar_mensaje_especifico("transacc_inv:None", jugador_ofrece)
                return
        elif pide == "Madera":
            if jugador_dest.madera < cant_p:
                self.parent.server.enviar_mensaje_especifico("transacc_inv:None", jugador_ofrece)
                return
        elif pide == "Trigo":
            if jugador_dest.trigo < cant_p:
                self.parent.server.enviar_mensaje_especifico("transacc_inv:None", jugador_ofrece)
                return
        self.parent.server.enviar_mensaje_especifico(f"sol_aprov_int:{emisario}:{ofrece}:{cant_o}:{pide}:{cant_p}", jugador_dest)

    def realizar_intercambio(self, emisario, destinatario, ofrece, cant_o, pide, cant_p):
        jugador_ofrece = self.orden[-1]
        for jugador in self.jugadores:
            if jugador.nombre == destinatario:
                jugador_dest = jugador
        if ofrece == "Arcilla":
            jugador_dest.arcilla += cant_o
            jugador_ofrece.arcilla -= cant_o
        elif ofrece == "Madera":
            jugador_dest.madera += cant_o
            jugador_ofrece.madera -= cant_o
        elif ofrece == "Trigo":
            jugador_dest.trigo += cant_o
            jugador_ofrece.trigo -= cant_o
        if pide == "Arcilla":
            jugador_ofrece.arcilla += cant_p
            jugador_dest.arcilla -= cant_p
        elif pide == "Madera":
            jugador_ofrece.madera += cant_p
            jugador_dest.madera -= cant_p
        elif pide == "Trigo":
            jugador_ofrece.trigo += cant_p
            jugador_dest.trigo -= cant_p
        self.parent.server.log(f"{jugador_ofrece.nombre} recibió {cant_p} de {pide} por intercambio")
        self.parent.server.log(f"{destinatario} recibió {cant_o} de {ofrece} por intercambio")
        self.actualizar_cant_materia()
        self.parent.server.enviar_mensaje_todos(f"interc_realiz:{emisario}:{destinatario}:{ofrece}:{cant_o}:{pide}:{cant_p}")

    def definir_carretera_mas_larga(self):
        jugador_mas_larga = None
        largo_mas_largo = 0
        for jugador in self.jugadores:
            mas_larga = 0
            for carretera in jugador.carreteras:
                self.carreteras_recorridas = []
                largo = self.recorrer_camino(carretera, 0, 1)
                if largo > mas_larga:
                    mas_larga = largo
            if mas_larga > largo_mas_largo:
                largo_mas_largo = mas_larga
                jugador_mas_larga = jugador
        for jugador in self.jugadores:
            jugador.puntos_carretera_larga = 0
        jugador_mas_larga.puntos_carretera_larga += 2
        if jugador_mas_larga != self.jugador_carretera_larga:
            self.parent.server.log(f"{jugador_mas_larga.nombre} tiene la carretera más larga de largo {largo_mas_largo}.")
            self.jugador_carretera_larga = jugador_mas_larga
        jugador = jugador_mas_larga.nombre
        self.parent.server.enviar_mensaje_todos(f"carretera_larga:{jugador}:{largo_mas_largo}")

    def recorrer_camino(self, carretera, largo, mayor_largo):
        if carretera in self.carreteras_recorridas:
            return mayor_largo
        self.carreteras_recorridas.append(carretera)
        largo += 1
        if len(carretera.carreteras_adyacentes) == 1:
            if largo > mayor_largo:
                mayor_largo = largo
            return mayor_largo
        for carretera_adyacente in carretera.carreteras_adyacentes:
            if carretera_adyacente in self.carreteras_recorridas:
                continue
            mayor_largo = self.recorrer_camino(carretera_adyacente, largo, mayor_largo)
        return mayor_largo

    def carta_desarrollo(self):
        jugador = self.orden[-1]
        if jugador.arcilla < parametros["CANTIDAD_ARCILLA_CARTA_DESARROLLO"]:
            self.parent.server.enviar_mensaje_especifico("carta_des_inv:None", jugador)
            return
        elif jugador.madera < parametros["CANTIDAD_MADERA_CARTA_DESARROLLO"]:
            self.parent.server.enviar_mensaje_especifico("carta_des_inv:None", jugador)
            return
        elif jugador.trigo < parametros["CANTIDAD_TRIGO_CARTA_DESARROLLO"]:
            self.parent.server.enviar_mensaje_especifico("carta_des_inv:None", jugador)
            return
        jugador.arcilla -= parametros["CANTIDAD_ARCILLA_CARTA_DESARROLLO"]
        jugador.madera -= parametros["CANTIDAD_MADERA_CARTA_DESARROLLO"]
        jugador.trigo -= parametros["CANTIDAD_TRIGO_CARTA_DESARROLLO"]
        carta = sacar_cartas(1)[0][0]
        if carta == "victoria":
            jugador.cartas_puntos_victoria += 1
            self.parent.server.enviar_mensaje_especifico("victoria:None", jugador)
        elif carta == "monopolio":
            self.parent.server.enviar_mensaje_especifico("monopolio:None", jugador)
        self.actualizar_cant_materia()

    def monopolio(self, materia):
        beneficiado = self.orden[-1]
        cantidad = 0
        for jugador in self.jugadores:
            if materia == "Madera":
                cantidad += jugador.madera
                jugador.madera = 0
        for jugador in self.jugadores:
            if materia == "Arcilla":
                cantidad += jugador.arcilla
                jugador.arcilla = 0
        for jugador in self.jugadores:
            if materia == "Trigo":
                cantidad += jugador.trigo
                jugador.trigo = 0
        if materia == "Arcilla":
            beneficiado.arcilla = cantidad
        if materia == "Madera":
            beneficiado.madera = cantidad
        if materia == "Trigo":
            beneficiado.trigo = cantidad
        self.parent.server.log(f"{beneficiado.nombre} recibió {cantidad} de {materia} por monopolio")
        self.actualizar_cant_materia()
    
    def ladron(self):
        ladron(self)
        self.actualizar_cant_materia()


            



            
from generador_grilla import GeneradorGrillaHexagonal
from elementos_mapa import Vertice
import os
import json
import random
from dccolonos import Juego

path = os.path.join("grafo.json")
with open(path, "rb") as archivo:
    grafo = json.load(archivo)
class Logica:
    def __init__(self, parent):
        self.server = parent
        self.generador_grilla = GeneradorGrillaHexagonal(80)
        self.vertices = dict()
        self.aristas = dict()
        self.adyacencia_nodos = grafo["nodos"]
        self.adyacencia_hexagonos = grafo["hexagonos"]
        self.hexagonos = dict()
        self.juego = None
        self.numero_materia = dict()
        self.adyacencia_aristas = dict()

    def crear_grilla(self):
        diccionario_vertices = self.generador_grilla.generar_grilla([5, 2], 60, 30)
        vertices_enviar = {}
        for vertice in diccionario_vertices:
            pos_x = diccionario_vertices[vertice][0]
            pos_y = diccionario_vertices[vertice][1]
            self.vertices[vertice] = Vertice(pos_x, pos_y, vertice)
            vertices_enviar[vertice] = [pos_x, pos_y]
        return vertices_enviar

    def establecer_hexagonos(self):
        for i in range(10):
            valido = False
            while not valido:
                materia = random.randint(0, 2)
                self.hexagonos[i] = materia
                contador_madera = 0
                contador_arcilla = 0
                contador_trigo = 0
                for hexagono in self.hexagonos:
                    if self.hexagonos[hexagono] == 0:
                        contador_arcilla += 1
                    elif self.hexagonos[hexagono] == 1:
                        contador_madera += 1
                    else:
                        contador_trigo += 1
                if contador_trigo > 4 or contador_arcilla > 4 or contador_madera > 4:
                    pass
                else:
                    valido = True

        return self.hexagonos

    def procesar_mensaje(self, mensaje):
        contador = 0
        for caracter in mensaje:
            if caracter == ":":
                break
            contador += 1
        clave = mensaje[: contador]
        mensaje = mensaje[contador + 1:]
        
        return self.manejar_mensaje(clave, mensaje)

    def manejar_mensaje(self, clave, mensaje):
        if clave == "lanzar_dados":
            self.server.enviar_resultados_dados(self.juego.lanzar_dados())
        elif clave == "terminar_turno":
            self.juego.terminar_turno()
        elif clave == "solicitar_choza":
            nombre, indice = self.procesar_mensaje_largo(mensaje)
            self.juego.solicitar_choza(nombre, indice)
        elif clave == "solicitar_carretera":
            nombre, indice = self.procesar_mensaje_largo(mensaje)
            self.juego.solicitar_carretera(nombre, indice)
        elif clave == "sol_interc":
            self.procesar_intercambio(mensaje)
        elif clave == "real_interc":
            self.realizar_intercambio(mensaje)
        elif clave == "rechaz_interc":
            self.rechazar_intercambio(mensaje)
        elif clave == "carta_desarrollo":
            self.juego.carta_desarrollo()
        elif clave == "monopolio":
            self.juego.monopolio(mensaje)
            

    def instanciar_juego(self, lista_jugadores):
        self.juego = Juego(self, lista_jugadores, self.hexagonos, grafo["hexagonos"])

    def enviar_adyacencia(self):
        adyacencia = self.adyacencia_nodos
        aristas_listas = []
        contador = 0
        aristas = dict()
        for vertice_1 in adyacencia:
            for vertice_2 in adyacencia[vertice_1]:
                if [vertice_2, vertice_1] not in aristas_listas:
                    self.adyacencia_aristas[contador] = [vertice_1, vertice_2]
                    pos_x = (self.vertices[vertice_1].pos_x + self.vertices[vertice_2].pos_x)/2
                    pos_y = (self.vertices[vertice_1].pos_y + self.vertices[vertice_2].pos_y)/2
                    aristas_listas.append([vertice_1, vertice_2])
                    aristas[contador] = [pos_x, pos_y]
                    contador += 1
        self.server.enviar_python_todos(aristas, "adyacencia")

    def definir_numeros_hexagonos(self):
        hexagonos = dict()
        for hexagono in self.hexagonos:
            numero = 7
            while numero == 7:
                numero = random.randint(2, 12)
            materia = self.hexagonos[hexagono]
            hexagonos[hexagono] = [materia, numero]
        self.numero_materia = hexagonos
        self.server.enviar_python_todos(hexagonos, "numeros_hexagonos")

    def empezar_juego(self):
        self.juego.empezar(self.vertices, self.adyacencia_nodos,
            self.adyacencia_hexagonos, self.hexagonos, self.numero_materia, self.adyacencia_aristas)

    def enviar_chozas(self, choza, jugador):
        if choza < 10:
            choza = f"0{choza}"
        self.server.enviar_mensaje_especifico(f"choza_propia:{str(choza)}", jugador)
        self.server.enviar_mensaje_todos(f"choza:{str(choza)},{jugador.color}")

    def enviar_carreteras(self, carretera, jugador):
        if carretera < 10:
            carretera = f"0{carretera}"
        self.server.enviar_mensaje_especifico(f"carretera_propia:{str(carretera)}", jugador)
        self.server.enviar_mensaje_todos(f"carretera:{str(carretera)},{jugador.color}")

    def comenzar_turno(self, jugador):
        self.server.enviar_mensaje_especifico("empezar_turno:None", jugador)
        self.server.enviar_mensaje_todos(f"turno_de:{jugador.nombre}")

    def procesar_mensaje_largo(self, mensaje):
        contador = 0
        for caracter in mensaje:
            if caracter == ":":
                break
            contador += 1
        primera_parte = mensaje[: contador]
        segunda_parte = mensaje[contador + 1:]
        return primera_parte, segunda_parte

    def choza_invalida(self, jugador):
        self.server.enviar_mensaje_especifico("choza_invalida:None", jugador)

    def carretera_invalida(self, jugador):
        self.server.enviar_mensaje_especifico("carretera_invalida:None", jugador)

    def procesar_intercambio(self, mensaje):
        emisario, mensaje = self.procesar_mensaje_largo(mensaje)
        destinatario, mensaje = self.procesar_mensaje_largo(mensaje)
        ofrece, mensaje = self.procesar_mensaje_largo(mensaje)
        cant_o, mensaje = self.procesar_mensaje_largo(mensaje)
        pide, cant_p = self.procesar_mensaje_largo(mensaje)
        self.juego.procesar_intercambio(
            emisario, destinatario, ofrece, int(cant_o), pide, int(cant_p)
        )

    def realizar_intercambio(self, mensaje):
        emisario, mensaje = self.procesar_mensaje_largo(mensaje)
        destinatario, mensaje = self.procesar_mensaje_largo(mensaje)
        ofrece, mensaje = self.procesar_mensaje_largo(mensaje)
        cant_o, mensaje = self.procesar_mensaje_largo(mensaje)
        pide, cant_p = self.procesar_mensaje_largo(mensaje)
        self.server.log(
            f"{destinatario} acepta intercambio con {emisario}. Recibirá {cant_o} de {ofrece} y dará {cant_p} de {pide}")
        self.juego.realizar_intercambio(
            emisario, destinatario, ofrece, int(cant_o), pide, int(cant_p)
        )

    def rechazar_intercambio(self, mensaje):
        ofrece, rechaza = self.procesar_mensaje_largo(mensaje)
        for jugador in self.juego.jugadores:
            if jugador.nombre == ofrece:
                self.server.enviar_mensaje_especifico(f"intercambio_rechazado:{rechaza}", jugador)
        


        




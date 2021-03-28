import socket
import threading
from jugadores import Jugadores
import random
import os
import json
from logica_server import Logica
import pickle
from dccolonos import Juego

path = os.path.join("parametros.json")
with open(path, "rb") as archivo:
    parametros = json.load(archivo)

class Servidor:

    escuchar_lock = threading.Lock()
    enviar_lock = threading.Lock()

    def __init__(self, host, port, log_activado=True):
        self.host = host
        self.port = port
        self.log_activado = log_activado
        self.lista_jugadores = []
        self.lista_threads_escuchando = []
        self.nombres = []
        self.logica = Logica(self)
        self.indice = 1
        self.colores_disponibles = ["rojo", "verde", "azul", "rosado"]
        self.colores = dict()

        self.log("Inicializando servidor...")

        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.socket_server.bind((self.host, self.port))

        self.socket_server.listen()
        self.log(f"Servidor escuchando en {self.host}:{self.port}")
        self.log("Servidor aceptando conexiones")

        thread = threading.Thread(target=self.aceptar_clientes, daemon=True)
        thread.start()

    def aceptar_clientes(self):
        while True:
            try:
                socket_jugador, address = self.socket_server.accept()
                while True:
                    indice = random.randint(0, 6)
                    nombre = parametros["nombres"][indice]
                    if nombre not in self.nombres:
                        self.nombres.append(nombre)
                        break
                jugador = Jugadores(socket_jugador, address, nombre, self.indice)
                self.indice += 1
                self.log(f"Cliente indice {jugador.indice} intentando entrar")
                if len(self.lista_jugadores) >= parametros["MAX_JUGADORES"]:
                    self.enviar_mensaje_especifico("Critico:maximo_excedido", jugador)
                    self.log("CLIENTE RECHAZADO")
                    self.eliminar_cliente(jugador)
                    self.nombres.remove(jugador.nombre)
                else:
                    self.lista_jugadores.append(jugador)
                    thread_escuchar = threading.Thread(target=self.escuchar_cliente, args=(jugador,), daemon=True)
                    self.lista_threads_escuchando.append(thread_escuchar)
                    thread_escuchar.start()
                    self.log("CLIENTE ACEPTADO")
                    jugador.color = self.colores_disponibles.pop()
                    self.colores[jugador.nombre] = jugador.color
                    self.log(f"Conexión establecida con cliente {jugador}")
                    self.iniciar_cliente(jugador)
                    if len(self.lista_jugadores) >= parametros["MAX_JUGADORES"]:
                        self.comenzar_partida()
                        self.log("Hay suficientes jugadores, comenzando partida.")
            except ConnectionError:
                self.log("[SERVER] Ocurrió un error")

    def log(self, mensaje):
        print(f"LOG: {mensaje}")

    def iniciar_cliente(self, jugador):
        self.enviar_mensaje_especifico(f"Nombre:{jugador.nombre}", jugador)
        max_jugadores = str(parametros["MAX_JUGADORES"])
        self.enviar_mensaje_especifico(f"Cantidad:{max_jugadores}", jugador)
        if len(self.lista_jugadores) > 1:
            for otro_jugador in self.lista_jugadores:
                if otro_jugador.nombre != jugador.nombre:
                    self.enviar_mensaje_especifico(f"Actualizar_VI:{otro_jugador.nombre}", jugador)
                    self.enviar_mensaje_especifico(f"Actualizar_VI:{jugador.nombre}", otro_jugador)
        
    def escuchar_cliente(self, jugador):
        try:
            while True:
                largo_mensaje = jugador.socket.recv(4)
                self.escuchar_lock.acquire()
                if largo_mensaje == b'':
                    break
                else:
                    mensaje = self.recibir(jugador, largo_mensaje)
                    self.escuchar_lock.release()
                    self.logica.procesar_mensaje(mensaje)
        except ConnectionResetError:
            self.log(f"Error: conexión con {jugador} fue reseteada.")

        self.log(f"Cerrando conexión con {jugador}.")
        self.eliminar_cliente(jugador)

    def recibir(self, jugador, largo_mensaje):
        socket_cliente = jugador.socket
        largo_mensaje = int.from_bytes(largo_mensaje, byteorder="big")
        mensaje = bytearray()

        while len(mensaje) <= largo_mensaje:
            indice_mensaje = socket_cliente.recv(4)
            #print(int.from_bytes(indice_mensaje, byteorder="little"))
            mensaje.extend(socket_cliente.recv(60))

        mensaje = mensaje[:largo_mensaje]
        mensaje = mensaje.decode(encoding="utf-8")
        self.log(f"Mensaje de largo {largo_mensaje} recibido de {jugador.nombre}: {mensaje}")
        return mensaje

    def eliminar_cliente(self, jugador):
        if jugador in self.lista_jugadores:
            self.lista_jugadores.remove(jugador)
            self.nombres.remove(jugador.nombre)
            self.colores_disponibles.append(jugador.color)
            del self.colores[jugador.nombre]
            self.enviar_mensaje_todos(f"Eliminar_jugador:{jugador.nombre}")

    def enviar_mensaje_todos(self, mensaje):
        self.enviar_lock.acquire()
        mensaje_bytes = mensaje.encode(encoding="utf-8")
        largo = len(mensaje_bytes).to_bytes(4, byteorder="big")
        self.log(f"Enviando mensaje a todos los jugadores, contenido: \"{mensaje}\", largo: {len(mensaje_bytes)}")
        for jugador in self.lista_jugadores:
            jugador.socket.send(largo)
            contador = 1
            while len(mensaje_bytes) >= 60:
                jugador.socket.send(contador.to_bytes(4, byteorder="little"))
                jugador.socket.send(mensaje_bytes[:60])
                mensaje_bytes = mensaje_bytes[60:]
                contador += 1
            if len(mensaje_bytes) < 60:
                jugador.socket.send(contador.to_bytes(4, byteorder="little"))
                nuevo_mensaje = mensaje_bytes
                while len(nuevo_mensaje) < 60:
                    nuevo_mensaje += b'\x00'
                jugador.socket.send(nuevo_mensaje)
        self.enviar_lock.release()

    def enviar_mensaje_especifico(self, mensaje, destinatario):
        self.enviar_lock.acquire()
        mensaje_bytes = mensaje.encode(encoding="utf-8")
        largo = len(mensaje_bytes).to_bytes(4, byteorder="big")
        self.log(f"Enviando mensaje a {destinatario.nombre}, contenido: \"{mensaje}\", largo: {len(mensaje_bytes)}")
        destinatario.socket.send(largo)
        contador = 0
        while len(mensaje_bytes) >= 60:
            destinatario.socket.send(contador.to_bytes(4, byteorder="little"))
            destinatario.socket.send(mensaje_bytes[:60])
            mensaje_bytes = mensaje_bytes[60:]
            contador += 1
        if len(mensaje_bytes) < 60:
            destinatario.socket.send(contador.to_bytes(4, byteorder="little"))
            nuevo_mensaje = mensaje_bytes
            while len(nuevo_mensaje) < 60:
                nuevo_mensaje += b'\x00'
            destinatario.socket.send(nuevo_mensaje)
        self.enviar_lock.release()

    def comenzar_partida(self):
        nombres = ""
        for nombre in self.nombres:
            nombres += f"{nombre},"
        nombres = nombres[:-1]
        self.enviar_mensaje_todos(f"Comenzar:{nombres}")
        vertices = self.logica.crear_grilla()
        self.enviar_python_todos(vertices, "vertices")
        self.enviar_python_todos(self.logica.establecer_hexagonos(), "hexagonos")
        self.logica.instanciar_juego(self.lista_jugadores)
        self.enviar_python_todos(self.colores, "colores")
        self.logica.enviar_adyacencia()
        self.logica.definir_numeros_hexagonos()

        self.log("Elementos del tablero listos.")

        self.logica.empezar_juego()

    def enviar_python_todos(self, diccionario, mensaje):
        mensaje_bytes = pickle.dumps(diccionario)
        self.enviar_mensaje_todos(mensaje + ":None")
        self.enviar_lock.acquire()
        largo = len(mensaje_bytes).to_bytes(4, byteorder="big")
        self.log(f"Enviando pickle a todos los jugadores largo: {len(mensaje_bytes)}")
        for jugador in self.lista_jugadores:
            mensaje_bytes = pickle.dumps(diccionario)
            jugador.socket.send(largo)
            contador = 0
            while len(mensaje_bytes) >= 60:
                jugador.socket.send(contador.to_bytes(4, byteorder="little"))
                jugador.socket.send(mensaje_bytes[:60])
                mensaje_bytes = mensaje_bytes[60:]
                contador += 1
            if len(mensaje_bytes) < 60:
                jugador.socket.send(contador.to_bytes(4, byteorder="little"))
                nuevo_mensaje = mensaje_bytes
                while len(nuevo_mensaje) < 60:
                    nuevo_mensaje += b'\x00'
                jugador.socket.send(nuevo_mensaje)
        self.enviar_lock.release()

    def enviar_resultados_dados(self, dados):
        self.enviar_mensaje_todos(f"dados:{dados[0]}{dados[1]}")



    


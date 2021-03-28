import socket
import threading
from BackEnd.logica import LogicaCliente
from PyQt5.QtWidgets import QApplication
import sys
import pickle


class Cliente:

    escuchar_lock = threading.Lock()
    enviar_lock = threading.Lock()

    def __init__(self, port, host):
        print("Inicializando cliente...")
        self.host = host
        self.port = port
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conectado = False
        self.nombre = None
        self.logica = LogicaCliente(self)
        self.recibido = None

    def start(self):
        try:
            self.socket_cliente.connect((self.host, self.port))
            self.conectado = True
            self.thread_escuchar = threading.Thread(
                target=self.escuchar_servidor,
                daemon=True
            )
            self.thread_escuchar.start()
        except ConnectionRefusedError:
            self.log("No se pudo conectar al server :(")
            self.socket_cliente.close()
        
        self.enviar_mensaje("MENSAJE DE PRUEBA INICIO CONEXIÓN")

    def escuchar_servidor(self):
        while True:
            largo_mensaje = self.socket_cliente.recv(4)
            self.escuchar_lock.acquire()
            self.leer_mensaje(largo_mensaje)

    def leer_mensaje(self, largo_mensaje):
        largo_mensaje = int.from_bytes(largo_mensaje, byteorder="big")
        mensaje = bytearray()

        while len(mensaje) <= largo_mensaje:
            indice_mensaje = self.socket_cliente.recv(4)
            #print(int.from_bytes(indice_mensaje, byteorder="little"))
            mensaje.extend(self.socket_cliente.recv(60))
        self.escuchar_lock.release()

        mensaje = mensaje[:largo_mensaje]
        mensaje = mensaje.decode(encoding="utf-8")
        self.log(f"Mensaje recibido de server: {mensaje}")
        self.accion(self.logica.procesar_mensaje(mensaje))

    def enviar_mensaje(self, mensaje):
        self.enviar_lock.acquire()
        mensaje_bytes = mensaje.encode(encoding="utf-8")
        largo = len(mensaje_bytes).to_bytes(4, byteorder="big")
        self.socket_cliente.send(largo)
        contador = 1
        while len(mensaje_bytes) >= 60:
            self.socket_cliente.send(contador.to_bytes(4, byteorder="little"))
            self.socket_cliente.send(mensaje_bytes[:60])
            mensaje_bytes = mensaje_bytes[60:]
            contador += 1
        if len(mensaje_bytes) < 60:
            self.socket_cliente.send(contador.to_bytes(4, byteorder="little"))
            nuevo_mensaje = mensaje_bytes
            while len(nuevo_mensaje) < 60:
                nuevo_mensaje += b'\x00'
            self.socket_cliente.send(nuevo_mensaje)
        self.enviar_lock.release()

    def log(self, mensaje):
        print(f"LOG: {mensaje}")

    def accion(self, accion):
        self.log(accion)
        if accion[:-2] == "recibir_pickle":
            if accion[-2:] == "_v":
                self.logica.enviar_vertices(self.recibir_pickle())
            elif accion[-2:] == "_h":
                self.logica.enviar_hexagonos(self.recibir_pickle())
            elif accion[-2:] == "_c":
                self.logica.enviar_colores(self.recibir_pickle())
            elif accion[-2:] == "_a":
                self.logica.enviar_adyacencia(self.recibir_pickle())
            elif accion[-2:] == "_n":
                self.logica.enviar_numero_hex(self.recibir_pickle())
        else:
            pass

    def recibir_pickle(self):
        self.escuchar_lock.acquire()
        largo_mensaje = self.socket_cliente.recv(4)
        largo_mensaje = int.from_bytes(largo_mensaje, byteorder="big")
        mensaje = bytearray()

        while len(mensaje) <= largo_mensaje:
            indice_mensaje = self.socket_cliente.recv(4)
            #print(int.from_bytes(indice_mensaje, byteorder="little"))
            mensaje.extend(self.socket_cliente.recv(60))

        mensaje = mensaje[:largo_mensaje]
        
        self.recibido = pickle.loads(mensaje)
        self.escuchar_lock.release()
        return self.recibido
        























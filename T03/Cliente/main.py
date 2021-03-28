import socket
from FrontEnd import ventana_espera
from BackEnd.cliente import Cliente
import json
from PyQt5.QtWidgets import QApplication
import sys
import os
from FrontEnd.interfaz import Interfaz
from PyQt5.QtCore import pyqtSignal

path = os.path.join("parametros.json")
with open(path, "rb") as archivo:
    parametros = json.load(archivo)

app = QApplication([])

port = parametros["port"]
host = parametros["host"]
cliente = Cliente(port, host)
interfaz = Interfaz()

def imprimir_hola(numerito):
    print("holaaaaa")
    print(numerito)

#Conectar Señales
cliente.logica.enviar_cantidad_jugadores.connect(interfaz.actualizar_cantidad_jugadores)
cliente.logica.actualizar_nombres_sala_espera.connect(interfaz.actualizar_ventana_inicio)
cliente.logica.comenzar_partida.connect(interfaz.comenzar_partida)
cliente.logica.senal_enviar_vertices.connect(interfaz.recibir_vertices)
cliente.logica.senal_enviar_hexagonos.connect(interfaz.recibir_hexagonos)
interfaz.senal_lanzar_dados.connect(cliente.logica.lanzar_dados)
cliente.logica.senal_enviar_dados.connect(interfaz.recibir_dados)
cliente.logica.senal_enviar_colores.connect(interfaz.recibir_colores)
cliente.logica.senal_enviar_adyacencia.connect(interfaz.recibir_adyacencia)
cliente.logica.senal_enviar_numeros_hex.connect(interfaz.recibir_numeros_hex)
cliente.logica.senal_ubicar_choza_ajena.connect(interfaz.ubicar_choza_ajena)
cliente.logica.senal_ubicar_choza_propia.connect(interfaz.ubicar_choza_propia)
cliente.logica.senal_ubicar_carretera_ajena.connect(interfaz.ubicar_carretera_ajena)
cliente.logica.senal_ubicar_carretera_propia.connect(interfaz.ubicar_carretera_propia)
cliente.logica.senal_comenzar_turno.connect(interfaz.comenzar_turno)
interfaz.senal_terminar_turno.connect(cliente.logica.terminar_turno)
cliente.logica.senal_enviar_turno.connect(interfaz.recibir_turno)
cliente.logica.senal_recibir_materia.connect(interfaz.recibir_materia)
cliente.logica.senal_recibio_materia.connect(interfaz.contrincante_recibe)
interfaz.senal_solicitar_carretera.connect(cliente.logica.solicitar_carretera)
interfaz.senal_solicitar_choza.connect(cliente.logica.solicitar_choza)
cliente.logica.senal_choza_invalida.connect(interfaz.choza_invalida)
cliente.logica.senal_carretera_invalida.connect(interfaz.carretera_invalida)
interfaz.senal_solicitar_intercambio.connect(cliente.logica.solicitar_intercambio)
cliente.logica.senal_transacc_inv.connect(interfaz.transacc_inv)
cliente.logica.senal_solicit_aprov_interc.connect(interfaz.solicit_aprov_interc)
interfaz.senal_realizar_intercambio.connect(cliente.logica.realizar_intercambio)
interfaz.senal_rechazar_intercambio.connect(cliente.logica.rechazar_intercambio)
cliente.logica.senal_intercambio_rechazado.connect(interfaz.intercambio_rechazado)
cliente.logica.senal_intercambio_realizado.connect(interfaz.intercambio_realizado)
cliente.logica.senal_juego_terminado.connect(interfaz.juego_terminado)
cliente.logica.senal_enviar_puntos.connect(interfaz.recibir_puntos)
cliente.logica.senal_enviar_carretera_larga.connect(interfaz.recibir_carretera_larga)
interfaz.senal_pedir_cart_des.connect(cliente.logica.pedir_carta_desarrollo)
cliente.logica.senal_carta_monopolio.connect(interfaz.carta_monopolio)
cliente.logica.senal_carta_victoria.connect(interfaz.carta_victoria)
interfaz.senal_monopolio.connect(cliente.logica.monopolio)
cliente.logica.senal_carta_desarrollo_invalida.connect(interfaz.carta_desarrollo_invalida)


cliente.start()


sys.exit(app.exec_())
























from FrontEnd.ventana_espera import VentanaInicio
from FrontEnd.ventana_juego import VentanaJuego
from PyQt5.QtCore import pyqtSignal, QObject
from FrontEnd.vertices_aristas import Arista
import os
import json
from FrontEnd.ventana_intercambio import VentanaIntercambio, VentanaSolicitudIntercambio

path = os.path.join("parametros.json")
with open(path, "rb") as archivo:
    parametros = json.load(archivo)

class Interfaz(QObject):

    senal_lanzar_dados = pyqtSignal()
    senal_actualizar_cantidad = pyqtSignal(int)
    senal_terminar_turno = pyqtSignal()
    senal_solicitar_choza = pyqtSignal(str, str)
    senal_solicitar_carretera = pyqtSignal(str, str)
    senal_solicitar_intercambio = pyqtSignal(str, str, str, str, str, str)
    senal_realizar_intercambio = pyqtSignal(str, str, str, str, str, str)
    senal_rechazar_intercambio = pyqtSignal(str, str)
    senal_pedir_cart_des = pyqtSignal()
    senal_monopolio = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.ventana_inicio = VentanaInicio()
        self.ventana_juego = VentanaJuego(self)
        self.nombre_cliente = ""
        self.ventana_intercambio = VentanaIntercambio(self)
        self.ventana_solicitud = VentanaSolicitudIntercambio(self)
        self.vertices = dict()
        self.pide = ""
        self.ofrece = ""
        self.cant_o = ""
        self.cant_p = ""
        self.pide_interc = ""

        self.mostrar_inicio()

        self.senal_actualizar_cantidad.connect(self.actualizar_cantidad_jugadores)

    def mostrar_inicio(self):
        self.ventana_inicio.show()

    def actualizar_ventana_inicio(self, nombre, mensaje):
        if mensaje == "es_cliente":
            self.nombre_cliente = nombre
            self.ventana_inicio.actualizar(nombre, True)
            self.ventana_juego.nombre_cliente = nombre
        elif mensaje == "no_cliente":
            self.ventana_inicio.actualizar(nombre, False)
        elif mensaje == "eliminar":
            self.ventana_inicio.eliminar_nombre(nombre)

    def actualizar_cantidad_jugadores(self, cantidad):
        self.ventana_inicio.mostrar_labels(cantidad)

    def comenzar_partida(self, lista_nombres):
        self.ventana_inicio.hide()
        self.ventana_juego.definir_jugadores(lista_nombres)
        self.ventana_juego.show()

    def recibir_vertices(self, vertices):
        self.vertices = vertices
        self.ventana_juego.recibir_vertices(vertices)

    def recibir_hexagonos(self, hexagonos):
        self.ventana_juego.recibir_hexagonos(hexagonos)

    def lanzar_dados(self):
        self.ventana_juego.boton_lanzar.setEnabled(False)
        self.senal_lanzar_dados.emit()

    def recibir_dados(self, dado_1, dado_2):
        self.ventana_juego.definir_dados(dado_1, dado_2)
        self.ventana_juego.boton_terminar_turno.setEnabled(True)
        self.ventana_juego.boton_intercambiar.setEnabled(True)
        self.ventana_juego.en_turno = True

    def recibir_colores(self, colores):
        for nombre in colores:
            if nombre == self.nombre_cliente:
                self.ventana_juego.definir_color_construcciones(colores[nombre])
                
            if colores[nombre] == "rojo":
                colores[nombre] = "red"
            elif colores[nombre] == "verde":
                colores[nombre] = "lightgreen"
            elif colores[nombre] == "azul":
                colores[nombre] = "blue"
            else:
                colores[nombre] = "#E5097F"
            self.ventana_juego.definir_colores(colores)

    def recibir_adyacencia(self, aristas):
        for arista in aristas:
            self.ventana_juego.aristas[arista] = Arista(
                self.ventana_juego, arista, aristas[arista][0], aristas[arista][1])
            if not self.ventana_juego.prueba:
                self.ventana_juego.aristas[arista].hide()

    def recibir_numeros_hex(self, hexagonos):
        self.ventana_juego.definir_numeros_hex(hexagonos)

    def ubicar_choza_ajena(self, choza, color):
        if color == "rosado":
            color = "violeta"
        path = os.path.join(*parametros[f"path_{color}"][3])
        self.ventana_juego.ubicar_choza(path, choza)

    def ubicar_carretera_ajena(self, carretera, color, angulo):
        if color == "rosado":
            color = "violeta"
        path = os.path.join(*parametros[f"path_{color}"][int(angulo)])
        self.ventana_juego.ubicar_carretera(path, carretera)

    def ubicar_choza_propia(self, choza):
        color = self.ventana_juego.color
        if color == "rosado":
            color = "violeta"
        path = os.path.join(*parametros[f"path_{color}"][3])
        self.ventana_juego.ubicar_choza(path, choza)

    def ubicar_carretera_propia(self, carretera, angulo):
        color = self.ventana_juego.color
        if color == "rosado":
            color = "violeta"
        path = os.path.join(*parametros[f"path_{color}"][int(angulo)])
        self.ventana_juego.ubicar_carretera(path, carretera)

    def comenzar_turno(self):
        self.ventana_juego.boton_lanzar.setEnabled(True)
        self.ventana_juego.label_turno.show()

    def terminar_turno(self):
        self.ventana_juego.boton_intercambiar.setEnabled(False)
        self.ventana_juego.boton_lanzar.setEnabled(False)
        self.ventana_juego.boton_terminar_turno.setEnabled(False)
        self.ventana_juego.label_turno.hide()
        self.senal_terminar_turno.emit()
        self.ventana_juego.en_turno = False
        self.ventana_juego.clickeado = None
        self.ventana_juego.carretera.setStyleSheet("background-color: lightgrey")
        self.ventana_juego.choza.setStyleSheet("background-color: lightgrey")

    def recibir_turno(self, nombre):
        self.ventana_juego.editable_nombre_turno.setText(nombre)

    def recibir_materia(self, materia, cantidad):
        if materia == "arcilla":
            self.ventana_juego.editable_arcilla.setText(str(cantidad))
        elif materia == "madera":
            self.ventana_juego.editable_madera.setText(str(cantidad))
        elif materia == "trigo":
            self.ventana_juego.editable_trigo.setText(str(cantidad))

    def contrincante_recibe(self, materia, cantidad, nombre):
        if nombre == self.nombre_cliente:
            return
        if self.ventana_juego.editable_contrincante_1.text() == nombre:
            if materia == "arcilla":
                self.ventana_juego.editable_arcilla_1.setText(str(cantidad))
            elif materia == "madera":
                self.ventana_juego.editable_madera_1.setText(str(cantidad))
            if materia == "trigo":
                self.ventana_juego.editable_trigo_1.setText(str(cantidad))
        elif self.ventana_juego.editable_contrincante_2.text() == nombre:
            if materia == "arcilla":
                self.ventana_juego.editable_arcilla_2.setText(str(cantidad))
            elif materia == "madera":
                self.ventana_juego.editable_madera_2.setText(str(cantidad))
            if materia == "trigo":
                self.ventana_juego.editable_trigo_2.setText(str(cantidad))
        elif self.ventana_juego.editable_contrincante_3.text() == nombre:
            if materia == "arcilla":
                self.ventana_juego.editable_arcilla_3.setText(str(cantidad))
            elif materia == "madera":
                self.ventana_juego.editable_madera_3.setText(str(cantidad))
            if materia == "trigo":
                self.ventana_juego.editable_trigo_3.setText(str(cantidad))

    def choza_invalida(self):
        self.ventana_juego.choza_invalida()
    
    def carretera_invalida(self):
        self.ventana_juego.carretera_invalida()

    def intercambiar(self):
        for nombre in self.ventana_juego.lista_nombres:
            if nombre == self.nombre_cliente:
                continue
            self.ventana_intercambio.nombres.addItem(nombre)
        self.ventana_intercambio.show()

    def enviar_solicitud_intercambio(self, ofrece, pide, cant_ofrece, cant_pide, pide_a):
        self.senal_solicitar_intercambio.emit(
            self.nombre_cliente, pide_a, ofrece, cant_ofrece, pide, cant_pide
        )

    def transacc_inv(self):
        self.ventana_intercambio.mensaje_transacc_inv()

    def solicit_aprov_interc(self, jugador, ofrece, cant_o, pide, cant_p):
        print(f"{jugador} SOLICITA INTERCAMBIO DE {cant_o} {ofrece} por {cant_p} {pide}")
        self.pide = pide
        self.ofrece = ofrece
        self.cant_o = cant_o
        self.cant_p = cant_p
        self.pide_interc = jugador
        self.ventana_solicitud.nombre_destinatario.setText(jugador)
        self.ventana_solicitud.cantidad_ofrece.setText(str(cant_o))
        self.ventana_solicitud.cantidad_pide.setText(str(cant_p))
        self.ventana_solicitud.materia_ofrece.setText(ofrece)
        self.ventana_solicitud.materia_pide.setText(pide)
        self.ventana_solicitud.show()

    def aceptar_transaccion(self):
        self.senal_realizar_intercambio.emit(
            self.pide_interc, self.nombre_cliente, self.ofrece, self.cant_o, self.pide, self.cant_p
        )
        self.ventana_solicitud.hide()

    def rechazar_transaccion(self):
        self.senal_rechazar_intercambio.emit(self.pide_interc, self.nombre_cliente)
        self.ventana_solicitud.hide()

    def intercambio_realizado(self, ofrece, acepta, ofrecido, cant_o, pedido, cant_p):
        if self.ventana_intercambio.isVisible():
            self.ventana_intercambio.hide()
        self.ventana_juego.mensaje_intercambio_realizado(
            ofrece, acepta, ofrecido, cant_o, pedido, cant_p
        )

    def intercambio_rechazado(self, jugador_rechaza):
        self.ventana_intercambio.intercambio_rechazado()

    def juego_terminado(self, ganador):
        self.ventana_juego.juego_terminado(ganador)

    def reiniciar_partida(self):
        self.ventana_juego.hide()
        self.ventana_inicio.show()

    def recibir_puntos(self, jugador, puntos):
        if jugador == self.nombre_cliente:
            self.ventana_juego.editable_puntos_cliente.setText(puntos)
        elif self.ventana_juego.editable_contrincante_1.text() == jugador:
            self.ventana_juego.editable_puntos_contrincante_1.setText(puntos)
        elif self.ventana_juego.editable_contrincante_2.text() == jugador:
            self.ventana_juego.editable_puntos_contrincante_2.setText(puntos)
        elif self.ventana_juego.editable_contrincante_3.text() == jugador:
            self.ventana_juego.editable_puntos_contrincante_3.setText(puntos)

    def recibir_carretera_larga(self, jugador, largo):
        self.ventana_juego.editable_nombre_carretera_larga.setText(jugador)

    def carta_monopolio(self):
        self.ventana_juego.dialogo_carta_desarrollo("monopolio")

    def carta_victoria(self):
        self.ventana_juego.dialogo_carta_desarrollo("victoria")

    def realizar_monopolio(self):
        materia = self.ventana_juego.combo_box.currentText()
        self.senal_monopolio.emit(materia)
        self.ventana_juego.dialogo1.hide()

    def agregar_punto_victoria(self):
        puntos = self.ventana_juego.editable_puntos_victoria.text()[1:]
        puntos = int(puntos)
        puntos += 1
        self.ventana_juego.editable_puntos_victoria.setText(f":{puntos}")
        self.ventana_juego.dialogo2.hide()

    def carta_desarrollo_invalida(self):
        self.ventana_juego.carta_desarrollo_invalida()
        



            
            
        
                    


        

        

    



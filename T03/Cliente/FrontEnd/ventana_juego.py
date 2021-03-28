from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QMessageBox, QDialog, QComboBox
import sys
import os
from PyQt5.QtGui import QPixmap
import json
import random
from FrontEnd.labels_especiales import Ciudad, Choza, Carretera, CartaDesarrollo
from FrontEnd.vertices_aristas import Vertice
from PyQt5.QtCore import *

if __name__ == "__main__":
    path = os.path.join("DCColonos.ui")
else:
    #importar parametros
    path = os.path.join("parametros.json")
    with open(path, "rb") as archivo:
        parametros = json.load(archivo)

    path = os.path.join(*parametros["path_ui_VJ"])
window_name, base_class = uic.loadUiType(path)
class VentanaJuego(window_name, base_class):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setupUi(self)
        self.setup()
        self.lista_nombres = []
        self.nombre_cliente = ""
        self.vertices = dict()
        self.hexagonos = dict()
        self.vertices_ubicar_imagen = dict()
        self.color = ""
        self.colores_contrincantes = dict()
        self.aristas = dict()
        self.numeros_hexagonos = dict()
        self.clickeado = None
        self.en_turno = False
        self.mensaje = QMessageBox()
        self.dialogo1 = QDialog()
        self.dialogo2 = QDialog()

        self.prueba = True
        # Si este "switch" está en true, estamos en modo edición de programa
        # (se ve más feo)
    
    def setup(self):
        self.labels_optativos = [
            [self.carta_trigo_1, self.carta_madera_1, self.carta_arcilla_1, 
            self.editable_contrincante_1, self.label_3, 
            self.editable_puntos_contrincante_1, self.editable_arcilla_1, 
            self.editable_madera_1, self.editable_trigo_1], 
            [self.carta_trigo_2, self.carta_madera_2, self.carta_arcilla_2, 
            self.editable_contrincante_2, self.label_4, 
            self.editable_puntos_contrincante_2, self.editable_arcilla_2, 
            self.editable_madera_2, self.editable_trigo_2], 
            [self.carta_trigo_3, self.carta_madera_3, self.carta_arcilla_3,
            self.editable_contrincante_3, self.label_5, 
            self.editable_puntos_contrincante_3, self.editable_arcilla_3, 
            self.editable_madera_3, self.editable_trigo_3],
        ]
        for optativo in self.labels_optativos:
            for label in optativo:
                label.hide()

        path_arcilla = os.path.join(*parametros["path_carta_arcilla"])
        path_madera = os.path.join(*parametros["path_carta_madera"])
        path_trigo = os.path.join(*parametros["path_carta_trigo"])
        pixeles_arcilla_principal = QPixmap(path_arcilla).scaledToWidth(71)
        pixeles_madera_principal = QPixmap(path_madera).scaledToWidth(71)
        pixeles_trigo_principal = QPixmap(path_trigo).scaledToWidth(71)
        self.carta_arcilla.setPixmap(pixeles_arcilla_principal)
        self.carta_madera.setPixmap(pixeles_madera_principal)
        self.carta_trigo.setPixmap(pixeles_trigo_principal)
        pixeles_arcilla = QPixmap(path_arcilla).scaledToWidth(41)
        pixeles_madera = QPixmap(path_madera).scaledToWidth(41)
        pixeles_trigo = QPixmap(path_trigo).scaledToWidth(41)
        labels_arcilla = [self.carta_arcilla_1,
            self.carta_arcilla_2, self.carta_arcilla_3]
        labels_madera = [self.carta_madera_1,
            self.carta_madera_2, self.carta_madera_3]
        labels_trigo = [self.carta_trigo_1,
            self.carta_trigo_2, self.carta_trigo_3]
        for label in labels_arcilla:
            label.setPixmap(pixeles_arcilla)
        for label in labels_madera:
            label.setPixmap(pixeles_madera)
        for label in labels_trigo:
            label.setPixmap(pixeles_trigo)

        paths_dados = parametros["path_dados"]
        self.paths_dados = []
        for path in paths_dados:
            self.paths_dados.append(os.path.join(*path))
        pixeles_dados = QPixmap(self.paths_dados[5]).scaledToWidth(61)
        self.dado_1.setPixmap(pixeles_dados)
        self.dado_2.setPixmap(pixeles_dados)

        path = os.path.join(*parametros["path_punto_victoria"])
        pixeles_punto_victoria = QPixmap(path).scaledToWidth(41)
        self.carta_puntos_victoria.setPixmap(pixeles_punto_victoria)

        self.boton_lanzar = QPushButton("Lanzar", self)
        self.boton_lanzar.setGeometry(600, 380, 110, 41)
        self.boton_lanzar.clicked.connect(self.parent.lanzar_dados)
        self.boton_lanzar.setStyleSheet("background-color: blue; color: white")
        self.boton_lanzar.setEnabled(False)

        self.boton_terminar_turno = QPushButton("Terminar turno", self)
        self.boton_terminar_turno.setGeometry(600, 80, 110, 41)
        self.boton_terminar_turno.clicked.connect(self.parent.terminar_turno)
        self.boton_terminar_turno.setStyleSheet("background-color: blue; color: white")
        self.boton_terminar_turno.setEnabled(False)
        self.label_turno = QLabel("Es tu turno!", self)
        self.label_turno.setGeometry(600, 30, 110, 41)
        self.label_turno.setStyleSheet("font: 16pt")
        self.label_turno.hide()

        self.carta_desarrollo = CartaDesarrollo(self)
        self.boton_intercambiar = QPushButton("Intercambiar", self)
        self.boton_intercambiar.setGeometry(625, 550, 100, 71)
        self.boton_intercambiar.clicked.connect(self.parent.intercambiar)
        self.boton_intercambiar.setStyleSheet("background-color: blue; color: white")
        self.boton_intercambiar.setEnabled(False)

    def definir_jugadores(self, lista_nombres):
        cantidad = len(lista_nombres)
        for nombre in lista_nombres:
            self.lista_nombres.append(nombre)
        for i in range(cantidad - 1):
            labels = self.labels_optativos[i]
            for label in labels:
                label.show()
        indice = 0
        for nombre in self.lista_nombres:
            print(nombre)
            if nombre == self.nombre_cliente:
                self.editable_nombre_cliente.setText(f"{self.nombre_cliente} (Tú)")
            else:
                self.labels_optativos[indice][3].setText(nombre)
                indice += 1

    def recibir_vertices(self, vertices):
        self.vertices_ubicar_imagen = [
            vertices["4"], vertices["6"], vertices["10"], vertices["12"], vertices["14"],
            vertices["16"], vertices["20"], vertices["22"], vertices["24"], vertices["26"]
        ]
        self.vertices = vertices

    def recibir_hexagonos(self, hexagonos):
        ruta_arcilla = os.path.join(*parametros["path_hexagono_arcilla"])
        ruta_madera = os.path.join(*parametros["path_hexagono_madera"])
        ruta_trigo = os.path.join(*parametros["path_hexagono_trigo"])
        paths = [ruta_arcilla, ruta_madera, ruta_trigo]
        contador = 0
        for vertice in self.vertices_ubicar_imagen:
            path_imagen = paths[hexagonos[contador]]
            pixeles = QPixmap(path_imagen).scaledToWidth(160)
            label = QLabel(self)
            label_ficha = QLabel(self)
            label_numero = QLabel(self)
            self.hexagonos[contador] = [label, label_ficha, label_numero]
            label.setGeometry(vertice[0] + 7, vertice[1] - 72, 160, 160)
            label.setPixmap(pixeles)
            label.setStyleSheet('background-color: rgba(255, 255, 255, 0)')
            label.show()
            label_ficha.setGeometry(vertice[0] + 70, vertice[1] - 15, 41, 41)
            label_numero.setGeometry(vertice[0] + 82, vertice[1] - 5, 20, 20)
            contador += 1
        self.ubicar_vertices()

    def ubicar_vertices(self):
        vertices = dict()
        for vertice in self.vertices:
            label = Vertice(self, vertice, self.vertices[vertice][0], self.vertices
            [vertice][1])
            label.setStyleSheet('background-color: rgba(255, 255, 255, 0)')
            label.setText("")
            vertices[vertice] = label
            if not self.prueba:
                label.hide()
        self.vertices = vertices

    def definir_dados(self, dado_1, dado_2):
        dado_1 = QPixmap(self.paths_dados[dado_1 - 1]).scaledToWidth(61)
        dado_2 = QPixmap(self.paths_dados[dado_2 - 1]).scaledToWidth(61)
        self.dado_1.setPixmap(dado_1)
        self.dado_2.setPixmap(dado_2)

    def definir_color_construcciones(self, color):
        self.color = color
        self.carretera = Carretera(color, self)
        self.choza = Choza(color, self)

    def definir_colores(self, colores):
        for i in range(len(self.lista_nombres) - 1):
            nombre_ = self.labels_optativos[i][3].text()
            for nombre in colores:
                color = colores[nombre]
                if nombre == nombre_:
                    self.labels_optativos[i][3].setStyleSheet(
                        f"background-color: lightgrey;color: {color}")
                elif nombre == self.nombre_cliente:
                    self.editable_nombre_cliente.setStyleSheet(
                        f"background-color: lightgrey; color: {color}")

    def definir_numeros_hex(self, hexagonos):
        pixeles = QPixmap(os.path.join(*parametros["ficha_numero"])).scaledToWidth(41)
        for hexagono in hexagonos:
            label_ficha = self.hexagonos[hexagono][1]
            label_numero = self.hexagonos[hexagono][2]
            label_ficha.setStyleSheet('background-color: rgba(255, 255, 255, 0)')
            label_numero.setStyleSheet('background-color: rgba(255, 255, 255, 0)')
            label_ficha.setPixmap(pixeles)
            label_ficha.show()
            label_numero.show()
            label_numero.setText(str(hexagonos[hexagono][1]))
            self.hexagonos[hexagono].append(label_numero)

    def ubicar_choza(self, path, indice):
        pixeles = QPixmap(path).scaledToWidth(31)
        vertice = self.vertices[str(indice)]
        vertice.setPixmap(pixeles)
        vertice.setStyleSheet('background-color: rgba(255, 255, 255, 0)')
        vertice.ocupado = True
        vertice.show()

    def ubicar_carretera(self, path, indice):
        pixeles = QPixmap(path).scaledToWidth(31)
        arista = self.aristas[int(indice)]
        arista.setPixmap(pixeles)
        arista.setStyleSheet('background-color: rgba(255, 255, 255, 0)')
        arista.ocupado = True
        arista.show()

    def carretera_clickeada(self):
        if self.choza.clickeado:
            self.choza.clickeado = False
            self.choza.setStyleSheet("background-color: lightgrey")
        self.clickeado = self.carretera

    def choza_clickeada(self):
        if self.carretera.clickeado:
            self.carretera.clickeado = False
            self.carretera.setStyleSheet("background-color: lightgrey")
        self.clickeado = self.choza

    def choza_invalida(self):
        self.mensaje.setIcon(QMessageBox.Warning)
        self.mensaje.setText("Choza inválida! Fijate de que la posición sea la correcta y que tengas la cantidad de materias suficiente!")
        self.mensaje.setStandardButtons(QMessageBox.Ok)
        self.mensaje.show()

    def carretera_invalida(self):
        self.mensaje.setIcon(QMessageBox.Warning)
        self.mensaje.setText("Carretera inválida! Fijate de que la posición sea la correcta y que tengas la cantidad de materias suficiente!")
        self.mensaje.setStandardButtons(QMessageBox.Ok)
        self.mensaje.show()

    def mensaje_intercambio_realizado(self, ofrece, acepta, ofrecido, cant_o, pedido, cant_p):
        self.mensaje.setIcon(QMessageBox.Information)
        self.mensaje.setText(f"Intercambio realizado entre {ofrece} y {acepta}, {ofrece} recibió {cant_p} {pedido}s y {acepta} recibió {cant_o} {ofrecido}s.")
        self.mensaje.setStandardButtons(QMessageBox.Ok)
        self.mensaje.show()

    def juego_terminado(self, ganador):
        self.mensaje.setIcon(QMessageBox.Information)
        self.mensaje.setText(f"JUEGO TERMINADO!!!\n{ganador} ha ganado la partida!!!\nAprieta OK para volver a la sala de espera.")
        self.mensaje.setStandardButtons(QMessageBox.Ok)
        self.mensaje.buttonClicked.connect(self.parent.reiniciar_partida)
        self.mensaje.show()

    def carta_desarrollo_clickeada(self):
        self.parent.senal_pedir_cart_des.emit()

    def dialogo_carta_desarrollo(self, carta):
        if carta == "monopolio":
            self.dialogo1.boton = QPushButton("Confirmar", self.dialogo1)
            self.dialogo1.boton.clicked.connect(self.parent.realizar_monopolio)
            self.dialogo1.label1 = QLabel("Has conseguido una carta de monopolio!", self.dialogo1)
            self.dialogo1.label2 = QLabel("Elige la materia que deseas monopolizar y \nluego presiona confirmar:", self.dialogo1)
            self.combo_box = QComboBox(self.dialogo1)
            self.combo_box.addItem("Madera")
            self.combo_box.addItem("Arcilla")
            self.combo_box.addItem("Trigo")
            self.dialogo1.setFixedSize(400, 230)
            self.dialogo1.label1.move(70, 30)
            self.dialogo1.label2.move(65, 80)
            self.combo_box.move(150, 130)
            self.dialogo1.boton.move(150,180)
            self.dialogo1.setWindowTitle("Dialogo carta desarrollo.")
            self.dialogo1.setModal(True)
            self.dialogo1.show()
        elif carta == "victoria":
            self.dialogo2.boton = QPushButton("Confirmar", self.dialogo2)
            self.dialogo2.boton.clicked.connect(self.parent.agregar_punto_victoria)
            self.dialogo2.label1 = QLabel("Has conseguido una carta \nde victoria!", self.dialogo2)
            self.dialogo2.setFixedSize(230, 150)
            self.dialogo2.label1.move(30, 30)
            self.dialogo2.boton.move(60,100)
            self.dialogo2.setWindowTitle("Dialogo carta desarrollo.")
            self.dialogo2.setModal(True)
            self.dialogo2.show()

    def carta_desarrollo_invalida(self):
        self.mensaje.setIcon(QMessageBox.Warning)
        self.mensaje.setText("No puedes comprar cartas de desarrollo! Fíjate de tener las materias suficientes!")
        self.mensaje.setStandardButtons(QMessageBox.Ok)
        self.mensaje.show()

        
            


        




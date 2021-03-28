from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QMessageBox
import sys
import os
from PyQt5.QtGui import QPixmap
import json


path = os.path.join("parametros.json")
with open(path, "rb") as archivo:
    parametros = json.load(archivo)

path = os.path.join(*parametros["path_ui_VINT"])
window_name, base_class = uic.loadUiType(path)

path = os.path.join(*parametros["path_ui_VSI"])
window_name2, base_class2 = uic.loadUiType(path)

class VentanaIntercambio(window_name, base_class):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setupUi(self)
        self.boton_enviar.clicked.connect(self.enviar_solicitud)
        self.mensaje = QMessageBox()

    def enviar_solicitud(self):
        ofrece = self.ofrece.currentText()
        pide = self.pide.currentText()
        cantidad_ofrece = self.cantidad_ofrece.currentText()
        cantidad_pide = self.cantidad_pide.currentText()
        pide_a = self.nombres.currentText()
        self.parent.enviar_solicitud_intercambio(ofrece, pide, cantidad_ofrece, cantidad_pide, pide_a)

    def mensaje_transacc_inv(self):
        self.mensaje.setIcon(QMessageBox.Warning)
        self.mensaje.setText(
            "Transacción Inválida! Asegurate que tanto tú como el jugador con el que intentas intercambiar tengan las cantidades de materia solicitada.")
        self.mensaje.setStandardButtons(QMessageBox.Ok)
        self.mensaje.show()

    def intercambio_rechazado(self):
        self.mensaje.setIcon(QMessageBox.Warning)
        self.mensaje.setText("El jugador rechazó el intercambio! Intenta nuevamente con otro jugador!")
        self.mensaje.setStandardButtons(QMessageBox.Ok)
        self.mensaje.show()


class VentanaSolicitudIntercambio(window_name2, base_class2):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setupUi(self)
        self.setup()

    def setup(self):
        self.boton_aceptar.clicked.connect(self.parent.aceptar_transaccion)
        self.boton_rechazar.clicked.connect(self.parent.rechazar_transaccion)

    
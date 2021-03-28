from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
import sys
import os
from PyQt5.QtGui import QPixmap
import json

#importar parametros
path = os.path.join("parametros.json")
with open(path, "rb") as archivo:
    parametros = json.load(archivo)

path = os.path.join(*parametros["path_ui_VI"])
window_name, base_class = uic.loadUiType(path)
class VentanaInicio(window_name, base_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup()
    
    def setup(self):
        ruta_imagen = os.path.join(*parametros["path_logo_ventana_inicio"])
        pixeles = QPixmap(ruta_imagen).scaledToWidth(400)
        self.logo.setPixmap(pixeles)

        self.labels = [
            self.label1, self.label2, self.label3, self.label4
        ]
        for label in self.labels:
            label.hide()

    def mostrar_labels(self, cantidad):
        for i in range(cantidad):
            self.labels[i].show()

    def actualizar(self, nombre, es_cliente):
        for label in self.labels:
            if label.text() == "Esperando...":
                if es_cliente:
                    label.setText(f"{nombre} (Tú)")
                else:
                    label.setText(f"{nombre}")
                break

    def eliminar_nombre(self, nombre):
        for label in self.labels:
            if label.text() == nombre:
                label.setText("Esperando...")
                break


if __name__ == "__main__":
    app = QApplication([])
    ventana = VentanaInicio()
    ventana.show()
    sys.exit(app.exec_())

import json
import os
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap

path = os.path.join("parametros.json")
with open(path, "rb") as archivo:
    parametros = json.load(archivo)

class Carretera(QLabel):
    def __init__(self, color, parent):
        super().__init__(parent)
        self.parent = parent
        self.color = color
        self.clickeado = False

        self.setup()

    def setup(self):
        if self.color == "rosado":
            color = "violeta"
        else:
            color = self.color
        paths = [parametros[f"path_{color}"][0], parametros[f"path_{color}"][1],
            parametros[f"path_{color}"][2]]
        self.pixeles_0 = QPixmap(os.path.join(*paths[0])).scaledToWidth(51)
        self.pixeles_60 = QPixmap(os.path.join(*paths[1])).scaledToWidth(51)
        self.pixeles_120 = QPixmap(os.path.join(*paths[2])).scaledToWidth(51)
        self.setGeometry(465, 590, 51, 41)
        self.setStyleSheet("background-color: lightgrey")
        self.mostrar(0)
        self.show()

    def mostrar(self, grados):
        if grados == 0:
            self.setPixmap(self.pixeles_0)
        elif grados == 60:
            self.setPixmap(self.pixeles_60)
        else:
            self.setPixmap(self.pixeles_120)

    def mouseReleaseEvent(self, event):
        if not self.parent.en_turno:
            return
        self.setStyleSheet("background-color: grey")
        self.clickeado = True
        self.parent.carretera_clickeada()


class Choza(QLabel):
    def __init__(self, color, parent):
        super().__init__(parent)
        self.parent = parent
        self.color = color
        self.clickeado = False

        self.setup()
    
    def setup(self):
        if self.color == "rosado":
            color = "violeta"
        else:
            color = self.color
        path = parametros[f"path_{color}"][3]
        self.pixeles = QPixmap(os.path.join(*path)).scaledToWidth(41)
        self.setPixmap(self.pixeles)
        self.setStyleSheet("background-color: lightgrey")
        self.setGeometry(470, 530, 41, 41)
        self.show()

    def mouseReleaseEvent(self, event):
        if not self.parent.en_turno:
            return
        self.setStyleSheet("background-color: grey")
        self.clickeado = True
        self.parent.choza_clickeada()


class Ciudad(QLabel):
    def __init__(self, color, parent):
        super().__init__(parent)
        self.color = color

        self.setup()
    
    def setup(self):
        if self.color == "rosado":
            color = "violeta"
        else:
            color = self.color
        path = parametros[f"path_{color}"][4]
        self.pixeles = QPixmap(os.path.join(*path)).scaledToWidth(41)
        self.setPixmap(self.pixeles)
        self.setStyleSheet("background-color: lightgrey")


class CartaDesarrollo(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        path = os.path.join(*parametros["path_carta_reverso"])
        self.setPixmap(QPixmap(path).scaledToWidth(71))
        self.setGeometry(540, 530, 71, 103)
        self.show()

    def mouseReleaseEvent(self, event):
        if not self.parent.en_turno:
            return
        self.parent.carta_desarrollo_clickeada()




        
















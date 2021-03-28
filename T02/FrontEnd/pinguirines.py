from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtCore import Qt, QMimeData, QRect
from PyQt5.QtGui import QDrag, QPixmap, QPainter, QCursor
import parametros as par
import os

#Inspirado con https://www.youtube.com/watch?v=9CJV-GGP22c

class Pinguino(QLabel):
    def __init__(self, parent, color, pos_x, pos_y):
        super().__init__(parent)
        self.color = color
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = QRect(pos_x, pos_y, 60, 70)
        self.drag = True

        self.init_gui()

    def init_gui(self):
        if self.color == "celeste":
            ruta_imagen = os.path.join(*par.PATH_PINGUINOS["PINGUI_AZUL_NEUTRO"])
            self.pixeles = QPixmap(ruta_imagen).scaledToWidth(110)
            self.setPixmap(self.pixeles)
        elif self.color == "rojo":
            ruta_imagen = os.path.join(*par.PATH_PINGUINOS["PINGUI_ROJO_NEUTRO"])
            self.pixeles = QPixmap(ruta_imagen).scaledToWidth(110)
            self.setPixmap(self.pixeles)
        elif self.color == "amarillo":
            ruta_imagen = os.path.join(*par.PATH_PINGUINOS["PINGUI_AMAR_NEUTRO"])
            self.pixeles = QPixmap(ruta_imagen).scaledToWidth(110)
            self.setPixmap(self.pixeles)
        elif self.color == "morado":
            ruta_imagen = os.path.join(*par.PATH_PINGUINOS["PINGUI_MORA_NEUTRO"])
            self.pixeles = QPixmap(ruta_imagen).scaledToWidth(110)
            self.setPixmap(self.pixeles)
        elif self.color == "verde":
            ruta_imagen = os.path.join(*par.PATH_PINGUINOS["PINGUI_VERD_NEUTRO"])
            self.pixeles = QPixmap(ruta_imagen).scaledToWidth(110)
            self.setPixmap(self.pixeles)
        self.move(self.pos_x, self.pos_y)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.posicion_inicial_drag = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag: 
            drag = QDrag(self)
            data_label = QMimeData()  #movemos info del label junto a este
            data_label.setText(self.color)
            data_label.setImageData(self.pixmap().toImage) #Movemos imagen
            drag.setMimeData(data_label)
            #efectos de arrastre
            drop_action = drag.exec_(Qt.MoveAction)

class PinguinoBailarin(Pinguino):
    def __init__(self, parent, color, pos_x, pos_y):
        super().__init__(parent, color, pos_x, pos_y)
        
        self.sprites = []
        largo = len(self.color)
        for path in par.PATH_BAILES_PINGUINOS:
            if self.color.upper() == path[:largo]:
                self.sprites.append(par.PATH_BAILES_PINGUINOS[path])

    # 0 - izquierda / 1 - arriba / 2 - abajo / 3 - derecha
    def actualizar_paso(self, direc):
        self.setPixmap(self.pixeles)
        if len(direc) == 1:
            if direc[0] == 0:
                ruta_imagen = os.path.join(
                    *par.PATH_BAILES_PINGUINOS[f"{self.color.upper()}_IZQUIERDA"])
                self.nuevos_pixeles = QPixmap(ruta_imagen).scaledToWidth(110)
                self.setPixmap(self.nuevos_pixeles)
            elif direc[0] == 1:
                ruta_imagen = os.path.join(
                    *par.PATH_BAILES_PINGUINOS[f"{self.color.upper()}_ARRIBA"])
                self.nuevos_pixeles = QPixmap(ruta_imagen).scaledToWidth(110)
                self.setPixmap(self.nuevos_pixeles)
            elif direc[0] == 2:
                ruta_imagen = os.path.join(
                    *par.PATH_BAILES_PINGUINOS[f"{self.color.upper()}_ABAJO"])
                self.nuevos_pixeles = QPixmap(ruta_imagen).scaledToWidth(110)
                self.setPixmap(self.nuevos_pixeles)
            elif direc[0] == 3:
                ruta_imagen = os.path.join(
                    *par.PATH_BAILES_PINGUINOS[f"{self.color.upper()}_DERECHA"])
                self.nuevos_pixeles = QPixmap(ruta_imagen).scaledToWidth(110)
                self.setPixmap(self.nuevos_pixeles)
        elif len(direc) == 2:
            if (direc[0] == 0 and direc[1] == 1) or (direc[0] == 1 and direc[1] == 0):
                ruta_imagen = os.path.join(
                    *par.PATH_BAILES_PINGUINOS[f"{self.color.upper()}_ARRIBA_IZQUIERDA"])
                self.nuevos_pixeles = QPixmap(ruta_imagen).scaledToWidth(110)
                self.setPixmap(self.nuevos_pixeles)
            elif (direc[0] == 0 and direc[1] == 2) or (direc[0] == 2 and direc[1] == 0):
                ruta_imagen = os.path.join(
                    *par.PATH_BAILES_PINGUINOS[f"{self.color.upper()}_ABAJO_IZQUIERDA"])
                self.nuevos_pixeles = QPixmap(ruta_imagen).scaledToWidth(110)
                self.setPixmap(self.nuevos_pixeles)
            elif (direc[0] == 3 and direc[1] == 2) or (direc[0] == 2 and direc[1] == 3):
                ruta_imagen = os.path.join(
                    *par.PATH_BAILES_PINGUINOS[f"{self.color.upper()}_ABAJO_DERECHA"])
                self.nuevos_pixeles = QPixmap(ruta_imagen).scaledToWidth(110)
                self.setPixmap(self.nuevos_pixeles)
            elif (direc[0] == 3 and direc[1] == 1) or (direc[0] == 1 and direc[1] == 3):
                ruta_imagen = os.path.join(
                    *par.PATH_BAILES_PINGUINOS[f"{self.color.upper()}_ARRIBA_DERECHA"])
                self.nuevos_pixeles = QPixmap(ruta_imagen).scaledToWidth(110)
                self.setPixmap(self.nuevos_pixeles)
        elif len(direc) == 3:
            ruta_imagen = os.path.join(
                *par.PATH_BAILES_PINGUINOS[f"{self.color.upper()}_TRES_FLECHAS"])
            self.nuevos_pixeles = QPixmap(ruta_imagen).scaledToWidth(110)
            self.setPixmap(self.nuevos_pixeles)

    def posicion_normal(self):
        self.setPixmap(self.pixeles)


    

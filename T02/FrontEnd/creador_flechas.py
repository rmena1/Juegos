import os
from random import randint
from time import sleep

from PyQt5.QtCore import QThread, QTimer, pyqtSignal, QRect
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QMainWindow, QApplication

import parametros as par


class Flecha(QThread):

    actualizar = pyqtSignal(QLabel, int, int)
    senal_flecha_perdida = pyqtSignal(int)
    

    # 0 -> izquierda / 1 -> derecha / 2 -> arriba / 3 -> abajo
    # 0 -> normal / 1 -> x2 / 2 -> hielo / 3 -> dorada
    def __init__(self, parent, direccion, tipo, id_paso, cantidad_paso):
        super().__init__(parent)
        contador = 0
        ruta = (direccion + tipo*4)
        for path in par.PATH_FLECHAS:
            if contador == ruta:
                self.ruta_imagen = par.PATH_FLECHAS[path]
            contador += 1
        self.label = QLabel("", parent)
        self.tipo = tipo
        self.cantidad_paso = cantidad_paso
        ruta = self.ruta_imagen
        ruta_imagen = os.path.join(*ruta)
        pixeles = QPixmap(ruta_imagen).scaledToWidth(35)
        self.label.setPixmap(pixeles)
        #me equivoque en determinar direccion, por eso las vuelvo a definir
        if direccion == 1:
            direccion = 3
            self.direccion = 3
        elif direccion == 2:
            direccion = 1
            self.direccion = 1
        elif direccion == 3:
            direccion = 2
            self.direccion = 2
        else:
            self.direccion = 0
        self.posicion_x = 30 + direccion*45
        self.posicion_y = 150
        self.id_paso = id_paso
        self.rect = QRect(
            self.posicion_x, self.posicion_y, 20, par.ALTO_FLECHA)
        self.label.move(self.posicion_x, self.posicion_y)
        self.flecha_hielo = parent.flecha_hielo
        self.label.show()
        self.start()

    def run(self):
        while self.posicion_y < 640:
            sleep(0.12)
            mult = 1
            if self.flecha_hielo:
                mult = 0.5
            if self.tipo == 3:
                nuevo_y = self.posicion_y + 0.08*par.VELOCIDAD_FLECHA*1.5*mult
            else:
                nuevo_y = self.posicion_y + 0.08*par.VELOCIDAD_FLECHA*mult
            self.posicion_y = nuevo_y
            self.actualizar.emit(self.label, self.posicion_x, self.posicion_y)
            self.rect.moveTo(self.posicion_x, self.posicion_y)
            if self.posicion_y >= 625:
                if self.label.isVisible():
                    self.label.hide()
                    self.senal_flecha_perdida.emit(self.id_paso)
        



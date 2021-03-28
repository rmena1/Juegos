import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import parametros as par
from PyQt5.QtCore import pyqtSignal

class VentanaRanking(QWidget):
    
    senal_abrir_ranking = pyqtSignal()
    senal_volver_inicio = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.init_gui()
        self.senal_abrir_ranking.connect(self.show)

    def init_gui(self):
        self.setGeometry(100, 100, par.ANCHO_VENTANA_INICIO, par.ALTURA_VENTANA_INICIO)
        self.setMaximumHeight(par.ALTURA_VENTANA_INICIO)
        self.setMaximumWidth(par.ANCHO_VENTANA_INICIO)
        self.setMinimumHeight(par.ALTURA_VENTANA_INICIO)
        self.setMinimumWidth(par.ANCHO_VENTANA_INICIO)
        self.titulo = QLabel("Ranking de Puntajes", self)
        self.puesto1 = QLabel("", self)
        self.puesto2 = QLabel("", self)
        self.puesto3 = QLabel("", self)
        self.puesto4 = QLabel("", self)
        self.puesto5 = QLabel("", self)
        self.puesto1_editable = QLabel("", self)
        self.puesto2_editable = QLabel("", self)
        self.puesto3_editable = QLabel("", self)
        self.puesto4_editable = QLabel("", self)
        self.puesto5_editable = QLabel("", self)
        self.imagen = QLabel("", self)
        self.boton = QPushButton("Volver", self)

        self.titulo.setFont(QFont("Arial", 30))
        self.titulo.setGeometry(120, 10, 300, 50)
        self.puesto1.setGeometry(80, 80, 150, 40)
        self.puesto2.setGeometry(80, 120, 150, 40)
        self.puesto3.setGeometry(80, 160, 150, 40)
        self.puesto4.setGeometry(80, 200, 150, 40)
        self.puesto5.setGeometry(80, 240, 150, 40)
        self.puesto1_editable.setGeometry(230, 80, 100, 40)
        self.puesto2_editable.setGeometry(230, 120, 100, 40)
        self.puesto3_editable.setGeometry(230, 160, 100, 40)
        self.puesto4_editable.setGeometry(230, 200, 100, 40)
        self.puesto5_editable.setGeometry(230, 240, 100, 40)
        self.boton.setGeometry(220, 290, 80, 40)

        ruta_imagen = os.path.join(*par.PATH_PUFFLE_RANKING)
        pixeles = QPixmap(ruta_imagen).scaledToWidth(100)
        self.imagen.setPixmap(pixeles)

        self.imagen.move(340, 140)

        self.boton.clicked.connect(self.volver)

        self.cargar_datos()

    def volver(self):
        self.hide()
        self.senal_volver_inicio.emit()

    def cargar_datos(self):
        path = os.path.join(par.PATH_RESULTADOS)
        with open(path, 'a') as archivo:
            pass
        with open(os.path.join(path), 'rt') as archivo:
            ranking = archivo.readlines()

        for indice in range(len(ranking)):
            ranking[indice] = ranking[indice].strip('\n').split(', ')
            ranking[indice][1] = int(ranking[indice][1])
        
        puntaje_maximo = -1
        mejores_puntajes = []

        for puesto in range(5):
            if len(ranking) == 0:
                break
            for jugador in ranking:
                if jugador[1] > puntaje_maximo:
                    mejor_jugador = jugador
                    puntaje_maximo = jugador[1]
            mejores_puntajes.append(mejor_jugador)
            ranking.remove(mejor_jugador)
            puntaje_maximo = -1
            if len(ranking) == 0:
                break
        
        labels_puestos = [self.puesto1, self.puesto2, self.puesto3, self.puesto4, self.puesto5]
        labels_puestos_editables = [self.puesto1_editable, self.puesto2_editable, 
            self.puesto3_editable, self.puesto4_editable, self.puesto5_editable]
        i_puesto = 0
        for puesto in mejores_puntajes:
            labels_puestos[i_puesto].setText(puesto[0])
            labels_puestos_editables[i_puesto].setText(str(puesto[1]))
            labels_puestos[i_puesto].setFont(QFont("Arial", 16))
            labels_puestos_editables[i_puesto].setFont(QFont("Arial", 16))
            i_puesto += 1


if __name__ == "__main__":
    app = QApplication([])
    inicio = VentanaRanking()
    inicio.show()
    sys.exit(app.exec_())
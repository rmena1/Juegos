from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QApplication
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal
import parametros as par
import sys

class VentanaResumen(QWidget):

    senal_volver_juego = pyqtSignal()
    senal_volver_inicio = pyqtSignal()

    def __init__(self, puntaje, acumulado, combo, fallados, aprobacion, aceptado):
        super().__init__()

        self.puntaje = puntaje
        self.acumulado = acumulado
        self.combo = combo
        self.fallados = fallados
        self.aprobacion = aprobacion
        self.aceptado = aceptado

        self.init_gui()
        

    def init_gui(self):
        self.setGeometry(100, 100, par.ANCHO_VENTANA_INICIO, par.ALTURA_VENTANA_INICIO)
        self.titulo = QLabel("Resumen de la Ronda", self)
        self.label_puntaje = QLabel("Puntaje Obtenido:", self)
        self.label_acumulado = QLabel("Puntaje Acumulado:", self)
        self.label_combo = QLabel("Máximo Combo:", self)
        self.label_fallados = QLabel("Cantidad de pasos fallados:", self)
        self.label_aprobacion = QLabel("Porcentaje de aprobacion:", self)
        
        self.titulo.setFont(QFont("Arial", 30))
        self.titulo.setGeometry(100, 10, 300, 50)
        labels = [self.label_puntaje, self.label_acumulado, self.label_combo,
            self.label_fallados, self.label_aprobacion]
        eje_y = 80
        for label in labels:
            label.setFont(QFont("Arial", 16))
            label.setGeometry(90, eje_y, 200, 20)
            eje_y += 30

        self.label_puntaje_variable = QLabel(str(self.puntaje), self)
        self.label_acumulado_variable = QLabel(str(self.acumulado), self)
        self.label_combo_variable = QLabel("x" + str(self.combo), self)
        self.label_fallados_variable = QLabel(str(self.fallados), self)
        self.label_aprobacion_variable = QLabel(str(self.aprobacion) + "%", self)
        labels = [self.label_puntaje_variable, self.label_acumulado_variable,
            self.label_combo_variable, self.label_fallados_variable,
            self.label_aprobacion_variable]
        eje_y = 80
        for label in labels:
            label.setFont(QFont("Arial", 16))
            label.setGeometry(370, eje_y, 80, 20)
            eje_y += 30

        if self.aceptado:
            self.mensaje_final = QLabel(
                "Clasificaste a la siguiente ronda, excelentes pasos!", self)
            self.mensaje_final.setFont(QFont("Arial", 16))
            self.mensaje_final.setGeometry(70, 250, 600, 20)
            self.boton = QPushButton("Siguiente ronda", self)
            self.boton.setGeometry(190, 300, 120, 30)
            self.boton.clicked.connect(self.boton_apretado)
            
        else:
            espacio = " "
            self.mensaje_final = QLabel(
                f"No has clasificado a la siguiente ronda debido a una baja aprobación. \n {45*espacio}Nos vemos!",
                     self)
            self.mensaje_final.setFont(QFont("Arial", 14))
            self.mensaje_final.setGeometry(35, 250, 600, 40)
            self.boton = QPushButton("Volver al inicio", self)
            self.boton.setGeometry(190, 300, 120, 30)
            self.boton.clicked.connect(self.boton_apretado)

    def boton_apretado(self):
        if self.aceptado:
            self.senal_volver_juego.emit()
            self.hide()
        else:
            self.senal_volver_inicio.emit()
            self.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana_resumen = VentanaResumen(300, 13000, 6, 23, 43, False)
    ventana_resumen.show()
    sys.exit(app.exec_())
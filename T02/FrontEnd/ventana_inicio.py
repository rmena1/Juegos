import os
import sys
from PyQt5.QtWidgets import (
    QApplication, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit, QMessageBox
)
from PyQt5.QtGui import QPixmap
import parametros as par
from PyQt5.QtCore import pyqtSignal, QRect
from FrontEnd.ventana_ranking import VentanaRanking
from FrontEnd.ventana_juego import VentanaJuego
from BackEnd.logica_juego import Juego
from FrontEnd.creador_flechas import Flecha
from BackEnd.cerrar_partida import terminar_partida

class VentanaInicio(QWidget):

    senal_abrir_ranking = pyqtSignal()
    senal_volver_inicio = pyqtSignal()
    senal_comenzar_juego = pyqtSignal()
    senal_definir_nombre = pyqtSignal(str)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.senal_volver_inicio.connect(self.show)
        self.init_gui()
        self.instanciar()

    def instanciar(self):
        self.ventanas()
        self.senales()

    def ventanas(self):
        self.ventana_juego = VentanaJuego()
        self.juego = Juego()
        self.ventana_ranking = VentanaRanking()

    def senales(self):
        self.ventana_ranking.senal_volver_inicio.connect(self.senal_volver_inicio)
        self.senal_comenzar_juego.connect(self.ventana_juego.senal_comenzar_juego)
        self.ventana_juego.senal_salir.connect(self.senal_volver_inicio)
        self.ventana_juego.senal_salir.connect(self.juego.salir)
        self.ventana_juego.senal_salir.connect(self.reinstanciar)
        self.senal_definir_nombre.connect(self.juego.senal_definir_nombre)
        self.ventana_juego.senal_def_cancion_dificultad.connect(self.juego.senal_def_cancion_dificultad)
        self.ventana_juego.senal_iniciar_ronda.connect(self.juego.senal_iniciar_ronda)
        self.juego.senal_crear_flechas.connect(self.ventana_juego.creador_flechas)
        self.juego.senal_terminar_ronda.connect(self.ventana_juego.senal_terminar_ronda)
        self.ventana_juego.senal_recibir_flecha.connect(self.juego.senal_recibir_flecha)
        self.juego.senal_flecha_hielo_inicio.connect(self.ventana_juego.senal_flecha_hielo_inicio)
        self.juego.senal_flecha_hielo_fin.connect(self.ventana_juego.senal_flecha_hielo_fin)
        self.ventana_juego.senal_flecha_perdida.connect(self.juego.senal_flecha_perdida)
        self.juego.senal_actualizar_combo.connect(self.ventana_juego.senal_actualizar_combo)
        self.juego.senal_actualizar_aceptacion.connect(self.ventana_juego.senal_actualizar_aprobacion)
        self.ventana_juego.senal_reiniciar_ronda.connect(self.juego.senal_reiniciar_ronda)
        self.ventana_juego.senal_interseccion_fallida.connect(self.juego.senal_interseccion_fallida)
        self.juego.senal_resumen_ronda.connect(self.ventana_juego.senal_resumen_ronda)
        self.juego.senal_actualizar_dinero.connect(self.ventana_juego.senal_actualizar_dinero)
        self.ventana_juego.senal_comprar_pinguino.connect(self.juego.senal_comprar_pinguino)
        self.juego.senal_actualizar_paso.connect(self.ventana_juego.senal_actualizar_paso)
        self.ventana_juego.senal_mon.connect(self.juego.mon)
        self.ventana_juego.senal_niv.connect(self.juego.niv)
        self.juego.senal_actualizar_progreso.connect(self.ventana_juego.senal_actualizar_progreso)
        self.juego.senal_cerrar_partida.connect(terminar_partida)

    def init_gui(self):
        self.setGeometry(100, 100, par.ANCHO_VENTANA_INICIO, par.ALTURA_VENTANA_INICIO)
        self.setMaximumHeight(par.ALTURA_VENTANA_INICIO)
        self.setMaximumWidth(par.ANCHO_VENTANA_INICIO)
        self.setMinimumHeight(par.ALTURA_VENTANA_INICIO)
        self.setMinimumWidth(par.ANCHO_VENTANA_INICIO)
        self.setWindowTitle("Ventana de Inicio")
        self.logo = QLabel("", self)
        self.texto1 = QLabel("Ingresa el nombre de tu bailarín:", self)
        self.editable = QLineEdit("", self)
        self.boton1 = QPushButton("Ir a Ranking", self)
        self.boton1.resize(self.boton1.sizeHint())
        self.boton2 = QPushButton("Comenzar", self)
        self.boton2.resize(self.boton1.sizeHint())
        self.mensaje = QMessageBox()

        ruta_imagen = os.path.join(*par.PATH_LOGO)
        pixeles = QPixmap(ruta_imagen).scaledToWidth(200)
        self.logo.setPixmap(pixeles)

        self.logo.move(150, 10)
        self.texto1.setGeometry(150, 220, 200, 30)
        self.editable.setGeometry(150, 250, 200, 35)
        self.boton1.setGeometry(125, 290, 120, 50)
        self.boton2.setGeometry(250, 290, 120, 50)

        self.boton1.clicked.connect(self.ir_a_ranking)
        self.boton2.clicked.connect(self.verificar_nombre)

        self.show()

    def reinstanciar(self):
        self.instanciar()

    def ir_a_ranking(self):
        self.ventana_ranking.show()

    def verificar_nombre(self):
        nombre = self.editable.text()
        if nombre.isalnum():
            print("nombre cumple con requisitos")
            self.senal_definir_nombre.emit(self.editable.text())
            self.hide()
            self.senal_comenzar_juego.emit()
        else:
            #https://www.tutorialspoint.com/pyqt/pyqt_qmessagebox.htm
            self.mensaje.setIcon(QMessageBox.Warning)
            self.mensaje.setText("Nombre inválido. Tu nombre debe contener carácteres alfanuméricos únicamente. Intenta nuevamente.")
            self.mensaje.setStandardButtons(QMessageBox.Ok)
            self.mensaje.show()

if __name__ == "__main__":
    app = QApplication([])
    inicio = VentanaInicio()
    inicio.show()
    sys.exit(app.exec_())


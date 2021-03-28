import os
import sys
from PyQt5.QtWidgets import (
    QApplication, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit, QProgressBar, 
    QComboBox, QMessageBox
)
from PyQt5.QtGui import QPixmap, QFont
import parametros as par
from PyQt5.QtCore import pyqtSignal, QRect, QTimer, QRect, QUrl
import random
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QSound
from FrontEnd.creador_flechas import Flecha
from FrontEnd.pinguirines import Pinguino, PinguinoBailarin
from FrontEnd.ventana_resumen import VentanaResumen
from FrontEnd.cheats import LabelOculto, VentanaTrampa

class VentanaJuego(QWidget):
    senal_comenzar_juego = pyqtSignal()
    senal_salir = pyqtSignal()
    senal_def_cancion_dificultad = pyqtSignal(str, str)
    senal_iniciar_ronda = pyqtSignal()
    senal_terminar_ronda = pyqtSignal()
    senal_recibir_flecha = pyqtSignal(int, int, int, int)
    senal_flecha_hielo_inicio = pyqtSignal()
    senal_flecha_hielo_fin = pyqtSignal()
    senal_flecha_perdida = pyqtSignal(int)
    senal_actualizar_combo = pyqtSignal(int)
    senal_reiniciar_ronda = pyqtSignal()
    senal_actualizar_aprobacion = pyqtSignal(int)
    senal_interseccion_fallida = pyqtSignal(str)
    senal_resumen_ronda = pyqtSignal(int, int, int, int, int, bool)
    senal_actualizar_dinero = pyqtSignal(int)
    senal_comprar_pinguino = pyqtSignal()
    senal_actualizar_paso = pyqtSignal(list)
    senal_actualizar_progreso = pyqtSignal(int)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_gui()
        self.senal_comenzar_juego.connect(self.show)
        self.flechas = []
        self.parametros_definidos = False
        self.senal_terminar_ronda.connect(self.terminar_ronda)
        self.senal_flecha_hielo_inicio.connect(self.flecha_hielo_inicio)
        self.senal_flecha_hielo_fin.connect(self.flecha_hielo_fin)
        self.flecha_hielo = False
        self.senal_actualizar_combo.connect(self.actualizar_combo)
        self.setAcceptDrops(True)
        self.pinguinos_bailando = []
        self.flechas_perdidas = 0
        self.senal_reiniciar_emitida = False
        self.tienda_activa = True
        self.senal_actualizar_aprobacion.connect(self.actualizar_aprobacion)
        self.senal_resumen_ronda.connect(self.resumen_ronda)
        self.esperar = QTimer(self)
        self.esperar.setInterval(10)
        self.senal_actualizar_dinero.connect(self.actualizar_dinero)
        self.senal_actualizar_paso.connect(self.actualizar_paso)
        self.cheats = LabelOculto(self)
        self.ventana_trampa = VentanaTrampa()
        self.senal_mon = self.ventana_trampa.senal_mon
        self.senal_niv = self.ventana_trampa.senal_niv
        self.cheats.click.connect(self.hacer_trampa)
        self.musica = False
        self.senal_actualizar_progreso.connect(self.actualizar_progreso)

    def init_gui(self):
        # Secciones principales
        self.setGeometry(100, 100, par.ANCHO_VENTANA_JUEGO, par.ALTURA_VENTANA_JUEGO)
        self.setMaximumHeight(par.ALTURA_VENTANA_JUEGO)
        self.setMaximumWidth(par.ANCHO_VENTANA_JUEGO)
        self.setMinimumHeight(par.ALTURA_VENTANA_JUEGO)
        self.setMinimumWidth(par.ANCHO_VENTANA_JUEGO)
        self.setWindowTitle("Ventana de Juego")
        self.zona_estadisticas_seleccion_ronda = QLabel("", self)
        self.zona_ritmo = QLabel("", self)
        self.pista_baile = QLabel("", self)
        self.tienda = QLabel("", self)
        ruta_imagen = os.path.join(*par.PATH_PISTA_BAILE)
        pixeles = QPixmap(ruta_imagen).scaledToWidth(507)
        self.pista_baile.setPixmap(pixeles)
        self.zona_estadisticas_seleccion_ronda.setGeometry(3, 3, 994, 120)
        self.zona_estadisticas_seleccion_ronda.setStyleSheet(
            "background-color: lightgreen; border: 1px solid black;")
             #https://www.geeksforgeeks.org/pyqt5-how-to-change-color-of-the-label/
        self.zona_ritmo.setGeometry(3, 126, 230, 521)
        self.zona_ritmo.setStyleSheet(
            "background-color: lightgreen; border: 1px solid black;")
        self.tienda.setGeometry(767, 126, 230, 521)
        self.tienda.setStyleSheet(
            "background-color: lightgreen; border: 1px solid black;")
        self.pista_baile.move(245, 126)
        self.pista_baile.setStyleSheet(
            "border: 1px solid black;")
        #Elementos de zona estadisticas - seleccion
        self.logo = QLabel("", self)
        self.label_combo = QLabel("Combo:", self)
        self.label_combo_actualizable = QLabel("x0", self)
        self.label_mayorcombo = QLabel("Mayor Combo:", self)
        self.label_mayorcombo_actualizable = QLabel("x0", self)
        self.label_progreso = QLabel("Progreso:", self)
        self.barra_progreso = QProgressBar(self)
        self.label_aprobacion = QLabel("Aprobación:", self)
        self.barra_aprobacion = QProgressBar(self)
        self.label_cancion = QLabel("Canción:", self)
        self.opciones_cancion = QComboBox(self)
        self.label_dificultad = QLabel("Dificultad:", self)
        self.opciones_dificultad = QComboBox(self)
        self.boton_comenzar = QPushButton("Comenzar ronda", self)
        self.boton_pausa = QPushButton("Pausar", self)
        self.boton_exit = QPushButton("Salir", self)
        self.opciones_cancion.insertItem(0, "Temazo 1")
        self.opciones_cancion.insertItem(1, "Temazo 2")
        self.opciones_dificultad.insertItem(0, "Principiante")
        self.opciones_dificultad.insertItem(1, "Aficionado")
        self.opciones_dificultad.insertItem(2, "Maestro cumbia")
        self.boton_comenzar.clicked.connect(self.definir_cancion_dificultad)
        ruta_imagen = os.path.join(*par.PATH_LOGO)
        pixeles = QPixmap(ruta_imagen).scaledToWidth(110)
        self.logo.setPixmap(pixeles)
        self.logo.move(50, 6)
        self.label_combo.setGeometry(290, 40, 80, 15)
        self.label_mayorcombo.setGeometry(250, 80, 130, 15)
        self.label_combo_actualizable.setGeometry(345, 40, 25, 15)
        self.label_mayorcombo_actualizable.setGeometry(345, 80, 25, 15)
        self.label_progreso.setGeometry(400, 40, 80, 15)
        self.label_aprobacion.setGeometry(387, 80, 80, 15)
        self.barra_progreso.move(475, 38)
        self.barra_aprobacion.move(475, 78)
        self.label_cancion.setGeometry(620, 40, 80, 15)
        self.label_dificultad.setGeometry(615, 80, 80, 15)
        self.opciones_cancion.move(690, 33)
        self.opciones_dificultad.move(690, 73)
        self.boton_comenzar.move(830, 20)
        self.boton_pausa.move(830, 50)
        self.boton_exit.move(830, 80)
        self.boton_exit.clicked.connect(self.salir)
        #Elementos Tienda
        self.label_tienda = QLabel("Tienda", self)
        self.label_tienda.setFont(QFont("Arial", 25))
        self.label_dinero = QLabel("Dinero:", self)
        self.label_dinero.setFont(QFont("Arial", 15))
        self.cantidad_dinero = QLabel(f"${par.VALOR_PINGUINOS}", self)
        self.cantidad_dinero.setFont(QFont("Arial", 15))
        self.label_valor_pinguinos = QLabel(
            f"Valor pinguino: ${par.VALOR_PINGUINOS}", self)
        self.label_valor_pinguinos.setFont(QFont("Arial", 15))
        self.pingui_azul = Pinguino(self, "celeste", 880, 400)
        self.pingui_rojo = Pinguino(self, "rojo", 880, 300)
        self.pingui_amar = Pinguino(self, "amarillo", 770, 300)
        self.pingui_mora = Pinguino(self, "morado", 770, 400)
        self.lechuga = Pinguino(self, "verde", 825, 500)
        self.mensaje = QMessageBox()
        self.label_tienda.setGeometry(840, 140, 90, 30)
        self.label_dinero.setGeometry(830, 180, 100, 20)
        self.cantidad_dinero.setGeometry(890, 180, 90, 20)
        self.label_valor_pinguinos.setGeometry(810, 200, 150, 20)
        #Elementos constantes de zona ritmo
        self.caja_a = QLabel("", self)
        self.caja_w = QLabel("", self)
        self.caja_s = QLabel("", self)
        self.caja_d = QLabel("", self)
        self.label_a = QLabel("A", self)
        self.label_w = QLabel("W", self)
        self.label_s = QLabel("S", self)
        self.label_d = QLabel("D", self)
        self.caja_a.setGeometry(30, 550, 45, 45)
        self.caja_a.setStyleSheet(
            "background-color: lightblue; border: 1px solid black;")
        self.caja_a.rect = QRect(30, 550, 45, par.ALTO_CAPTURA)
        self.caja_w.setGeometry(75, 550, 45, 45)
        self.caja_w.setStyleSheet(
            "background-color: lightblue; border: 1px solid black;")
        self.caja_w.rect = QRect(75, 550, 45, par.ALTO_CAPTURA)
        self.caja_s.setGeometry(120, 550, 45, 45)
        self.caja_s.setStyleSheet(
            "background-color: lightblue; border: 1px solid black;")
        self.caja_s.rect = QRect(120, 550, 45, par.ALTO_CAPTURA)
        self.caja_d.setGeometry(165, 550, 45, 45)
        self.caja_d.setStyleSheet(
            "background-color: lightblue; border: 1px solid black;")
        self.caja_d.rect = QRect(165, 550, 45, par.ALTO_CAPTURA)
        self.label_a.setFont(QFont("Arial", 30))
        self.label_a.setGeometry(42, 600, 25, 25)
        self.label_w.setFont(QFont("Arial", 30))
        self.label_w.setGeometry(83, 600, 30, 25)
        self.label_s.setFont(QFont("Arial", 30))
        self.label_s.setGeometry(132, 600, 25, 25)
        self.label_d.setFont(QFont("Arial", 30))
        self.label_d.setGeometry(177, 600, 25, 25)

    def definir_cancion_dificultad(self):
        if len(self.pinguinos_bailando) == 0:
            self.mensaje.setIcon(QMessageBox.Warning)
            self.mensaje.setText("No tienes pinguinos bailando. Compra uno para comenzar!")
            self.mensaje.setStandardButtons(QMessageBox.Ok)
            self.mensaje.show()
            return
        self.boton_comenzar.setEnabled(False)
        self.opciones_dificultad.setEnabled(False)
        self.opciones_cancion.setEnabled(False)
        self.tienda_activa = False
        if not self.parametros_definidos:
            self.senal_def_cancion_dificultad.emit(
                self.opciones_cancion.currentText(), self.opciones_dificultad.currentText())
            self.parametros_definidos = True
        self.senal_iniciar_ronda.emit()
        self.flechas = []
        self.flechas_perdidas = 0
        self.id_paso_actual = 0
        self.label_mayorcombo_actualizable.setText(f"x0")
        self.senal_reiniciar_emitida = False
        if self.opciones_cancion.currentText() == "Temazo 1":
            path_cancion = os.path.join(*par.PATH_CANCIONES["TEMA_1"])
        else:
            path_cancion = os.path.join(*par.PATH_CANCIONES["TEMA_2"])
        self.musica = QSound(path_cancion)
        self.musica.play()

    def creador_flechas(self, cantidad, direccion, tipo, id_paso):
        for flecha in range(cantidad):
            nueva_flecha = Flecha(self, direccion[flecha], tipo[flecha], id_paso, cantidad)
            nueva_flecha.actualizar.connect(self.actualizar_label_flecha)
            nueva_flecha.senal_flecha_perdida.connect(self.flecha_perdida)
            self.flechas.append(nueva_flecha) 
    
    def actualizar_label_flecha(self, flecha, x, y):
        flecha.move(x, y)
        if len(self.flechas) - self.flechas_perdidas  != 0:
            pass
        elif not self.senal_reiniciar_emitida:
            self.esperar.timeout.connect(self.reiniciar)
            self.esperar.start()
        
    def reiniciar(self):
        self.esperar.stop()
        self.senal_reiniciar_ronda.emit()
        self.senal_reiniciar_emitida = True

    def terminar_ronda(self):
        self.boton_comenzar.setEnabled(True)
        self.opciones_cancion.setEnabled(True)
        self.opciones_cancion.setEnabled(True)
        self.flecha_hielo = False
        self.tienda_activa = True
        for pinguinos in self.pinguinos_bailando:
            pinguinos.posicion_normal()
        if self.musica:
            self.musica.stop()

    def keyPressEvent(self, event):
        if event.text() == "a":
            self.caja_a.setStyleSheet(
                "background-color: blue; border: 1px solid black;")
            for flecha in self.flechas:
                if flecha.rect.intersects(self.caja_a.rect):
                    flecha.label.hide()
                    self.senal_recibir_flecha.emit(
                        flecha.tipo, flecha.id_paso, flecha.direccion, flecha.cantidad_paso)
                    self.flechas.remove(flecha)
                else:
                    self.senal_interseccion_fallida.emit("a")
        if event.text() == "w":
            self.caja_w.setStyleSheet(
                "background-color: blue; border: 1px solid black;")
            for flecha in self.flechas:
                if flecha.rect.intersects(self.caja_w.rect):
                    flecha.label.hide()
                    self.senal_recibir_flecha.emit(
                        flecha.tipo, flecha.id_paso, flecha.direccion, flecha.cantidad_paso)
                    self.flechas.remove(flecha)
                else:
                    self.senal_interseccion_fallida.emit("w")
        if event.text() == "s":
            self.caja_s.setStyleSheet(
                "background-color: blue; border: 1px solid black;")
            for flecha in self.flechas:
                if flecha.rect.intersects(self.caja_s.rect):
                    flecha.label.hide()
                    self.senal_recibir_flecha.emit(
                        flecha.tipo, flecha.id_paso, flecha.direccion, flecha.cantidad_paso)
                    self.flechas.remove(flecha)
                else:
                    self.senal_interseccion_fallida.emit("s")
        if event.text() == "d":
            self.caja_d.setStyleSheet(
                "background-color: blue; border: 1px solid black;")
            for flecha in self.flechas:
                if flecha.rect.intersects(self.caja_d.rect):
                    flecha.label.hide()
                    self.senal_recibir_flecha.emit(
                        flecha.tipo, flecha.id_paso, flecha.direccion, flecha.cantidad_paso)
                    self.flechas.remove(flecha)
                else:
                    self.senal_interseccion_fallida.emit("d")

    def keyReleaseEvent(self, event):
        self.caja_a.setStyleSheet(
            "background-color: lightblue; border: 1px solid black;")
        self.caja_w.setStyleSheet(
            "background-color: lightblue; border: 1px solid black;")
        self.caja_s.setStyleSheet(
            "background-color: lightblue; border: 1px solid black;")
        self.caja_d.setStyleSheet(
            "background-color: lightblue; border: 1px solid black;")

    def flecha_hielo_inicio(self):
        self.flecha_hielo = True
        for flecha in self.flechas:
            flecha.flecha_hielo = True

    def flecha_hielo_fin(self):
        self.flecha_hielo = False
        for flecha in self.flechas:
            flecha.flecha_hielo = False

    def flecha_perdida(self, id_flecha):
        self.flechas_perdidas += 1
        self.senal_flecha_perdida.emit(id_flecha)

    def actualizar_combo(self, valor):
        self.label_combo_actualizable.setText(f"x{valor}")
        if valor > int(self.label_mayorcombo_actualizable.text()[1:]):
            self.label_mayorcombo_actualizable.setText(f"x{valor}")

    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        position = event.pos()
        if position.x() > 320 and position.y() > 370 and position.x() < 660 and( 
            position.y() < 600):
            pinguino = PinguinoBailarin(
                self, event.mimeData().text(), position.x() - 50, position.y() - 50)
            pinguino.show()
            acoplado = False
            if int(self.cantidad_dinero.text()[1:]) < par.VALOR_PINGUINOS:
                acoplado = True
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.setText("No tienes suficiente dinero, juega una ronda para conseguir más.")
                self.mensaje.setStandardButtons(QMessageBox.Ok)
                self.mensaje.show()
            else:
                self.senal_comprar_pinguino.emit()
            for pinguino_bailando in self.pinguinos_bailando:
                if pinguino.rect.intersects(pinguino_bailando.rect):
                    acoplado = True
            if acoplado or not self.tienda_activa:
                pinguino.hide()
                event.ignore()
            else:
                event.accept()
                self.pinguinos_bailando.append(pinguino)
                pinguino.drag = False
        else:
            event.ignore()

    def actualizar_aprobacion(self, aprobacion):
        self.barra_aprobacion.setValue(aprobacion)

    def actualizar_progreso(self, valor):
        self.barra_progreso.setValue(valor)

    def resumen_ronda(self, puntaje, acumulado, combo, fallados, aprobacion, aceptado):
        self.ventana_resumen = VentanaResumen(
            puntaje, acumulado, combo, fallados, aprobacion, aceptado
        )
        self.ventana_resumen.senal_volver_inicio.connect(self.salir)
        self.ventana_resumen.senal_volver_juego.connect(self.volver_juego)
        self.ventana_resumen.show()
        self.hide()

    def volver_juego(self):
        self.show()
        self.label_mayorcombo_actualizable.setText("x0")

    def salir(self):
        self.hide()
        self.senal_salir.emit()

    def actualizar_dinero(self, valor):
        self.cantidad_dinero.setText(f"${valor}")
    
    def actualizar_paso(self, direcciones):
        for pinguino in self.pinguinos_bailando:
            pinguino.actualizar_paso(direcciones)
    
    def hacer_trampa(self):
        self.ventana_trampa.show()
    

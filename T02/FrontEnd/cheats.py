import os
import sys
from PyQt5.QtWidgets import (
    QApplication, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit, QProgressBar, 
    QComboBox, QMessageBox
)
from PyQt5.QtGui import QPixmap, QFont
import parametros as par
from PyQt5.QtCore import pyqtSignal, QRect, QTimer, QRect, QUrl

class LabelOculto(QLabel):
    click = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.setGeometry(385, 235, 35, 35)
        #self.setStyleSheet("border: 1px solid red;")

    def mousePressEvent(self, event):
        self.click.emit()

class VentanaTrampa(QWidget):
    senal_mon = pyqtSignal()
    senal_niv = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 200, 100)
        self.label = QLabel("Ingresa un codigo:", self)
        self.label.setGeometry(10, 10, 150, 20)
        self.editable = QLineEdit("", self)
        self.editable.setGeometry(10, 35, 180, 30)
        self.boton = QPushButton("Aceptar", self)
        self.boton.setGeometry(65, 70, 80, 30)
        self.boton.clicked.connect(self.ejecutar)

    def ejecutar(self):
        codigo = self.editable.text()
        if codigo == "mon":
            self.senal_mon.emit()
        elif codigo == "niv":
            self.senal_niv.emit()
    
    


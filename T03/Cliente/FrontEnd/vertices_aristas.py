from PyQt5.QtWidgets import QLabel

class Vertice(QLabel):
    def __init__(self, parent, indice, pos_x, pos_y):
        super().__init__(parent)
        self.parent = parent
        self.indice = indice
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.setup()
        self.ocupado = False

    def setup(self):
        self.setGeometry(self.pos_x - 8, self.pos_y - 8, 30, 30)
        #self.setStyleSheet('background-color: rgba(255, 255, 255, 0)')
        self.setText(self.indice)
        self.show()
    
    def mouseReleaseEvent(self, event):
        if self.parent.clickeado == self.parent.choza and not self.ocupado:
            self.parent.parent.senal_solicitar_choza.emit(self.parent.parent.nombre_cliente, self.indice)

class Arista(QLabel):
    def __init__(self, parent, indice, pos_x, pos_y):
        super().__init__(parent)
        self.parent = parent
        self.indice = str(indice)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.setup()
        self.ocupado = False

    def setup(self):
        self.setGeometry(self.pos_x - 8, self.pos_y - 8, 30, 30)
        self.setStyleSheet('background-color: rgba(255, 255, 255, 0)')
        self.setText("")
        self.show()

    def mouseReleaseEvent(self, event):
        if self.parent.clickeado == self.parent.carretera and not self.ocupado:
            self.parent.parent.senal_solicitar_carretera.emit(self.parent.parent.nombre_cliente, self.indice)

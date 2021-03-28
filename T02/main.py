from FrontEnd.ventana_inicio import VentanaInicio
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana_inicio = VentanaInicio()
    ventana_inicio.show()
    sys.exit(app.exec_())

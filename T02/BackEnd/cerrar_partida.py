from PyQt5.QtCore import pyqtSignal
import parametros as par
import os

def terminar_partida(nombre, puntaje):
    path = os.path.join(par.PATH_RESULTADOS)
    with open(path, 'a') as archivo:
        archivo.write(f"{nombre}, {puntaje}\n")


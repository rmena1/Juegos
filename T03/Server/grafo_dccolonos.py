class Choza:
    def __init__(self, indice, vertice):
        self.indice = indice
        self.posicion = vertice
        self.carreteras_adyacentes = []
        

class Carretera:
    def __init__(self, indice, arista):
        self.carreteras_adyacentes = []
        self.indice = indice
        self.posicion = arista
        self.chozas_adyacentes = []

    def __repr__(self):
        return f"Carretera: {self.indice}"
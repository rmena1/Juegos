class Jugadores:
    def __init__(self, socket, adress, nombre, indice):
        self.socket = socket
        self.adress = adress
        self.nombre = nombre
        self.indice = indice
        self.color = None
        self.chozas = []
        self.carreteras = []
        self.ciudades = []
        self.en_turno = False
        self.arcilla = 0
        self.madera = 0
        self.trigo = 0
        self.indice_choza = 0
        self.indice_carretera = 0
        self.cartas_puntos_victoria = 0
        self.puntos_carretera_larga = 0
        self.puntos_victoria = 0

    def contar_puntos(self):
        self.puntos_victoria = (
            self.cartas_puntos_victoria + len(self.carreteras) + len(self.chozas) * 2 + self.puntos_carretera_larga
        )
        print(f"PUNTOS {self.nombre}: {self.puntos_victoria}")
        return self.puntos_victoria






    def __repr__(self):
        return str(self.indice)
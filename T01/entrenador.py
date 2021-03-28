

class Entrenador():
    
    def __init__(self, nombre, usuario, delegacion):
        self.nombre = nombre
        self.usuario = usuario
        self.delegacion = delegacion

    def entrenar(self):
        self.delegacion.entrenar_deportistas()
        return

    def fichar(self):
        self.delegacion.fichar_deportistas()
        return

    def sanar(self):
        self.delegacion.sanar_lesiones()
        return

    def comprar_tecnologia(self):
        self.delegacion.comprar_tecnologia()
        return

    def usar_habilidad_especial(self):
        self.usar_habilidad_especial()
        return

    def simular_acciones(self):
        #No implementado
        pass
from abc import ABC, abstractmethod
import random


class Delegacion(ABC):

    def __init__(self, entrenador, moral, equipo, medallas, dinero):
        self.entrenador = entrenador
        self.equipo = equipo
        self.medallas = int(medallas)
        self.__moral = float(moral)
        self.__dinero = int(dinero)
        self.__excelencia_respeto = float()
        self.__implementos_deportivos = float()
        self.__implementos_medicos = float()
        self.mostrando = list()

    @property
    def excelencia_respeto(self):
        return self.__excelencia_respeto

    @property
    def implementos_deportivos(self):
        return self.__implementos_deportivos

    @property
    def implementos_medicos(self):
        return self.__implementos_medicos

    @property
    def moral(self):
        return self.__moral

    @moral.setter
    def moral(self, n_moral):
        if n_moral > 100:
            self.__moral = 100
        elif n_moral < 0:
            self.__moral = 0
        else:
            self.__moral = n_moral

    def fichar_deportistas(self, deportista):
        if self.moral <= 20:
            print('No puedes fichar, tu moral es menor o igual a 20.')
            print('')
            return False
        else:
            if deportista.precio > self.__dinero:
                print('No puedes fichar, el deportista es muy caro.')
                print('')
                return False
            else:
                self.__dinero -= deportista.precio
                self.equipo.append(deportista)
                print(f'Felicidades! Has fichado a {deportista.nombre}.')
                print('')
                return True

    def entrenar_deportistas(self, deportista, cualidad):
        if self.__dinero < 30:
            print('Entrenar cuesta 30 DCCoins, no tienes dinero suficiente.')
            print('')
            return
        else:
            nueva_cualidad = deportista.entrenar(cualidad, False)
            self.dinero -= 30
            print(f'Felicidades! Has entrenado exitosamente a {deportista.nombre}.')
            print(f'Nueva {cualidad}: {nueva_cualidad}.')
            print('')
            return

    def sanar_lesiones(self, deportista):
        if not deportista.lesionado:
            print('Tu jugador no está lesionado.')
            print('')
            return
        elif self.__dinero < 30:
            print('No puedes sanar lesiones, no tienes suficiente dinero.')
            print('')
            return
        else:
            self.dinero -= 30
            probabilidad = min(1, max(0, (deportista.moral * (self.implementos_medicos + self.excelencia_respeto)) / 200))
            n_random = random.uniform(0, 1)
            n_random = round(n_random, 1)
            if n_random < probabilidad:
                deportista.lesionado = False
                print(f'{deportista.nombre} se ha sanado!.')
                print('')
                return
            else:
                print(f'{deportista.nombre} no se ha podido sanar.')
                print('')
                return

    @abstractmethod
    def utilizar_habilidad_especial(self):
        pass

    @property
    def dinero(self):
        return self.__dinero

    @dinero.setter
    def dinero(self, n_dinero):
        if n_dinero < 0:
            print('No tienes suficiente dinero.')
            print('')
        else:
            self.__dinero = n_dinero

    def mostrar_equipo(self, solo_lesionados):
        mostrar = []
        self.mostrando = []
        if solo_lesionados:
            for deportista in self.equipo:
                if deportista.lesionado:
                    mostrar.append(deportista)
        else:
            mostrar = self.equipo
        print('INDICE:  NOMBRE:               VELOCIDAD:  RESISTENCIA:  FLEXIBILIDAD:  MORAL:  LESIONADO:  PRECIO:')
        indice = 0
        for deportista in mostrar:
            print(f'{indice: ^7d}  {str(deportista.nombre):20.20s}  {str(deportista.velocidad):5.5s}       {str(deportista.resistencia):5.5s}         {str(deportista.flexibilidad):5.5s}          {str(deportista.moral):5.5s}   {str(deportista.lesionado):5.5s}       {str(deportista.precio):5.5s}')
            indice += 1
            self.mostrando.append(deportista)
        print('')

    def seleccionar_habilidad(self):
        print('[1] -> Velocidad. \n[2] -> Resistencia \n[3] -> flexibilidad')
        print('')
        while True:
            try:
                entrada = input('Selecciona una habilidad: ')
                if entrada == '1':
                    return 'velocidad'
                elif entrada == '2':
                    return 'resistencia'
                elif entrada == '3':
                    return 'flexibilidad'
                else:
                    raise TypeError
            except TypeError:
                print('Input incorrecto, intenta nuevamente.')
                print('')

    def seleccionar_deportista(self):
        while True:
            try:
                entrada = input('Ingresa el índice del deportista: ')
                deportista = self.mostrando[int(entrada)]
                return deportista
            except TypeError:
                print('Recuerda que el indice debe ser un número. Intenta nuevamente.')
            except ValueError:
                print('Recuerda que el indice debe ser un número. Intenta nuevamente.')
            except IndexError:
                print('Indice incorrecto. Intente nuevamente.')


class DCCrotona(Delegacion):

    def __init__(self, entrenador, moral, equipo, medallas, dinero):
        super().__init__(entrenador, moral, equipo, medallas, dinero)
        self.nombre_delegacion = 'DCCrotona'
        n_random = random.uniform(0.3, 0.7)
        self.__excelencia_respeto = round(n_random, 1)
        n_random = random.uniform(0.2, 0.6)
        self.__implementos_deportivos = round(n_random, 1)
        n_random = random.uniform(0.4, 0.8)
        self.__implementos_medicos = round(n_random, 1)
        self.habilidad_especial_disponible = True

    @property
    def excelencia_respeto(self):
        return self.__excelencia_respeto

    @excelencia_respeto.setter
    def excelencia_respeto(self, n_excelencia_respeto):
        n_excelencia_respeto = round(n_excelencia_respeto, 1)
        if n_excelencia_respeto < 0.3:
            self.__excelencia_respeto = 0.3
        elif n_excelencia_respeto > 0.7:
            self.__excelencia_respeto = 0.7
        else:
            self.__excelencia_respeto = n_excelencia_respeto

    @property
    def implementos_deportivos(self):
        return self.__implementos_deportivos

    @implementos_deportivos.setter
    def implementos_deportivos(self, n_implementos_deportivos):
        n_implementos_deportivos = round(n_implementos_deportivos, 1)
        if n_implementos_deportivos < 0.2:
            self.__implementos_deportivos = 0.2
        elif n_implementos_deportivos > 0.6:
            self.__implementos_deportivos = 0.6
        else:
            self.__implementos_deportivos = n_implementos_deportivos

    @property
    def implementos_medicos(self):
        return self.__implementos_medicos

    @implementos_medicos.setter
    def implementos_medicos(self, n_implementos_medicos):
        n_implementos_medicos = round(n_implementos_medicos, 1)
        if n_implementos_medicos < 0.4:
            self.__implementos_medicos = 0.4
        elif n_implementos_medicos > 0.8:
            self.__implementos_medicos = 0.8
        else:
            self.__implementos_medicos = n_implementos_medicos
    
    def utilizar_habilidad_especial(self):
        # Tomo como supuesto que no debemos modificar los parametros de ningun deportista con este super poder
        if self.habilidad_especial_disponible:
            self.medallas += 1
            self.dinero += 100
            self.excelencia_respeto += 0.02
            self.habilidad_especial_disponible = False
            print('DCCrotona ha utilizado su habilidad especial!')
        else:
            print('Habilidad especial no disponible!\nSolo la puedes utilizar una vez por partida.')
            

    def sanar_lesiones(self, deportista):
        if not deportista.lesionado:
            print('Tu jugador no está lesionado.')
            print('')
            return
        elif self.dinero < 60:
            print('No puedes sanar lesiones, no tienes suficiente dinero.')
            print('')
            return
        else:
            self.dinero -= 60
            probabilidad = min(1, max(0, (deportista.moral * (self.implementos_medicos + self.excelencia_respeto)) / 200))
            n_random = random.uniform(0, 1)
            n_random = round(n_random, 1)
            if n_random < probabilidad:
                deportista.lesionado = False
                print(f'{deportista.nombre} se ha sanado!.')
                print('')
                return
            else:
                print(f'{deportista.nombre} no se ha podido sanar.')
                print('')
                return

    def comprar_tecnología(self):
        if self.dinero < 20:
            print('No tienes dinero suficiente, comprar tecnología cuesta 20 DCCoins.')
            print('')
        else:
            self.dinero -= 20
            self.implementos_deportivos = self.implementos_deportivos * 1.1
            self.implementos_medicos = self.implementos_medicos * 1.1
            print('Has comprado nueva tecnología.')
            print(f'Implementos Deportivos: {self.implementos_deportivos}')
            print(f'Implementos Médicos: {self.implementos_medicos}')
            print('')


class IEEEsparta(Delegacion):

    def __init__(self, entrenador, moral, equipo, medallas, dinero):
        super().__init__(entrenador, moral, equipo, medallas, dinero)
        self.nombre_delegacion = 'IEEEsparta'
        n_random = random.uniform(0.4, 0.8)
        self.__excelencia_respeto = round(n_random, 1)
        n_random = random.uniform(0.3, 0.7)
        self.__implementos_deportivos = round(n_random, 1)
        n_random = random.uniform(0.2, 0.6)
        self.__implementos_medicos = round(n_random, 1)
        self.habilidad_especial_disponible = True

    @property
    def excelencia_respeto(self):
        return self.__excelencia_respeto

    @excelencia_respeto.setter
    def excelencia_respeto(self, n_excelencia_respeto):
        n_excelencia_respeto = round(n_excelencia_respeto, 1)
        if n_excelencia_respeto < 0.4:
            self.__excelencia_respeto = 0.4
        elif n_excelencia_respeto > 0.8:
            self.__excelencia_respeto = 0.8
        else:
            self.__excelencia_respeto = n_excelencia_respeto

    @property
    def implementos_deportivos(self):
        return self.__implementos_deportivos

    @implementos_deportivos.setter
    def implementos_deportivos(self, n_implementos_deportivos):
        n_implementos_deportivos = round(n_implementos_deportivos, 1)
        if n_implementos_deportivos < 0.3:
            self.__implementos_deportivos = 0.3
        elif n_implementos_deportivos > 0.7:
            self.__implementos_deportivos = 0.7
        else:
            self.__implementos_deportivos = n_implementos_deportivos

    @property
    def implementos_medicos(self):
        return self.__implementos_medicos

    @implementos_medicos.setter
    def implementos_medicos(self, n_implementos_medicos):
        n_implementos_medicos = round(n_implementos_medicos, 1)
        if n_implementos_medicos < 0.2:
            self.__implementos_medicos = 0.2
        elif n_implementos_medicos > 0.6:
            self.__implementos_medicos = 0.6
        else:
            self.__implementos_medicos = n_implementos_medicos

    def utilizar_habilidad_especial(self):
        if self.habilidad_especial_disponible:
            for atleta in self.equipo:
                atleta.moral = 100
            self.habilidad_especial_disponible = False
            print('IEEEsparta ha utilizado su habilidad especial!')
        else:
            print('Habilidad especial no disponible!\nSolo la puedes utilizar una vez por partida.')

    def entrenar_deportistas(self, deportista, cualidad):
        if self.dinero < 30:
            print('Entrenar cuesta 30 DCCoins, no tienes dinero suficiente.')
            print('')
            return
        else:
            nueva_cualidad = deportista.entrenar(cualidad, True)
            self.dinero -= 30
            print(f'Felicidades! Has entrenado exitosamente a {deportista.nombre}.')
            print(f'Nueva {cualidad}: {nueva_cualidad}.')
            print('')
            return

    def comprar_tecnología(self):
        if self.dinero < 20:
            print('No tienes dinero suficiente, comprar tecnología cuesta 20 DCCoins.')
            print('')
        else:
            self.dinero -= 20
            self.implementos_deportivos = self.implementos_deportivos * 1.1
            self.implementos_medicos = self.implementos_medicos * 1.1
            print('Has comprado nueva tecnología.')
            print(f'Implementos Deportivos: {self.implementos_deportivos}')
            print(f'Implementos Médicos: {self.implementos_medicos}')
            print('')

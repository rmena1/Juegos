from abc import ABC, abstractmethod


class Menu(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def verificar_opciones(self, eleccion, opciones):
        if eleccion in opciones:
            return True
        else:
            print('Opción incorrecta, intenta nuevamente.')
            return False

    @abstractmethod
    def realizar_accion(self):
        pass

    @abstractmethod
    def salir(self):
        quit()

    @abstractmethod
    def flujo_de_menu(self):
        input('Presiona enter para continuar.')
        print('')
        return


class MenuInicio(Menu):

    def __init__(self):
        self.delegacion_usuario: str()
        self.delegacion_rival: str()
        self.nombre_usuario: str()
        self.nombre_rival: str()
        self.opcion: int()

    def principal(self):
        print('')
        print('*** MENU DE INICIO ***')
        print('')
        while True:
            print('Bienvenido a DCCumbre Olímpica! \n[1] -> Comenzar Nueva Partida. \n[2] -> Salir.')
            print('')
            opcion = input('Ingresa tu opción: ')
            if self.verificar_opciones(opcion, ['1', '2']):
                self.opcion = opcion
                print('')
                return self.realizar_accion()
            self.flujo_de_menu()

    def verificar_opciones(self, opcion, opciones):
        return super().verificar_opciones(opcion, opciones)

    def realizar_accion(self):
        if self.opcion == '1':
            return self.pedir_nombres()
        else:
            return self.salir()

    def salir(self):
        return super().salir()

    def pedir_nombres(self):
        while True:
            print('Nombres deben contener letras y/o números.')
            print('')
            nombre_usuario = input('Ingresa tu nombre: ')
            print('')
            nombre_rival = input('Ingresa el nombre de tu enemigo: ')
            print('')
            if nombre_usuario.isalnum() and nombre_rival.isalnum():
                self.nombre_usuario = nombre_usuario
                self.nombre_rival = nombre_rival
                print('')
                return self.elegir_delegacion()
            else:
                print('Nombres solo pueden estar compuestos de letras y/o números. Intente nuevamente.')
                self.flujo_de_menu()

    def elegir_delegacion(self):
        while True:
            print('Elige tu delegación: \n[1] -> DCCrotona \n[2] -> IEEEsparta')
            print('')
            entrada = input('Ingresa una opción: ')
            print('')
            if self.verificar_opciones(entrada, ['1', '2']):
                if entrada == '1':
                    self.delegacion_usuario = 'DCCrotona'
                    self.delegacion_rival = 'IEEEsparta'
                    return
                else:
                    self.delegacion_usuario = 'IEEEsparta'
                    self.delegacion_rival = 'DCCrotona'
                    return
            self.flujo_de_menu()

    def flujo_de_menu(self):
        return super().flujo_de_menu()


class MenuPrincipal(Menu):
    
    def principal(self):
        print('*** MENU PRINCIPAL ***')
        print('')
        while True:
            print('[1] -> Menú entrenador. \n[2] -> Simular competencias. \n[3] -> Mostrar estado. \n[4] -> Salir del programa.')
            print('')
            entrada = input('Ingresa una opción: ')
            print('')
            if self.verificar_opciones(entrada, ['1', '2', '3', '4']):
                return self.realizar_accion(entrada)
            self.flujo_de_menu()

    def verificar_opciones(self, opcion, opciones):
        return super().verificar_opciones(opcion, opciones)

    def realizar_accion(self, opcion):
        if opcion == '1':
            return 'm_entrenador'
        elif opcion == '2':
            return 's_competencia'
        elif opcion == '3':
            return 'most_estado'
        else:
            self.salir()
            

    def salir(self):
        super().salir()

    def flujo_de_menu(self):
        return super().flujo_de_menu()

    def mostrar_opciones_finales(self):
        while True:
            print('[1] --> Salir del programa.\n[2] --> Realizar una nueva simulación.')
            print('')
            entrada = input('Ingresa una opción: ')
            if entrada == '1':
                quit()
            elif entrada == '2':
                return
            else:
                print('Opción incorrecta, intenta nuevamente.')
                print('')
                self.flujo_de_menu()



class MenuEntrenador(Menu):

    def principal(self):
        print('*** MENU ENTRENADOR ***')
        print('')
        while True:
            print('[1] -> Fichar. \n[2] -> Entrenar. \n[3] -> Sanar lesiones. \n[4] -> Comprar tecnología. \n[5] -> Usar habilidad especial. \n[6] -> Volver al menú anterior. \n[7] -> Salir del programa.')
            print('')
            entrada = input('Elige una opción: ')
            print('')
            if self.verificar_opciones(entrada, ['1', '2', '3', '4', '5', '6', '7']):
                return self.realizar_accion(entrada)
            self.flujo_de_menu()

    def verificar_opciones(self, opcion, opciones):
        return super().verificar_opciones(opcion, opciones)

    def salir(self):
        super().salir()

    def realizar_accion(self, opcion):
        if opcion == '1':
            return 'fichar'
        elif opcion == '2':
            return 'entrenar'
        elif opcion == '4':
            return 'comp_tecnologia'
        elif opcion == '5':
            return 'usar_hab_esp'
        elif opcion == '6':
            return 'volver'
        elif opcion == '3':
            return 'sanar'
        else:
            self.salir()

    def flujo_de_menu(self):
        return super().flujo_de_menu()


    
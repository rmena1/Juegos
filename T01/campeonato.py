import os
import parametros as par
import random


class Campeonato:
    
    def __init__(self, delegacion_usuario, delegacion_rival):
        self.dia_actual = 1
        self.medallero = {'DCCrotona': {'atletismo':0, 'gimnasia':0, 'natacion':0, 'ciclismo':0}, 'IEEEsparta':{'atletismo':0, 'gimnasia':0, 'natacion':0, 'ciclismo':0}}
        self.ganadores_del_dia = []
        self.delegacion_usuario = delegacion_usuario
        self.delegacion_rival = delegacion_rival
        self.competidores_usuario = []
        self.competidores_rival = []

    def elegir_deportista_aleatorio(self):
        self.competidores_rival = []
        for i in range(4):
            self.competidores_rival.append(self.delegacion_rival.equipo[random.randint(0, (len(self.delegacion_rival.equipo) - 1))])

    def realizar_competencia(self, deporte):
        # Aquí se ve si la competencia es válida (siguiendo con el flujo de simulación) o si es inválida (cortando el flujo)
        ganador = deporte.validez_de_competencia()
        if ganador == 'seguir':
            return deporte.calcular_ganador()
        else:
            return ganador

    def premiar_deportistas(self, ganador, deporte):
        # Se toma como supuesto que perder por lesión o falta de implementos genera los mismos efectos en los deportistas que perder la competencia en condiciones normales.
        print(f'Premiación {deporte.nombre_deporte}')
        print('')
        if deporte.nombre_deporte == 'natacion':
            nombre_deporte = 'Natación'
        else:
            nombre_deporte = deporte.nombre_deporte.capitalize()
        if ganador == 'empate':
            delegacion_ganadora = 'Empate'
            deportista_ganador = 'Empate'
            print(f'Ha habido un empate en {nombre_deporte}, no hay medallas!')
        elif ganador == 'usuario':
            delegacion_ganadora = deporte.delegacion_usuario.nombre_delegacion
            deportista_ganador = deporte.deportista_usuario.nombre
            print(f'Felicidades {deportista_ganador} de la delegación {delegacion_ganadora}. Has ganado la competencia de {nombre_deporte} del día {self.dia_actual}. \nAquí tienes tu medalla junto a 100 DCCoins de recompensa para tu delegación!')
            deporte.delegacion_usuario.dinero += 100
            deporte.delegacion_usuario.medallas += 1
            deporte.deportista_usuario.moral += 20
            if delegacion_ganadora == 'DCCrotona':
                deporte.deportista_usuario.moral += 20
                deporte.deportista_rival.moral -= 10
            deporte.deportista_rival.moral -= 10
            deporte.delegacion_rival.excelencia_respeto -= 0.02
            self.medallero[delegacion_ganadora][deporte.nombre_deporte] += 1
        elif ganador == 'rival':
            delegacion_ganadora = deporte.delegacion_rival.nombre_delegacion
            deportista_ganador = deporte.deportista_rival.nombre
            print(f'Felicidades {deportista_ganador} de la delegación {delegacion_ganadora}. El rival ha ganado la competencia de {nombre_deporte} del día {self.dia_actual}.')
            deporte.delegacion_rival.dinero += 100
            deporte.delegacion_rival.medallas += 1
            deporte.deportista_rival.moral += 20
            if delegacion_ganadora == 'DCCrotona':
                deporte.deportista_rival.moral += 20
                deporte.deportista_usuario.moral -= 10
            deporte.deportista_usuario.moral -= 10
            deporte.delegacion_usuario.excelencia_respeto -= 0.02
            self.medallero[delegacion_ganadora][deporte.nombre_deporte] += 1
        if nombre_deporte == 'Atletismo':
            self.escribir_resultados(True, False, nombre_deporte, delegacion_ganadora, deportista_ganador)
        elif nombre_deporte == 'Natación':
            self.escribir_resultados(False, True, nombre_deporte, delegacion_ganadora, deportista_ganador)
        else:
            self.escribir_resultados(False, False, nombre_deporte, delegacion_ganadora, deportista_ganador)
        return

    def calcular_nivel_moral(self):
        moral_delegacion_usuario = 0
        moral_delegacion_rival = 0
        conteo = 0
        for atleta in self.delegacion_usuario.equipo:
            moral_delegacion_usuario += atleta.moral
            conteo += 1
        moral_delegacion_usuario = moral_delegacion_usuario / conteo
        conteo = 0
        for atleta in self.delegacion_rival.equipo:
            moral_delegacion_rival += atleta.moral
            conteo += 1
        moral_delegacion_rival = moral_delegacion_rival / conteo
        moral_delegacion_usuario = round(moral_delegacion_usuario, 1)
        moral_delegacion_rival = round(moral_delegacion_rival, 1)
        if self.delegacion_usuario.nombre_delegacion == 'DCCrotona':
            print(f'Moral DCCrotona: {moral_delegacion_usuario}')
            print(f'Moral IEEEsparta: {moral_delegacion_rival}')
            print('')
        else:
            print(f'Moral DCCrotona: {moral_delegacion_rival}')
            print(f'Moral IEEEsparta: {moral_delegacion_usuario}')
            print('')
        self.delegacion_usuario.moral = moral_delegacion_usuario
        self.delegacion_rival.moral = moral_delegacion_rival 
        return

    def elegir_deportista_por_deporte(self):
        self.competidores_usuario = []
        print('Elige un deportista para competir en Atletismo.')
        self.competidores_usuario.append(self.delegacion_usuario.seleccionar_deportista())
        print('')
        print('Elige un deportista para competir en Ciclismo.')
        self.competidores_usuario.append(self.delegacion_usuario.seleccionar_deportista())
        print('')
        print('Elige un deportista para competir en Gimnasia.')
        self.competidores_usuario.append(self.delegacion_usuario.seleccionar_deportista())
        print('')
        print('Elige un deportista para competir en Natación.')
        self.competidores_usuario.append(self.delegacion_usuario.seleccionar_deportista())
        print('')

    def mostrar_estado(self):
        # Fuente métodos de formato: https://uniwebsidad.com/libros/python/capitulo-6/metodos-de-formato
        print('*** ESTADO DE LAS DELEGACIONES Y SUS DEPORTISTAS ***'.center(120, ' '))
        print('-' * 120)
        for deleg in [self.delegacion_usuario, self.delegacion_rival]:
            print(deleg.nombre_delegacion)
            print(f'Entrenador: {deleg.entrenador.nombre}')
            print(f'Moral del equipo: {deleg.moral}')
            print(f'Medallas: {deleg.medallas}')
            print(f'Dinero: {deleg.dinero}')
            print('')
            print(f'Excelencia y respeto: {deleg.excelencia_respeto}')
            print(f'Implementos deportivos: {deleg.implementos_deportivos}')
            print(f'Implementos médicos: {deleg.implementos_medicos}')
            print('')
            print('EQUIPO DEPORTIVO:')
            deleg.mostrar_equipo(False)
            print('*' * 120)
        print('')
        print(f'Día: {self.dia_actual}')
        print('')
        medallas_atletismo = [self.medallero['IEEEsparta']['atletismo'], self.medallero['DCCrotona']['atletismo']]
        medallas_ciclismo = [self.medallero['IEEEsparta']['ciclismo'], self.medallero['DCCrotona']['ciclismo']]
        medallas_gimnasia = [self.medallero['IEEEsparta']['gimnasia'], self.medallero['DCCrotona']['gimnasia']]
        medallas_natacion = [self.medallero['IEEEsparta']['natacion'], self.medallero['DCCrotona']['natacion']]
        print('MEDALLERO')
        print('Deporte     |  IEEEsparta  |  DCCrotona')
        print(f'Atletismo      {str(medallas_atletismo[0]):10.10s}     {str(medallas_atletismo[1]):10.10s}')
        print(f'Ciclismo       {str(medallas_ciclismo[0]):10.10s}     {str(medallas_ciclismo[1]):10.10s}')
        print(f'Gimnasia       {str(medallas_gimnasia[0]):10.10s}     {str(medallas_gimnasia[1]):10.10s}')
        print(f'Natación       {str(medallas_natacion[0]):10.10s}     {str(medallas_natacion[1]):10.10s}')
        print('-' * 120)

    def escribir_resultados(self, primer_deporte_dia, ultimo_deporte_dia, competencia, delegacion_ganadora, deportista_ganador):
        path = os.path.join(par.PATH_RESULTADOSTXT)
        with open(path, 'a') as archivo:
            if primer_deporte_dia:
                archivo.write(f'Día: {self.dia_actual}\n\n')
            archivo.write(f'Competencia: {competencia}\n')
            archivo.write(f'Delegación Ganadora: {delegacion_ganadora}\n')
            archivo.write(f'Deportista Ganador: {deportista_ganador}\n\n')
            if ultimo_deporte_dia:
                archivo.write(f'***************************************\n')

    def mostrar_resultado(self):
        print('*** RESULTADOS DCCUMBRE OLÍMPICA ***')
        print('')
        medallas_atletismo = [self.medallero['IEEEsparta']['atletismo'], self.medallero['DCCrotona']['atletismo']]
        medallas_ciclismo = [self.medallero['IEEEsparta']['ciclismo'], self.medallero['DCCrotona']['ciclismo']]
        medallas_gimnasia = [self.medallero['IEEEsparta']['gimnasia'], self.medallero['DCCrotona']['gimnasia']]
        medallas_natacion = [self.medallero['IEEEsparta']['natacion'], self.medallero['DCCrotona']['natacion']]
        print('Deporte     |  IEEEsparta  |  DCCrotona')
        print(f'Atletismo      {str(medallas_atletismo[0]):10.10s}     {str(medallas_atletismo[1]):10.10s}')
        print(f'Ciclismo       {str(medallas_ciclismo[0]):10.10s}     {str(medallas_ciclismo[1]):10.10s}')
        print(f'Gimnasia       {str(medallas_gimnasia[0]):10.10s}     {str(medallas_gimnasia[1]):10.10s}')
        print(f'Natación       {str(medallas_natacion[0]):10.10s}     {str(medallas_natacion[1]):10.10s}')
        for delegacion in [self.delegacion_usuario, self.delegacion_rival]:
            if delegacion.nombre_delegacion == 'DCCrotona':
                if medallas_atletismo[1] + medallas_ciclismo[1] + medallas_gimnasia[1] + medallas_natacion[1] != delegacion.medallas:
                    print(f'Superpoder     {str(0):10.10s}     {str(1):10.10s}')
        print('')
        print(f'Total medallas {self.delegacion_rival.nombre_delegacion}: {self.delegacion_rival.medallas}')
        print(f'Total medallas {self.delegacion_usuario.nombre_delegacion}: {self.delegacion_usuario.medallas}')
        print('')
        if self.delegacion_usuario.medallas < self.delegacion_rival.medallas:
            print(f'Oh no! Has perdido contra {self.delegacion_usuario.entrenador.nombre}. Intenta nuevamente!')
        elif self.delegacion_usuario.medallas > self.delegacion_rival.medallas:
            print(f'Felicidades {self.delegacion_usuario.entrenador.nombre}! Has ganado la DCCumbre con la delegación {self.delegacion_usuario.nombre_delegacion}.')
        else:
            print('Empate! Deberás volver a simular la DCCumbre para desempatar!')
        return
        

class Mercado:

    def __init__(self, deportistas_disponibles):
        self.deportistas_disponibles = deportistas_disponibles
        self.lista_nombres = []

    def ofrecer_deportistas(self):
        print('*** DEPORTISTAS DISPOMIBLES ***')
        print('')
        print('INDICE:  NOMBRE:               VELOCIDAD:  RESISTENCIA:  FLEXIBILIDAD:  MORAL:  LESIONADO:  PRECIO:')
        indice = 0
        self.lista_nombres = []
        for deportista in self.deportistas_disponibles:
            print(f'{indice: ^7d}  {str(self.deportistas_disponibles[deportista].nombre):20.20s}  {str(self.deportistas_disponibles[deportista].velocidad):5.5s}       {str(self.deportistas_disponibles[deportista].resistencia):5.5s}         {str(self.deportistas_disponibles[deportista].flexibilidad):5.5s}          {str(self.deportistas_disponibles[deportista].moral):5.5s}   {str(self.deportistas_disponibles[deportista].lesionado):5.5s}       {str(self.deportistas_disponibles[deportista].precio):5.5s}')
            indice += 1
            self.lista_nombres.append(deportista)
        print('')

    def seleccionar_deportista(self):
        seleccionado = False
        while not seleccionado:
            try:
                entrada = input('Ingresa el indice del deportista que deseas comprar: ').strip(' ')
                print('')
                deportista = self.lista_nombres[int(entrada)]
                seleccionado = True
            except TypeError:
                print('Recuerda que el indice debe ser un número. Intenta nuevamente.')
            except IndexError:
                print('Indice incorrecto. Intente nuevamente.')
        return self.deportistas_disponibles[deportista]

    def deportista_vendido(self, deportista):
        del self.deportistas_disponibles[deportista.nombre]
        return












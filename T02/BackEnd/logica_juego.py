from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QThread
import time
import threading
import parametros as par
import random

class Juego(QObject):
    senal_definir_nombre = pyqtSignal(str)
    senal_def_cancion_dificultad = pyqtSignal(str, str)
    senal_iniciar_ronda = pyqtSignal()
    senal_crear_flechas = pyqtSignal(int, list, list, int)
    senal_terminar_ronda = pyqtSignal()
    senal_recibir_flecha = pyqtSignal(int, int, int, int)
    senal_flecha_hielo_inicio = pyqtSignal()
    senal_flecha_hielo_fin = pyqtSignal()
    senal_flecha_perdida = pyqtSignal(int)
    senal_actualizar_combo = pyqtSignal(int)
    senal_actualizar_aceptacion = pyqtSignal(int)
    senal_reiniciar_ronda = pyqtSignal()
    senal_interseccion_fallida = pyqtSignal(str)
    senal_resumen_ronda = pyqtSignal(int, int, int, int, int, bool)
    senal_actualizar_dinero = pyqtSignal(int)
    senal_comprar_pinguino = pyqtSignal()
    senal_actualizar_paso = pyqtSignal(list)
    senal_cerrar_partida = pyqtSignal(str, int)
    senal_actualizar_progreso = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        self.cancion = None
        self.dificultad = None
        self.nombre = None
        self.puntaje = 0
        self.__dinero = par.VALOR_PINGUINOS
        self.__combo = 0
        self.mayor_combo = 0
        self.senal_definir_nombre.connect(self.definir_nombre)
        self.senal_def_cancion_dificultad.connect(self.definir_cancion_dificultad)
        self.senal_iniciar_ronda.connect(self.ronda)
        self.timer_crea_flechas = QTimer(self)
        self.timer_terminar_ronda = QTimer(self)
        self.timer_crea_flechas.timeout.connect(self.numero_flechas)
        self.senal_recibir_flecha.connect(self.recibir_flecha)
        self.timer_flecha_hielo = QTimer(self)
        self.senal_flecha_perdida.connect(self.flecha_perdida)
        self.timer_reiniciar_ronda = QTimer(self)
        self.timer_reiniciar_ronda.timeout.connect(self.reiniciar_ronda)
        self.pasos_fallados = []
        self.flechas_recibidas = []
        self.id_paso_actual = 0
        self.senal_reiniciar_ronda.connect(self.reiniciar_ronda)
        self.__aprobacion = 0
        self.senal_interseccion_fallida.connect(self.esperar_timer)
        self.intersecciones_fallidas = 0
        self.timer_esperar_falla = QTimer(self)
        self.timer_esperar_falla.timeout.connect(self.esperar_falla)
        self.esperando_falla = False
        self.timer_flecha_a = QTimer(self)
        self.timer_flecha_a.timeout.connect(self.flecha_a_reiniciar)
        self.timer_flecha_w = QTimer(self)
        self.timer_flecha_w.timeout.connect(self.flecha_w_reiniciar)
        self.timer_flecha_s = QTimer(self)
        self.timer_flecha_s.timeout.connect(self.flecha_s_reiniciar)
        self.timer_flecha_d = QTimer(self)
        self.timer_flecha_d.timeout.connect(self.flecha_d_reiniciar)
        self.timer_pasos_vacios = QTimer(self)
        self.timer_pasos_vacios.timeout.connect(self.reiniciar_pasos_vacios)
        self.flecha_a_recibida = False
        self.flecha_w_recibida = False
        self.flecha_s_recibida = False
        self.flecha_d_recibida = False
        self.paso_vacio_recibido = False
        self.pasos_vacios = 0
        self.timer_pasos_vacios.setInterval(par.TIEMPO_ESPERA_FALLA)
        self.timer_esperar_falla.setInterval(par.TIEMPO_ESPERA_FALLA)
        self.timer_flecha_a.setInterval(par.TIEMPO_ESPERA_FALLA)
        self.timer_flecha_w.setInterval(par.TIEMPO_ESPERA_FALLA)
        self.timer_flecha_s.setInterval(par.TIEMPO_ESPERA_FALLA)
        self.timer_flecha_d.setInterval(par.TIEMPO_ESPERA_FALLA)
        self.puntaje_acumulado = 0
        self.pasos_incorrectos = 0
        self.esperar = QTimer(self)
        self.esperar.setInterval(1)
        self.esperar.timeout.connect(self.interseccion_fallida)
        self.esperar2 = QTimer(self)
        self.esperar2.setInterval(1500)
        self.esperar2.timeout.connect(self.reiniciar_ronda_2)
        self.senal_comprar_pinguino.connect(self.comprar_pinguino)
        self.correctos = 0
        self.cantidades_pasos = []
        self.direcciones = []
        self.duracion = 0
        self.timer_progreso = QTimer(self)
        self.conteo_progreso = 0

    @property
    def combo(self):
        return self.__combo
    
    @combo.setter
    def combo(self, valor):
        self.__combo = valor
        if valor > self.mayor_combo:
            self.mayor_combo = valor
        self.senal_actualizar_combo.emit(valor)

    @property
    def aprobacion(self):
        return self.__aprobacion

    @aprobacion.setter
    def aprobacion(self, valor):
        if valor < 0:
            self.__aprobacion = 0
        else:
            self.__aprobacion = valor
        self.senal_actualizar_aceptacion.emit(self.aprobacion)

    @property
    def dinero(self):
        return self.__dinero

    @dinero.setter
    def dinero(self, valor):
        if valor >= 0:
            self.__dinero = valor
            self.senal_actualizar_dinero.emit(self.dinero)

    def definir_nombre(self, nombre):
        self.nombre = nombre
        print(f"nombre usuario = {self.nombre}")

    def definir_cancion_dificultad(self, i_cancion, i_dificultad):
        self.cancion = i_cancion
        if i_dificultad == "Principiante":
            self.dificultad = 0
        elif i_dificultad == "Aficionado":
            self.dificultad = 1
        else:
            self.dificultad = 2
        print(self.cancion, self.dificultad)

    def ronda(self):
        self.timer_crea_flechas.setInterval(1000*(1 - 0.25*self.dificultad))
        self.timer_crea_flechas.start()
        self.duracion = (par.DURACION_RONDA + self.dificultad*par.DURACION_EXTRA_POR_DIFICULTAD)*1000
        self.timer_terminar_ronda.setInterval(self.duracion)
        self.timer_terminar_ronda.timeout.connect(self.terminar_ronda)
        self.timer_terminar_ronda.start()
        self.timer_progreso.setInterval(1000)
        self.timer_progreso.timeout.connect(self.progreso)
        self.timer_progreso.start()

    def progreso(self):
        self.conteo_progreso += 1000
        self.senal_actualizar_progreso.emit((self.conteo_progreso/self.duracion)*100)
        if self.conteo_progreso == self.duracion:
            self.timer_progreso.stop()

    def terminar_ronda(self):
        print("RONDA TERMINADA")
        self.timer_crea_flechas.stop()
        self.timer_terminar_ronda.stop()

    def reiniciar_ronda(self):
        self.senal_terminar_ronda.emit()
        self.esperar_timer2()
        self.calcular_aceptacion()

    def reiniciar_ronda_2(self):
        self.esperar2.stop()
        self.resumen_ronda()
        print(f"MAYOR COMBO: {self.mayor_combo}")
        self.mayor_combo = 0
        self.combo = 0
        self.pasos_fallados = []
        self.intersecciones_fallidas = 0
        self.pasos_vacios = 0
        self.id_paso_actual = 0
        self.aprobacion = 0
        self.pasos_incorrectos = 0
        self.correctos = 0
        self.cantidades_pasos = []
        self.direcciones = []
        self.flechas_recibidas = []
        self.puntaje = 0
        self.conteo_progreso = 0

    def numero_flechas(self):
        if self.dificultad == 0:
            self.crear_flechas(1)
        elif self.dificultad == 1:
            probabilidad = random.random()
            if par.PROB_2_FLECHAS < probabilidad:
                self.crear_flechas(2)
            else:
                self.crear_flechas(1)
        elif self.dificultad == 2:
            probabilidad = random.random()
            if par.PROB_2_FLECHAS < probabilidad:
                self.crear_flechas(2)
            elif par.PROB_3_FLECHAS < probabilidad:
                self.crear_flechas(3)
            else:
                self.crear_flechas(1)

    def crear_flechas(self, cantidad):
        direccion = []
        tipo = []
        for _ in range(cantidad):
            direccion.append(random.randint(0, 3))
            prob_tipo = random.random()
            if prob_tipo < par.PROB_NORMAL:
                tipo.append(0)
            elif prob_tipo < (par.PROB_NORMAL + par.PROB_FLECHA_X2):
                tipo.append(1)
            elif prob_tipo < (
                par.PROB_NORMAL + par.PROB_FLECHA_X2 + par.PROB_FLECHA_HIELO):
                tipo.append(2)
            else:
                tipo.append(3)
        self.senal_crear_flechas.emit(cantidad, direccion, tipo, self.id_paso_actual)
        self.id_paso_actual += 1
    
    def recibir_flecha(self, tipo, id_flecha, direccion, cantidad_paso):
        if tipo == 0:
            self.puntaje += par.PUNTOS_FLECHA
        elif tipo == 1:
            self.puntaje += par.PUNTOS_FLECHA*2
        elif tipo == 2:
            self.puntaje += par.PUNTOS_FLECHA
            self.flecha_hielo()
        elif tipo == 3:
            self.puntaje += par.PUNTOS_FLECHA*10
        self.combo += 1
        if direccion == 0:
            self.flecha_a_recibida = True
            self.timer_flecha_a.start()
        elif direccion == 1:
            self.flecha_w_recibida = True
            self.timer_flecha_w.start()
        elif direccion == 2:
            self.flecha_s_recibida = True
            self.timer_flecha_s.start()
        elif direccion == 3:
            self.flecha_d_recibida = True
            self.timer_flecha_d.start()
        self.esperando_falla = True
        self.timer_esperar_falla.start()
        self.flechas_recibidas.append(id_flecha)
        self.cantidades_pasos.append(cantidad_paso)
        self.direcciones.append(direccion)
        self.calcular_aceptacion()

    def esperar_falla(self):
        self.esperando_falla = False
        self.timer_esperar_falla.stop()

    def calcular_aceptacion(self):
        if self.id_paso_actual == 0:
            return
        fallados = 0
        correctos = 0
        id_max_recibidas = 0
        id_max_fallados = 0
        if self.flechas_recibidas:
            id_max_recibidas = max(self.flechas_recibidas)
        if self.pasos_fallados:
            id_max_fallados = max(self.pasos_fallados)
        id_max = max(id_max_fallados, id_max_recibidas)
        for indice in range(id_max + 1):
            if indice in self.pasos_fallados:
                fallados += 1
            else:
                correctos += 1
        self.aprobacion = 100*(
            (correctos - fallados - 2*self.intersecciones_fallidas)/(self.id_paso_actual))
        self.aprobacion = int(self.aprobacion)
        self.pasos_incorrectos = fallados + self.intersecciones_fallidas
        if correctos > self.correctos:
            if len(self.cantidades_pasos) == 0:
                paso_completo = False
            else:
                cantidad_paso = self.cantidades_pasos[-1]
                paso_completo = True
                for _ in range(cantidad_paso):
                    if len(self.cantidades_pasos) == 0:
                        paso_completo = False
                    else:
                        if self.cantidades_pasos.pop() != cantidad_paso:
                            paso_completo = False
            if paso_completo:
                direcciones = []
                for _ in range(cantidad_paso):
                    direcciones.append(self.direcciones.pop())
                self.senal_actualizar_paso.emit(direcciones)
        self.correctos = correctos

    def flecha_hielo(self):
        self.timer_flecha_hielo.setInterval(0.2*par.DURACION_RONDA*1000)
        self.timer_flecha_hielo.timeout.connect(
            self.fin_flecha_hielo)
        self.senal_flecha_hielo_inicio.emit()
        self.timer_flecha_hielo.start()
        
    def fin_flecha_hielo(self):
        self.senal_flecha_hielo_fin.emit()
        self.timer_flecha_hielo.stop()

    def flecha_perdida(self, id_paso):
        self.combo = 0
        if id_paso not in self.pasos_fallados:
            self.pasos_fallados.append(id_paso)
            self.calcular_aceptacion()

    def interseccion_fallida(self):
        self.esperar.stop()
        interseccion = self.interseccion
        if not self.esperando_falla:
            if not self.paso_vacio_recibido:
                self.pasos_vacios += 1
                self.paso_vacio_recibido = True
                self.timer_pasos_vacios.start()
                print(f"PASOS VACIOS: {self.pasos_vacios}")
            return
        elif interseccion == "a":
            if self.flecha_a_recibida:
                return
            else:
                self.intersecciones_fallidas += 1
        elif interseccion == "w":
            if self.flecha_w_recibida:
                return
            else:
                self.intersecciones_fallidas += 1
        elif interseccion == "s":
            if self.flecha_s_recibida:
                return
            else:
                self.intersecciones_fallidas += 1
        elif interseccion == "d":
            if self.flecha_d_recibida:
                return
            else:
                self.intersecciones_fallidas += 1
        print(f"INTERSECCIONES FALLIDAS: {self.intersecciones_fallidas}")
        self.esperando_falla = False
        
    def flecha_a_reiniciar(self):
        self.flecha_a_recibida = False
        self.timer_flecha_a.stop()

    def flecha_w_reiniciar(self):
        self.flecha_w_recibida = False
        self.timer_flecha_w.stop()

    def flecha_s_reiniciar(self):
        self.flecha_s_recibida = False
        self.timer_flecha_s.stop()

    def flecha_d_reiniciar(self):
        self.flecha_d_recibida = False
        self.timer_flecha_d.stop()

    def reiniciar_pasos_vacios(self):
        self.paso_vacio_recibido = False
        self.timer_pasos_vacios.stop()

    def resumen_ronda(self):
        self.puntaje = self.mayor_combo*self.puntaje
        self.puntaje_acumulado += self.puntaje
        self.dinero += self.puntaje
        if self.dificultad == 0:
            aprobado = (par.REQUISITO_PRINCIPIANTE <= self.aprobacion)
        elif self.dificultad == 1:
            aprobado = ((par.REQUISITO_PRINCIPIANTE + 20) <= self.aprobacion)
        else:
            aprobado = ((par.REQUISITO_PRINCIPIANTE + 40) <= self.aprobacion)
        self.senal_resumen_ronda.emit(
            self.puntaje, self.puntaje_acumulado, self.mayor_combo,
            self.pasos_incorrectos, self.aprobacion, aprobado)

    def esperar_timer(self, interseccion):
        self.esperar.start()
        self.interseccion = interseccion

    def esperar_timer2(self):
        self.esperar2.start()

    def comprar_pinguino(self):
        self.dinero -= par.VALOR_PINGUINOS

    def mon(self):
        self.dinero += par.DINERO_TRAMPA
    
    def niv(self):
        if self.timer_terminar_ronda.isActive():
            self.terminar_ronda()

    def salir(self):
        self.senal_cerrar_partida.emit(self.nombre, self.puntaje_acumulado)




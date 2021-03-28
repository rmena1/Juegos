from PyQt5.QtCore import pyqtSignal, QObject


class LogicaCliente(QObject):

    enviar_cantidad_jugadores = pyqtSignal(int)
    actualizar_nombres_sala_espera = pyqtSignal(str, str)
    comenzar_partida = pyqtSignal(list)
    senal_enviar_vertices = pyqtSignal(dict)
    senal_enviar_hexagonos = pyqtSignal(dict)
    senal_enviar_dados = pyqtSignal(int, int)
    senal_enviar_colores = pyqtSignal(dict)
    senal_enviar_adyacencia = pyqtSignal(dict)
    senal_enviar_numeros_hex = pyqtSignal(dict)
    senal_ubicar_carretera_propia = pyqtSignal(int, str)
    senal_ubicar_carretera_ajena = pyqtSignal(int, str, str)
    senal_ubicar_choza_propia = pyqtSignal(int)
    senal_ubicar_choza_ajena = pyqtSignal(int, str)
    senal_comenzar_turno = pyqtSignal()
    senal_enviar_turno = pyqtSignal(str)
    senal_recibir_materia = pyqtSignal(str, int)
    senal_recibio_materia = pyqtSignal(str, str, str)
    senal_carretera_invalida = pyqtSignal()
    senal_choza_invalida = pyqtSignal()
    senal_transacc_inv = pyqtSignal()
    senal_solicit_aprov_interc = pyqtSignal(str, str, str, str, str)
    senal_intercambio_rechazado = pyqtSignal(str)
    senal_intercambio_realizado = pyqtSignal(str, str, str, str, str, str)
    senal_juego_terminado = pyqtSignal(str)
    senal_enviar_puntos = pyqtSignal(str, str)
    senal_enviar_carretera_larga = pyqtSignal(str, str)
    senal_carta_victoria = pyqtSignal()
    senal_carta_monopolio = pyqtSignal()
    senal_carta_desarrollo_invalida = pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.cliente = parent
        self.cantidad_jugadores = 4
        self.nombre = None
        self.lista_nombres = []

    def procesar_mensaje(self, mensaje):
        contador = 0
        for caracter in mensaje:
            if caracter == ":":
                break
            contador += 1
        clave = mensaje[: contador]
        mensaje = mensaje[contador + 1:]
        
        return self.manejar_mensaje(clave, mensaje)

    def manejar_mensaje(self, clave, mensaje):
        if clave == "Nombre":
            self.nombre = mensaje
            self.actualizar_nombres_sala_espera.emit(self.nombre, "es_cliente")
            return "ok"
        elif clave == "Critico":
            if mensaje == "maximo_excedido":
                print("LOG: Máximo excedido, conexión a server rechazada...")
                return "maximo_excedido"
        elif clave == "Cantidad":
            cantidad = int(mensaje)
            self.cantidad_jugadores = cantidad
            self.enviar_cantidad_jugadores.emit(cantidad)
            return "ok"
        elif clave == "Actualizar_VI":
            self.actualizar_nombres_sala_espera.emit(mensaje, "no_cliente")
            return "ok"
        elif clave == "Eliminar_jugador":
            self.actualizar_nombres_sala_espera.emit(mensaje, "eliminar")
            return "ok"
        elif clave == "Comenzar":
            mensaje = mensaje.split(",")
            self.lista_nombres = mensaje
            self.comenzar_partida.emit(self.lista_nombres)
            return "ok"
        elif clave == "vertices":
            return "recibir_pickle_v"
        elif clave == "hexagonos":
            return "recibir_pickle_h"
        elif clave == "dados":
            self.senal_enviar_dados.emit(int(mensaje[0]), int(mensaje[1]))
            return "ok"
        elif clave == "colores":
            return "recibir_pickle_c"
        elif clave == "adyacencia":
            return "recibir_pickle_a"
        elif clave == "numeros_hexagonos":
            return "recibir_pickle_n"
        elif clave == "choza_propia":
            self.senal_ubicar_choza_propia.emit(int(mensaje))
        elif clave == "choza":
            choza = int(mensaje[:2])
            color = mensaje[3:]
            self.senal_ubicar_choza_ajena.emit(choza, color)
        elif clave == "carretera_propia":
            angulo = self.definir_angulo(int(mensaje))
            self.senal_ubicar_carretera_propia.emit(int(mensaje), angulo)
        elif clave == "carretera":
            carretera = int(mensaje[:2])
            color = mensaje[3:]
            angulo = self.definir_angulo(carretera)
            self.senal_ubicar_carretera_ajena.emit(carretera, color, angulo)
        elif clave == "empezar_turno":
            self.senal_comenzar_turno.emit()
        elif clave == "turno_de":
            self.senal_enviar_turno.emit(mensaje)
        elif clave == "recibir":
            materia, cantidad = self.procesar_recibir(mensaje)
            self.senal_recibir_materia.emit(materia, int(cantidad))
        elif clave == "recibio":
            print("ENVIAR MATERIA")
            materia, datos = self.procesar_recibir(mensaje)
            nombre, cantidad = self.procesar_recibir(datos)
            self.senal_recibio_materia.emit(materia, cantidad, nombre)
        elif clave == "choza_invalida":
            self.senal_choza_invalida.emit()
        elif clave == "carretera_invalida":
            self.senal_carretera_invalida.emit()
        elif clave == "transacc_inv":
            self.senal_transacc_inv.emit()
        elif clave == "sol_aprov_int":
            emisario, mensaje = self.procesar_recibir(mensaje)
            ofrece, mensaje = self.procesar_recibir(mensaje)
            cant_o, mensaje = self.procesar_recibir(mensaje)
            pide, cant_p = self.procesar_recibir(mensaje)
            self.senal_solicit_aprov_interc.emit(
                emisario, ofrece, cant_o, pide, cant_p)
        elif clave == "interc_realiz":
            emisario, mensaje = self.procesar_recibir(mensaje)
            destinatario, mensaje = self.procesar_recibir(mensaje)
            ofrece, mensaje = self.procesar_recibir(mensaje)
            cant_o, mensaje = self.procesar_recibir(mensaje)
            pide, cant_p = self.procesar_recibir(mensaje)
            self.senal_intercambio_realizado.emit(emisario, destinatario, ofrece, cant_o, pide, cant_p)
        elif clave == "intercambio_rechazado":
            self.senal_intercambio_rechazado.emit(mensaje)
        elif clave == "juego_terminado":
            self.senal_juego_terminado.emit(mensaje)
        elif clave == "puntos":
            jugador, puntos = self.procesar_recibir(mensaje)
            self.senal_enviar_puntos.emit(jugador, puntos)
        elif clave == "carretera_larga":
            jugador, largo = self.procesar_recibir(mensaje)
            self.senal_enviar_carretera_larga.emit(jugador, str(largo))
        elif clave == "victoria":
            self.senal_carta_victoria.emit()
        elif clave == "monopolio":
            self.senal_carta_monopolio.emit()
        elif clave == "carta_des_inv":
            self.senal_carta_desarrollo_invalida.emit()


        return "ok"

    def enviar_vertices(self, vertices):
        self.senal_enviar_vertices.emit(vertices)

    def enviar_hexagonos(self, hexagonos):
        self.senal_enviar_hexagonos.emit(hexagonos)

    def lanzar_dados(self):
        self.cliente.enviar_mensaje("lanzar_dados:None")
    
    def enviar_colores(self, colores):
        self.senal_enviar_colores.emit(colores)

    def enviar_adyacencia(self, adyacencia):
        self.senal_enviar_adyacencia.emit(adyacencia)
    
    def enviar_numero_hex(self, hexagonos):
        self.senal_enviar_numeros_hex.emit(hexagonos)

    def definir_angulo(self, carretera):
        grad_0 = [0, 3, 7, 10, 13, 16, 21, 24, 27, 30, 35, 38, 40, 41]
        grad_60 = [1, 4, 8, 11, 14, 17, 19, 22, 25, 28, 31, 33, 36, 39]
        if carretera in grad_0:
            return "0"
        elif carretera in grad_60:
            return "1"
        else:
            return "2"

    def terminar_turno(self):
        self.cliente.enviar_mensaje("terminar_turno")

    def procesar_recibir(self, mensaje):
        contador = 0
        for caracter in mensaje:
            if caracter == ":":
                break
            contador += 1
        materia = mensaje[: contador]
        cantidad = mensaje[contador + 1:]
        return materia, cantidad

    def solicitar_choza(self, nombre, indice):
        self.cliente.enviar_mensaje(f"solicitar_choza:{nombre}:{indice}")

    def solicitar_carretera(self, nombre, indice):
        self.cliente.enviar_mensaje(f"solicitar_carretera:{nombre}:{indice}")

    def solicitar_intercambio(self, emisario, destinatario, ofrece, cant_o, pide, cant_p):
        self.cliente.enviar_mensaje(
            f"sol_interc:{emisario}:{destinatario}:{ofrece}:{cant_o}:{pide}:{cant_p}")
    
    def realizar_intercambio(self, emisario, destinatario, ofrece, cant_o, pide, cant_p):
        self.cliente.enviar_mensaje(
            f"real_interc:{emisario}:{destinatario}:{ofrece}:{cant_o}:{pide}:{cant_p}")

    def rechazar_intercambio(self, ofrece, rechaza):
        self.cliente.enviar_mensaje(f"rechaz_interc:{ofrece}:{rechaza}")

    def pedir_carta_desarrollo(self):
        self.cliente.enviar_mensaje(f"carta_desarrollo:None")

    def monopolio(self, materia):
        self.cliente.enviar_mensaje(f"monopolio:{materia}")




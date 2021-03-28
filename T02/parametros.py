PATH_LOGO = ["FrontEnd", "sprites", "logo.png"]
ALTURA_VENTANA_INICIO = 350
ANCHO_VENTANA_INICIO = 500
PATH_PUFFLE_RANKING = ["FrontEnd", "sprites", "puffles", "puffle_06.png"]
ALTURA_VENTANA_JUEGO = 650
ANCHO_VENTANA_JUEGO = 1000
PATH_PISTA_BAILE = ["FrontEnd", "sprites", "fondos", "fondo.png"]
VALOR_PINGUINOS = 500
PATH_PINGUINOS = {
    "PINGUI_ROJO_NEUTRO" : ["FrontEnd", "sprites", "pinguirin_rojo", "rojo_neutro.png"],
    "PINGUI_AZUL_NEUTRO" : ["FrontEnd", "sprites", "pinguirin_celeste", "celeste_neutro.png"],
    "PINGUI_AMAR_NEUTRO" : ["FrontEnd", "sprites", "pinguirin_amarillo", "amarillo_neutro.png"],
    "PINGUI_MORA_NEUTRO" : ["FrontEnd", "sprites", "pinguirin_morado", "morado_neutro.png"],
    "PINGUI_VERD_NEUTRO" : ["FrontEnd", "sprites", "pinguirin_verde", "verde_neutro.png"]
}
VELOCIDAD_FLECHA = 10
PUNTOS_FLECHA = 3
PATH_FLECHAS = {
    "IZQUIERDA" : ["FrontEnd", "sprites", "flechas", "left_1.png"],
    "DERECHA" : ["FrontEnd", "sprites", "flechas", "right_1.png"],
    "ARRIBA" : ["FrontEnd", "sprites", "flechas", "up_1.png"],
    "ABAJO" : ["FrontEnd", "sprites", "flechas", "down_1.png"],
    "IZQUIERDA_X2" : ["FrontEnd", "sprites", "flechas", "left_4.png"],
    "DERECHA_X2" : ["FrontEnd", "sprites", "flechas", "right_4.png"],
    "ARRIBA_X2" : ["FrontEnd", "sprites", "flechas", "up_4.png"],
    "ABAJO_X2" : ["FrontEnd", "sprites", "flechas", "down_4.png"],
    "IZQUIERDA_H" : ["FrontEnd", "sprites", "flechas", "left_8.png"],
    "DERECHA_H" : ["FrontEnd", "sprites", "flechas", "right_8.png"],
    "ARRIBA_H" : ["FrontEnd", "sprites", "flechas", "up_8.png"],
    "ABAJO_H" : ["FrontEnd", "sprites", "flechas", "down_8.png"],
    "IZQUIERDA_D" : ["FrontEnd", "sprites", "flechas", "left_2.png"],
    "DERECHA_D" : ["FrontEnd", "sprites", "flechas", "right_2.png"],
    "ARRIBA_D" : ["FrontEnd", "sprites", "flechas", "up_2.png"],
    "ABAJO_D" : ["FrontEnd", "sprites", "flechas", "down_2.png"]
}
DURACION_RONDA = 30
DURACION_EXTRA_POR_DIFICULTAD = 15
PROB_NORMAL = 0.8
PROB_FLECHA_X2 = 0.1
PROB_FLECHA_DORADA = 0.02
PROB_FLECHA_HIELO = 0.08
PROB_2_FLECHAS = 0.4
PROB_3_FLECHAS = 0.3
VELOCIDAD_FLECHA = 100
ALTO_FLECHA = 30
ALTO_CAPTURA = 45
PATH_CANCIONES = {
    "TEMA_1" : ["FrontEnd", "songs", "cancion_1.wav"],
    "TEMA_2" : ["FrontEnd", "songs", "cancion_2.wav"]
}
TIEMPO_ESPERA_FALLA = 350
REQUISITO_PRINCIPIANTE = 30
PATH_BAILES_PINGUINOS = {}
colores = ["amarillo", "celeste", "verde", "morado", "rojo"]
for color in colores:
    PATH_BAILES_PINGUINOS[f"{color.upper()}_ABAJO_DERECHA"] = [
        "FrontEnd", "sprites", f"pinguirin_{color}", f"{color}_abajo_derecha.png"]
    PATH_BAILES_PINGUINOS[f"{color.upper()}_ABAJO_IZQUIERDA"] = [
        "FrontEnd", "sprites", f"pinguirin_{color}", f"{color}_abajo_izquierda.png"]
    PATH_BAILES_PINGUINOS[f"{color.upper()}_ABAJO"] = [
        "FrontEnd", "sprites", f"pinguirin_{color}", f"{color}_abajo.png"]
    PATH_BAILES_PINGUINOS[f"{color.upper()}_ARRIBA_DERECHA"] = [
        "FrontEnd", "sprites", f"pinguirin_{color}", f"{color}_arriba_derecha.png"]
    PATH_BAILES_PINGUINOS[f"{color.upper()}_ARRIBA_IZQUIERDA"] = [
        "FrontEnd", "sprites", f"pinguirin_{color}", f"{color}_arriba_izquierda.png"]
    PATH_BAILES_PINGUINOS[f"{color.upper()}_ARRIBA"] = [
        "FrontEnd", "sprites", f"pinguirin_{color}", f"{color}_arriba.png"]
    PATH_BAILES_PINGUINOS[f"{color.upper()}_DERECHA"] = [
        "FrontEnd", "sprites", f"pinguirin_{color}", f"{color}_derecha.png"]
    PATH_BAILES_PINGUINOS[f"{color.upper()}_IZQUIERDA"] = [
        "FrontEnd", "sprites", f"pinguirin_{color}", f"{color}_izquierda.png"]
    PATH_BAILES_PINGUINOS[f"{color.upper()}_TRES_FLECHAS"] = [
        "FrontEnd", "sprites", f"pinguirin_{color}", f"{color}_tres_flechas.png"]

DINERO_TRAMPA = 5000
PATH_RESULTADOS = "resultados.txt"


import os
import parametros as par
from campeonato import Mercado
from delegaciones import IEEEsparta, DCCrotona
from entrenador import Entrenador
from deportistas_deportes import Deportista

def cargar_delegaciones():
    path = os.path.join(par.PATH_DELEGACIONES)
    with open(path, 'rt') as archivo:
        lineas = archivo.readlines()
        llaves = lineas.pop(0)
        llaves = llaves.strip('\n').split(',')
        primera_delegacion = {llaves[0]:'', llaves[1]:'', llaves[2]:'', llaves[3]:'', llaves[4]:''}
        segunda_delegacion = {llaves[0]:'', llaves[1]:'', llaves[2]:'', llaves[3]:'', llaves[4]:''}
        primera_linea = lineas[0].strip('\n').split(',')
        segunda_linea = lineas[1].strip('\n').split(',')
        conteo = 0
        for llave in llaves:
            primera_delegacion[llave] = primera_linea[conteo]
            segunda_delegacion[llave] = segunda_linea[conteo]
            conteo += 1
        primera_delegacion['Equipo'] = primera_delegacion['Equipo'].split(';')
        segunda_delegacion['Equipo'] = segunda_delegacion['Equipo'].split(';')
        primera_delegacion = {primera_delegacion['Delegacion']:primera_delegacion}
        segunda_delegacion = {segunda_delegacion['Delegacion']:segunda_delegacion}
    return primera_delegacion, segunda_delegacion

def cargar_deportistas():
    path = os.path.join(par.PATH_DEPORTISTAS)
    deportistas = list()
    with open(path, 'rt') as archivo:
        lineas = archivo.readlines()
        llaves = lineas.pop(0).strip('\n').split(',')
        conteo_0 = 0
        for llave in llaves:
            llaves[conteo_0] = llave.strip(' ')
            conteo_0 += 1
        conteo_1 = 0
        for linea in lineas:
            linea = linea.strip('\n').split(' ,')
            deportistas.append({llaves[0].strip(' '):'', llaves[1].strip(' '):'', llaves[2].strip(' '):'', llaves[3].strip(' '):'', llaves[4].strip(' '):'', llaves[5].strip(' '):'', llaves[6].strip(' '):''})
            conteo_2 = 0
            for palabra in linea:
                deportistas[conteo_1][llaves[conteo_2]] = palabra.strip(' ')
                conteo_2 += 1
            conteo_1 += 1
    return deportistas

def instanciar_deportistas_mercado():
    diccionario_deportistas = {}
    lista_deportistas = cargar_deportistas()
    for deportista in lista_deportistas:
        diccionario_deportistas[deportista['nombre']] = Deportista(deportista['nombre'], deportista['velocidad'], deportista['resistencia'], deportista['flexibilidad'], deportista['moral'], deportista['lesionado'], deportista['precio'])
    mercado = Mercado(diccionario_deportistas)
    return mercado

def instanciar_entrenador(nombre, usuario, delegacion):
    return Entrenador(nombre, usuario, delegacion)


def instanciar_delegaciones(mercado, entrenador_usuario, entrenador_rival):
    primera_delegacion, segunda_delegacion = cargar_delegaciones()
    deportistas_esparta = []
    deportistas_crotona = []
    if list(primera_delegacion.keys())[0] == 'IEEEsparta':
        esparta = primera_delegacion['IEEEsparta']
        crotona = segunda_delegacion['DCCrotona']
    else:
        esparta = segunda_delegacion['IEEEsparta']
        crotona = primera_delegacion['DCCrotona']
    for deportista in esparta['Equipo']:
        deportistas_esparta.append(mercado.deportistas_disponibles[deportista])
        del mercado.deportistas_disponibles[deportista]
    for deportista in crotona['Equipo']:
        deportistas_crotona.append(mercado.deportistas_disponibles[deportista])
        del mercado.deportistas_disponibles[deportista]
    esparta['Equipo'] = deportistas_esparta
    crotona['Equipo'] = deportistas_crotona
    if entrenador_usuario.delegacion == 'IEEEsparta':
        delegacion_usuario = IEEEsparta(entrenador_usuario, esparta['Moral'], esparta['Equipo'], esparta['Medallas'], esparta['Dinero'])
        delegacion_rival = DCCrotona(entrenador_rival, crotona['Moral'], crotona['Equipo'], crotona['Medallas'], crotona['Dinero'])
        return delegacion_usuario, delegacion_rival
    else:
        delegacion_rival = IEEEsparta(entrenador_rival, esparta['Moral'], esparta['Equipo'], esparta['Medallas'], esparta['Dinero'])
        delegacion_usuario = DCCrotona(entrenador_usuario, crotona['Moral'], crotona['Equipo'], crotona['Medallas'], crotona['Dinero'])
        return delegacion_usuario, delegacion_rival

#mercado = instanciar_deportistas_mercado()
#print(mercado.deportistas_disponibles)
#usuario = instanciar_entrenador('raimundo', True, 'IEEEsparta')
#rival = instanciar_entrenador('pepe', False, 'DCCrotona')
#deleg_usuario, deleg_rival = instanciar_delegaciones(mercado, usuario, rival)
#print('\n')
#print(deleg_rival.equipo)
#print(deleg_rival.entrenador.usuario)
#print('')
#print(deleg_usuario.equipo)
#print(deleg_usuario.entrenador.usuario)
#print('\n')
#print(mercado.deportistas_disponibles)


        



    




        
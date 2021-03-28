from menu import MenuInicio, MenuPrincipal, MenuEntrenador
from campeonato import Mercado, Campeonato
import entrenador
from delegaciones import DCCrotona, IEEEsparta
from cargar_instanciar import instanciar_delegaciones, instanciar_deportistas_mercado, instanciar_entrenador
from deportistas_deportes import Deporte
import os
import parametros as par

while True:
    menu_inicio = MenuInicio()
    menu_inicio.principal()
    #instanciamos clases
    entrenador_usuario = instanciar_entrenador(menu_inicio.nombre_usuario, True, menu_inicio.delegacion_usuario)
    entrenador_rival = instanciar_entrenador(menu_inicio.nombre_rival, False, menu_inicio.delegacion_rival)
    mercado = instanciar_deportistas_mercado()
    delegacion_usuario, delegacion_rival = instanciar_delegaciones(mercado, entrenador_usuario, entrenador_rival)
    # Creamos archivo en blanco resultados.txt
    path = os.path.join(par.PATH_RESULTADOSTXT)
    with open(path, 'wt') as archivo:
        archivo.write('RESULTADOS DÍA A DÍA DCCUMBRE OLÍMPICA\n---------------------------------------\n')
    #continuamos con flujo a menu principal, iniciando la simulacion
    menu_principal = MenuPrincipal()
    menu_entrenador = MenuEntrenador()
    campeonato = Campeonato(delegacion_usuario, delegacion_rival)
    # Creamos archivo en blanco resultados.txt
    simulando = True
    while simulando:
        entrada = menu_principal.principal()

        if entrada == 'm_entrenador':
            entrada = menu_entrenador.principal()
            if entrada == 'fichar':
                mercado.ofrecer_deportistas()
                deportista_seleccionado = mercado.seleccionar_deportista()
                if delegacion_usuario.fichar_deportistas(deportista_seleccionado):
                    mercado.deportista_vendido(deportista_seleccionado)
                menu_entrenador.flujo_de_menu()
            elif entrada == 'entrenar':
                delegacion_usuario.mostrar_equipo(False)
                deportista = delegacion_usuario.seleccionar_deportista()
                habilidad = delegacion_usuario.seleccionar_habilidad()
                delegacion_usuario.entrenar_deportistas(deportista, habilidad)
                menu_entrenador.flujo_de_menu()
            elif entrada == 'sanar':
                delegacion_usuario.mostrar_equipo(True)
                deportista = delegacion_usuario.seleccionar_deportista()
                delegacion_usuario.sanar_lesiones(deportista)
                menu_principal.flujo_de_menu()
            elif entrada == 'comp_tecnologia':
                delegacion_usuario.comprar_tecnología()
                menu_principal.flujo_de_menu()
            elif entrada == 'usar_hab_esp':
                delegacion_usuario.utilizar_habilidad_especial()
                menu_principal.flujo_de_menu()
            else:
                continue

        elif entrada == 's_competencia':
            campeonato.dia_actual += 1
            campeonato.calcular_nivel_moral()
            menu_principal.flujo_de_menu()
            delegacion_usuario.mostrar_equipo(False)
            campeonato.elegir_deportista_por_deporte()
            campeonato.elegir_deportista_aleatorio()
            #instanciar deportes
            atletismo = Deporte('atletismo', False, campeonato.competidores_usuario[0], campeonato.competidores_rival[0], delegacion_usuario, delegacion_rival)
            ciclismo = Deporte('ciclismo', True, campeonato.competidores_usuario[1], campeonato.competidores_rival[1], delegacion_usuario, delegacion_rival)
            gimnasia = Deporte('gimnasia', True, campeonato.competidores_usuario[2], campeonato.competidores_rival[2], delegacion_usuario, delegacion_rival)
            natacion = Deporte('natacion', False, campeonato.competidores_usuario[3], campeonato.competidores_rival[3], delegacion_usuario, delegacion_rival)
            #simular competencias
            ganador_atletismo = campeonato.realizar_competencia(atletismo)
            campeonato.premiar_deportistas(ganador_atletismo, atletismo)
            menu_principal.flujo_de_menu()
            ganador_ciclismo = campeonato.realizar_competencia(ciclismo)
            campeonato.premiar_deportistas(ganador_ciclismo, ciclismo)
            menu_principal.flujo_de_menu()
            ganador_gimnasia = campeonato.realizar_competencia(gimnasia)
            campeonato.premiar_deportistas(ganador_gimnasia, gimnasia)
            menu_principal.flujo_de_menu()
            ganador_natacion = campeonato.realizar_competencia(natacion)
            campeonato.premiar_deportistas(ganador_natacion, natacion)
            menu_principal.flujo_de_menu()
            campeonato.calcular_nivel_moral()
            menu_principal.flujo_de_menu()
            if campeonato.dia_actual == par.DIAS_COMPETENCIA:
                print('La DCCumbre Olímpica ha terminado! Gracias por participar!')
                print('')
                menu_principal.flujo_de_menu()
                campeonato.mostrar_resultado()
                menu_principal.flujo_de_menu()
                menu_principal.mostrar_opciones_finales()
                simulando = False
            campeonato.dia_actual += 1

        elif entrada == 'most_estado':
            campeonato.mostrar_estado()
            menu_principal.flujo_de_menu()


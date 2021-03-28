import parametros as par
import random


class Deportista():
    
    def __init__(self, nombre, velocidad, resistencia, flexibilidad, moral, lesionado, precio):
        self.nombre = nombre
        self.__velocidad = int(velocidad)
        self.__resistencia = int(resistencia)
        self.__flexibilidad = int(flexibilidad)
        self.__moral = int(moral)
        if lesionado == 'True':
            self.lesionado = True
        else:
            self.lesionado = False
        self.precio = int(precio)

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

    def entrenar(self, cualidad, especial):
        self.moral += 1
        if especial:
            puntos_entrenamiento = par.PUNTOS_ENTRENAMIENTO * 1.7
        else:
            puntos_entrenamiento = par.PUNTOS_ENTRENAMIENTO
        if cualidad == 'velocidad':
            self.velocidad += puntos_entrenamiento
            return self.velocidad
        elif cualidad == 'resistencia':
            self.resistencia += puntos_entrenamiento
            return self.resistencia
        elif cualidad == 'flexibilidad':
            self.flexibilidad += puntos_entrenamiento
            return self.flexibilidad

    def lesionarse(self, riesgo):
        # Se calcula la probabilidad de lesion, se cambia el atributo lesionado de ser necesario y se devuelve un bool que indica si hubo lesion
        n_random = random.uniform(0, 1)
        n_random = round(n_random, 2)
        if n_random < riesgo:
            print('Uuuh! Eso debe doler!')
            print(f'{self.nombre} se ha lesionado!')
            self.lesionado = True
            return True
        else:
            return False

    def __str__(self):
        return f'Hola! soy {self.nombre}'

    def __repr__(self):
        return f'soy {self.nombre}'

    @property
    def velocidad(self):
        return self.__velocidad

    @property
    def resistencia(self):
        return self.__resistencia

    @property
    def flexibilidad(self):
        return self.__flexibilidad

    @velocidad.setter
    def velocidad(self, n_velocidad):
        if n_velocidad > 100:
            self.__velocidad = 100
        else:
            self.__velocidad = n_velocidad

    @resistencia.setter
    def resistencia(self, n_resistencia):
        if n_resistencia > 100:
            self.__resistencia = 100
        else:
            self.__resistencia = n_resistencia

    @flexibilidad.setter
    def flexibilidad(self, n_flexibilidad):
        if n_flexibilidad > 100:
            self.__flexibilidad = 100
        else:
            self.__flexibilidad = n_flexibilidad


class Deporte():
    
    def __init__(self, nombre, implemento, deportista_usuario, deportista_rival, delegacion_usuario, delegacion_rival):
        self.nombre_deporte = nombre
        self.implemento = implemento
        self.riesgo = float()
        self.deportista_usuario = deportista_usuario
        self.deportista_rival = deportista_rival
        self.delegacion_usuario = delegacion_usuario
        self.delegacion_rival = delegacion_rival

    def validez_de_competencia(self):
        if self.deportista_usuario.lesionado and self.deportista_rival.lesionado:
            return 'empate'
        elif self.deportista_usuario.lesionado:
            return 'rival'
        elif self.deportista_rival.lesionado:
            return 'usuario'
        if self.implemento:
            if self.delegacion_usuario.implementos_deportivos <= par.NIVEL_IMPLEMENTOS and self.delegacion_rival.implementos_deportivos <= par.NIVEL_IMPLEMENTOS:
                return 'empate'
            elif self.delegacion_usuario.implementos_deportivos <= par.NIVEL_IMPLEMENTOS:
                return 'rival'
            elif self.delegacion_rival.implementos_deportivos <= par.NIVEL_IMPLEMENTOS:
                return 'usuario'
        return 'seguir'

    def calcular_ganador(self):
        # En este método se calcula el ganador (por deporte) y se evalúa si hubo lesionado, devolviendo el ganador correspondiente en cada caso
        if self.nombre_deporte == 'atletismo':
            self.riesgo = 0.2
            ganador = self.calcular_ganador_atletismo()
            ganador_por_lesion, lesionado = self.lesionar()
            if lesionado:
                if ganador_por_lesion == 'los dos':
                    return 'empate'
                else:
                    return ganador_por_lesion
            else:
                return ganador
        elif self.nombre_deporte == 'ciclismo':
            self.riesgo = 0.35
            ganador = self.calcular_ganador_ciclismo()
            ganador_por_lesion, lesionado = self.lesionar()
            if lesionado:
                if ganador_por_lesion == 'los dos':
                    return 'empate'
                else:
                    return ganador_por_lesion
            else:
                return ganador
        elif self.nombre_deporte == 'gimnasia':
            self.riesgo = 0.3
            ganador = self.calcular_ganador_gimnasia()
            ganador_por_lesion, lesionado = self.lesionar()
            if lesionado:
                if ganador_por_lesion == 'los dos':
                    return 'empate'
                else:
                    return ganador_por_lesion
            else:
                return ganador
        elif self.nombre_deporte == 'natacion':
            self.riesgo = 0.25
            ganador = self.calcular_ganador_natacion()
            ganador_por_lesion, lesionado = self.lesionar()
            if lesionado:
                if ganador_por_lesion == 'los dos':
                    return 'empate'
                else:
                    return ganador_por_lesion
            else:
                return ganador

    def calcular_ganador_atletismo(self):
        puntaje_usuario = max(par.PUNTAJE_MINIMO, 0.55 * self.deportista_usuario.velocidad + 0.2 * self.deportista_usuario.resistencia + 0.25 * self.deportista_usuario.moral)
        puntaje_rival = max(par.PUNTAJE_MINIMO, 0.55 * self.deportista_rival.velocidad + 0.2 * self.deportista_rival.resistencia + 0.25 * self.deportista_rival.moral)
        if puntaje_usuario < puntaje_rival:
            return 'rival'
        elif puntaje_usuario > puntaje_rival:
            return 'usuario'
        else:
            return 'empate'

    def calcular_ganador_ciclismo(self):
        puntaje_usuario = max(par.PUNTAJE_MINIMO, 0.47 * self.deportista_usuario.velocidad + 0.36 * self.deportista_usuario.resistencia + 0.17 * self.deportista_usuario.flexibilidad)
        puntaje_rival = max(par.PUNTAJE_MINIMO, 0.47 * self.deportista_rival.velocidad + 0.36 * self.deportista_rival.resistencia + 0.17 * self.deportista_rival.flexibilidad)
        if puntaje_usuario < puntaje_rival:
            return 'rival'
        elif puntaje_usuario > puntaje_rival:
            return 'usuario'
        else:
            return 'empate'

    def calcular_ganador_gimnasia(self):
        puntaje_usuario = max(par.PUNTAJE_MINIMO, 0.5 * self.deportista_usuario.flexibilidad + 0.3 * self.deportista_usuario.resistencia + 0.2 * self.deportista_usuario.moral)
        puntaje_rival = max(par.PUNTAJE_MINIMO, 0.5 * self.deportista_rival.flexibilidad + 0.3 * self.deportista_rival.resistencia + 0.2 * self.deportista_rival.moral)
        if puntaje_usuario < puntaje_rival:
            return 'rival'
        elif puntaje_usuario > puntaje_rival:
            return 'usuario'
        else:
            return 'empate'

    def calcular_ganador_natacion(self):
        puntaje_usuario = max(par.PUNTAJE_MINIMO, 0.45 * self.deportista_usuario.velocidad + 0.3 * self.deportista_usuario.resistencia + 0.25 * self.deportista_usuario.flexibilidad)
        puntaje_rival = max(par.PUNTAJE_MINIMO, 0.45 * self.deportista_rival.velocidad + 0.3 * self.deportista_rival.resistencia + 0.25 * self.deportista_rival.flexibilidad)
        if puntaje_usuario < puntaje_rival:
            return 'rival'
        elif puntaje_usuario > puntaje_rival:
            return 'usuario'
        else:
            return 'empate'

    def lesionar(self):
        # se llama al metodo lesionar de cada deportista y se devuelve el ganador debido a cada lesion, seguido de un bool que indica si hubo lesion
        deportista_usuario_lesionado = False
        deportista_rival_lesionado = False
        if self.deportista_usuario.lesionarse(self.riesgo):
            deportista_usuario_lesionado = True
        if self.deportista_rival.lesionarse(self.riesgo):
            deportista_rival_lesionado = True
        if deportista_rival_lesionado and deportista_usuario_lesionado:
            print(f'* Se han lesionado los dos deportistas en {self.nombre_deporte}. *')
            print('')
            return 'los dos', True
        elif deportista_rival_lesionado:
            print(f'* Se ha lesionado el deportista rival en {self.nombre_deporte}. *')
            print('')
            return 'usuario', True
        elif deportista_usuario_lesionado:
            print(f'* Se ha lesionado tu deportista en {self.nombre_deporte}. *')
            print('')
            return 'rival', True
        else:
            return 'nadie', False
        
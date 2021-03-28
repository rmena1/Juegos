# Tarea 00: DCCombateNaval :school_satchel:

## Consideraciones generales :octocat:

La simulación está implementado en su totalidad y cumple con todos los puntos de la pauta y del enunciado. Realicé varios test de prueba al código y no tuve ningún error en la última versión que subí a github.
Todo fue implementado y funciona correctamente si se recibe el input esperado, aunque no probé con todos los posibles input que se puedan dar (aunque según yo no hay ningún caso en el que el programa se caiga).
En la simulación implementé cosas extras que no se pedían en la pauta tales como:
* Flujo de output controlado por el jugador. Esto quiere decir que se le pedirá al jugador introducir ENTER luego de recibir un output para así facilitar una correcta lectura de los textos por parte del jugador (tal como sucede con las burbujas de texto en juegos como Pokemon).
No implementé el comportamiento del rival, aunque en un inicio si quería implementarlo. Esta es la principal razón de la existencia de la clase entrenador (donde hay un método que no se implementó ni se utiliza en el programa).

### Cosas implementadas y no implementadas :white_check_mark: :x:

* Programación Orientada a objetos<sub>1</sub>: Hecha completa.
    * Diagrama<sub>1.2</sub>: Hecha completa.
    * Definición de clases, atributos y métodos<sub>1.3</sub>: Hecha completa.
    * Relaciones entre clases<sub>1.3</sub>: Puede que esté un poco pobre en este punto. Lo implementé pero al final programé muy apurado y creo que este fue el punto que más se paso a llevar por esto. (Tengan piedad, tuve una carga académica horrible ): )
* Partidas<sub>2</sub>: Hecha completa.
    * Crear partida<sub>2.1</sub>: Hecha completa.
    * Guardar<sub>2.2</sub>: Hecha completa.
* Acciones<sub>3</sub>: Hecha completa.
    * Delegaciones<sub>3.1</sub>: Hecha completa.
    * Deportistas<sub>3.2</sub>: Hecha completa.
    * Competencia<sub>3.3</sub>: Hecha completa.
* Consola<sub>4</sub>: Hecha completa.
* Manejo de archivos<sub>5</sub>: Hecha completa.
    * Archivos CSV<sub>5.1</sub>: Hecha completa.
    * parametros.py<sub>5.2</sub>: Hecha completa.
    * resultados.txt<sub>5.3</sub>: Hecha completa.


## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```.


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```os```: ```join() / path```
2. ```random```: ```randint()```, ```uniform()```
3. ```abc```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```menu```: Contiene a ```Menu(ABC)```, ```MenuInicio```, ```MenuPrincipal```, ```MenuEntrenador```. Esta librería fue hecha para incluir todas las clases de los menús.
2. ```campeonato```: Contiene a ```Campeonato```, ```Mercado```. Esta librería fue hecha para incluir todos los elementos propios del campeonato.
3. ```cargar_instanciar```: Este módulo no contiene ninguna clase, pero en el están todas las funciones necesarias para cargar e instanciar los deportistas y las delegaciones.
4. ```delegaciones```: Contiene a ```Delegacion(ABC)```, ```DCCrotona```, ```IEEEsparta```. En esta librería se encuentran todas las clases relacionadas con las delegaciones.
5. ```deportistas_deportes```: Contiene a ```Deportista```, ```Deporte```. En esta librería se encuentran todas las clases relacionadas a los deportes y deportistas.
6. ```entrenador```: Contiene a ```Entrenador```. Esta librería contiene a una única clase, la cual se suponía que iba a tener el comportamiento del rival, pero por temas de tiempo no se pudo implementar.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. El superpoder de DCCrotona no afecta las habilidades de ningún deportista.
2. Deportes que terminan por invalidez generan los mismos efectos sobre los deportistas y sus delegaciones a si hubieran ganado o perdido debido a condiciones normales.
3. Nombres pueden tener cualquier cantidad de digitos (de cero en adelante, no se especificaba en el enunciado).

PD: Muchas gracias por la corrección y fuerza para seguir con las otras!!!


## Descuentos:

Mi código se desordena mucho en la parte de delegaciones, perdón, me quede sin tiempo :(.

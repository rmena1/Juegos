# Tarea 00: DCCombateNaval :school_satchel:

## Consideraciones generales :octocat:

El juego está implementado en su totalidad y cumple con todos los puntos de la pauta y del enunciado. Realicé varios test de prueba al código y no tuve ningún error en la última versión que subí a github.
Todo fue implementado y funciona correctamente si se recibe el input esperado, aunque no probé con todos los posibles input que se puedan dar (aunque según yo no hay ningún caso en el que el programa se caiga).
En el juego implementé cosas extras que no se pedían en la pauta tales como:
* Texto de contexto de juego al comenzar a jugar, con frases adecuadas al contexto de una batalla naval.
* Flujo de output controlado por el jugador. Esto quiere decir que se le pedirá al jugador introducir ENTER luego de recibir un output para así facilitar una correcta lectura de los textos por parte del jugador (tal como sucede con las burbujas de texto en juegos como Pokemon).

### Cosas implementadas y no implementadas :white_check_mark: :x:

* Inicio del programa<sub>1</sub>: Hecha completa.
    * Menú de inicio<sub>1.2</sub>: Hecha completa.
    * Funcionalidades<sub>1.3</sub>: Hecha completa.
    * Puntajes<sub>1.3</sub>: La interfaz es un poco distinta al ejemplo del enunciado para así coincidir con el modo de flujo de texto implementado en el juego (hay que apretar ENTER en vez de ingresar 0 para volver.), pero funciona correctamente y cumple con todos los requerimientos.
* Flujo del juego<sub>2</sub>: Hecha completa.
    * Menú de juego<sub>2.1</sub>: Hecha completa.
    * Tablero<sub>2.2</sub>: Hecha completa.
    * Turnos<sub>2.3</sub>: Hecha completa.
    * Bombas<sub>2.4</sub>: Hecha completa.
    * Barcos<sub>2.5</sub>: Hecha completa.
    * Oponente<sub>2.6</sub>: Hecha completa.
* Termino del juego<sub>3</sub>: Hecha completa.
    * Fin del juego<sub>3.1</sub>: Hecha completa.
    * Puntajes<sub>3.2</sub>: Hecha completa.
* Archivos<sub>4</sub>: Hecha completa.
* General<sub>5</sub>: Hecha completa.
    * Menús<sub>5.1</sub>: Hecha completa.
    * Parámetros<sub>5.2</sub>: Hecha completa.
    * Módulos<sub>5.3</sub>: Hecha completa.
    * PEP8<sub>5.4</sub>: Hecha completa.


## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Además se debe crear los siguientes archivos y directorios adicionales:
1. ```puntajes.txt``` en carpeta principal


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```os```: ```join() / path```
2. ```random```: ```randint()```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```menu```: Contiene a ```menu_principal()```, ```apodo()```, ```tamaño_tablero()```, ```rankings()```, ```ubicar_flota()```. Esta librería fue hecha para incluir todas las funciones de los menús, incluida la lectura de los rankings.
2. ```batalla_naval```: Contiene a ```menu_juego()```, ```seleccionar_bomba()```, ```seleccionar_coordenadas()```, ```resultado_bomba_normal()```, ```resultado_bomba_especial()```, ```bomba()```, ```bomba_cruz()```, ```bomba_x()```, ```bomba_diamante()```, ```puntaje()```. Esta librería fue hecha para incluir todas las funcionalidades propias del juego, menos el comportamiento del oponente, ya que este comportamiento fue incluido en la clase juego la cual está definida en el módulo principal main.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Los menús se podían modificar ligeramente respecto a los menús entregados en el enunciado: Siempre y cuando estas modificaciones no influyan en el funcionamiento de los menús, lo cual es lo más importante de estos.
2. Las bombas especiales se pueden tirar en cualquier punto del mapa, este esté descubierto o no: Ya que el efecto de estas bombas es en área, por lo que el centro de la explosión no tiene como finalidad encontrar un barco (como si lo es para la bomba normal), sino que es ser el centro de la explosión, por lo que no importa si ya sabíamos lo que había en ese punto o no.
3. Las bombas especiales pueden 'reventar' en lugares ya conocidos sin generar cambios en estas celdas: La justificación es similar a la justificación del punto 2. y sigue la misma idea.

PD: Muchas gracias por la corrección y fuerza para seguir con las otras!!!


## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. https://stackoverflow.com/questions/45198007/write-to-the-last-line-of-a-text-file: Este permite escribir partiendo desde la última línea de un archivo, lo utilicé en el módulo batalla_naval, en la función ```puntaje()```, línea 331 y lo utilicé con este mismo propósito.


## Descuentos:

Según yo mi código podría haber estado más ordenado (incluyendo las clases de main en batalla_naval, que es donde deberían haber estado), y también importé librerias en algunos módulos en los cuales terminé no ocupandolas y se me olvidó eliminar el importado de la librería (en batalla_naval importé random y no lo utilicé). Fuera de esto, no creo haber tenido más problemas.
No le puse demasiada atención a PEP8 al momento de escribir el código y cambié varias cosas al final, por lo que puede que en algunos puntos específicos me haya salido de la regla, aunque no se a priori en cuales.

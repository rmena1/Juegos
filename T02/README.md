# Tarea 02: DCCumbia :school_satchel:

## Consideraciones generales :octocat:

Para correr la tarea se debe correr el módulo main.py el cual se encuentra en la carpeta raiz del programa.

Partes a corregir en código (partes amarillas en pauta) se encuentran en ```cosas implementadas y no implementadas```

El juego está implementado en su totalidad menos la funcionalidad de pausar el juego, la cual no está implementada en ningún nivel (está el botón pero al presionarlo no hace absolutamente nada).

Por otro lado, la funcionalidad de ```cheatcodes``` la implementé de una forma distinta a las opciones ofrecidas en el enunciado. Estas fueron implementadas de una forma más parecida al juego real de club penguin donde había objetos escondidos en la escena del juego los cuales al presionarlos realizaban ciertas acciones. En el caso de mi programa, al apretar los audifonos en la zona del dj de la pista de baile se abre una ventana donde se pueden ingresar los cheatcode ```mon```y ```niv```, los cuales realizan las acciones pedidas en el enunciado. Cabe destacar que al ingresar ```niv``` dejan de salir flechas, pero las flechas que habían aparecido hasta ese momento siguen su camino por la pantalla, por lo cual al ingresar el código hay que volver a apretar la ventana de juego rápidamente (para que se 'active' el programa de juego luego de apretar una ventana distinto) y seguir apretando las fleschas que aún no desaparecen para no perder aceptación (ya que la aceptación no se pausa al ingresar el codigo ```niv```).

Respecto a los colores de las flechas, la flecha verde hace referencia a flechas normales, la morada a las x2, la blanca a la flecha hielo y la amarilla a la dorada.
Al presionar la tecla ```salir``` se cierra la ventana de juego, guardando la partida y volviendo a la ventana de inicio para comenzar una nueva partida. Si se presiona este botón durante una partida el juego se cae, y si se aprieta el botón x para cerrar la ventana durante una ronda también se cae. Según yo estas son las únicas ocaciones donde mi programa se cae.

Quisiera agregar un par de líneas en mi código, las dos en el módulo ```ventana_juego``` el cual se encuentra en la carpeta FrontEnd:
1) En el módulo ```ventana_juego``` carpeta FrontEnd, en el método ```definir_cancion_dificultad```, entre las líneas 199 y 200 agragar (con mismo nivel de identación que líneas 199 y 200) self.opciones_cancion.setEnabled(False)
2) En el módulo ```ventana_juego``` carpeta FrontEnd, en el método ```terminar_ronda```, entre las líneas 240 y 241 agragar (con mismo nivel de identación que líneas 240 y 241) self.opciones_cancion.setEnabled(True)

Esto es para que las opciones de las canciones se desactiven durante las rondas, y se desactive al finalizar la ronda para así poder cambiar la canción.

En el enunciado salía que en la barra de progreso había que poner el progreso de la canción, y supuse que se refería al progreso de la ronda (me hacía más sentido), así que la implementé de esta forma.

Finalmente, mi tarea se laguea mucho en los niveles aficionado y maestro cumbia debido a la cantidad de threads que se activan al mismo tiempo (por lo menos en mi computador), lo que hace que la canción se reproduzca entrecortada. (si ajusté el tiempo sleep de los threads para evitar que esto ocurra).

```Acompañame a ver esta triste historia:```
Luego de entregar la tarea (a las 8 en punto), me fui a duchar y me puse a pensar en posibles errores de la tarea y me di cuenta que habia instanciado todo el Back End en el Front End :( Esto lo hice cuando estaba buscando formas alternativas de instanciar las distintas clases para así implementar de forma más fácil la salida del juego y reiniciar la partida para comenzar una nueva ronda. Al momento de hacer estos cambios se me olvidó por completo el tema de la separación Front - Back End y mi juego fue entregado con estos errores... 
Big efe por esto.
Espero haber dado la pena suficiente y que tengan piedad con la corrección en este ítem.


### Cosas implementadas y no implementadas :white_check_mark: :x:

* Ventana de Inicio<sub>1</sub>: Hecha completa.
* Ventana de Ranking<sub>2</sub>: Hecha completa.
    * Corrección de código<sub>2.1</sub>: Esta parte se encuentra en la carpeta FrontEnd, módulo ventana_ranking, a partir de la línea 66 en el método cargar_datos.
* Ventana de Juego<sub>3</sub>: Parcialmente completa.
    * Generales<sub>3.1</sub>: Hecha completa. Si se presiona el botón salir durante una ronda el programa se cae.
    * Fase de pre Ronda<sub>3.2</sub>: Hecha completa. Corrección de código: Esta parte del código se encuentra en los módulos ventana_juego (dentro del método dropEvent, línea 328) y en lógica_juego (método comprar_pinguino, línea 389 y en setter de dinero, línea 122). El primer módulo en carpeta FrontEnd y el segundo en BackEnd.
    * Fase de Ronda<sub>3.3</sub>: Hecha completa. Corrección de Código: Aprobación del público se calcula en el módulo logica_juego (dentro del método calcular aceptación, línea 258, hasta línea 277).
    * Fase de post-ronda<sub>3.3</sub>: Hecha completa. Corrección de Código: Calculo de puntaje se realiza en módulo lógica_juego a medida que se agarran las flechas (método recibir flecha línea 224) y se multiplica por el mayor combo al finalizar la ronda en el mismo módulo (método resumen_ronda, línea 369).
* Mecánicas<sub>4</sub>: Hecha parcialmente.
    * Pingüirin<sub>4.1</sub>: Hecha completa. Pingüinos pasan por posición neutra, aunque creo que no se ve en el programa (no entendí bien a que se refería con esto en el enunciado). Esto se hace en la línea 69 del módulo pinguirines, carpeta FrontEnd.
    * Flechas<sub>4.2</sub>: Hecha completa. Corrección de código: La identificación de pasos correctos se hace en módulo logica_juego, carpeta BackEnd. Esta identificación comienza en el módulo recibir_flecha, línea 224 (start timers para flecha capturada y timer para esperar un error), luego se continúa en el método intersección_fallida, línea 315 donde se determina si un paso errado es vacío (no se apreta flecha) o es una intersección fallida (definí así al caso en el que se aprieta una flecha y una caja vacía). Estos dos métodos son para el caso de pasos normales, para el caso de pasos combinados, se pasa por los métodos anteriores y luego al método calcular_aceptación, donde a partir de la línea 278 se calcula si un paso combinado es correcto o no.
* Funcionalidades extra<sub>5</sub>: Parcialmente incompleta.
    * Pausa<sub>5.1</sub>: No hecha.
    * mon<sub>5.2</sub>: Hecha completa. Implementación se explica en consideraciones generales.
    * niv<sub>5.3</sub>: Hecha completa. Implementación se explica en consideraciones generales.
* General<sub>6</sub>: Parcialmente completa.
    * Modularización<sub>6.1</sub>: Medianamente completa. Error mencionado en consideraciones generales se encuentra en módulo ventana_inicio (carpeta FrontEnd), donde se instancia el BackEnd en el FrontEnd en vez de en el módulo main. El resto de separaciones se realiza correctamente entre las carpetas FrontEnd y BackEnd, y las señales las cuales se instancian en ventana_inicio.
    * Modelación<sub>6.2</sub>: Hecha completa. Cabe destacar que estuve muy al límite de las 400 líneas en logica_juego y ventana_juego, pero se cumplió y además estos modulos tienen solo una clase por archivo.
    * Archivos<sub>6.3</sub>: Hecha completa. Corrección código: Archivos se importan y manipulan en ventana_juego métodos init_gui (líneas 78, 117), método definir_cancion_dificultad (línea 212), módulo ventana_inicio en método init_gui (línea 81), módulo ventana_ranking en método init_gui (línea 52), módulo pinguirines, clase pinguino, método init_gui (desde línea 20), clase PinguinoBailarin (desde línea 57) en todos sus métodos.
    * Parametros.py<sub>6.3</sub>: Hecha completa. Módulo parametros se encuentra en la carpeta raiz de la tarea y se importa en todos los módulos de esta, al inicio de estos (primeras 10 líneas en todos los casos).
* Bonus<sub>7<sub>: No implementados.


## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```.


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```os```: ```join() / path```
2. ```random```: ```randint()```, ```random()```
3. ```PyQt5```
4. ```sys```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```ventana_inicio```: Contiene a ```VentanaInicio```. En esta clase se implementa el FrontEnd de la ventana de inicio, y se instancian todas las otras clases y señales.
2. ```ventana_ranking```: Contiene a ```VentanaRanking```. En esta clase se implementa el FrontEnd de la ventana de ranking, no se hizo un BackEnd ya que los cálculos necesarios son muy pocos (estos se incluyeron en este mismo módulo).
3. ```cheats```: Contiene a ```LabelOculto``` y ```VentanaRanking```. En esta libreria se implementa el FrontEnd del label escondido en la pista de baile y la ventana que se despliega al presionarlo.
4. ```creador_flechas```: Contiene a ```Flecha```. En esta clase se implementa el FrontEnd de las flechas y el QThread que provoca su movimiento.
5. ```pinguirines```: Contiene a ```Pinguino``` y ```PinguinoBailarin```. En esta librería se encuentran todas las clases relacionadas a los pinguinos.
6. ```ventana_juego```: Contiene a ```VentanaJuego```. En esta clase se implementa el FrontEnd de la ventana de juego.
7. ```ventana_resumen```: Contiene a ```VentanaResumen```. En esta clase se implementa el FrontEnd de la ventana de resumen.
8. ```logica_juego```: Contiene a ```Juego```. En esta clase se implementa casi todo el BackEnd del juego.
9. ```ventana_resumen```: Contiene a ```VentanaResumen```. En esta clase se implementa el FrontEnd de la ventana de resumen.
10. ```cerrar_partida```: Contiene a ```terminar_partida```. Este módulo contiene una función que guarda el resultado de la partida al salir de esta.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Barra progreso muestra el progreso de la ronda (no entendí bien el enunciado así que supuse esto).
2. Nombres pueden tener cualquier cantidad de digitos (de cero en adelante, no se especificaba en el enunciado).
3. Se puede cambiar la canción entre rondas, pero no la dificultad.
4. Al cerrar la ventana de juego no se debe guardar el progreso actual (salir sin guardar).

PD: Muchas gracias por la corrección y fuerza para seguir con las otras!!!


## Descuentos:

Mis módulos son muy largos y el código tiene poca separación de funciones.
Hay funciones que hacen más de una acción o función.

-------
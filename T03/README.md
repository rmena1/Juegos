# Tarea 03: DCColonos :school_satchel:

## Consideraciones generales :octocat:

Para correr el server se debe correr el archivo main.py que se encuentra en la carpeta Server, para correr el cliente se debe correr el archivo main.py que se encuentra en la carpeta Cliente.

Antes de correr la tarea se debe agregar la carpera sprites entregada junto al enunciado en la carpeta FrontEnd ubicada en la carpeta Cliente

El juego está implementado en su totalidad, pero al terminar cada partida no se puede comenzar una partida nueva (hay que reiniciar el server y los clientes manualmente) y ciertas condiciones para la carretera más larga no se implementaron (chozas de contrincantes no cortan las carreteras).

Para agregar chozas y carreteras al mapa se debe apretar su ícono correspondiente en la barra inferior de la interfaz, lo cual seleccionará la estructura, y luego apretar los vertices o aristas (según corresponda) donde se quiera poner las construcciones.

El server printea los LOGS en el formato LOG: "texto" donde el texto contiene toda la información pedida. Quisiera pedir perdón ya que hay logs muy largos y es difícil entender estos una vez que se abre la ventana principal del juego (ya que se printean muchos logs).

Todas las ventanas emergentes del programa se crean en el mismo lugar, por lo que hay que buscar ventanas detrás de otras (esto sucede, por ejemplo, al intercambiar materias, donde la ventana para aceptar o rechazar el intercambio se genera detrás de la ventana donde se eligen las materias a intercambiar).

Algunas partes del juego que creo que están incompletas son las siguientes:
1)Desconexión de clientes: No implementé el manejo de la desconección de los clientes durante una partida, aunque si fue implementada en la ventana de espera y el server reconoce cuando se desconecta un cliente.
2) Desconexión del servidor: Clientes se caen cuando se desconecta el servidor
3) Mostrar información al final de la partida: Cuando un jugador gana se le da un mensaje a todos los jugadores diciendo quién fue el ganador, pero no se da toda la información pedida en el enunciado. Cuando se apriera el botón para volver se redirige a la sala de espera pero en este punto hay que cerrar los clientes y el servidor para poder volver a jugar otra partida.
4) Hay errores en el cálculo de la carretera más larga.
5) En sala de espera, cuando se conecta un cliente y la partida ya se inició no se le da aviso, pero se rechaza su conexión al servidor.


### Cosas implementadas y no implementadas :white_check_mark: :x:
Las partes implementadas y no implementadas de la pauta son las siguientes:

* Networking<sub>1</sub>: Parcialmente completa.
    * Protocolo<sub>1.1</sub>: Hecha completa.
    * Correcto uso de sockets<sub>1.2</sub>: Hecha completa.
    * Conexión<sub>1.3</sub>: Hecha completa.
    * Manejo de clientes<sub>1.4</sub>: Tal como se mencionó anteriormente, no se pueden desconectar clientes ni el servidor sin que esto afecte al programa, si se pueden conectar varios clientes.
* Arquitectura cliente-servidor<sub>2</sub>: Hecha completa.
    * Roles<sub>2.1</sub>: Hecha completa.
    * Consistencia<sub>2.2</sub>: Hecha completa.
    * Logs<sub>2.3</sub>: Hecha completa.
* Manejo de Bytes<sub>3</sub>: Hecha completa.
    * Codificación<sub>3.1</sub>: Hecha completa.
    * Decodificación<sub>3.2</sub>: Hecha completa.
    * Integración<sub>3.3</sub>: Hecha completa.
* Intefaz gráfica<sub>4</sub>: Parcialmente completa.
    * Modelación<sub>4.1</sub>: Hecha completa.
    * Sala de espera<sub>4.2</sub>: Cuando se conecta un usuario extra, se rechaza su conexión con el servidor, pero no se le avisa ni se da opción de cerrar el programa.
    * Sala de juego<sub>4.3</sub>: Hecha completa.
    * Fin de la partida<sub>4.4</sub>: Hecha parcialmente: No se muestra toda la información pedida en el enunciado.
* Grafo<sub>5</sub>: Hecha completa (creo). 
    * Archivo<sub>5.1</sub>: Hecha completa.
    * Modelación<sub>5.2</sub>: Hecha completa.
    * Funcionalidades<sub>5.3</sub>: Creo que hecha completa. Revisar errores en calcular la carretera más larga, creo que hay casos borde no considerados lo cual genera pequeños errores en el cálculo.
* Reglas del DCColonos<sub>6</sub>: Hecha completa.
    * Inicio del juego<sub>6.1</sub>: Hecha completa.
    * Lanzamiento de dados<sub>6.2</sub>: Hecha completa.
    * Turno<sub>6.3</sub>: Hecha completa.
    * Termino del juego<sub>6.3</sub>: Hecha completa.
* General<sub>7<sub>: Hecha completa.
* Bonus<sub>8<sub>: No implementados.

## Corrección de código

Las distintas partes a corregir en código se encuentran en las siguientes partes:

1. Correcto uso de TCP/IP: Esto se puede encontrar en las primeras líneas de las clases Server (T03/Server/server.py) y Cliente (T03/Cliente/BackEnd/cliente.py).
2. Instancia y conecta sockets: Instanciado de socket servidor: Clase Server (T03/Server/server.py) línea 30. Instanciado socket cliente: Clase Cliente (T03/Cliente/BackEnd/cliente.py) línea 17. Conexión de cliente en método start() desde línea 23 de clase Cliente y en server (thread escuchar clientes) desde línea 34 de clase Server (incluido el método aceptar_clientes() desde línea 41).
3. Correcta separación de recursos entre cliente y servidor: Esto se ve en cada una de las clases Cliente (T03/Cliente/BackEnd/cliente.py) y Servidor (T03/Server/server.py).
4. Las responsabilidades de cada cliente son consistentes con el enunciado: Clase Cliente (T03/Cliente/BackEnd/cliente.py)
5. Las responsabilidades del servidor son consistentes con el enunciado: Clase Servidor (T03/Server/server.py)
6. Se utilizan locks cuando es necesario: Estos locks se ocupan al enviar y recibir información desde el cliente y el server. En clase Cliente (T03/Cliente/BackEnd/cliente.py) se ocupan locks en los siguientes métodos: escuchar_servidor (línea 39), leer_mensaje (línea 45), enviar_mensaje (línea 60), recibir_pickle (línea 98). En clase Servidor (T03/Server/server.py) en los métodos escuchar_cliente (línea 92), enviar_mensaje_todos (línea 132), enviar_mensaje_especifico (línea 153) y enviar_python_todos (línea 191).
7. Se utiliza big y little indian: Esto se utiliza al enviar mensajes y datos. En clase Cliente (T03/Cliente/BackEnd/cliente.py) se ocupa little y big endian en los siguientes métodos: escuchar_servidor (línea 39), leer_mensaje (línea 45), enviar_mensaje (línea 60), recibir_pickle (línea 98). En clase Servidor (T03/Server/server.py) en los métodos escuchar_cliente (línea 92), enviar_mensaje_todos (línea 132), enviar_mensaje_especifico (línea 153) y enviar_python_todos (línea 191).
8. Correcta implementación y manejo de bytes: Esto se utiliza en los mismos métodos que los dos puntos anteriores.
9. Utiliza correctamente el protocolo para el envío de mensajes: Esto se utiliza en los mismos métodos que los tres puntos anteriores.
10. Existe una correcta separación entre front y back end: esto se implementa en la separación entre carpetas FrontEnd y BackEnd en la carpeta Cliente, todos los códigos contenidos en cada una de estas carpetas se conecta mediante señales en el módulo main.py de la carpeta Cliente.
11. Se instancia correctamente un grafo no dirigido: Esto se hace a medida que se van añadiendo carreteras en el método ubicar_carretera (línea 214) de la clase Juego que se encuentra en el módulo dccolonos.py (T03/Server/dccolonos.py) y se utilizan las clases Carretera y Choza (T03/Server/grafo_dccolonos.py)
12. El grafo se actualiza correctamente: Esto ocurre en el mismo método descrito en el punto anterior, el cual es llamado cada vez que se agrega una carretera.
13. Se verifica que se cumplan las condiciones para ubicar una choza: Método solicitar_choza (línea 156) de la clase Juego que se encuentra en el módulo dccolonos.py (T03/Server/dccolonos.py).
14. Se verifica que se cumplan las condiciones para construir una carretera: Método solicitar_carretera (línea 186) de la clase Juego que se encuentra en el módulo dccolonos.py (T03/Server/dccolonos.py).
15. Se calcula carretera más larga: Método definir_carretera_mas_larga (línea 315) y método recorrer_camino (línea 337) de la clase Juego que se encuentra en el módulo dccolonos.py (T03/Server/dccolonos.py).
16. Se implementa carta punto victoria: Método carta_desarrollo (línea 352) de la clase Juego que se encuentra en el módulo dccolonos.py (T03/Server/dccolonos.py).
17. Se implementa carta monopolio: Método carta_desarrollo (línea 352) y método monopolio (línea 374) de la clase Juego que se encuentra en el módulo dccolonos.py (T03/Server/dccolonos.py).
18. Parametros.json: Se encuentra una versión de este archivo en las carpetas Server y Cliente, y se instancia al inicio de casi todos los módulos de la tarea.
19. Grafo.json: Se carga en línea 8 del módulo logica_server (T03/Server/logica_server.py) y se utiliza en varios métodos del módulo dccolonos (T03/Server/dccolonos.py), algunos de estos métodos son: ubicar_fichas_aleatorias (línea 56), otorgar_materia (línea 151), solicitar_choza, solicitar_carretera, ubicar_choza, ubicar_carretera (a partir de línea 156), entre otros.
20. Generador de mazos: Se utiliza en módulo dccolonos (T03/Server/dccolonos.py), método carta_desarrollo (línea 352), especificamente en la línea 366.


## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```, esto se debe hacer tanto para el server (carpeta Server) como para cada uno de los clientes (carpeta Cliente).


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```os```: ```join() / path```
2. ```random```: ```randint()```
3. ```PyQt5```
4. ```sys```

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Las dos cartas de punto de victoria tiene el mismo efecto (no entendí por qué había dos así que solo utilicé una).
2. Si dos jugadores empatan en el largo de sus carreteras, los puntos se le otorga a cualquiera de los dos, luego, para traspasar los puntos de un jugador a otro, la carretera debe sobrepasar el largo de la carretera anterior (si tengo la carretera más larga y me empatan, mantengo los puntos hasta que alguien me pase).

PD: Muchas gracias por la corrección y fuerza para seguir con las otras!!!

PD2: Muchas gracias por el ramo!!! Hasta ahora el mejor que he tenido en la universidad, espero que seamos ayudantes juntos de este ramo el próximo semestre!!!


## Descuentos:

Según yo no debería tener descuentos... :)

-------
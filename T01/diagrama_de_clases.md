# Explicación de la modelación

## El programa se basa en 2 apartados:

### Apartado menús

 Es la parte "externa" del programa con la cual interactuará el usuario. Este apartado incluye una clase abstracta ```Menu``` la cual contiene los módulos mínimos que debe contener cada menú. Entre estas destacan los módulos ```elegir_opcion``` y ```realizar_accion``` las cuales se deberán implementar en cada menú para permitir al usuario elegir una opción (evitando errores) y realizar la acción relacionada con esta opción respectivamente.
 
 En este apartado se incluyen todos los menús en los cuales el usuario podrá interactuar (inicio, principal, simulación y entrenador).

### Apartado simulación
 
 Esta será la parte "interna" del programa, donde se contienen todas las clases necesarias para realizar la simulación de la *DCCumbre Olímpica*. Entre estas destacan las siguientes clases:
 * ```Delegacion```: Clase abstracta la cual contiene todos los atributos y métodos comunes para las dos delegaciones (casi todos los atributos y métodos serán iguales (en un inicio) menos el método ```utilizar_habilidad_especial```).
 * ```Entrenador```: Clase que representará tanto al usuario como al rival de este, entre sus entidades destaca ```usuario``` la cual contendrá un bool el cual será **True** si el entrenador instanciado será el entrenador que representa al usuario y **False** en caso contrario.
 * ```Campeonato```: Será la clase más grande del programa y en esta se realizarán la mayor parte de funciones relacionadas al campeonato (menos los métodos estrictamente relacionados con los deportes los cuales se encontrarán en la clase ```Deporte```). En esta clase destaca la entidad ```ganadores_del_día``` la cual será una lista de diccionarios, donde cada sección de la lista representará un día y cada diccionario tendrá como llave los 4 deportes y el ganador de cada deporte del día que corresponda, esto se hace para simplificar la escritura de los datos, la cual se hará una vez finalizada la simulación.  
 * ```Deporte```: Decidí incluir los 4 deportes en la misma clase por simplicidad, esta clase se ocupará para determinar al ganador en cada deporte de cada día. Los métodos que calculan al ganador de cada deporte devuelven un bool el cual será **True** en el caso que el ganador sea el usuario.

### Interacción entre apartados

 Todas las clases relacionadas con el el apartado simulación se instanciarán en la clase ```MenuInicio```una vez elegidos los nombres y la delegación que representará el usuario, y las clases relacionadas a menús se instanciarán en el código principal del programa.
  Todas las relaciones entre menús y simulación se harán a través del código principal del programa, en el cual se evaluarán los inputs del usuario y se ejecutarán los métodos correspondientes.

Cabe destacar que en el programa los métodos que retornan bool (en su mayoría) se utiliza este retorno para determinar si la acción se pudo realizar o no.
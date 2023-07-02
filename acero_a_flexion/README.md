# Acero a flexión
El proyecto original trata del *"Diseño a flexión según la norma ACI 318-14"* [1].

El objetivo es transcribir los códigos originales y plantear otras soluciones más profesionales que sean legibles, modulares, sin redundancias, testeables y preparadas para los cambios futuros.

Referencia:

[1] https://marcelopardo.com/flexion-simple-diagrama-de-flujo-para-acero-a-flexion-norma-aci-318-14


## Análisis

La estructura del código tiene sentido para un desarrollador principiante y las explicaciones vertidas en el video me recuerdan a mis primeros pasos en la programación. Esa programación *procedural* se asimila fácilmente al tipo de problema a resolver.

De mi análisis del código encuentro los siguientes aspectos a mejorar:

* No hay descripción sobre el propósito del software ni sobre las unidades que los parámetros de entrada.

* Las variables son algo crípticas, se debe tener a mano el [diagrama de flujo](doc/diagramaFlujoFlexionACI14.jpg) para entender en qué parte del código estamos parados.

* Asociado al punto anterior, no hay una buena legibilidad en general: fórmulas sin espacios que apoyen las partes de los cálculos, difícil de seguir la lógica por tener tantas líneas de código consecutivas.

* El resultado del algoritmo son cuatro textos, cuando en verdad los resultados deberían ser de valores numéricos. Esto muestra una dependencia entre los resultados objetivos (valores) y cómo se deben interpretar (mensajes de texto).

* No es posible probar si el código hace bien o no sus cálculos. Además los valores de entrada están fijos dentro del mismo algoritmo.

* Dependencia directa entre el algorítmo y la interfaz gráfica que lo utiliza. Para peor, hay duplicidad de código.

* Pobre utilización de características básicas del lenguaje Python.

## Desarrollo

En función de lo observado, distintas etapas de refactoring serán aplicadas como una evolución incremental del código que permita mostrar la metodología que los desarrolladores de software utilizamos para mejorar el código, minizando la probabilidad de la introducción de errores.

Como el propósito de este trabajo es educativo, habrá decisiones donde implemente modificaciones que a priori sé que no tienen sentido, porque sé que en la versión final hay cosas que serán muy distintas. Espero, sin embargo, que el viaje te resulte interesante y despierte tu espíritu crítico.

Cada etapa tendrá un commit inicial con la versión de la etapa precedente y otro con los cambios aplicados. De esta manera será más facil ver el historial de cambios sobre un archivo en una etapa en particular, e incluso un simple analisis de diferencias por medio de la inspección entre los archivos de distintas etapas puede hacerse por alguien que no domine GIT.

### Refactoring 1 - Legibilidad
Agregar información sobre el autor, referencia hacia la publicación original y el propósito del código.

Debería haber una licencia, el autor original no la estableció y en este caso la licencia ya está definida a nivel global del repositorio. Agregaré una en la versión final.

Clarificar los datos de entrada que el usuario debe proveer a través de los parametros de una función que englobe el algoritmo.

Además es bueno aplicar una primera buena práctica sobre que la carga de un archivo Python tenga una forma diferente de ejecutarse cuando se lo llama directamente como script o se lo carga como módulo desde otro archivo.

Ahora incluso es posible llamar `help("flexion")` en un intérprete Python que dará la información del módulo como de las funciones definidas dentro.

Por último, los nombres de variables son crípticos y no siguen el estilo esperado en los códigos Python (u otro lenguaje). Sin embargo, después de reflexionar un poco, decidí que los mantendré hasta etapas de refactoring más avanzadas para que aquellos que ya están familiarizados con esos nombres (similares a los del diagrama de flujo) encuentren menos dificultades a la hora de seguir los cambios.

### Refactoring 2 - Pruebas unitarias
Las pruebas unitarias (Unit Tests en inglés) son indispensables en todo desarrollo de software. Nos permiten comprobar que los resultados de nuestros algoritmos son los que esperamos para las entradas dadas.

La existencia de este código que prueba nuestro código es requisito necesario para todo proceso de refactoring, nuestra premisa es mejorar (modificar) el código sin introducir errores en el algoritmo.

Yo no soy un experto en el algoritmo en cuestión, pero aún así puedo crear una batería de pruebas consiguiendo que se pase por cáda una de las ramas de decisión en cada caso. Un experto debería agregar los casos de prueba para las condiciones límites y asegurarse de modificar el algoritmo para que valores inchoerentes den una respuesta que parece válida cuando en realidad carece de lógica.

### Refactoring 3 - Legibilidad del algoritmo
La resolución del algoritmo sigue un relativamente largo diagrama de flujo que hace que al final la solución lleve muchas líneas. Por el momento veo problemas con eso: 1) dificulta la comprensión lectora y 2) puede que existan etapas que se repitan en otros algoritmos y por tanto terminemos con una duplicación del código.

Puede que el punto 2 no sea evidente en este pequeño ejemplo, pero no está de más tener en cuenta que el copiar/pegar código nos dice que hay algo mal en nuestro diseño (salvo contadas excepciones).

Las fórmulas se reemplazaron por funciones que describen su propósito hacen que no se necesiten comentarios para saber el resultado que devuelven. El código debe expresar por sí mismo el propósito y los comentarios deben dejarse para quellas condiciones o hipótesis no evidentes.

Al principio realicé la extracción de codigo en funciones sobre el mismo archivo y luego las pasé a otro donde las mismas puedan ser reutilizadas para otros proyectos. Aunque no se si correspondía para todas las funciones, dejo a un revisor que me apunte cualquier corrección.

### Refactoring 4 - Separación entre datos calculados y la presentación de resultados
En el refactoring 2 agregué las pruebas unitarias que se basan en que la respuesta del algoritmo son textos.
Esto en general no es lo adecuado.

Imaginemos que queremos hacer un algoritmo de optimización que a través de pequeñas variaciones en los datos de entrada evalúe si cumplimos o no con los criterios esperados. Ello sólo se puede hacer si contamos con los valores numéricos reales y no con las versiones *redondeadas* de ellos.

Ahora el algoritmo retorna los 3 valores numéricos en las unidades numéricas en las que opera y la conclusión está codificada en una enumeración clara, no ambigua, no sujeta a cómo se quiera presentar al usuario.

La presentación de los resultados se realiza ahora por medio de una función independiente.

### Refactoring 5 - Evitar duplicación de código en la Interfaz Gráfica de Usuario (GUI)
En esta etapa se importa el algoritmo definido en `flexion.py` y se utiliza la función correspondiente para convertir los resultados numéricos en las descripciones textuales. Ya no se deben mantener los dos algoritmos en paralelo.

Otra pequeña mejora fue centralizar la creación de componentes gráficos en funciones. Esto mejora la legibilidad de la construcción de la interfaz y permite que cualquier cambio en una misma categoría de la interfaz (entradas o resultados) sea automaticamente aplicado a todos los elementos del mismo tipo.

Esta separación tiene un gran impacto, sólo debemos preocuparnos en pasar los valores correctos entre interfaz y algoritmo, que la lógica está separada y verificada por las pruebas unitarias.

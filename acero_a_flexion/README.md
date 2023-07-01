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


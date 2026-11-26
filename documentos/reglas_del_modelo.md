# Reglas del modelo: minority game con opción de abstención

Acordadas con el Dr. Ricardo Mansilla (8 de octubre de 2026). Base para la sección de Metodología del protocolo.

## Reglas definitivas

- N agentes, con N no múltiplo de 3, de modo que nunca empatan las tres opciones.
- Cada agente elige 0 (comprar), 1 (vender) o 2 (abstenerse). Abstenerse es una tercera decisión propia, al mismo nivel que comprar y vender.
- El resultado del turno es la opción menos elegida, contando también una opción con cero agentes.
- Si las dos opciones menos elegidas empatan, se elige una con una moneda al aire (50 % cada una). Esto incluye el caso en que todos eligen lo mismo y las dos opciones vacías empatan en cero.
- El símbolo ganador se agrega a la serie de resultados colectivos, con alfabeto {0, 1, 2}.
- Ganan los agentes de la opción minoritaria; si está vacía, no gana ningún agente. Abstenerse puede ganar como cualquier otra opción.
- Cada agente tiene s estrategias que leen los últimos m resultados (3^m historias posibles) y prescriben 0, 1 o 2.
- Después de cada turno, las estrategias que habrían elegido la opción ganadora suman un punto virtual (incluidas las que prescribían abstenerse), y cada agente juega con la de mayor puntaje.

## Notas para la Introducción y perspectivas

- Conexión con la física: el minority game binario se ha estudiado con la mecánica estadística de sistemas desordenados (vidrios de espín; Challet, Marsili y Zecchina, PRL 2000). Con tres opciones simétricas, la analogía natural es el modelo de Potts de tres estados y su versión desordenada (vidrio de Potts). Usar como motivación y perspectiva, no como objetivo.

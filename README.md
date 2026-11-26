# Tesis
Simulación en Python de un minority game de tres decisiones (comprar, vender, abstenerse) y análisis de sus resultados con información mutua y complejidad física. Tesis de licenciatura en Ingeniería Física, UADY.

# Econofísica de un mercado artificial con abstención

Análisis informacional de un *minority game* de tres decisiones

Tesis de licenciatura en Ingeniería Física, Facultad de Ingeniería, Universidad Autónoma de Yucatán (UADY).

- **Autor:** Héctor Quijano Munguía
- **Asesores:** Ricardo Mansilla Corona (UNAM) y Saul J. Díaz Ceballos (UADY)

## Descripción

En el *minority game* (MG), N agentes eligen en cada turno entre dos opciones y ganan
los que quedan en la opción menos elegida. Cada agente recuerda solo los últimos m
resultados y decide con un conjunto de estrategias que califica según cómo le han ido.
El juego puede leerse como un modelo simplificado de mercado financiero.

En el juego original, todos los agentes tienen que participar en cada turno. Esta tesis
agrega una tercera decisión, **abstenerse**, con el mismo estatus que **comprar** y
**vender**: la abstención también puede ser la opción minoritaria y, por lo tanto, ganar.

El objetivo es estudiar cómo esta tercera opción cambia la estructura de información y
las dependencias temporales de la serie de resultados del juego, comparada con el juego
binario y con secuencias aleatorias.

## Qué contiene el repositorio

- Simulación en Python del MG de tres decisiones, con parámetros N, m, s y T y semillas
  reproducibles.
- Comparación entre agentes que eligen al azar, agentes con estrategias sin puntaje y
  agentes con puntaje.
- Variación del número de agentes N, con el parámetro de control γ = 3^m / N.
- Agentes conservadores, que se abstienen, y agresivos, que venden, siguiendo la
  tendencia reciente.
- Cálculo de la función de información mutua M(d) y su análisis en escala log-log.

## Trabajo en curso

- Complejidad física C(l) y espectro de potencias de M(d).
- Validación con la versión binaria del juego y homologación de las medidas entre
  alfabetos de 2 y 3 símbolos.
- Variación de la memoria m.
- Definición de un precio para el mercado simulado, comparación con índices bursátiles
  reales y búsqueda de burbujas con el modelo log-periódico de ley de potencias (LPPL).

## Referencias principales

- D. Challet y Y.-C. Zhang, *Physica A* 246, 407 (1997).
- R. Mansilla, *Phys. Rev. E* 62, 4553 (2000).
- R. Mansilla, *Physica A* 301, 483 (2001).

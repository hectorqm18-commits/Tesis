# Tesis: minority game de tres decisiones

Tesis de licenciatura de Héctor Quijano Munguía (Ingeniería Física, UADY). Asesores: Ricardo Mansilla Corona (UNAM) y Saul J. Díaz Ceballos (UADY).

Simulación en Python de un minority game con tres opciones (comprar, vender, abstenerse) y análisis de la serie de resultados con la función de información mutua M(d).

## Forma de trabajo

- Héctor decide. No se modifica, crea ni borra nada sin su autorización: primero se propone el cambio y se explica.
- Se avanza paso a paso. Héctor indica por dónde empezar.
- Héctor no es experto en Python: explica en español y con palabras sencillas qué hace cada cambio y por qué.
- `notebooks/` y `referencias/` son el respaldo de lo ya hecho y no se editan. Para cambiar o correr un notebook, se copia a `resultados/` y se trabaja en la copia.
- Todo lo nuevo (notebooks, CSV, gráficas) va en `resultados/`.
- Si un número no coincide con lo esperado, detente y repórtalo. No ajustes nada para que cuadre.
- Al terminar algo, di qué comprobaste y cómo. Si algo no se comprobó, dilo.

## Estructura de carpetas

```
tesis_mg/
  CLAUDE.md
  documentos/
    reglas_del_modelo.md
    fase4_decisiones.md       bitácora de decisiones y resultados
  reportes/                   reportes en PDF
  notebooks/
    Fase 2/                   ingenuos, 2 estrategias sin puntaje y 2 con puntaje (mismos parámetros); promedios de M(d)
    Fase 3/                   variación del número de agentes N; promedios de M(d)
    Fase 4/                   códigos anteriores a la corrida del 19/10 (fracciones de 0 a 20 %); promedios de M(d)
      Agresivos/              solo un script .py, con el mismo código que "Conservadores y agresivos.ipynb"
      Conservadores/          notebook con conservadores, agresivos y combinados, y carpetas con sus resultados
      Conservadores y agresivos/
    Fase 5/                   gráficas log-log de M(d); no simulan, leen los CSV de las fases 2, 3 y 4
  referencias/                resultados ya obtenidos (CSV e imágenes)
    Ref Fase 2/
    Ref Fase 3/               N = 125, 151 y 175; en "resultados anteriores": N = 100 a 4000 e imágenes
    Ref Fase 4/               solo resultados de conservadores
    Ref Fase 5/
      Ref Fase 5.1/           log-log de la fase 2: CSV de entrada; gráficas y resultados en "resultados_fase4_paso1"
      Ref Fase 5.2/           log-log de la fase 3: CSV de entrada; gráficas y resultados en "resultados_fase3_loglog"
      Ref Fase 5.3/           fase 4: CSV de entrada en "csv", imágenes sueltas, resumen y ajustes en CSV; faltan las gráficas log-log
  resultados/                 todo el trabajo nuevo
    Fase 6/                   transición al variar N (m = 2, s = 3); csv/, graficas/ y comprobaciones/
  TESIS/                      carpeta de trabajo anterior a la reorganización; contiene el notebook de la corrida del 19/10
```

Los notebooks se reorganizaron después de correrlos, así que sus rutas pueden apuntar a lugares que ya no existen. Las rutas se ajustan en la copia, nunca en el original.

## Fases y códigos

La numeración de las carpetas es la vigente. En los apuntes y en nombres de archivo antiguos, el análisis log-log aparece junto a la fase 4; por eso algunos archivos de la fase 5 se llaman `Fase4_...`.

| Fase | Archivo | Contenido |
|---|---|---|
| 2 | `Segundo_paso_tres_casos.ipynb` | Tres casos con N = 50 |
| 2 | `Segundo paso.ipynb` | Ingenuos, 2 estrategias sin recompensa y 3 estrategias con puntaje, en celdas separadas |
| 3 | `Paso 3.ipynb` | Variación de N de 100 a 4000 (`Paso_3`) y búsqueda de picos (`Paso_3b_picos`), con puntaje |
| 3 | `Paso_3.1.ipynb` | N = 125, 151 y 175, con puntaje |
| 4 | `TESIS/5/datos/5.3/Fase4_conservadores_agresivos.ipynb` | Corrida del 19/10: 10, 25 y 30 %; solo conservadores, solo agresivos y combinados. No está en `notebooks/` |
| 5 | `Fase 5.1.ipynb` | Log-log de los datos de la fase 2 (antes `Fase4_paso2_loglog_tres_casos`) |
| 5 | `fase 5.2.ipynb` | Log-log de los datos de la fase 3 (antes `Fase3_loglog_N100_N200`) |
| 5 | `Fase5.3_loglog.ipynb` | Log-log de los datos de la fase 4 (antes `Fase4_loglog`) |

Los códigos de `notebooks/Fase 4/` usan fracciones de 0 a 20 % y no reproducen la corrida del 19/10. `Conservadores.ipynb` (7/10) incluye conservadores, agresivos y combinados. `Conservadores y agresivos.ipynb` (12/10) y el `.py` de `Agresivos/` tienen las mismas líneas de código. Confírmalo con Héctor antes de usarlos.

`Ref Fase 5.3/csv` parece ser la salida de la corrida del 19/10 (108 archivos: 3 tipos, 6 valores de N, 3 fracciones, promedio y todas las cadenas).

## Modelo

@documentos/reglas_del_modelo.md

- Etiquetas: 0 = comprar, 1 = vender, 2 = abstenerse (protocolo). Los comentarios e impresiones de los notebooks todavía dicen 0 = vender y 1 = comprar. Por la simetría del juego no cambia ningún número, pero hay que unificarlas antes de definir el precio.
- Conservadores: eligen 2 si el 2 ganó en más de la mitad de los últimos m turnos (con m = 3: 022, 122, 202, 212, 220, 221, 222).
- Agresivos: eligen 1 si el 1 ganó en más de la mitad de los últimos m turnos (con m = 3: 011, 101, 110, 111, 112, 121, 211).
- N no debe ser múltiplo de 3. Si una corrida nueva usa un múltiplo de 3, avisa antes. Ya existen corridas con N = 150, 300 y 3000.

## Parámetros base

m = 3, s = 2, K = 3, T = 6000, sin burn-in, 100 cadenas, d = 1..100. Semilla maestra: 1907443528.

## Análisis

- M(d) se calcula con frecuencias relativas y logaritmo base 2 (bits), y se promedia sobre las 100 cadenas.
- Log-log: log10 M(d) contra log10 d, con ajuste lineal (`np.polyfit` de grado 1) usando todos los d = 1..100. El único filtro es quitar los puntos con M(d) = 0.
- Toda gráfica log-log reporta la pendiente y R².
- No agregues ajuste semilog, filtro de piso de ruido ni otras comparaciones si Héctor no lo pide.
- Nivel de referencia: M(d) promedio de agentes ingenuos, ≈ 4.9×10⁻⁴ bits (log10 M ≈ −3.31).
- γ = K^m/N es el parámetro de control. No va en los títulos de las gráficas, pero sí en el CSV (columna `gamma`).
- En el protocolo v5.5, el exponente de M(d) es b (M(d) ∝ d^−b) y α es el exponente de C(l). Los apuntes del 19/10 llaman α al exponente de M(d), y los códigos más viejos llamaban alfa a γ.

## Convenciones de los notebooks

- Casi todos los notebooks tienen una sola celda con código, con los parámetros al inicio y cada lista en una línea (por ejemplo, `LISTA_N`). Las excepciones son `Segundo paso` (3 códigos), `Paso 3` (2) y `Conservadores` (4).
- Las opciones `DESCARGAR_GRAFICAS` y `GUARDAR_CSV` van al inicio.
- Las cadenas se reparten entre núcleos con `joblib`, y el resultado debe ser idéntico al de un solo núcleo.
- Los nombres de los archivos llevan los parámetros de la corrida para no sobrescribir corridas anteriores.
- Entorno: Windows, con Jupyter en VS Code.

## Valores para comprobar que todo se reproduce

| Caso (ajuste log-log) | Pendiente | R² |
|---|---|---|
| Fase 2, N = 50, ingenuos | −0.0014 | 0.0004 |
| Fase 2, N = 50, 2 estrategias sin puntaje | −0.9921 | 0.8419 |
| Fase 2, N = 50, 2 estrategias con puntaje | −0.6067 | 0.5842 |
| Fase 3, N = 100, con puntaje | −0.4437 | 0.5322 |
| Fase 3, N = 200, con puntaje | +0.0320 | 0.0078 |

Las 54 pendientes de la fase 4 están en `documentos/fase4_decisiones.md`.

Una simulación se reproduce si sus CSV son idénticos número por número (`np.array_equal`) a los de `referencias/`.

## En pausa hasta que Héctor lo indique

Indicaciones del 21/10:
- Buscar qué función describe la forma de M(d).
- Explicar por qué N = 50, combinados 30 %, sale mucho más plana que las demás.

## Detalles conocidos del código

Ninguno cambia los resultados. No los corrijas sin autorización.
- En `Segundo_paso_tres_casos`, el comentario sobre `CASOS` está desactualizado: T ya es 6000 en los tres casos.
- En ese mismo notebook, `BURN_IN` solo se aplica a los ingenuos.
- La tasa de éxito al azar 0.265 está escrita a mano y solo vale para N = 50.
- Todavía no se registra la frecuencia de turnos decididos con moneda, que el protocolo pide.

## Lo que falta según el protocolo (v5.5)

Complejidad física C_K(l) y su versión normalizada, espectro de potencias de M(d), referencias con series barajadas, versión binaria del juego para validar, homologación entre alfabetos, variación de m (N = 101 sugerido, s = 2 y 3), precio y series de tiempo, y burbujas con LPPL.

## Documentos de consulta

- `documentos/fase4_decisiones.md`: decisiones y resultados de las fases 2 a 5. Léelo antes de cambiar cualquier análisis.
- `reportes/`: reportes en PDF. Los de más de 10 páginas se leen por rangos de páginas.

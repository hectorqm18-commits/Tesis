# Análisis log-log de M(d) (ley de potencias) — apuntes de decisiones

Inicio: 19 de octubre de 2026. Insumo para el reporte en LaTeX para el Dr. Mansilla.

## Nombres de las fases (según Héctor, 19/10)
- Fase 2: tres casos con N = 50 (ingenuos, 2 estrategias sin puntaje, 2 estrategias con puntaje). Código: Segundo_paso_tres_casos.
- Fase 3: aumento del número de agentes, N = 100, 200, 300, 400 y 1000, 2000, 3000, 4000 (m = 3, s = 2); el 19/10 se agregaron N = 125, 150, 175. Código: Paso_3 (con Paso 3b de picos).
- Fase 4: agentes conservadores y agresivos. Nueva corrida el 19/10 con el código Fase4_conservadores_agresivos.

## Origen (reunión con Mansilla)
- Toda gráfica de M(d) con forma de exponencial negativa se grafica en escala log-log, log M(d) contra log d, para ver si forma una línea recta.
- Hipótesis de ley de potencias: M(d) = A / d^α, de donde log M(d) = log A − α·log d.
  - Pendiente de la recta = −α (α es el exponente de decaimiento).
  - Ordenada al origen = log A; A = M(1) es la amplitud.
- Motivación: una recta en log-log indica decaimiento sin escala característica (correlaciones de largo alcance). Una exponencial (memoria corta, como una cadena de Markov) es recta en semilog. Ver W. Li (1990), Sec. 3 y Fig. 4; Mansilla PRE 62, Sec. III (espectro 1/f^a, ausencia de escala de tiempo característica).

## Decisiones tomadas
1. (19/10) NOTACIÓN: el parámetro de control 3^m/N se llama ahora **γ** (antes α). El exponente de la ley de potencias es **α**.
2. (19/10) Valores a reportar para TODAS las gráficas: **R²** y **la pendiente** del ajuste lineal en log-log.
3. (19/10) ÚNICO filtro: se eliminan los puntos con M(d) = 0 (log 0 no existe). Indicado por Mansilla.
4. (19/10) Una sola versión de cada gráfica: con el filtro de ceros. NO se hace versión con datos crudos ni con filtro de piso de ruido (series barajadas). Ese filtro queda descartado por ahora.
5. (19/10) NO se agrega ninguna comparación (ni ajuste semilog/exponencial).
6. (19/10) Forma de trabajo: Héctor pasa cada código con sus resultados y las gráficas se construyen paso a paso, sin prisa. Héctor indica por dónde empezar. No se modifica nada sin su autorización.
7. (19/10) Se llevará un reporte en LaTeX con los resultados.
8. (19/10) γ NO va en el título de las gráficas (a Mansilla no le gusta), pero no se desecha: se guarda en el CSV de resultados (columna gamma) y en el código.
9. (19/10) Fase 3: se hace el log-log de N = 100 y N = 200 con el mismo procedimiento (todos los puntos, solo filtro de ceros). Según lo que diga Mansilla se decide si se sigue con N mayores (y si se ajustaría desde d = 4).
10. (19/10) Fase 3: Héctor decidió correr N = 125, 150 y 175 (incluye 150 aunque es múltiplo de 3; se avisó de la regla y Héctor eligió 150).
11. (19/10) Código Paso_3 adaptado: los N se cambian en UNA línea (LISTA_N); las gráficas se agrupan solas en grupos de hasta 4 N; los nombres de gráficas y resumen llevan los N corridos (no se sobrescriben corridas anteriores); "alfa" → "gamma" en pantalla y CSV; γ quitado de la leyenda de las gráficas. Verificado: con LISTA_N = [100] reproduce exactamente el CSV de N = 100 que ya tenía Héctor.
12. (19/10) Fase 4 nueva corrida (pedida por Héctor): fracciones 10 %, 25 % y 30 %; N = 50, 100, 125, 151, 175, 200 (Héctor usó 151, no 150); tres casos por (N, fracción): solo conservadores, solo agresivos y combinados (misma fracción de cada tipo). Un solo código (Fase4_conservadores_agresivos); N y fracciones en una línea cada uno. Gráficas agrupadas por N (confirmado por Héctor): una figura por N con un panel por fracción y las tres curvas juntas.
13. (19/10) Fase 4: log-log de las 54 curvas, agrupadas por N, guardando pendiente y R² de todas (pedido de Héctor). Código aparte (Fase4_loglog) que lee los CSV, mismo procedimiento que fases 2 y 3. Figura por N: cuadrícula 3×3 (filas = %, columnas = tipo), cada panel con su recta, pendiente y R².
14. (20/10) Reporte LaTeX (Reporte_loglog_Quijano.pdf, 14 págs., XeLaTeX): se QUITÓ la fórmula (K−1)²/(2n ln 2) porque Héctor aún no la puede sustentar. En su lugar se usa el "nivel de referencia" empírico: M(d) promedio de los agentes ingenuos ≈ 4.9×10⁻⁴ bits (log10 M ≈ −3.31). La versión con la fórmula quedó guardada aparte.

## Reunión con Mansilla (21/10)
- Vio bien el reporte en general.
- Preguntó por qué N = 50, combinados 30 % sale mucho más "chata" que las demás y por qué no pasa con N mayores ("¿está mal?"). Héctor pidió NO contestarlo por ahora (21/10). Lo que ya se sabe (sin presentar aún): una de las 100 cadenas (semilla 2010503120) entra en el turno 593 a un ciclo "1212…" del que no sale. En la historia 121 los 15 agresivos van forzados al 1 y gana el 2 (conteos 15/24/11); en la 212 los 15 conservadores van forzados al 2 y gana el 1 por un agente (15/14/21). En los demás casos de la fase 4 (5400 cadenas en total) no hay ninguna otra cadena atrapada. Se intentó contar la frecuencia con 500 semillas nuevas, pero se detuvo a pedido de Héctor.
- Como no se formó una recta, ahora hay que buscar QUÉ FUNCIÓN describe y predice la forma de M(d). TENERLO EN CUENTA, NO HACERLO TODAVÍA (indicación de Héctor).
- Pidió el CSV de una curva con esa forma: se le entregó la de la fase 2, N = 50, 2 estrategias con puntaje (la del reporte), con columna 1 = log10 M(d) (eje y) y columna 2 = log10 d (eje x), d = 1..100. Archivo: loglog_Md_N50_2estrategias_con_puntaje.csv. Verificado: con esas columnas el ajuste da pendiente −0.6067 y R² 0.5842, igual que el reporte. (Héctor la llamó "3 estrategias"; en realidad es m = 3, s = 2.)

## Detalles de implementación (análisis log-log)
Códigos: Fase4_paso2_loglog_tres_casos (fase 2), Fase3_loglog_N100_N200 (fase 3; la lista N_A_ANALIZAR permite agregar más N) y Fase4_loglog (fase 4).
- No se vuelve a simular: se leen los CSV "todas_las_cadenas" y se promedia M(d) sobre las 100 cadenas (misma curva promedio de los notebooks originales).
- Logaritmo base 10 (la pendiente y R² no dependen de la base).
- Ajuste por mínimos cuadrados (np.polyfit grado 1) con todos los puntos d = 1..100 que quedan tras quitar los ceros.
- R² = 1 − SS_res/SS_tot sobre los puntos en log-log.
- Se grafica log10 M(d) contra log10 d en ejes lineales, con la recta y los valores de pendiente y R² en la gráfica.
- Opciones DESCARGAR_GRAFICAS y GUARDAR_CSV al inicio del código.
- Verificación de datos (19/10): los CSV de la fase 2 y los de N = 100 y 200 de la fase 3 tienen 100 filas con las 100 semillas de la semilla maestra 1907443528, sus promedios coinciden con la salida de los notebooks y no tienen ceros.

## Detalles de implementación (código Fase4_conservadores_agresivos)
- Reglas tomadas del código original de la fase 4 (chat del 7/10): conservadores eligen 2 en historias con al menos dos "2" (022, 122, 202, 212, 220, 221, 222); agresivos eligen 1 en historias con al menos dos "1" (011, 101, 110, 111, 112, 121, 211); en ambas tablas de estrategias.
- Elección de tipos: generador aparte np.random.default_rng([semilla, 2024]), permutación de los N agentes; conservadores = los primeros, agresivos = los últimos (nunca se enciman).
- Número por tipo: floor(fracción·N + 0.5). N=50: 5, 13, 15; N=100: 10, 25, 30; N=125: 13, 31, 38; N=151: 15, 38, 45; N=175: 18, 44, 53; N=200: 20, 50, 60.
- Base: 2 estrategias con puntaje, m=3, K=3, T=6000, sin burn-in, 100 semillas (semilla maestra 1907443528). joblib para varios núcleos.
- Verificado: con 0 % de especiales reproduce los datos de N = 50 (fase 2) y N = 100 (fase 3).
- Salidas: CSV promedio y todas_las_cadenas por (tipo, N, fracción) en resultados_fase4/csv (108 archivos); Fase4_resumen.csv; una PNG por N (Fase4_Md_N<N>.png), paneles con la misma escala vertical.
- Tiempo: 11.3 min en el entorno de Claude (2 núcleos).

## Ideas descartadas por ahora (por si se retoman)
- Piso de ruido con series barajadas para excluir valores muy pequeños de M(d). Contexto: el estimador por frecuencias se estanca en un sesgo positivo ≈ (K−1)²/(2·T·ln 2) bits (≈ 4.8×10⁻⁴ con K = 3, T = 6000), que puede aplanar la recta.
- Ajuste semilog para distinguir exponencial de ley de potencias.

## Inventario de curvas por analizar
- [HECHO 19/10] Fase 2: 3 casos (ingenuos, sin puntaje, con puntaje) con N = 50.
- [HECHO 19/10] Fase 3, con puntaje: log-log de N = 100 y N = 200.
- [DATOS LISTOS 19/10] Fase 3, con puntaje: N = 125, 150, 175 (falta decidir si se les hace log-log).
- Fase 3, con puntaje, N ≥ 300: en espera de lo que diga Mansilla.
- Fase 3, sin puntaje: pendiente saber si hay datos.
- [HECHO 19/10] Fase 4: log-log de conservadores, agresivos y combinados; 10/25/30 %; N = 50, 100, 125, 151, 175, 200.
- No aplica: curva en U del Paso 1 (es volatilidad, no M(d)).

## Bitácora de resultados

### 19/10 — Fase 2, tres casos (N = 50, m = 3, K = 3, T = 6000, γ = 0.54, 100 semillas)
| Caso | Ceros eliminados | Puntos | Pendiente | R² |
|---|---|---|---|---|
| Ingenuos | 0 | 100 | −0.0014 | 0.0004 |
| 2 estrategias sin puntaje | 0 | 100 | −0.9921 | 0.8419 |
| 2 estrategias con puntaje | 0 | 100 | −0.6067 | 0.5842 |

Observaciones (lectura de Claude, pendiente de discutir con Héctor):
- Ninguna curva promedio tiene ceros, así que el filtro no quitó puntos.
- Ingenuos: nube horizontal alrededor de log10 M ≈ −3.31 (M ≈ 4.9×10⁻⁴). No hay decaimiento; pendiente ≈ 0 y R² ≈ 0. Es la curva de referencia.
- Sin puntaje: los puntos bajan de forma curva, no recta: meseta en d = 1–3, caída fuerte hasta d ≈ 10 y luego se aplana cerca de −3.25. La recta pasa por encima al inicio y por debajo al final.
- Con puntaje: mismo patrón, más marcado: meseta en d = 1–3, caída hasta d ≈ 9 y desde d ≈ 10 queda plana en ≈ −3.3. R² más bajo porque la mayoría de los puntos están en la parte plana.

### 19/10 — Fase 3, con puntaje: forma de las curvas (notebook Paso_3; N = 125, 150, 175 corridos el 19/10)
| N | γ | M(1) | M(2) | M(3) | M(4) | Máximo en |
|---|---|---|---|---|---|---|
| 100 | 0.270 | 9.2×10⁻³ | 1.13×10⁻² | 1.03×10⁻² | 3.4×10⁻³ | d = 2 |
| 125 | 0.216 | 4.8×10⁻³ | 5.4×10⁻³ | 5.6×10⁻³ | 2.9×10⁻³ | d = 3 |
| 150 | 0.180 | 1.7×10⁻³ | 1.7×10⁻³ | 2.0×10⁻³ | 3.0×10⁻³ | d = 4 |
| 175 | 0.154 | 3.8×10⁻⁴ | 4.5×10⁻⁴ | 4.1×10⁻⁴ | 3.5×10⁻³ | d = 4 |
| 200 | 0.135 | 1.9×10⁻⁴ | 8.5×10⁻⁵ | 1.3×10⁻⁴ | 3.7×10⁻³ | d = 4 |
| 300 | 0.090 | 2.0×10⁻⁶ | 2.2×10⁻⁶ | 2.1×10⁻⁶ | 4.6×10⁻³ | d = 4 |
| 400 | 0.0675 | 1.3×10⁻⁶ | 1.6×10⁻⁶ | 1.5×10⁻⁶ | 5.4×10⁻³ | d = 4 |
| 1000–4000 | ≤ 0.027 | ≈ 1×10⁻⁶ | ≈ 1×10⁻⁶ | ≈ 1×10⁻⁶ | 6.4–7.0×10⁻³ | d = 4 |
(Nivel de referencia, agentes ingenuos: ≈ 4.9×10⁻⁴.)
Tasa de éxito vs. azar: N = 125: 0.3130 vs 0.2901; N = 150: 0.3129 vs 0.2937; N = 175: 0.3099 vs 0.2967 (los tres todavía por encima del azar; el cruce está entre 200 y 300).
Observaciones (lectura de Claude):
- N = 100 y 125: meseta en d = 1–3 y caída. Cumplen el criterio de Mansilla.
- N = 150: caso intermedio. M(1)–M(3) siguen por encima del nivel de referencia (≈ 3.5 veces), pero el máximo ya está en d = 4.
- N = 175: M(1)–M(3) ya están en el nivel de referencia; forma igual a N = 200.
- El cambio de forma es progresivo entre N = 125 y N = 175: M(1) baja ~25 veces (4.8×10⁻³ → 3.8×10⁻⁴) mientras M(4) apenas cambia.

### 19/10 — Fase 3, con puntaje: ajuste log-log de N = 100 y N = 200 (código Fase3_loglog_N100_N200)
| N | γ | Ceros eliminados | Puntos | Pendiente | R² |
|---|---|---|---|---|---|
| 100 | 0.270 | 0 | 100 | −0.4437 | 0.5322 |
| 200 | 0.135 | 0 | 100 | +0.0320 | 0.0078 |

Observaciones (lectura de Claude):
- N = 100: misma forma que N = 50 con puntaje: meseta en d = 1–3 (log10 M ≈ −2.0), caída hasta d ≈ 8 y luego plana en ≈ −3.3. Pendiente menos negativa que con N = 50 (−0.61) y R² algo menor (0.53 contra 0.58).
- N = 200: d = 1–3 muy abajo (log10 M entre −3.7 y −4.1), pico en d = 4 (≈ −2.43), caída hasta d ≈ 7 y luego plano en ≈ −3.3. La recta queda casi horizontal (pendiente ≈ 0, R² ≈ 0): con todos los puntos no hay ley de potencias.
- Secuencia con puntaje: N = 50 → −0.61 (R² 0.58); N = 100 → −0.44 (R² 0.53); N = 200 → +0.03 (R² 0.01). El cambio grande ocurre entre N = 100 y N = 200 (γ entre 0.27 y 0.135).

### 19/10 — Fase 4 (nueva corrida): conservadores, agresivos y combinados; 10/25/30 %
Valores clave (Fase4_resumen.csv):
| N | Caso | 10 %: M(1) | 25 %: M(1) | 30 %: M(1) | Máximo en |
|---|---|---|---|---|---|
| 50 | cons / agr / comb | 3.6 / 3.0 / 4.4 ×10⁻² | 4.2 / 3.7 / 6.5 ×10⁻² | 4.1 / 3.6 / 7.1 ×10⁻² | d = 1–2 |
| 100 | cons / agr / comb | 1.7 / 1.6 / 2.6 ×10⁻² | 2.0 / 1.9 / 3.7 ×10⁻² | 2.0 / 1.8 / 3.6 ×10⁻² | d = 2 |
| 200 | cons / agr / comb | 0.68 / 0.67 / 2.0 ×10⁻² | 1.3 / 1.2 / 3.1 ×10⁻² | 1.3 / 1.2 / 3.1 ×10⁻² | d = 2 |
Frecuencias (N = 200): solo conservadores 25–30 %: f(2) = 0.277; solo agresivos: f(1) = 0.277; combinados: f(0) = 0.397, f(1) = f(2) = 0.302. Con 10 %: f(2) = 0.296 (cons), f(0) = 0.386 (comb).
Tasa de éxito (N = 200, 30 %): especiales 0.266–0.269; comunes 0.327 (solo un tipo) y 0.333 (combinados).
Observaciones (lectura de Claude):
- Con agentes especiales, en TODAS las N la curva decae desde d ≈ 1–2 (máximo en d = 1, 2 o 3). La forma de la fase abarrotada sin especiales (M(1)–M(3) ≈ 0 y pico en d = 4 desde N ≈ 175) desaparece: con 10 % o más de especiales ya no aparece en N = 175–200.
- Conservadores y agresivos dan prácticamente lo mismo (espejo), como en la corrida del 7/10.
- 25 % y 30 % dan casi lo mismo: el sistema está saturado. Las frecuencias coinciden con las predicciones de cadena de Markov del 7/10: f = 5/18 = 0.278 para el símbolo "protegido" con un tipo; f(0) = 25/63 = 0.397 con combinados.
- Con 10 % y N grande todavía no está saturado (f(2) = 0.296 > 0.278).
- Combinados tienen M(d) mayor que un solo tipo (en N = 200, unas 2.5 veces).
- Arriba de la saturación los especiales pierden (≈ 0.27) y los comunes ganan (hasta 0.333).

### 19/10 — Fase 4: ajuste log-log de las 54 curvas (código Fase4_loglog)
Figuras: una por N (Fase4_loglog_N<N>.png), cuadrícula 3×3 (filas = 10/25/30 %, columnas = solo conservadores, solo agresivos, combinados). CSV: Fase4_ajustes_loglog.csv (tipo, N, gamma, %, agentes, ceros, puntos, pendiente, R², ordenada). Ninguna curva tuvo ceros (100 puntos en todas).
Pendientes (N = 50, 100, 125, 151, 175, 200):
| Caso | 10 % | 25 % | 30 % |
|---|---|---|---|
| Solo conservadores | −0.66, −0.54, −0.47, −0.43, −0.40, −0.36 | −0.71, −0.57, −0.53, −0.50, −0.47, −0.46 | −0.73, −0.56, −0.52, −0.49, −0.47, −0.46 |
| Solo agresivos | −0.66, −0.52, −0.48, −0.44, −0.41, −0.36 | −0.68, −0.56, −0.54, −0.49, −0.47, −0.46 | −0.69, −0.56, −0.52, −0.49, −0.47, −0.44 |
| Combinados | −0.72, −0.61, −0.61, −0.56, −0.55, −0.54 | −0.89, −0.74, −0.73, −0.68, −0.65, −0.65 | −0.31*, −0.74, −0.72, −0.67, −0.67, −0.64 |
R²: entre 0.47 y 0.66 en todas las curvas.
Observaciones (lectura de Claude):
- Todas las curvas tienen la misma forma que en la fase 2: meseta en d = 1–3, caída hasta d ≈ 8–10 y luego plano en el nivel de referencia (log10 M ≈ −3.3). Por eso R² ≈ 0.5–0.6: no es una recta.
- La pendiente se vuelve menos negativa al crecer N, en todos los casos.
- Conservadores y agresivos dan pendientes casi iguales (espejo). Combinados, más negativas.
- 25 % y 30 % casi iguales (saturación), salvo el caso marcado con *.
- * N = 50, combinados 30 %: UNA de las 100 cadenas (semilla 2010503120) quedó atrapada en un ciclo determinista "2121…" (frecuencias 0: 0.04, 1: 0.48, 2: 0.48; M(d) ≈ 0.84 bits a toda distancia). Esa sola cadena sube el promedio en ≈ 8.4×10⁻³ y deja la cola plana en log10 M ≈ −2.05 en vez de −3.3; de ahí la pendiente −0.31. En las otras 99 cadenas la cola está en el nivel de referencia. Es un resultado real de la dinámica, no un error del código. Mansilla preguntó por esto el 21/10 (ver arriba).

### Notas
- Regla del modelo (acordada con Mansilla el 8/10): N no múltiplo de 3. Las corridas de N = 300 y 3000 (7/10) y la de N = 150 (19/10, decisión de Héctor) son múltiplos de 3. Conviene mencionárselo a Mansilla.
- Fase 4 usa N = 151; no hay curva de referencia sin especiales para N = 151 (la fase 3 usó 150).

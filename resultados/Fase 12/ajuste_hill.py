#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ajuste de la función H(x) = A + B / (1 + (x/C)**alfa).

INSTALACIÓN (Python 3.10 o posterior):
    python -m pip install numpy scipy pandas openpyxl matplotlib
    # Para Excel antiguo (.xls), instalar además: python -m pip install xlrd

EJEMPLOS:
    python ajuste_hill.py datos.xlsx
    python ajuste_hill.py datos.csv
    python ajuste_hill.py datos.csv --separador ";" --decimal ","
    python ajuste_hill.py datos.xlsx --hoja "Hoja2" --cabecera si
    python ajuste_hill.py datos.csv --cabecera no --mostrar
    python ajuste_hill.py
    # Sin argumentos, se abre un selector de archivo; si no hay interfaz,
    # se solicita la ruta en la consola.

SIGNIFICADO DE LOS COEFICIENTES:
    A: valor al que tiende H(x) cuando x crece indefinidamente.
    B: diferencia entre H(0) y A; por tanto, H(0) = A + B.
    C: valor positivo de x donde H(C) = A + B/2; tiene las unidades de x.
    alfa: exponente positivo que controla la forma y rapidez de la transición.
    Si la entrada contiene x = log10(d) e y = log10(M(d)), estos parámetros
    describen la curva en esas coordenadas, no directamente la escala original.

ENTRADA:
    Primera columna: x. Segunda columna: y. Otras columnas se ignoran.
    Admite .xlsx, .xlsm, .xls y .csv (también la extensión escrita .cvs).
    La primera hoja se usa por defecto. Puede haber o no encabezados.
    Se ignoran solamente las filas con AMBAS celdas vacías; las demás filas
    inválidas producen un error con su número de fila/registro.
    No se transforman las variables: si ya son logaritmos, se ajustan así.
    Se necesita x >= 0, al menos 5 pares válidos y 4 valores distintos de x.
    --cabecera auto interpreta la primera fila no vacía como encabezado
    solamente si ambas celdas son textos no numéricos. Use si o no para
    indicar explícitamente si el archivo contiene encabezados.

MÉTODO:
    Mínimos cuadrados no ponderados en los valores y suministrados.
    Para cada C y alfa, A y B se obtienen por mínimos cuadrados lineales.
    Se optimizan log(C) y log(alfa) con múltiples puntos iniciales, conservando
    la mejor solución convergente. Esto reduce problemas numéricos, aunque
    no garantiza el mínimo global. A y B pueden tener cualquier signo;
    C > 0 y alfa > 0. B > 0 describe una curva decreciente y B < 0, creciente.
    Por defecto se busca 0.01 <= alfa <= 100 y min(x>0)/1000 <= C <= max(x)*1000.
    Estos límites son configurables. Una solución en el límite se advierte.

INDICADORES DEL AJUSTE:
    Residuo_i = y_i - H(x_i).
    SSE = suma de los cuadrados de los residuos.
    RMSE = raíz de SSE/n, en las mismas unidades que la columna dependiente.
    R² = 1 - SSE / suma((y_i - media(y))**2).
    Se trata de medidas del ajuste a los datos utilizados, no de validación
    predictiva. El código avisa si detecta parámetros débilmente identificados.

SALIDAS (en una carpeta nueva junto al archivo, o en --salida):
    coeficientes.json: A, B, C, alfa, R², RMSE, SSE y detalles del ajuste.
    predicciones.csv: filas originales, x, y, y ajustada y residuos.
    ajuste_hill.png: datos, curva ajustada y residuos.
    El archivo original no se modifica. Si la carpeta ya existe, se crea
    otra con un sufijo numérico para conservar los resultados anteriores.

REFERENCIAS TÉCNICAS:
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html
    https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html
    https://docs.python.org/3/library/csv.html
"""

from __future__ import annotations

import argparse
import csv
import itertools
import json
from pathlib import Path
import sys

try:
    import numpy as np
    import pandas as pd
    from scipy.optimize import least_squares
    from scipy.special import expit
except ImportError as exc:
    raise SystemExit(
        "Falta una dependencia. Ejecute:\n"
        "python -m pip install numpy scipy pandas openpyxl matplotlib"
    ) from exc


def hill(x, A, B, C, alfa):
    """Calcula H(x) = A + B / (1 + (x/C)**alfa).

    Parámetros
    ----------
    x : número o arreglo de números
        Variable independiente, con valores finitos no negativos.
    A, B : números reales finitos
        Nivel asintótico y amplitud, respectivamente.
    C, alfa : números reales positivos
        Escala de x y exponente de Hill.

    Devuelve
    --------
    Valor o arreglo con la misma forma que x, con la función evaluada.

    Notas
    -----
    Se usa 1/(1+exp(t)) = expit(-t), con t = alfa*log(x/C),
    para evitar desbordamientos al elevar x/C a potencias grandes.
    En x = 0 se usa su límite: H(0) = A + B.
    """
    x = np.asarray(x, dtype=float)
    if not np.isfinite(x).all() or np.any(x < 0):
        raise ValueError("La función necesita valores finitos de x >= 0.")
    if not (np.isfinite([A, B, C, alfa]).all() and C > 0 and alfa > 0):
        raise ValueError("A y B deben ser finitos; C y alfa deben ser positivos.")
    logx = np.full(x.shape, -np.inf)
    np.log(x, out=logx, where=x > 0)
    return A + B * expit(-alfa * (logx - np.log(C)))


def _numero(valor, decimal="."):
    """Convierte una celda a número; devuelve NaN si no es convertible.

    El NaN se usa solamente para detectar errores de entrada más adelante.
    No se eliminan automáticamente los registros que no son numéricos.
    """
    if isinstance(valor, str):
        valor = valor.strip().replace(decimal, ".")
    try:
        return float(valor)
    except (ValueError, TypeError):
        return np.nan


def cargar_datos(archivo, hoja=0, cabecera="auto", separador=None,
                 decimal=".", codificacion="utf-8-sig"):
    """Lee las dos primeras columnas de Excel o CSV y comprueba sus valores.

    Parámetros
    ----------
    archivo : ruta o cadena
        Archivo que contiene la variable independiente y la dependiente.
    hoja : entero o cadena
        Índice (desde cero) o nombre de la hoja Excel. No se usa para CSV.
    cabecera : 'auto', 'si' o 'no'
        Determina si la primera fila no vacía contiene los nombres.
    separador : carácter o None
        Separador del CSV; None intenta detectar coma, punto y coma,
        tabulador o barra vertical.
    decimal : '.' o ','
        Separador decimal empleado en las celdas de texto.
    codificacion : cadena
        Codificación del CSV. 'utf-8-sig' también admite archivos con BOM.

    Devuelve
    --------
    x, y : arreglos numéricos
        Datos originales, en su orden de entrada, sin aplicar logaritmos.
    filas : arreglo de enteros
        Filas de Excel o registros de CSV, contando desde uno.
    etiquetas : pareja de cadenas
        Nombres de las columnas; si no hay encabezados, se usa ('x', 'y').

    Genera ValueError si faltan datos, hay pares incompletos o valores
    no numéricos. Solo se ignoran las filas con ambas celdas vacías.
    """
    archivo = Path(archivo).expanduser()
    if decimal not in (".", ",") or cabecera not in ("auto", "si", "no"):
        raise ValueError("Revise --decimal y --cabecera.")
    if not archivo.is_file():
        raise ValueError(f"No existe el archivo: {archivo}")
    extension = archivo.suffix.lower()
    try:
        if extension in (".xlsx", ".xlsm", ".xls"):
            motor = "xlrd" if extension == ".xls" else "openpyxl"
            tabla = pd.read_excel(archivo, sheet_name=hoja, header=None,
                                  engine=motor, keep_default_na=False)
        elif extension in (".csv", ".cvs"):
            if separador is None:
                with archivo.open(encoding=codificacion) as entrada:
                    muestra = "\n".join(linea for linea in entrada.read(65536).splitlines()
                                          if linea.strip())
                try:
                    separador = csv.Sniffer().sniff(muestra, delimiters=",;\t|").delimiter
                except csv.Error as exc:
                    raise ValueError("No se pudo detectar el separador. Indíquelo con --separador.") from exc
            if separador == "\\t":
                separador = "\t"
            if len(separador) != 1:
                raise ValueError("--separador debe ser un solo carácter.")
            try:
                with archivo.open(encoding=codificacion, newline="") as entrada:
                    registros = [fila[:2] + [None] * max(0, 2 - len(fila))
                                 for fila in csv.reader(entrada, delimiter=separador, strict=True)]
                tabla = pd.DataFrame(registros, columns=[0, 1])
            except csv.Error as exc:
                raise ValueError(f"CSV mal formado: {exc}") from exc
        else:
            raise ValueError("Formato admitido: .xlsx, .xlsm, .xls o .csv.")
    except ImportError as exc:
        motor = "xlrd" if extension == ".xls" else "openpyxl"
        raise ValueError(f"Para leer este Excel, instale: python -m pip install {motor}") from exc
    if tabla.shape[1] < 2:
        raise ValueError("El archivo debe contener al menos dos columnas. Revise el separador del CSV.")
    tabla = tabla.iloc[:, :2].copy()
    # Conservar el índice de origen incluso si se eliminan filas vacías.
    vacia = tabla.apply(lambda col: col.map(
        lambda v: pd.isna(v) or (isinstance(v, str) and not v.strip())
    )).all(axis=1)
    tabla = tabla.loc[~vacia]
    if tabla.empty:
        raise ValueError("El archivo no contiene pares de datos.")
    primero = tabla.iloc[0].tolist()
    tiene_cabecera = cabecera == "si" or (
        cabecera == "auto" and all(
            isinstance(v, str) and v.strip() and np.isnan(_numero(v, decimal))
            for v in primero
        )
    )
    etiquetas = tuple(str(v) for v in primero) if tiene_cabecera else ("x", "y")
    if tiene_cabecera:
        tabla = tabla.iloc[1:]
    numeros = np.array([[_numero(v, decimal) for v in fila]
                        for fila in tabla.itertuples(index=False, name=None)], dtype=float)
    if numeros.size == 0:
        raise ValueError("No hay datos después del encabezado.")
    invalidas = ~np.isfinite(numeros).all(axis=1)
    if invalidas.any():
        filas = ", ".join(str(i + 1) for i in tabla.index[invalidas][:10])
        raise ValueError(
            f"Datos no numéricos, incompletos o infinitos en filas/registros: {filas}. "
            "Corrija los datos o revise --cabecera y --decimal. No se han descartado esos pares."
        )
    return numeros[:, 0], numeros[:, 1], tabla.index.to_numpy() + 1, etiquetas


def ajustar_hill(x, y, inicios=30, semilla=12345, alfa_min=0.01,
                 alfa_max=100.0, c_min=None, c_max=None):
    """Estima A, B, C y alfa minimizando suma((y - H(x))**2).

    Parámetros
    ----------
    x, y : arreglos unidimensionales de igual longitud
        Pares observados. Se da el mismo peso a cada par.
    inicios : entero positivo
        Número de puntos iniciales para buscar distintas soluciones.
    semilla : entero no negativo
        Semilla para que la selección de puntos iniciales sea reproducible.
    alfa_min, alfa_max : números positivos
        Límites inferior y superior del exponente.
    c_min, c_max : números positivos o None
        Límites de C. None calcula los límites a partir del rango de x.

    Devuelve
    --------
    Diccionario con los cuatro coeficientes, n, R², RMSE, SSE, los límites
    empleados, el número de inicios convergentes y los avisos del diagnóstico.

    Método
    ------
    Para C y alfa fijos, el modelo es lineal en A y B. Esos dos parámetros
    se calculan exactamente por mínimos cuadrados lineales en cada paso.
    La búsqueda no lineal se realiza sobre log(C) y log(alfa), para mantener
    ambos positivos. Normalizar y internamente mejora la estabilidad y no
    cambia el objetivo del ajuste, pues se aplica un único factor común.
    Se conserva la solución convergente con menor suma de cuadrados.
    """
    x, y = np.asarray(x, float), np.asarray(y, float)
    if x.ndim != 1 or y.ndim != 1 or x.size != y.size:
        raise ValueError("x e y deben ser vectores de igual longitud.")
    if x.size < 5 or np.unique(x).size < 4:
        raise ValueError("Se requieren al menos 5 pares y 4 valores distintos de x.")
    if not np.isfinite(x).all() or not np.isfinite(y).all() or np.any(x < 0):
        raise ValueError("Se necesitan pares finitos y x >= 0. No se desplaza ni transforma x.")
    if inicios < 1 or not (0 < alfa_min < alfa_max < np.inf):
        raise ValueError("Use inicios >= 1 y 0 < alfa_min < alfa_max finitos.")
    positivos = x[x > 0]
    c_min = float(positivos.min() / 1000) if c_min is None else float(c_min)
    c_max = float(x.max() * 1000) if c_max is None else float(c_max)
    if not (0 < c_min < c_max < np.inf):
        raise ValueError("Los límites de C deben ser finitos y satisfacer 0 < c_min < c_max.")
    centro, escala = float(np.mean(y)), float(np.std(y))
    if not np.isfinite(escala) or escala <= np.finfo(float).eps * max(float(np.max(abs(y))), np.finfo(float).tiny):
        raise ValueError("y es constante o no tiene variación numérica suficiente para identificar cuatro parámetros.")
    yn = (y - centro) / escala
    logx = np.full(x.shape, -np.inf)
    np.log(x, out=logx, where=x > 0)
    inferior = np.log([c_min, alfa_min])
    superior = np.log([c_max, alfa_max])

    def proyectar(z):
        """Para z = (log(C), log(alfa)), resuelve A y B en escala normalizada."""
        g = expit(-np.exp(z[1]) * (logx - z[0]))
        matriz = np.column_stack((np.ones(x.size), g))
        ab, _, _, _ = np.linalg.lstsq(matriz, yn, rcond=None)
        return matriz @ ab - yn, ab, g

    # Parrilla en C y alfa más puntos aleatorios, todos reproducibles.
    rng = np.random.default_rng(semilla)
    centros = np.quantile(np.log(positivos), np.linspace(0, 1, 6))
    exponentes = np.log(np.array([0.3, 1, 3, 10, 30]))
    candidatos = [np.clip(np.array(z), inferior + 1e-8, superior - 1e-8)
                  for z in itertools.product(centros, exponentes)]
    # Mezclar para que un número reducido de inicios explore diferentes C.
    rng.shuffle(candidatos)
    while len(candidatos) < inicios:
        candidatos.append(rng.uniform(inferior, superior))
    soluciones = []
    for z0 in candidatos[:inicios]:
        ajuste = least_squares(lambda z: proyectar(z)[0], z0,
                               bounds=(inferior, superior), max_nfev=4000,
                               ftol=1e-11, xtol=1e-11, gtol=1e-11)
        if ajuste.success and np.isfinite(ajuste.fun).all():
            soluciones.append(ajuste)
    if not soluciones:
        raise ValueError("Ningún ajuste convergió. Revise los datos y los límites de C y alfa.")
    mejor = min(soluciones, key=lambda s: float(s.fun @ s.fun))
    _, ab, g = proyectar(mejor.x)
    A, B = float(centro + escala * ab[0]), float(escala * ab[1])
    C, alfa = (float(v) for v in np.exp(mejor.x))
    prediccion = hill(x, A, B, C, alfa)
    residuos = y - prediccion
    sse = float(residuos @ residuos)
    sst = float((y - centro) @ (y - centro))
    avisos = []
    if np.any((mejor.x - inferior < 1e-4) | (superior - mejor.x < 1e-4)):
        avisos.append("C o alfa está junto a un límite de búsqueda; amplíe los límites y compare el resultado.")
    # Diagnóstico local del modelo completo en parámetros normalizados.
    w = g * (1 - g)
    derivada_alfa = np.zeros(x.size)
    mascara = x > 0
    derivada_alfa[mascara] = -ab[1] * alfa * (logx[mascara] - np.log(C)) * w[mascara]
    jac = np.column_stack((np.ones(x.size), g, ab[1] * alfa * w, derivada_alfa))
    singular = np.linalg.svd(jac, compute_uv=False)
    condicion = float(singular[0] / singular[-1]) if singular[-1] > 0 else np.inf
    if condicion > 1e8:
        avisos.append("Los datos identifican débilmente algunos parámetros: combinaciones diferentes pueden dar curvas similares.")
    return {
        "modelo": "H(x) = A + B / (1 + (x/C)^alfa)",
        "coeficientes": {"A": A, "B": B, "C": C, "alfa": alfa},
        "n": int(x.size), "R2": float(1 - sse / sst),
        "RMSE": float(np.sqrt(sse / x.size)), "SSE": sse,
        "criterio": "Minimizar la suma de (y - H(x))^2; igual peso por par; sin transformar x ni y",
        "inicios": int(inicios), "inicios_convergentes": len(soluciones),
        "semilla": int(semilla), "limites": {"C": [c_min, c_max], "alfa": [alfa_min, alfa_max]},
        "condicion_jacobiano_normalizado": condicion if np.isfinite(condicion) else None,
        "avisos": avisos,
    }


def guardar_resultados(carpeta, archivo, x, y, filas, etiquetas, resultado, mostrar=False):
    """Guarda coeficientes JSON, predicciones CSV y gráfico PNG.

    carpeta indica el destino; archivo identifica la fuente de los datos.
    x, y, filas y etiquetas proceden de cargar_datos, y resultado procede
    de ajustar_hill. Si mostrar es True, también se abre el gráfico.
    Devuelve la ruta de la carpeta creada. Si ya existe, añade un sufijo.
    Los residuos guardados siguen la convención: observado menos ajustado.
    """
    import matplotlib
    if not mostrar:
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    carpeta = Path(carpeta).expanduser().resolve()
    destino, indice = carpeta, 2
    while destino.exists():
        destino = carpeta.with_name(f"{carpeta.name}_{indice}")
        indice += 1
    destino.mkdir(parents=True)
    p = resultado["coeficientes"]
    prediccion = hill(x, **p)
    reporte = dict(resultado, archivo_origen=str(Path(archivo).resolve()),
                   columnas={"x": etiquetas[0], "y": etiquetas[1]})
    (destino / "coeficientes.json").write_text(
        json.dumps(reporte, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")
    pd.DataFrame({"fila_origen": filas, "x": x, "y": y,
                  "y_ajustada": prediccion, "residuo": y - prediccion}).to_csv(
                      destino / "predicciones.csv", index=False, encoding="utf-8-sig")
    xx = np.unique(np.concatenate((np.linspace(x.min(), x.max(), 800), x)))
    fig, (ax, ar) = plt.subplots(2, 1, figsize=(9, 7), sharex=True,
                                 gridspec_kw={"height_ratios": [3, 1]}, layout="constrained")
    ax.scatter(x, y, s=25, color="#165d9c", label="Datos", zorder=3)
    ax.plot(xx, hill(xx, **p), color="#d65a24", lw=2, label="Ajuste Hill")
    ax.set_title(f"Ajuste de Hill | R² = {resultado['R2']:.6f} | RMSE = {resultado['RMSE']:.6g}")
    ax.set_ylabel(etiquetas[1])
    ax.legend(frameon=False)
    ar.scatter(x, y - prediccion, s=20, color="#165d9c", zorder=3)
    ar.axhline(0, color="gray", lw=1)
    ar.set(xlabel=etiquetas[0], ylabel="Residuo")
    for eje in (ax, ar):
        eje.grid(alpha=0.25)
        eje.spines[["top", "right"]].set_visible(False)
    fig.savefig(destino / "ajuste_hill.png", dpi=180)
    if mostrar:
        plt.show()
    plt.close(fig)
    return destino


def seleccionar_archivo():
    """Solicita el archivo mediante una ventana o, si no está disponible, la consola."""
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        try:
            ruta = filedialog.askopenfilename(title="Seleccione los datos para el ajuste de Hill",
                                              filetypes=[("Datos", "*.xlsx *.xlsm *.xls *.csv *.cvs"),
                                                         ("Todos los archivos", "*.*")])
        finally:
            root.destroy()
        if not ruta:
            raise ValueError("Selección cancelada.")
        return ruta
    except (ImportError, RuntimeError):
        return input("Ruta del archivo Excel o CSV: ").strip().strip('"')
    except Exception as exc:
        if exc.__class__.__name__ == "TclError":
            return input("Ruta del archivo Excel o CSV: ").strip().strip('"')
        raise


def main():
    """Ejecuta lectura, ajuste y guardado; devuelve 0 si termina correctamente.

    Consulte `python ajuste_hill.py --help` para ver las opciones.
    Un error de entrada o de acceso a archivos devuelve el código 1.
    """
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("archivo", nargs="?", help="Ruta del Excel o CSV; con espacios, use comillas.")
    parser.add_argument("--hoja", default="0", help="Nombre o índice de la hoja Excel; por defecto, 0 (primera).")
    parser.add_argument("--cabecera", choices=["auto", "si", "no"], default="auto")
    parser.add_argument("--separador", default=None, help="Separador CSV; por defecto se detecta. Ejemplo: ';'.")
    parser.add_argument("--decimal", choices=[".", ","], default=".")
    parser.add_argument("--codificacion", default="utf-8-sig", help="Para CSV; ejemplo alternativo: cp1252.")
    parser.add_argument("--inicios", type=int, default=30)
    parser.add_argument("--semilla", type=int, default=12345)
    parser.add_argument("--alfa-min", type=float, default=0.01)
    parser.add_argument("--alfa-max", type=float, default=100)
    parser.add_argument("--c-min", type=float, default=None)
    parser.add_argument("--c-max", type=float, default=None)
    parser.add_argument("--salida", help="Carpeta de resultados; si existe, se crea una carpeta con sufijo.")
    parser.add_argument("--mostrar", action="store_true", help="Mostrar el gráfico además de guardarlo.")
    args = parser.parse_args()
    try:
        archivo = Path(args.archivo or seleccionar_archivo()).expanduser().resolve()
        hoja = int(args.hoja) if args.hoja.isdigit() else args.hoja
        x, y, filas, etiquetas = cargar_datos(archivo, hoja, args.cabecera,
                                             args.separador, args.decimal, args.codificacion)
        resultado = ajustar_hill(x, y, args.inicios, args.semilla, args.alfa_min,
                                 args.alfa_max, args.c_min, args.c_max)
        destino = guardar_resultados(args.salida or archivo.with_name(archivo.stem + "_ajuste_hill"),
                                     archivo, x, y, filas, etiquetas, resultado, args.mostrar)
    except (ValueError, OSError, ImportError, pd.errors.ParserError, EOFError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print("\nH(x) = A + B / (1 + (x/C)^alfa)")
    for nombre, valor in resultado["coeficientes"].items():
        print(f"{nombre:5s} = {valor:.12g}")
    print(f"n = {resultado['n']}\nR² = {resultado['R2']:.8f}\nRMSE = {resultado['RMSE']:.8g}")
    for aviso in resultado["avisos"]:
        print(f"Aviso: {aviso}")
    print(f"Resultados guardados en: {destino}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

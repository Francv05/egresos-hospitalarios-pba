"""
data_loader.py
==============
Funciones compartidas para cargar y limpiar los CSV de egresos
hospitalarios. Lo usan tanto los notebooks como la app Streamlit.

Tener UN solo punto de carga de datos es buena práctica:
- Si mañana cambian los nombres de columnas, los actualizás acá
  y todo el proyecto sigue andando.
- Garantiza que notebooks y dashboard usen exactamente los mismos
  datos limpios.
"""

from pathlib import Path
from typing import List
import pandas as pd
import unicodedata


# Mapeo flexible: el dataset real puede usar nombres distintos
# (ej. "Año" vs "anio" vs "AÑO"). Normalizamos todo a un esquema canónico.
COLUMNAS_CANONICAS = {
    "anio": ["anio", "año", "ano", "year"],
    "region_sanitaria": ["region_sanitaria", "region sanitaria", "region", "regional", "region_de_salud"],
    "municipio": ["municipio", "municipio_nombre", "muncipio_nombre", "partido", "departamento"],
    "causa": ["causa", "causa_egreso", "causa_egreso_capitulo", "diagnostico", "diagnóstico", "motivo_egreso", "grupo_de_causas"],
    "tipo_egreso": ["tipo_egreso", "tipo", "condicion_egreso", "condicion_al_egreso"],
    "cantidad_egresos": ["cantidad_egresos", "cantidad", "egresos", "n_egresos", "count"],
    "dias_estadia_promedio": ["dias_estadia_promedio", "dias_estadia", "dias", "estadia_promedio"],
    "sexo": ["sexo", "genero"],
    "grupo_edad": ["grupo_edad", "rango_edad", "edad_grupo", "grupo_etario"],
}


def _normalizar(texto: str) -> str:
    """Pasa a minúsculas, quita acentos y reemplaza espacios por guiones bajos."""
    if not isinstance(texto, str):
        return texto
    texto = texto.strip().lower()
    # Quitar acentos
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    # Espacios -> _
    texto = texto.replace(" ", "_").replace("-", "_")
    return texto


def _renombrar_columnas(df: pd.DataFrame) -> pd.DataFrame:
    """Renombra las columnas al esquema canónico."""
    df.columns = [_normalizar(c) for c in df.columns]

    rename_map = {}
    for canonico, alias in COLUMNAS_CANONICAS.items():
        for a in alias:
            a_norm = _normalizar(a)
            if a_norm in df.columns and a_norm != canonico:
                rename_map[a_norm] = canonico

    return df.rename(columns=rename_map)


def cargar_dataset(raw_dir: Path = None, años: List[int] = None) -> pd.DataFrame:
    """
    Carga TODOS los CSV de egresos disponibles y los concatena en un solo DataFrame.

    Args:
        raw_dir: carpeta con los .csv (por defecto: data/raw del repo)
        años:    lista de años a cargar (por defecto: todos los que encuentre)

    Returns:
        DataFrame único con todos los años apilados.
    """
    if raw_dir is None:
        raw_dir = Path(__file__).resolve().parent.parent / "data" / "raw"
    raw_dir = Path(raw_dir)

    archivos = sorted(raw_dir.glob("egresos-*.csv"))
    if not archivos:
        raise FileNotFoundError(
            f"No se encontraron CSV en {raw_dir}.\n"
            f"Corré primero:  python download_data.py\n"
            f"O como fallback: python generate_synthetic_data.py"
        )

    dfs = []
    for archivo in archivos:
        # Extraer el año del nombre: egresos-2018.csv -> 2018
        try:
            año = int(archivo.stem.split("-")[-1])
        except ValueError:
            año = None

        if años is not None and año not in años:
            continue

        # Probar varias codificaciones — los CSV del gobierno a veces vienen en latin-1
        for enc in ["utf-8", "latin-1", "cp1252"]:
            try:
                df = pd.read_csv(archivo, encoding=enc, sep=None, engine="python")
                break
            except UnicodeDecodeError:
                continue
        else:
            raise RuntimeError(f"No se pudo decodificar {archivo}")

        df = _renombrar_columnas(df)

        # Asegurar que 'anio' exista
        if "anio" not in df.columns and año is not None:
            df["anio"] = año

        dfs.append(df)

    df_total = pd.concat(dfs, ignore_index=True)

    # Limpieza básica
    if "cantidad_egresos" in df_total.columns:
        df_total["cantidad_egresos"] = pd.to_numeric(
            df_total["cantidad_egresos"], errors="coerce"
        ).fillna(0).astype(int)

    if "dias_estadia_promedio" in df_total.columns:
        df_total["dias_estadia_promedio"] = pd.to_numeric(
            df_total["dias_estadia_promedio"], errors="coerce"
        )

    if "anio" in df_total.columns:
        df_total["anio"] = pd.to_numeric(df_total["anio"], errors="coerce").astype("Int64")

    return df_total


if __name__ == "__main__":
    # Smoke test: si corrés `python data_loader.py` te dice qué cargó
    df = cargar_dataset()
    print(f"Cargado: {len(df):,} filas, {len(df.columns)} columnas")
    print(f"Columnas: {list(df.columns)}")
    print(f"Años: {sorted(df['anio'].dropna().unique().tolist())}")
    print("\nPrimeras filas:")
    print(df.head())

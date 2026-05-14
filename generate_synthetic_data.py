"""
generate_synthetic_data.py
==========================
Genera un dataset sintético de egresos hospitalarios con la misma estructura
que el dataset oficial de la Provincia de Buenos Aires.

Lo usamos como fallback cuando no podemos descargar los datos reales.
Los valores son inventados pero las distribuciones son realistas (basadas
en estadísticas públicas del Ministerio de Salud).

Uso:
    python generate_synthetic_data.py
"""

import numpy as np
import pandas as pd
from pathlib import Path

RAW_DIR = Path(__file__).parent / "data" / "raw"
np.random.seed(42)  # Para que sea reproducible

# --- Catálogos realistas ---
REGIONES = [f"Región Sanitaria {n}" for n in ["I", "II", "III", "IV", "V",
                                                "VI", "VII", "VIII", "IX",
                                                "X", "XI", "XII"]]

MUNICIPIOS = [
    "La Plata", "Mar del Plata", "Bahía Blanca", "Tandil", "Olavarría",
    "Junín", "Pergamino", "San Nicolás", "Zárate", "Campana",
    "Tigre", "Pilar", "Escobar", "Moreno", "Merlo",
    "La Matanza", "Lomas de Zamora", "Quilmes", "Florencio Varela", "Berazategui",
    "Avellaneda", "Lanús", "Almirante Brown", "Esteban Echeverría", "Ezeiza",
    "Tres de Febrero", "San Martín", "San Isidro", "Vicente López", "Morón",
]

# Causas con pesos realistas (las más frecuentes pesan más)
CAUSAS_PESO = {
    "Embarazo, parto y puerperio": 0.18,
    "Enfermedades del sistema digestivo": 0.10,
    "Traumatismos y envenenamientos": 0.10,
    "Enfermedades del sistema circulatorio": 0.09,
    "Enfermedades del sistema respiratorio": 0.08,
    "Tumores (neoplasias)": 0.07,
    "Enfermedades del sistema genitourinario": 0.06,
    "Enfermedades infecciosas y parasitarias": 0.06,
    "Ciertas afecciones originadas en el período perinatal": 0.05,
    "Enfermedades del sistema osteomuscular": 0.05,
    "Enfermedades endócrinas, nutricionales y metabólicas": 0.04,
    "Enfermedades del sistema nervioso": 0.03,
    "Trastornos mentales y del comportamiento": 0.03,
    "Enfermedades de la piel": 0.02,
    "Malformaciones congénitas": 0.02,
    "Otras causas": 0.02,
}

TIPOS_EGRESO = {
    "Alta médica": 0.85,
    "Traslado a otro establecimiento": 0.07,
    "Retiro voluntario": 0.04,
    "Defunción": 0.04,
}


def generar_año(año: int, n_filas: int) -> pd.DataFrame:
    """Genera n_filas de datos sintéticos para un año dado."""
    causas = list(CAUSAS_PESO.keys())
    pesos_causas = list(CAUSAS_PESO.values())

    tipos = list(TIPOS_EGRESO.keys())
    pesos_tipos = list(TIPOS_EGRESO.values())

    # En 2020 sube la mortalidad por COVID -> ajustamos los pesos
    if año == 2020:
        pesos_tipos = [0.78, 0.08, 0.04, 0.10]

    df = pd.DataFrame({
        "anio": año,
        "region_sanitaria": np.random.choice(REGIONES, n_filas),
        "municipio": np.random.choice(MUNICIPIOS, n_filas),
        "causa": np.random.choice(causas, n_filas, p=pesos_causas),
        "tipo_egreso": np.random.choice(tipos, n_filas, p=pesos_tipos),
        "cantidad_egresos": np.random.poisson(lam=15, size=n_filas) + 1,
        "dias_estadia_promedio": np.round(np.random.gamma(shape=2.5, scale=2.0, size=n_filas), 1),
        "sexo": np.random.choice(["Femenino", "Masculino"], n_filas, p=[0.55, 0.45]),
        "grupo_edad": np.random.choice(
            ["0-14", "15-29", "30-44", "45-59", "60-74", "75+"],
            n_filas,
            p=[0.15, 0.20, 0.18, 0.17, 0.18, 0.12]
        ),
    })

    return df


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    # Generamos volúmenes realistas (más egresos en años sin pandemia)
    volumenes = {2016: 2800, 2017: 2900, 2018: 3000, 2019: 3050, 2020: 2400}

    print("Generando datos sintéticos (fallback)...")
    for año, n in volumenes.items():
        df = generar_año(año, n)
        destino = RAW_DIR / f"egresos-{año}.csv"
        df.to_csv(destino, index=False, encoding="utf-8")
        print(f"   {destino.name}: {len(df):,} filas")

    print(f"\nListo. Archivos en {RAW_DIR}")
    print("AVISO: Estos son datos sintéticos, NO reales.")
    print("Aclaralo en el README si usás esta versión.")


if __name__ == "__main__":
    main()

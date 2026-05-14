"""
download_data.py
================
Descarga el dataset de Egresos Hospitalarios de la Provincia de Buenos Aires
para los años 2016-2020 desde el portal de datos abiertos.

Fuente: Ministerio de Salud de la Provincia de Buenos Aires
URL del catálogo: https://catalogo.datos.gba.gob.ar/dataset/egresos-hospitalarios
Licencia: Creative Commons Attribution 4.0

Uso:
    python download_data.py
"""

import os
import sys
from pathlib import Path
import requests

# URLs de los CSV oficiales (provincia de Buenos Aires)
URLS = {
    2016: "https://catalogo.datos.gba.gob.ar/dataset/baf07a7a-8cd2-47ad-bae0-52c6f3b45bb7/resource/66e005f4-d88b-4abf-9797-5809def5131e/download/egresos-2016.csv",
    2017: "https://catalogo.datos.gba.gob.ar/dataset/baf07a7a-8cd2-47ad-bae0-52c6f3b45bb7/resource/3f9fd7e0-5d92-4b8c-a87b-951607637e89/download/egresos-2017.csv",
    2018: "https://catalogo.datos.gba.gob.ar/dataset/baf07a7a-8cd2-47ad-bae0-52c6f3b45bb7/resource/ddf7a32f-bc60-45b0-ad91-d3acd6813cd0/download/egresos-2018.csv",
    2019: "https://catalogo.datos.gba.gob.ar/dataset/baf07a7a-8cd2-47ad-bae0-52c6f3b45bb7/resource/6a839c98-9cbb-475a-840f-4b0e29c378e0/download/egresos-2019.csv",
    2020: "https://catalogo.datos.gba.gob.ar/dataset/baf07a7a-8cd2-47ad-bae0-52c6f3b45bb7/resource/06d4b138-11cb-4b72-a87b-bff09f6af07d/download/egresos-2020.csv",
}

# Carpeta destino (relativa a este script)
RAW_DIR = Path(__file__).parent / "data" / "raw"


def descargar_archivo(url: str, destino: Path) -> bool:
    """
    Descarga un archivo desde una URL y lo guarda en 'destino'.
    Devuelve True si tuvo éxito, False si falló.
    """
    try:
        print(f"   Descargando {destino.name}...")
        # stream=True permite descargar archivos grandes sin cargar todo en memoria
        response = requests.get(url, stream=True, timeout=60, verify=False)
        response.raise_for_status()

        with open(destino, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        tamaño_kb = destino.stat().st_size / 1024
        print(f"   OK -> {destino.name} ({tamaño_kb:,.1f} KB)")
        return True

    except Exception as e:
        print(f"   ERROR descargando {destino.name}: {e}")
        return False


def main():
    print("=" * 60)
    print("Descarga de Egresos Hospitalarios - PBA 2016-2020")
    print("=" * 60)

    # Crear carpeta destino si no existe
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    exitos = 0
    for año, url in URLS.items():
        destino = RAW_DIR / f"egresos-{año}.csv"

        if destino.exists():
            print(f"[{año}] Ya existe en {destino.name} (skip)")
            exitos += 1
            continue

        print(f"[{año}]")
        if descargar_archivo(url, destino):
            exitos += 1

    print("=" * 60)
    print(f"Descargados {exitos}/{len(URLS)} archivos en {RAW_DIR}")
    print("=" * 60)

    if exitos == 0:
        print("\nNo se pudo descargar ningún archivo.")
        print("Como fallback, podés correr 'python generate_synthetic_data.py'")
        print("para generar datos sintéticos similares.")
        sys.exit(1)


if __name__ == "__main__":
    # Desactivar warnings de SSL (datos.gba.gob.ar a veces tiene cert vencido)
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    main()

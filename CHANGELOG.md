# CHANGELOG

## [2026-05-14] — Sesion 01

### Archivos creados
- `.claude/settings.json` — permisos de proyecto para evitar confirmaciones repetidas en comandos Python, Jupyter, pip y git
- `CHANGELOG.md` — este archivo de registro de cambios

### Archivos modificados
- `app/data_loader.py` — se agregaron alias de columnas al diccionario `COLUMNAS_CANONICAS`:
  - `municipio_nombre` y `muncipio_nombre` (typo en años 2016/2019) como alias de `municipio`
  - `causa_egreso_capitulo` como alias de `causa`
  Razon: los CSV reales usan nombres distintos a los que el loader asumia originalmente.

- `notebooks/01_exploracion.ipynb` — se corrigieron 2 celdas que usaban la columna `dias_estadia_promedio`, ausente en el dataset real:
  - Celda 8 (codigo): query de egresos por año simplificada (se elimino AVG de dias_estadia)
  - Celda 9 (codigo): reemplazada por mensaje informativo (la columna no existe)

- `notebooks/02_analisis.ipynb` — se corrigieron 5 celdas con problemas de compatibilidad con el dataset real:
  - Celda 1: se agrego `WHERE causa IS NOT NULL AND anio IN (2019, 2020)` en query de comparacion 2019 vs 2020
  - Celda 3: se agrego `WHERE municipio IS NOT NULL` en query de concentracion por municipio
  - Celda 5: se reemplazo heatmap de dias_estadia por heatmap de egresos por causa/año (columna `dias_estadia_promedio` inexistente)
  - Celda 6: se agrego `WHERE grupo_edad IS NOT NULL AND sexo IS NOT NULL` en query demografica
  - Celdas 7 y 8: se reemplazaron analisis de carga asistencial (que requerian dias_estadia) por barplot de top causas por volumen

### Decisiones tecnicas
- **Virtualenv en ruta corta (`C:\venv\salud`)**: el path del usuario es demasiado largo para que pip instale paquetes con paths internos extensos (ej. jupyterlab). Se creo el venv en `C:\venv\salud` para evitar el error de Windows Long Paths.
- **Git instalado via winget**: git no estaba en el sistema; se instalo con `winget install Git.Git`.
- **Columna `dias_estadia_promedio` ausente**: el dataset real de la Provincia de Buenos Aires no incluye esta columna (si existe en el dataset sintetico que se usaba durante el desarrollo). Se adapto en lugar de agregar datos ficticios.
- **NaN como etiquetas categoricas**: matplotlib 3.x no acepta NaN como label en graficos categoricos. Se agrego `WHERE ... IS NOT NULL` en todas las queries SQL que alimentan graficos.

### Comandos ejecutados
- `python -m pip install -r requirements.txt` — fallo por Windows Long Paths
- `python -m venv C:\venv\salud` — OK
- `C:\venv\salud\Scripts\pip install -r requirements.txt` — OK (790 paquetes)
- `python download_data.py` — OK (5 archivos, ~20 MB cada uno, datos reales PBA 2016-2020)
- `python app/data_loader.py` — OK (790,990 filas, 11 columnas)
- `jupyter nbconvert --execute notebooks/01_exploracion.ipynb` — OK (tras correcciones)
- `jupyter nbconvert --execute notebooks/02_analisis.ipynb` — OK (tras correcciones)
- `streamlit run app/app.py` — OK (sin errores, levanta en localhost:8501)
- `winget install Git.Git` — OK
- `git init && git add . && git commit` — pendiente (ver Paso 7)

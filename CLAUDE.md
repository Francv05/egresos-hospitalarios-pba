# Instrucciones para Claude Code

> Este archivo se lee automÃ¡ticamente al iniciar Claude Code en este proyecto.

## Contexto

Soy Franco, estoy armando un proyecto de portfolio de Data Analyst.
El proyecto analiza egresos hospitalarios de la Provincia de Buenos Aires (2016-2020)
usando Python + SQL (DuckDB) + Streamlit.

El proyecto **YA estÃ¡ armado** (notebooks, app, README, todo). Solo falta:
1. Que tenga las dependencias instaladas
2. Que se descarguen los CSV reales
3. Que se ejecuten los notebooks
4. Subirlo a GitHub
5. Deployar en Streamlit Cloud

## Tarea autoejecutable

Si te digo "ejecutÃ¡ todo" o "hacelo", quiero que corras en orden, sin pedirme confirmaciÃ³n entre pasos:

### Paso 1 â Instalar dependencias

```powershell
python -m pip install -r requirements.txt
```

Si `python` no existe, probÃ¡ `py` o `python3`. Si tampoco, sugerime instalar Python desde python.org/downloads.

### Paso 2 â Descargar datos reales

```powershell
python download_data.py
```

VerificÃ¡ que en `data/raw/` haya 5 archivos `egresos-YYYY.csv` mayores a 100 KB cada uno (los sintÃ©ticos son ~300 KB pero los reales pueden ser distintos). Si fallan todas las descargas, decÃ­melo y vemos.

### Paso 3 â Verificar carga

```powershell
python app/data_loader.py
```

DeberÃ­a imprimir "Cargado: X filas, N columnas" y la lista de columnas reales del dataset.

**IMPORTANTE â adaptaciÃ³n de columnas:**
Los nombres de columnas del CSV real pueden NO coincidir con los del esquema canÃ³nico que asumiÃ³ `data_loader.py` (anio, region_sanitaria, municipio, causa, tipo_egreso, cantidad_egresos, dias_estadia_promedio, sexo, grupo_edad).

Si ves columnas distintas, editÃ¡ `app/data_loader.py` y agregÃ¡ los alias reales en el diccionario `COLUMNAS_CANONICAS`. Por ejemplo, si el CSV trae "AÃ±o" y "Region Sanitaria" en lugar de "anio" y "region_sanitaria", ya estÃ¡n como alias â deberÃ­a funcionar. Si no, ajustÃ¡.

Si una columna esperada NO existe en el CSV real (ej. no hay `sexo` o `grupo_edad`), estÃ¡ OK â los notebooks ya tienen checks `if columna in df.columns`. La secciÃ³n demogrÃ¡fica del notebook 2 se salta sola si faltan esas columnas.

### Paso 4 â Ejecutar notebooks

```powershell
jupyter nbconvert --to notebook --execute notebooks/01_exploracion.ipynb --output 01_exploracion.ipynb
jupyter nbconvert --to notebook --execute notebooks/02_analisis.ipynb --output 02_analisis.ipynb
```

Esto regenera todos los grÃ¡ficos en `assets/` y el parquet limpio en `data/processed/`.

Si alguna celda falla, leÃ© el error, ajustÃ¡ (probablemente algÃºn nombre de columna), y reintentÃ¡.

### Paso 5 â Verificar la app

```powershell
streamlit run app/app.py
```

Dejala corriendo 5 segundos para confirmar que no tira error y despuÃ©s cortala con Ctrl+C.

### Paso 6 â Subir a GitHub

Asegurate de que `.gitignore` estÃ¡ respetando el lÃ­mite de tamaÃ±o (los CSV crudos NO se suben):

```powershell
git init
git add .
git status
```

VerificÃ¡ que NO hay CSV en el staging area. Si los hay, revisÃ¡ `.gitignore`.

DespuÃ©s:

```powershell
git commit -m "feat: anÃ¡lisis de egresos hospitalarios PBA 2016-2020"
```

Y para el remoto, decime cuÃ¡l es mi user de GitHub y creo el repo desde gh CLI si estÃ¡ instalado; si no, te digo los pasos manuales para crearlo en github.com.

### Paso 7 â Deploy en Streamlit Cloud

Una vez subido a GitHub, decime que vaya a https://share.streamlit.io y te asisto desde acÃ¡ para configurar el deploy.

## Si encontrÃ¡s errores

- **Encoding raro**: `data_loader.py` ya prueba utf-8, latin-1, cp1252. Si igual falla, agregÃ¡ la codificaciÃ³n que necesite.
- **Falta una columna**: agregala como alias en `COLUMNAS_CANONICAS`.
- **DataFrame vacÃ­o despuÃ©s de filtrar**: probablemente algÃºn filtro del notebook asume valores que no existen. AdaptÃ¡.
- **Streamlit no encuentra los datos**: regenerÃ¡ el parquet corriendo el notebook 1 entero.

## Stack y convenciones

- Python 3.10+
- Comentarios y prints en **espaÃ±ol**
- Nombres de columnas en `snake_case` sin acentos
- Visualizaciones: matplotlib/seaborn para notebooks, plotly para la app
- SQL via DuckDB sobre DataFrames

## CÃ³mo me gusta trabajar

- HacÃ© el laburo, no me preguntes cada cosa
- Si tomÃ¡s una decisiÃ³n tÃ©cnica, explicÃ¡mela brevemente al final
- Si algo no se puede automatizar, decÃ­melo claramente
- No uses emojis en cÃ³digo ni en archivos a menos que te lo pida

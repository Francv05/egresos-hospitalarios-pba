# Cómo correr el proyecto en tu compu — Franco

Acá tenés los pasos exactos. Si algo falla, copiame el error.

## Paso 1: Abrir terminal en la carpeta del proyecto

Abrí PowerShell (o CMD) y andá a la carpeta:

```powershell
cd C:\Users\Franco\Documents\Claude\proyecto_salud
```

## Paso 2: Crear entorno virtual (recomendado)

Esto aísla las dependencias para que no te rompan otras cosas en tu compu:

```powershell
python -m venv venv
venv\Scripts\activate
```

Vas a ver `(venv)` al inicio del prompt — eso quiere decir que está activo.

## Paso 3: Instalar dependencias

```powershell
pip install -r requirements.txt
```

Esto tarda 1-2 minutos. Si falla algún paquete (raro), copiame el error.

## Paso 4: Bajar los datos reales

```powershell
python download_data.py
```

**Si funciona:** vas a ver mensajes "OK -> egresos-2016.csv (XYZ KB)" etc.

**Si falla** (URL del gobierno caída, cert SSL, etc.): usá el fallback con datos sintéticos:

```powershell
python generate_synthetic_data.py
```

## Paso 5: Verificar que la carga funciona

```powershell
python app\data_loader.py
```

Debería imprimir algo como:
```
Cargado: 14,150 filas, 9 columnas
Columnas: ['anio', 'region_sanitaria', 'municipio', 'causa', ...]
Años: [2016, 2017, 2018, 2019, 2020]
```

Si te da error, copiame el mensaje.

## Paso 6: Correr el notebook 1 (exploración)

```powershell
jupyter notebook notebooks\01_exploracion.ipynb
```

Se te abre el navegador. Apretá `Cell > Run All` para correr todas las celdas.

Si todas las celdas corren sin errores, vas a tener:
- Tablas con top causas, regiones, etc.
- 4 imágenes guardadas en `assets/`
- Un parquet limpio en `data/processed/egresos_2016_2020.parquet`

## Paso 7: Correr el notebook 2 (análisis profundo)

Mismo procedimiento. Cuando termine, mirá los gráficos — son los más "vendedores":
- Heatmap de días de estadía
- Pareto de municipios
- Scatter de carga asistencial

## Paso 8: Correr la app Streamlit

```powershell
streamlit run app\app.py
```

Se abre solo en `http://localhost:8501`. Probá los filtros del sidebar.

## Paso 9: Subir a GitHub

```powershell
cd C:\Users\Franco\Documents\Claude\proyecto_salud
git init
git add .
git commit -m "Análisis de egresos hospitalarios PBA 2016-2020"
```

Después en GitHub creás un repo nuevo (sin README, sin .gitignore) y:

```powershell
git remote add origin https://github.com/<TU_USUARIO>/<NOMBRE_REPO>.git
git branch -M main
git push -u origin main
```

## Paso 10: Deployar a Streamlit Cloud (gratis)

1. Andá a https://share.streamlit.io
2. Login con GitHub
3. "New app" → seleccioná el repo
4. **Main file path:** `app/app.py`
5. Deploy

En 2 minutos tenés un link público que podés pegar en LinkedIn.

---

## ¿Algo no funciona?

Pegame el error y lo arreglamos. Los problemas más comunes:

- **`No module named 'pandas'`** → no activaste el venv. Hacé `venv\Scripts\activate` y reintentá.
- **`SSL: CERTIFICATE_VERIFY_FAILED`** → el script ya desactiva esto, pero si igual falla usá el fallback sintético.
- **`No se encontraron CSV`** → el `download_data.py` no descargó nada. Probá `generate_synthetic_data.py`.
- **Encoding raro en columnas** → el `data_loader.py` ya prueba utf-8, latin-1 y cp1252. Si igual falla, copiame el error.

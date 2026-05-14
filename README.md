# Análisis de Egresos Hospitalarios — Provincia de Buenos Aires (2016-2020)

Proyecto de análisis de datos sobre el sistema de salud pública bonaerense. Combina **Python (pandas)**, **SQL (DuckDB)** y un **dashboard interactivo en Streamlit** para responder preguntas concretas de gestión sanitaria sobre 5 años de datos oficiales.

> **Autor:** Franco Vigna · **Stack:** Python · SQL (DuckDB) · pandas · matplotlib · seaborn · Plotly · Streamlit

---

## Demo en vivo

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

> Una vez deployada la app en Streamlit Cloud, pegá el link acá.

![Vista previa del dashboard](assets/preview.png)

---

## Preguntas que responde el análisis

1. **¿Cómo cambió la composición de causas entre 2016 y 2020?** Cuantifica el impacto de la pandemia en los egresos hospitalarios.
2. **¿Qué municipios concentran la carga asistencial?** Análisis tipo Pareto sobre 135 municipios.
3. **¿Qué patologías consumen más días-cama?** Métrica de carga asistencial = volumen × estadía promedio.
4. **¿Cómo varía la estadía promedio según causa y año?** Heatmap para detectar tendencias.
5. **¿Cómo se distribuyen los egresos por demografía?** Pirámide poblacional por grupo etario y sexo.

---

## Estructura del proyecto

```
proyecto_salud/
├── data/
│   ├── raw/                  # CSV originales del Ministerio de Salud PBA
│   └── processed/            # Dataset limpio en parquet (más rápido)
├── notebooks/
│   ├── 01_exploracion.ipynb  # EDA inicial + SQL en DuckDB
│   └── 02_analisis.ipynb     # Análisis profundo + insights
├── app/
│   ├── app.py                # Dashboard Streamlit
│   └── data_loader.py        # Carga y limpieza compartida
├── assets/                   # Imágenes generadas por los notebooks
├── download_data.py          # Descarga el dataset oficial
├── generate_synthetic_data.py# Fallback con datos sintéticos
├── requirements.txt
└── README.md
```

---

## Cómo correrlo localmente

### 1. Cloná el repo

```bash
git clone https://github.com/<TU_USUARIO>/proyecto-egresos-hospitalarios.git
cd proyecto-egresos-hospitalarios
```

### 2. Instalá las dependencias

```bash
python -m venv venv
source venv/bin/activate          # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Descargá el dataset

```bash
python download_data.py
```

Si el portal del gobierno está caído o cambió la URL, podés usar el fallback:

```bash
python generate_synthetic_data.py
```

> **Importante:** los datos sintéticos NO son reales, son para que el proyecto funcione siempre. Si los usás, aclaralo.

### 4. Corré los notebooks

```bash
jupyter notebook notebooks/
```

Empezá por `01_exploracion.ipynb` y seguí con `02_analisis.ipynb`.

### 5. Corré el dashboard

```bash
streamlit run app/app.py
```

Se abre en `http://localhost:8501`.

---

## Hallazgos principales

> _(Completá esta sección después de correr los notebooks con los números reales)_

- **Causa más frecuente:** _completar_
- **Caída de egresos 2019 → 2020:** _completar % por pandemia_
- **Concentración geográfica:** _ej. 20 municipios concentran el X% de los egresos_
- **Patología de mayor carga asistencial:** _completar_

---

## Decisiones técnicas (por qué este stack)

- **DuckDB en lugar de SQLite**: permite correr SQL directamente sobre DataFrames sin necesidad de cargar a una base. Sintaxis ANSI estándar, ideal para portfolio.
- **Parquet para datos procesados**: comprime 5-10× más que CSV y se lee más rápido. Buena práctica en pipelines reales.
- **`data_loader.py` compartido**: notebooks y app usan exactamente el mismo dato. Cero divergencia.
- **Normalización de columnas**: el script tolera cambios en nombres de columnas del dataset oficial (alias múltiples).
- **Fallback sintético**: si el dataset oficial no está disponible, el proyecto sigue corriendo. Robusto.

---

## Datos

- **Fuente:** [Datos Abiertos PBA - Egresos Hospitalarios](https://catalogo.datos.gba.gob.ar/dataset/egresos-hospitalarios)
- **Publicado por:** Ministerio de Salud de la Provincia de Buenos Aires - Dirección Provincial de Estadística y Salud Digital
- **Licencia:** [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Período:** 2016-2020 (5 archivos CSV anuales)

---

## Contacto

**Franco Vigna** - Analista de Datos
- LinkedIn: _completar_
- Email: francovigna05@gmail.com
- Portfolio: _completar_

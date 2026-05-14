"""
app.py — Dashboard interactivo de Egresos Hospitalarios PBA 2016-2020

Para correr localmente:
    streamlit run app/app.py

Para deployar (gratis):
    1. Subir el proyecto a GitHub
    2. Ir a https://share.streamlit.io
    3. Conectar el repo, apuntar a app/app.py
    4. Listo: link compartible para el LinkedIn
"""

import sys
from pathlib import Path

import duckdb
import pandas as pd
import plotly.express as px
import streamlit as st

# Asegurar que data_loader sea importable
sys.path.insert(0, str(Path(__file__).resolve().parent))
from data_loader import cargar_dataset

# -----------------------------------------------------------------------------
# Configuración de página
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Egresos Hospitalarios PBA 2016-2020",
    page_icon="🏥",
    layout="wide",
)


# -----------------------------------------------------------------------------
# Carga de datos (cacheada para no recargar en cada interacción)
# -----------------------------------------------------------------------------
@st.cache_data(show_spinner="Cargando dataset...")
def cargar():
    """Carga datos desde el parquet limpio o, si no existe, desde los CSV."""
    ROOT = Path(__file__).resolve().parent.parent
    parquet = ROOT / "data" / "processed" / "egresos_2016_2020.parquet"
    if parquet.exists():
        return pd.read_parquet(parquet)
    return cargar_dataset()


try:
    df = cargar()
except FileNotFoundError as e:
    st.error(
        "No se encontraron los datos. Corré primero:\n\n"
        "```\npython download_data.py\n```\n\n"
        "O como fallback:\n\n"
        "```\npython generate_synthetic_data.py\n```"
    )
    st.stop()


# -----------------------------------------------------------------------------
# Header
# -----------------------------------------------------------------------------
st.title("🏥 Egresos Hospitalarios — Provincia de Buenos Aires")
st.markdown(
    "**Período:** 2016-2020 · "
    "**Fuente:** [Datos Abiertos PBA - Ministerio de Salud]"
    "(https://catalogo.datos.gba.gob.ar/dataset/egresos-hospitalarios)"
)


# -----------------------------------------------------------------------------
# Sidebar - filtros
# -----------------------------------------------------------------------------
st.sidebar.header("Filtros")

años_disponibles = sorted(df["anio"].dropna().unique().tolist())
años_sel = st.sidebar.multiselect(
    "Año", años_disponibles, default=años_disponibles
)

regiones = sorted(df["region_sanitaria"].dropna().unique().tolist()) if "region_sanitaria" in df.columns else []
region_sel = st.sidebar.multiselect("Región sanitaria", regiones, default=regiones)

# Filtrar df
filtrado = df[df["anio"].isin(años_sel)]
if region_sel and "region_sanitaria" in df.columns:
    filtrado = filtrado[filtrado["region_sanitaria"].isin(region_sel)]


# -----------------------------------------------------------------------------
# KPIs principales
# -----------------------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

total_egresos = int(filtrado["cantidad_egresos"].sum()) if "cantidad_egresos" in filtrado else len(filtrado)
col1.metric("Total egresos", f"{total_egresos:,}")

n_causas = filtrado["causa"].nunique() if "causa" in filtrado.columns else 0
col2.metric("Causas distintas", f"{n_causas:,}")

n_municipios = filtrado["municipio"].nunique() if "municipio" in filtrado.columns else 0
col3.metric("Municipios", f"{n_municipios:,}")

if "dias_estadia_promedio" in filtrado.columns:
    estadia = filtrado["dias_estadia_promedio"].mean()
    col4.metric("Estadía promedio", f"{estadia:.1f} días")
else:
    col4.metric("Años", f"{len(años_sel)}")


st.divider()


# -----------------------------------------------------------------------------
# DuckDB para consultas
# -----------------------------------------------------------------------------
con = duckdb.connect()
con.register("egresos", filtrado)


# -----------------------------------------------------------------------------
# Tabs principales
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(
    ["📊 Resumen", "🗺️ Geografía", "🧬 Causas", "🔍 Datos crudos"]
)


# === Tab 1: Resumen ===
with tab1:
    st.subheader("Evolución temporal")

    q = """
    SELECT anio, SUM(cantidad_egresos) AS egresos
    FROM egresos
    GROUP BY anio
    ORDER BY anio;
    """
    evolucion = con.execute(q).df()
    fig = px.line(
        evolucion, x="anio", y="egresos",
        markers=True, title="Egresos por año",
    )
    fig.update_traces(line=dict(width=3, color="#2E86AB"))
    fig.update_layout(height=400, xaxis_title="Año", yaxis_title="Egresos")
    st.plotly_chart(fig, use_container_width=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Top 10 causas")
        q = """
        SELECT causa, SUM(cantidad_egresos) AS egresos
        FROM egresos
        GROUP BY causa
        ORDER BY egresos DESC
        LIMIT 10;
        """
        top = con.execute(q).df()
        fig = px.bar(
            top, x="egresos", y="causa", orientation="h",
            color_discrete_sequence=["#2E86AB"],
        )
        fig.update_layout(
            height=420, yaxis=dict(autorange="reversed"),
            xaxis_title="", yaxis_title="",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        if "tipo_egreso" in filtrado.columns:
            st.subheader("Tipo de egreso")
            q = """
            SELECT tipo_egreso, SUM(cantidad_egresos) AS egresos
            FROM egresos
            GROUP BY tipo_egreso
            ORDER BY egresos DESC;
            """
            tipos = con.execute(q).df()
            fig = px.pie(
                tipos, values="egresos", names="tipo_egreso",
                color_discrete_sequence=px.colors.qualitative.Set2,
            )
            fig.update_layout(height=420)
            st.plotly_chart(fig, use_container_width=True)


# === Tab 2: Geografía ===
with tab2:
    st.subheader("Distribución por municipio")
    q = """
    SELECT municipio, SUM(cantidad_egresos) AS egresos
    FROM egresos
    GROUP BY municipio
    ORDER BY egresos DESC
    LIMIT 20;
    """
    geo = con.execute(q).df()
    fig = px.bar(
        geo, x="municipio", y="egresos",
        color="egresos", color_continuous_scale="Blues",
    )
    fig.update_layout(height=500, xaxis_tickangle=-45, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    if "region_sanitaria" in filtrado.columns:
        st.subheader("Egresos por región sanitaria")
        q = """
        SELECT region_sanitaria, SUM(cantidad_egresos) AS egresos
        FROM egresos
        GROUP BY region_sanitaria
        ORDER BY egresos DESC;
        """
        reg = con.execute(q).df()
        fig = px.bar(reg, x="region_sanitaria", y="egresos",
                     color_discrete_sequence=["#F18F01"])
        fig.update_layout(height=400, xaxis_title="", yaxis_title="Egresos")
        st.plotly_chart(fig, use_container_width=True)


# === Tab 3: Causas ===
with tab3:
    st.subheader("Heatmap: estadía promedio por causa y año")
    if "dias_estadia_promedio" in filtrado.columns:
        q = """
        WITH top AS (
            SELECT causa
            FROM egresos
            GROUP BY causa
            ORDER BY SUM(cantidad_egresos) DESC
            LIMIT 10
        )
        SELECT e.causa, e.anio, ROUND(AVG(e.dias_estadia_promedio), 2) AS dias
        FROM egresos e
        JOIN top t USING (causa)
        WHERE e.dias_estadia_promedio IS NOT NULL
        GROUP BY e.causa, e.anio
        ORDER BY e.causa, e.anio;
        """
        h = con.execute(q).df().pivot(index="causa", columns="anio", values="dias")
        fig = px.imshow(h, text_auto=".1f", color_continuous_scale="YlOrRd",
                        aspect="auto")
        fig.update_layout(height=500, xaxis_title="Año", yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Carga asistencial (egresos × estadía)")
    if "dias_estadia_promedio" in filtrado.columns:
        q = """
        SELECT
            causa,
            SUM(cantidad_egresos) AS volumen,
            ROUND(AVG(dias_estadia_promedio), 2) AS estadia,
            ROUND(SUM(cantidad_egresos * COALESCE(dias_estadia_promedio, 0)), 0) AS dias_cama
        FROM egresos
        GROUP BY causa
        ORDER BY dias_cama DESC
        LIMIT 12;
        """
        carga = con.execute(q).df()
        fig = px.scatter(
            carga, x="volumen", y="estadia",
            size="dias_cama", hover_name="causa",
            color="dias_cama", color_continuous_scale="Viridis",
        )
        fig.update_layout(
            height=500,
            xaxis_title="Volumen de egresos",
            yaxis_title="Estadía promedio (días)",
        )
        st.plotly_chart(fig, use_container_width=True)


# === Tab 4: Datos crudos ===
with tab4:
    st.subheader("Tabla filtrada")
    st.caption(f"Mostrando {len(filtrado):,} filas (aplican filtros del sidebar)")
    st.dataframe(filtrado.head(1000), use_container_width=True)

    csv = filtrado.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Descargar CSV filtrado",
        data=csv,
        file_name="egresos_filtrado.csv",
        mime="text/csv",
    )


# -----------------------------------------------------------------------------
# Footer
# -----------------------------------------------------------------------------
st.divider()
st.markdown(
    """
    <div style="text-align:center; color:#888; font-size:0.85em">
    Proyecto de portfolio · Data Analyst · Franco Vigna ·
    <a href="https://github.com/" target="_blank">GitHub</a>
    </div>
    """,
    unsafe_allow_html=True,
)

import pandas as pd
import plotly.express as px
import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Vehicle Dashboard", layout="wide")

st.title("Data viewer")

# Cargar datos
df = pd.read_csv("vehicles_us.csv")

# Crear columna manufacturer a partir de model
df["manufacturer"] = df["model"].str.split().str[0]

# Limpiar algunas filas para evitar problemas en gráficos
df_graphs = df.dropna(subset=["odometer", "price", "model_year"]).copy()

#========================================
# SECCIÓN PARA CUMPLIR CON REQUERIMIENTOS
# =======================================

st.header("Project Vehicles Charts")

build_histogram = st.checkbox("Build histogram")
if build_histogram:
    st.write("Histogram for the odometer column")
    fig_hist_req = px.histogram(
        df_graphs,
        x="odometer",
        title="Odometer distribution"
    )
    st.plotly_chart(fig_hist_req, width="stretch")
    
build_scatter = st.checkbox("Build scatter plot")
if build_scatter:
    st.write("Scatter plot: price vs odometer")
    fig_scatter_req = px.scatter(
        df_graphs,
        x="odometer",
        y="price",
        title="Price vs odometer"
    )
    st.plotly_chart(fig_scatter_req, width="stretch")
    
# =========================
# 1. FILTRO POR FABRICANTE
# =========================

manufacturer_counts = df["manufacturer"].value_counts()

checkbox = st.checkbox("Include manufacturers with less than 1000 ads", value=True)

if not checkbox:
    valid_manufacturers = manufacturer_counts[manufacturer_counts >= 1000].index
    df = df[df["manufacturer"].isin(valid_manufacturers)]

# Mostrar tabla
st.dataframe(df)

# =========================
# 2. VEHICLE TYPES
# =========================

st.header("Vehicle types by manufacturer")

df_grouped = df.groupby(["manufacturer", "type"]).size().reset_index(name="count")

fig_bar = px.bar(
    df_grouped,
    x="manufacturer",
    y="count",
    color="type",
    title="Vehicle types by manufacturer"
)

st.plotly_chart(fig_bar, width="stretch")

# =========================
# 3. HISTOGRAMA CONDITION
# =========================

st.header("Histogram of condition vs model_year")

fig_hist = px.histogram(
    df,
    x="model_year",
    color="condition",
    title="Histogram of condition vs model_year"
)

st.plotly_chart(fig_hist, width="stretch")

# =========================
# 4. COMPARADOR DE PRECIOS
# =========================

st.header("Compare price distribution between manufacturers")

manufacturers = sorted(df["manufacturer"].dropna().unique())

col1, col2 = st.columns(2)

with col1:
    m1 = st.selectbox("Select manufacturer 1", manufacturers, index=0)

with col2:
    default_index_2 = 1 if len(manufacturers) > 1 else 0
    m2 = st.selectbox("Select manufacturer 2", manufacturers, index=default_index_2)

normalize = st.checkbox("Normalize histogram", value=True)

df_m1 = df[df["manufacturer"] == m1]
df_m2 = df[df["manufacturer"] == m2]

df_compare = pd.concat([
    df_m1.assign(source=m1),
    df_m2.assign(source=m2)
])

histnorm = "percent" if normalize else None

fig_price = px.histogram(
    df_compare,
    x="price",
    color="source",
    histnorm=histnorm,
    barmode="overlay",
    title="Price distribution comparison"
)

st.plotly_chart(fig_price, width="stretch")

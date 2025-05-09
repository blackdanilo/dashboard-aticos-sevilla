import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Cargar datos
@st.cache_data
def load_data():
    df = pd.read_excel("aticos_sevilla_1900.xlsx")
    df["price"] = pd.to_numeric(df["price"])
    df["meters"] = df["meters"].str.replace(" m²", "").astype(int)
    df["rooms"] = df["rooms"].str.extract(r"(\d+)").astype(int)
    return df

st.set_page_config(page_title="Dashboard Áticos Sevilla", layout="wide")
st.title("📊 Dashboard de Áticos en Sevilla")

df = load_data()

# Filtros
with st.sidebar:
    st.header("Filtros")
    max_price = st.slider("Precio máximo", int(df["price"].min()), int(df["price"].max()), int(df["price"].max()))
    rooms = st.multiselect("Número de habitaciones", sorted(df["rooms"].unique()), default=sorted(df["rooms"].unique()))
    df_filtered = df[(df["price"] <= max_price) & (df["rooms"].isin(rooms))]

# Métricas
col1, col2, col3 = st.columns(3)
col1.metric("Precio promedio", f"{df_filtered['price'].mean():,.0f} €")
col2.metric("Metros cuadrados promedio", f"{df_filtered['meters'].mean():.0f} m²")
col3.metric("Cantidad de propiedades", f"{df_filtered.shape[0]}")

# Gráficos
st.subheader("Distribución de precios")
fig1, ax1 = plt.subplots()
sns.histplot(df_filtered["price"], bins=30, kde=True, ax=ax1)
ax1.set_xlabel("Precio (€)")
st.pyplot(fig1)

st.subheader("Precio por habitaciones")
fig2, ax2 = plt.subplots()
sns.boxplot(x="rooms", y="price", data=df_filtered, ax=ax2)
ax2.set_xlabel("Habitaciones")
st.pyplot(fig2)

st.subheader("Precio vs Metros cuadrados")
fig3, ax3 = plt.subplots()
sns.scatterplot(x="meters", y="price", data=df_filtered, ax=ax3)
ax3.set_xlabel("Metros cuadrados")
ax3.set_ylabel("Precio (€)")
st.pyplot(fig3)

st.markdown("---")
st.caption("Danilo & Niké 💫 - Datos simulados para fines de aprendizaje")

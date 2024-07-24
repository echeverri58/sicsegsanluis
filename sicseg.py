import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import io
from urls import urls

# Configuración de la página
st.set_page_config(layout="wide", page_title="Sistema de Información y Seguridad Ciudadana - San Luis")

# Título y subtítulo
st.title("MUNICIPIO DE SAN LUIS")
st.subheader("SISTEMA DE INFORMACIÓN Y SEGURIDAD CIUDADANA")

# Función para cargar datos
@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    df['fecha_hecho'] = pd.to_datetime(df['fecha_hecho'])
    df['fecha_hecho'] = df['fecha_hecho'].dt.year
    return df

# Paleta de colores
palette = [
    '#d73027', '#f46d43', '#fdae61', '#fee08b', '#d9ef8b', '#a6d96a',
    '#66bd63', '#1a9850', '#006837'
]

# Función para crear gráficos
def create_chart(url, titulo, color):
    df = load_data(url)
    cantidad_por_año = df['cantidad'].groupby(df['fecha_hecho']).sum().astype('int')

    fig = px.bar(
        x=cantidad_por_año.index,
        y=cantidad_por_año.values,
        labels={'x': 'Año', 'y': 'Cantidad'},
        title=titulo,
        text=cantidad_por_año.values
    )

    fig.update_layout(
        showlegend=False,
        xaxis=dict(type='category', categoryorder='category ascending'),
        xaxis_tickangle=-90
    )

    fig.update_traces(marker_color=color, texttemplate='%{text}', textposition='outside')

    return fig

# Información de los gráficos
info_graficos = urls[:-1]  # Excluye la URL de contratos para el loop general

# Crear y mostrar los gráficos para los datos de seguridad
for i, info in enumerate(info_graficos):
    fig = create_chart(info['url'], info['titulo'], palette[i % len(palette)])
    st.plotly_chart(fig, use_container_width=True)

# Procesar y mostrar los datos de contratos
contracts_url = urls[-1]['url']
contracts_title = urls[-1]['titulo']

# Función para cargar datos de contratos
def load_contract_data(url):
    df = pd.read_csv(url)
    return df

contracts_df = load_contract_data(contracts_url)

# Mostrar tabla de contratos
st.subheader(contracts_title)
st.dataframe(contracts_df)

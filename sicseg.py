import streamlit as st
import pandas as pd
import plotly.express as px
from urls import urls
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(layout="wide", page_title="Sistema de Información y Seguridad Ciudadana - San Luis", page_icon="🏙️")

# Estilo personalizado
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stTitle {
        color: #1e3d59;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stSubheader {
        color: #ff6e40;
        font-size: 1.5rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

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

# Paleta de colores moderna
palette = [
    '#003f5c', '#2f4b7c', '#665191', '#a05195', '#d45087', '#f95d6a',
    '#ff7c43', '#ffa600', '#2ecc71', '#3498db'
]

# Función para crear gráficos
def create_chart(url, titulo, color):
    df = load_data(url)
    cantidad_por_año = df['cantidad'].groupby(df['fecha_hecho']).sum().astype('int')
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=cantidad_por_año.index,
        y=cantidad_por_año.values,
        marker_color=color,
        text=cantidad_por_año.values,
        textposition='outside'
    ))
    fig.update_layout(
        title={
            'text': titulo,
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Año",
        yaxis_title="Cantidad",
        showlegend=False,
        xaxis=dict(type='category', categoryorder='category ascending'),
        xaxis_tickangle=-45,
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(gridcolor='rgba(0,0,0,0.1)')
    )
    return fig

# Información de los gráficos
info_graficos = urls[:-1]  # Excluye la URL de contratos para el loop general

# Crear pestañas
tab1, tab2 = st.tabs(["📊 Gráficas de Seguridad", "📑 Contratos"])

with tab1:
    # Mostrar los gráficos para los datos de seguridad
    for i in range(0, len(info_graficos), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j < len(info_graficos):
                with col:
                    info = info_graficos[i + j]
                    fig = create_chart(info['url'], info['titulo'], palette[(i + j) % len(palette)])
                    st.plotly_chart(fig, use_container_width=True)

with tab2:
    # Procesar y mostrar los datos de contratos
    contracts_url = urls[-1]['url']
    contracts_title = urls[-1]['titulo']

    # Función para cargar datos de contratos
    @st.cache_data
    def load_contract_data(url):
        df = pd.read_csv(url)
        df['fecha_inicio'] = pd.to_datetime(df['fecha_inicio'])
        return df.sort_values('fecha_inicio', ascending=False)

    contracts_df = load_contract_data(contracts_url)

    # Aplicar estilo a la tabla de contratos
    st.subheader(contracts_title)

    # Crear una tabla interactiva con Plotly
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=list(contracts_df.columns),
            fill_color='#003f5c',
            align='left',
            font=dict(color='white', size=12)
        ),
        cells=dict(
            values=[contracts_df[col] for col in contracts_df.columns],
            fill_color=['#f0f2f6', 'white']*5,
            align='left',
            font=dict(color='darkslate', size=11)
        ))
    ])
    
    fig.update_layout(
        autosize=False,
        width=1200,
        height=500,
        margin=dict(l=0, r=0, b=0, t=30),
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown("""
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #003f5c;
        color: white;
        text-align: center;
        padding: 10px;
    }
    </style>
    <div class="footer">
        © 2024 Municipio de San Luis - Sistema de Información y Seguridad Ciudadana
    </div>
    """, unsafe_allow_html=True)

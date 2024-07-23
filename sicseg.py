import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

# Función para cargar datos de contrataciones
@st.cache_data
def load_contratos_data():
    url = "URL_AQUI"
    df = pd.read_csv(url)
    return df

# Paleta de colores
palette = [
    '#d73027', '#f46d43', '#fdae61', '#fee08b', '#d9ef8b', '#a6d96a',
    '#66bd63', '#1a9850', '#006837'
]

# Función para crear gráficos de delitos
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
        xaxis_tickangle=-90,
        annotations=[dict(
            x=1, y=-0.15,
            xref='paper', yref='paper',
            text='Datos extraidos automáticamente del Ministerio de Defensa',
            showarrow=False,
            font=dict(size=12, color='grey')
        )]
    )

    fig.update_traces(marker_color=color, texttemplate='%{text}', textposition='outside')

    return fig

# Información de los gráficos (sin URLs)
info_graficos = [
    {'url': "URL_AQUI", 'titulo': 'Amenazas en San Luis Antioquia por año'},
    {'url': "URL_AQUI", 'titulo': 'Delitos sexuales en San Luis Antioquia por año'},
    {'url': "URL_AQUI", 'titulo': 'Extorsión en San Luis Antioquia por año'},
    {'url': "URL_AQUI", 'titulo': 'Hurtos al comercio en San Luis'},
    {'url': "URL_AQUI", 'titulo': 'Hurto a personas en San Luis'},
    {'url': "URL_AQUI", 'titulo': 'Hurtos a residencias en San Luis'},
    {'url': "URL_AQUI", 'titulo': 'Hurtos a vehículos en San Luis'},
    {'url': "URL_AQUI", 'titulo': 'Lesiones accidente transito San Luis'},
    {'url': "URL_AQUI", 'titulo': 'Lesiones personales en San Luis'},
    {'url': "URL_AQUI", 'titulo': 'Piratería terrestre en San Luis'},
    {'url': "URL_AQUI", 'titulo': 'Homicidios en San Luis'},
    {'url': "URL_AQUI", 'titulo': 'Secuestros en San Luis'},
    {'url': "URL_AQUI", 'titulo': 'Violencia intrafamiliar en San Luis'},
]

# Función para crear gráficos de contratos
def create_contrato_chart():
    df = load_contratos_data()
    fig = go.Figure()

    for i, estado in enumerate(df['estado_contrato'].unique()):
        df_estado = df[df['estado_contrato'] == estado]
        fig.add_trace(go.Scatter(
            x=df_estado['fecha_firma'],
            y=df_estado['monto'],
            mode='lines',
            name=estado,
            line=dict(color='blue' if i % 2 == 0 else 'white')
        ))

    fig.update_layout(title="Contratos en San Luis",
                      xaxis_title='Fecha de Firma',
                      yaxis_title='Monto',
                      legend_title='Estado del Contrato')
    return fig

# Diseño de la página
st.markdown("""
    <style>
        .main {
            background: linear-gradient(to bottom, #ffffff, #e0e0e0);
            padding: 20px;
            border-radius: 10px;
        }
        h1, h2, h3 {
            color: #003366;
        }
    </style>
    """, unsafe_allow_html=True)

# Tabs
tab1, tab2 = st.tabs(["Delitos", "Contratos"])

# Tab de Delitos
with tab1:
    cols = st.columns(3)
    for idx, info in enumerate(info_graficos):
        fig = create_chart(info['url'], info['titulo'], palette[idx % len(palette)])
        cols[idx % 3].plotly_chart(fig, use_container_width=True)
        cols[idx % 3].download_button(
            label="Descargar gráfico",
            data=fig.to_image(format="png"),
            file_name=f"{info['titulo']}.png",
            mime="image/png"
        )

# Tab de Contratos
with tab2:
    fig = create_contrato_chart()
    st.plotly_chart(fig, use_container_width=True)

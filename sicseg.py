import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import io
from datetime import datetime

# Configuración de la página
st.set_page_config(layout="wide", page_title="Sistema de Información y Seguridad Ciudadana - San Luis")

# Título y subtítulo
st.title("MUNICIPIO DE SAN LUIS")
st.subheader("SISTEMA DE INFORMACIÓN Y SEGURIDAD CIUDADANA")

# --- FUNCIONES DE CARGA DE DATOS ---

@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    # dayfirst=True y errors='coerce' evitan errores por formatos mixtos o valores vacíos
    df['fecha_hecho'] = pd.to_datetime(df['fecha_hecho'], dayfirst=True, errors='coerce')
    # Eliminamos registros sin fecha válida
    df = df.dropna(subset=['fecha_hecho'])
    df['fecha_hecho'] = df['fecha_hecho'].dt.year.astype(int)
    return df

@st.cache_data
def load_lab_data(url):
    df = pd.read_csv(url)
    df['fecha_hecho'] = pd.to_datetime(df['fecha_hecho'], dayfirst=True, errors='coerce')
    df = df.dropna(subset=['fecha_hecho'])
    df['año'] = df['fecha_hecho'].dt.year.astype(int)
    return df

@st.cache_data
def load_contratos_data():
    # URL base de SECOP II - Contratos Electrónicos
    base_url = "https://www.datos.gov.co/resource/jbjy-vk9h.csv"
    
    # Parámetros de la consulta: Filtramos por departamento y ciudad, y seleccionamos las columnas necesarias
    # Usamos $where para filtrar y $select para las columnas (o quitamos select para traer todas)
    params = {
        "$where": "caseless_one_of(departamento, 'Antioquia') AND caseless_one_of(ciudad, 'San Luis')",
        "$limit": 5000,
        "$order": "fecha_de_inicio_del_contrato DESC"
    }
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    data = pd.read_csv(io.StringIO(response.text))

    columnas_deseadas = [
        'nombre_entidad', 'objeto_del_contrato', 'tipo_de_contrato', 'duraci_n_del_contrato',
        'modalidad_de_contratacion', 'valor_del_contrato', 'fecha_de_firma',
        'fecha_de_inicio_del_contrato', 'fecha_de_fin_del_contrato',
        'fecha_de_inicio_de_ejecucion', 'fecha_de_fin_de_ejecucion', 'urlproceso',
        'nombre_representante_legal', 'nacionalidad_representante_legal',
        'domicilio_representante_legal', 'tipo_de_identificaci_n_representante_legal',
        'identificaci_n_representante_legal'
    ]

    # Filtrar solo las columnas que realmente existan en el resultado
    columnas_existentes = [col for col in columnas_deseadas if col in data.columns]
    data = data[columnas_existentes]
    return data

# --- LÓGICA DE GRÁFICOS ---

palette = ['#d73027', '#f46d43', '#fdae61', '#fee08b', '#d9ef8b', '#a6d96a', '#66bd63', '#1a9850', '#006837', '#3399ff']

def create_chart_data(url, titulo, color, is_lab=False):
    if is_lab:
        df = load_lab_data(url)
        df_anual = df.groupby('año')['cantidad'].sum().reset_index()
        # Filtrar últimos 20 años
        año_actual = datetime.now().year
        df_anual = df_anual[df_anual['año'] >= (año_actual - 20)]
        fig = px.bar(df_anual, x='año', y='cantidad', title=titulo, text='cantidad')
        display_df = df_anual
    else:
        df = load_data(url)
        cantidad_por_año = df.groupby('fecha_hecho')['cantidad'].sum().reset_index()
        fig = px.bar(cantidad_por_año, x='fecha_hecho', y='cantidad', title=titulo, text='cantidad')
        display_df = cantidad_por_año

    fig.update_layout(
        showlegend=False,
        xaxis=dict(type='category', categoryorder='category ascending'),
        xaxis_tickangle=-90,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    fig.update_traces(marker_color=color, texttemplate='%{text}', textposition='outside')
    return fig, display_df

# URLs de Datos Abiertos
info_graficos = [
    {'url': "https://www.datos.gov.co/resource/meew-mguv.csv?$query=SELECT%20*%20WHERE%20caseless_one_of(departamento,%20'ANTIOQUIA')%20AND%20caseless_one_of(municipio,%20'SAN%20LUIS')", 'titulo': 'Amenazas'},
    {'url': "https://www.datos.gov.co/resource/bz43-8ahq.csv?$query=SELECT%20*%20WHERE%20caseless_one_of(departamento,%20'ANTIOQUIA')%20AND%20caseless_one_of(municipio,%20'SAN%20LUIS')", 'titulo': 'Delitos sexuales'},
    {'url': "https://www.datos.gov.co/resource/q2ib-t9am.csv?$query=SELECT%20*%20WHERE%20caseless_one_of(departamento,%20'ANTIOQUIA')%20AND%20caseless_one_of(municipio,%20'SAN%20LUIS')", 'titulo': 'Extorsión'},
    {'url': "https://www.datos.gov.co/resource/7i2x-h5vp.csv?$query=SELECT%20*%20WHERE%20caseless_one_of(departamento,%20'ANTIOQUIA')%20AND%20caseless_one_of(municipio,%20'SAN%20LUIS')", 'titulo': 'Hurtos al comercio'},
    {'url': "https://www.datos.gov.co/resource/4rxi-8m8d.csv?$query=SELECT%20*%20WHERE%20caseless_one_of(departamento,%20'ANTIOQUIA')%20AND%20caseless_one_of(municipio,%20'SAN%20LUIS')", 'titulo': 'Hurto a personas'},
    {'url': "https://www.datos.gov.co/resource/csb4-y6v2.csv?$query=SELECT%20*%20WHERE%20caseless_one_of(departamento,%20'ANTIOQUIA')%20AND%20caseless_one_of(municipio,%20'SAN%20LUIS')", 'titulo': 'Hurtos a residencias'},
    {'url': "https://www.datos.gov.co/resource/f68p-q56e.csv?$query=SELECT%20*%20WHERE%20caseless_one_of(departamento,%20'ANTIOQUIA')%20AND%20caseless_one_of(municipio,%20'SAN%20LUIS')", 'titulo': 'Hurtos a vehículos'},
    {'url': "https://www.datos.gov.co/resource/ntej-qq7v.csv?$query=SELECT%20*%20WHERE%20caseless_one_of(departamento,%20'ANTIOQUIA')%20AND%20caseless_one_of(municipio,%20'SAN%20LUIS')", 'titulo': 'Lesiones accidente tránsito'},
    {'url': "https://www.datos.gov.co/resource/jr6v-i33g.csv?$query=SELECT%20*%20WHERE%20caseless_one_of(departamento,%20'ANTIOQUIA')%20AND%20caseless_one_of(municipio,%20'SAN%20LUIS')", 'titulo': 'Lesiones personales'},
    {'url': "https://www.datos.gov.co/resource/u584-j4s6.csv?$query=SELECT%20*%20WHERE%20caseless_one_of(departamento,%20'ANTIOQUIA')%20AND%20caseless_one_of(municipio,%20'SAN%20LUIS')", 'titulo': 'Piratería terrestre'},
    {'url': "https://www.datos.gov.co/resource/m8fd-ahd9.csv?$query=SELECT%20*%20WHERE%20caseless_one_of(departamento,%20'ANTIOQUIA')%20AND%20caseless_one_of(municipio,%20'SAN%20LUIS')", 'titulo': 'Homicidios'},
    {'url': "https://www.datos.gov.co/resource/dyu3-v3bp.csv?$query=SELECT%20*%20WHERE%20caseless_one_of(departamento,%20'ANTIOQUIA')%20AND%20caseless_one_of(municipio,%20'SAN%20LUIS')", 'titulo': 'Secuestros'},
    {'url': "https://www.datos.gov.co/resource/gepp-dxcs.csv?$query=SELECT%20*%20WHERE%20caseless_one_of(departamento,%20'ANTIOQUIA')%20AND%20caseless_one_of(municipio,%20'SAN%20LUIS')", 'titulo': 'Violencia intrafamiliar'},
    {'url': "https://www.datos.gov.co/resource/s29y-2xjd.csv?$query=SELECT%20fecha_hecho,%20cantidad%20WHERE%20caseless_one_of(departamento,%20'ANTIOQUIA')%20AND%20caseless_one_of(municipio,%20'SAN%20LUIS')", 'titulo': 'Laboratorios destruidos', 'is_lab': True},
]

# --- UI DE TABS ---

tab1, tab2 = st.tabs(["📊 Gráficos de Delitos", "📑 Contrataciones"])

with tab1:
    st.header("Estadísticas de Seguridad - San Luis")
    
    # Lista para almacenar los datos de cada delito
    dfs_para_consolidar = []
    
    # Grid de 3 columnas para los gráficos
    for i in range(0, len(info_graficos), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(info_graficos):
                index = i + j
                with cols[j]:
                    color = palette[index % len(palette)]
                    try:
                        fig, df_tabla = create_chart_data(
                            info_graficos[index]['url'], 
                            info_graficos[index]['titulo'], 
                            color, 
                            info_graficos[index].get('is_lab', False)
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Preparar datos para la tabla consolidada
                        # Renombramos 'cantidad' al título del delito para la unión
                        temp_df = df_tabla.copy()
                        # El nombre de la columna de tiempo varía entre 'fecha_hecho' y 'año'
                        time_col = 'año' if info_graficos[index].get('is_lab', False) else 'fecha_hecho'
                        temp_df = temp_df.rename(columns={time_col: 'Año', 'cantidad': info_graficos[index]['titulo']})
                        dfs_para_consolidar.append(temp_df.set_index('Año'))
                        
                    except Exception as e:
                        st.error(f"Error cargando {info_graficos[index]['titulo']}")

    # Sección para la Tabla Única Consolidada
    st.markdown("---")
    st.subheader("📑 Tabla Consolidada de Delitos por Año")
    if dfs_para_consolidar:
        try:
            # Consolidar todos los dataframes en uno solo usando el índice (Año)
            df_consolidado = pd.concat(dfs_para_consolidar, axis=1)
            # Ordenar por año descendente
            df_consolidado = df_consolidado.sort_index(ascending=False).fillna(0).astype(int)
            st.dataframe(df_consolidado, use_container_width=True)
            
            # Botón de descarga opcional
            csv = df_consolidado.to_csv().encode('utf-8')
            st.download_button(
                label="📥 Descargar tabla consolidada (CSV)",
                data=csv,
                file_name=f"seguridad_san_luis_{datetime.now().strftime('%Y%m%d')}.csv",
                mime='text/csv',
            )
        except Exception as e:
            st.error(f"No se pudo generar la tabla consolidada: {e}")


with tab2:
    st.header("Historial de Contrataciones Públicas")
    try:
        contratos_df = load_contratos_data()
        st.dataframe(contratos_df, use_container_width=True)
    except Exception as e:
        st.error(f"No se pudieron cargar los datos de contratación: {e}")

# Pie de página
st.markdown("---")
st.markdown("**Fuente:** Datos Abiertos Colombia (datos.gov.co)")
st.caption("Creado por John Alexander Echeverry Ocampo, politólogo y analista de datos")

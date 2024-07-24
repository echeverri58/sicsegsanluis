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

# Información de los gráficos (sin URLs)
info_graficos = [
    {'url': "https://www.datos.gov.co/resource/meew-mguv.csv?$query=SELECT%0A%20%20%60departamento%60%2C%0A%20%20%60municipio%60%2C%0A%20%20%60codigo_dane%60%2C%0A%20%20%60armas_medios%60%2C%0A%20%20%60fecha_hecho%60%2C%0A%20%20%60genero%60%2C%0A%20%20%60grupo_etario%60%2C%0A%20%20%60cantidad%60%0AWHERE%0A%20%20caseless_one_of(%60departamento%60%2C%20%22ANTIOQUIA%22)%0A%20%20AND%20caseless_one_of(%60municipio%60%2C%20%22SAN%20LUIS%22)", 'titulo': 'Amenazas en San Luis Antioquia por año'},
    {'url': "https://www.datos.gov.co/resource/bz43-8ahq.csv?$query=SELECT%0A%20%20%60fecha_hecho%60%2C%0A%20%20%60cod_depto%60%2C%0A%20%20%60departamento%60%2C%0A%20%20%60cod_muni%60%2C%0A%20%20%60municipio%60%2C%0A%20%20%60zona%60%2C%0A%20%20%60sexo%60%2C%0A%20%20%60cantidad%60%0AWHERE%0A%20%20caseless_one_of(%60departamento%60%2C%20%22ANTIOQUIA%22)%0A%20%20AND%20caseless_one_of(%60municipio%60%2C%20%22SAN%20LUIS%22)%0AORDER%20BY%20%60fecha_hecho%60%20DESC%20NULL%20LAST", 'titulo': 'Delitos sexuales en San Luis Antioquia por año'},
    {'url': "https://www.datos.gov.co/resource/q2ib-t9am.csv?$query=SELECT%0A%20%20%60fecha_hecho%60%2C%0A%20%20%60cod_depto%60%2C%0A%20%20%60departamento%60%2C%0A%20%20%60cod_muni%60%2C%0A%20%20%60municipio%60%2C%0A%20%20%60cantidad%60%0AWHERE%0A%20%20caseless_one_of(%60departamento%60%2C%20%22ANTIOQUIA%22)%0A%20%20AND%20caseless_one_of(%60municipio%60%2C%20%22SAN%20LUIS%22)%0AORDER%20BY%20%60fecha_hecho%60%20DESC%20NULL%20LAST", 'titulo': 'Extorsión en San Luis Antioquia por año'},
    {'url': "https://www.datos.gov.co/resource/7i2x-h5vp.csv?$query=SELECT%0A%20%20%60fecha_hecho%60%2C%0A%20%20%60cod_depto%60%2C%0A%20%20%60departamento%60%2C%0A%20%20%60cod_muni%60%2C%0A%20%20%60municipio%60%2C%0A%20%20%60cantidad%60%0AWHERE%0A%20%20caseless_one_of(%60departamento%60%2C%20%22ANTIOQUIA%22)%0A%20%20AND%20caseless_one_of(%60municipio%60%2C%20%22SAN%20LUIS%22)%0AORDER%20BY%20%60fecha_hecho%60%20DESC%20NULL%20LAST", 'titulo': 'Hurtos al comercio en San Luis'},
    {'url': "https://www.datos.gov.co/resource/4rxi-8m8d.csv?$query=SELECT%0A%20%20%60fecha_hecho%60%2C%0A%20%20%60cod_depto%60%2C%0A%20%20%60departamento%60%2C%0A%20%20%60cod_muni%60%2C%0A%20%20%60municipio%60%2C%0A%20%20%60cantidad%60%0AWHERE%0A%20%20caseless_one_of(%60departamento%60%2C%20%22ANTIOQUIA%22)%0A%20%20AND%20caseless_one_of(%60municipio%60%2C%20%22SAN%20LUIS%22)", 'titulo': 'Hurto a personas en San Luis'},
    {'url': "https://www.datos.gov.co/resource/csb4-y6v2.csv?$query=SELECT%0A%20%20%60fecha_hecho%60%2C%0A%20%20%60cod_depto%60%2C%0A%20%20%60departamento%60%2C%0A%20%20%60cod_muni%60%2C%0A%20%20%60municipio%60%2C%0A%20%20%60tipo_delito%60%2C%0A%20%20%60zona%60%2C%0A%20%20%60cantidad%60%0AWHERE%0A%20%20caseless_one_of(%60departamento%60%2C%20%22ANTIOQUIA%22)%0A%20%20AND%20caseless_one_of(%60municipio%60%2C%20%22SAN%20LUIS%22)%0AORDER%20BY%20%60fecha_hecho%60%20DESC%20NULL%20LAST", 'titulo': 'Hurtos a residencias en San Luis'},
    {'url': "https://www.datos.gov.co/resource/csb4-y6v2.csv?$query=SELECT%0A%20%20%60fecha_hecho%60%2C%0A%20%20%60cod_depto%60%2C%0A%20%20%60departamento%60%2C%0A%20%20%60cod_muni%60%2C%0A%20%20%60municipio%60%2C%0A%20%20%60tipo_delito%60%2C%0A%20%20%60zona%60%2C%0A%20%20%60cantidad%60%0AWHERE%0A%20%20caseless_one_of(%60departamento%60%2C%20%22ANTIOQUIA%22)%0A%20%20AND%20caseless_one_of(%60municipio%60%2C%20%22SAN%20LUIS%22)%0AORDER%20BY%20%60fecha_hecho%60%20DESC%20NULL%20LAST", 'titulo': 'Hurtos a vehículos en San Luis'},
    {'url': "https://www.datos.gov.co/resource/ntej-qq7v.csv?$query=SELECT%0A%20%20%60fecha_hecho%60%2C%0A%20%20%60cod_depto%60%2C%0A%20%20%60departamento%60%2C%0A%20%20%60cod_muni%60%2C%0A%20%20%60municipio%60%2C%0A%20%20%60cantidad%60%0AWHERE%0A%20%20caseless_one_of(%60departamento%60%2C%20%22ANTIOQUIA%22)%0A%20%20AND%20caseless_one_of(%60municipio%60%2C%20%22SAN%20LUIS%22)%0AORDER%20BY%20%60fecha_hecho%60%20DESC%20NULL%20LAST", 'titulo': 'Lesiones accidente transito San Luis'},
    {'url': "https://www.datos.gov.co/resource/jr6v-i33g.csv?$query=SELECT%0A%20%20%60fecha_hecho%60%2C%0A%20%20%60cod_depto%60%2C%0A%20%20%60departamento%60%2C%0A%20%20%60cod_muni%60%2C%0A%20%20%60municipio%60%2C%0A%20%20%60sexo%60%2C%0A%20%20%60cantidad%60%0AWHERE%0A%20%20caseless_one_of(%60departamento%60%2C%20%22ANTIOQUIA%22)%0A%20%20AND%20caseless_one_of(%60municipio%60%2C%20%22SAN%20LUIS%22)%0AORDER%20BY%20%60fecha_hecho%60%20DESC%20NULL%20LAST", 'titulo': 'Lesiones personales en San Luis'},
    {'url': "https://www.datos.gov.co/resource/sutf-7dyz.csv?$query=SELECT%0A%20%20%60fecha_hecho%60%2C%0A%20%20%60cod_depto%60%2C%0A%20%20%60departamento%60%2C%0A%20%20%60cod_muni%60%2C%0A%20%20%60municipio%60%2C%0A%20%20%60zona%60%2C%0A%20%20%60cantidad%60%0AWHERE%0A%20%20caseless_one_of(%60departamento%60%2C%20%22ANTIOQUIA%22)%0A%20%20AND%20caseless_one_of(%60municipio%60%2C%20%22SAN%20LUIS%22)", 'titulo': 'Piratería terrestre en San Luis'},
    {'url': "https://www.datos.gov.co/resource/m8fd-ahd9.csv?$query=SELECT%0A%20%20%60fecha_hecho%60%2C%0A%20%20%60cod_depto%60%2C%0A%20%20%60departamento%60%2C%0A%20%20%60cod_muni%60%2C%0A%20%20%60municipio%60%2C%0A%20%20%60zona%60%2C%0A%20%20%60sexo%60%2C%0A%20%20%60cantidad%60%0AWHERE%0A%20%20caseless_one_of(%60departamento%60%2C%20%22ANTIOQUIA%22)%0A%20%20AND%20caseless_one_of(%60municipio%60%2C%20%22SAN%20LUIS%22)", 'titulo': 'Homicidios en San Luis'},
    {'url': "https://www.datos.gov.co/resource/d7zw-hpf4.csv?$query=SELECT%0A%20%20%60fecha_hecho%60%2C%0A%20%20%60cod_depto%60%2C%0A%20%20%60departamento%60%2C%0A%20%20%60cod_muni%60%2C%0A%20%20%60municipio%60%2C%0A%20%20%60tipo_delito%60%2C%0A%20%20%60cantidad%60%0AWHERE%0A%20%20caseless_one_of(%60departamento%60%2C%20%22ANTIOQUIA%22)%0A%20%20AND%20caseless_one_of(%60municipio%60%2C%20%22SAN%20LUIS%22)%0AORDER%20BY%20%60fecha_hecho%60%20DESC%20NULL%20LAST", 'titulo': 'Secuestros en San Luis'},
    {'url': "https://www.datos.gov.co/resource/gepp-dxcs.csv?$query=SELECT%0A%20%20%60fecha_hecho%60%2C%0A%20%20%60cod_depto%60%2C%0A%20%20%60departamento%60%2C%0A%20%20%60cod_muni%60%2C%0A%20%20%60municipio%60%2C%0A%20%20%60zona%60%2C%0A%20%20%60cantidad%60%0AWHERE%0A%20%20caseless_one_of(%60departamento%60%2C%20%22ANTIOQUIA%22)%0A%20%20AND%20caseless_one_of(%60municipio%60%2C%20%22SAN%20LUIS%22)%0AORDER%20BY%20%60fecha_hecho%60%20DESC%20NULL%20LAST", 'titulo': 'Violencia intrafamiliar en San Luis'},
]

# Función para cargar datos de contrataciones
@st.cache_data
def load_contratos_data():
    url = "https://www.datos.gov.co/resource/jbjy-vk9h.csv?$query=SELECT%0A%20%20%60nombre_entidad%60%2C%0A%20%20%60nit_entidad%60%2C%0A%20%20%60departamento%60%2C%0A%20%20%60ciudad%60%2C%0A%20%20%60localizaci_n%60%2C%0A%20%20%60orden%60%2C%0A%20%20%60sector%60%2C%0A%20%20%60rama%60%2C%0A%20%20%60entidad_centralizada%60%2C%0A%20%20%60proceso_de_compra%60%2C%0A%20%20%60id_contrato%60%2C%0A%20%20%60referencia_del_contrato%60%2C%0A%20%20%60estado_contrato%60%2C%0A%20%20%60codigo_de_categoria_principal%60%2C%0A%20%20%60descripcion_del_proceso%60%2C%0A%20%20%60tipo_de_contrato%60%2C%0A%20%20%60modalidad_de_contratacion%60%2C%0A%20%20%60justificacion_modalidad_de%60%2C%0A%20%20%60fecha_de_firma%60%2C%0A%20%20%60fecha_de_inicio_del_contrato%60%2C%0A%20%20%60fecha_de_fin_del_contrato%60%2C%0A%20%20%60fecha_de_inicio_de_ejecucion%60%2C%0A%20%20%60fecha_de_fin_de_ejecucion%60%2C%0A%20%20%60condiciones_de_entrega%60%2C%0A%20%20%60tipodocproveedor%60%2C%0A%20%20%60documento_proveedor%60%2C%0A%20%20%60proveedor_adjudicado%60%2C%0A%20%20%60es_grupo%60%2C%0A%20%20%60es_pyme%60%2C%0A%20%20%60habilita_pago_adelantado%60%2C%0A%20%20%60liquidaci_n%60%2C%0A%20%20%60obligaci_n_ambiental%60%2C%0A%20%20%60obligaciones_postconsumo%60%2C%0A%20%20%60reversion%60%2C%0A%20%20%60origen_de_los_recursos%60%2C%0A%20%20%60destino_gasto%60%2C%0A%20%20%60valor_del_contrato%60%2C%0A%20%20%60valor_de_pago_adelantado%60%2C%0A%20%20%60valor_facturado%60%2C%0A%20%20%60valor_pendiente_de_pago%60%2C%0A%20%20%60valor_pagado%60%2C%0A%20%20%60valor_amortizado%60%2C%0A%20%20%60valor_pendiente_de%60%2C%0A%20%20%60valor_pendiente_de_ejecucion%60%2C%0A%20%20%60estado_bpin%60%2C%0A%20%20%60c_digo_bpin%60%2C%0A%20%20%60anno_bpin%60%2C%0A%20%20%60saldo_cdp%60%2C%0A%20%20%60saldo_vigencia%60%2C%0A%20%20%60espostconflicto%60%2C%0A%20%20%60dias_adicionados%60%2C%0A%20%20%60puntos_del_acuerdo%60%2C%0A%20%20%60pilares_del_acuerdo%60%2C%0A%20%20%60urlproceso%60%2C%0A%20%20%60nombre_representante_legal%60%2C%0A%20%20%60nacionalidad_representante_legal%60%2C%0A%20%20%60domicilio_representante_legal%60%2C%0A%20%20%60tipo_de_identificaci_n_representante_legal%60%2C%0A%20%20%60identificaci_n_representante_legal%60%2C%0A%20%20%60g_nero_representante_legal%60%2C%0A%20%20%60presupuesto_general_de_la_nacion_pgn%60%2C%0A%20%20%60sistema_general_de_participaciones%60%2C%0A%20%20%60sistema_general_de_regal_as%60%2C%0A%20%20%60recursos_propios_alcald_as_gobernaciones_y_resguardos_ind_genas_%60%2C%0A%20%20%60recursos_de_credito%60%2C%0A%20%20%60recursos_propios%60%2C%0A%20%20%60ultima_actualizacion%60%2C%0A%20%20%60codigo_entidad%60%2C%0A%20%20%60codigo_proveedor%60%2C%0A%20%20%60fecha_inicio_liquidacion%60%2C%0A%20%20%60fecha_fin_liquidacion%60%2C%0A%20%20%60objeto_del_contrato%60%2C%0A%20%20%60duraci_n_del_contrato%60%2C%0A%20%20%60nombre_del_banco%60%2C%0A%20%20%60tipo_de_cuenta%60%2C%0A%20%20%60n_mero_de_cuenta%60%2C%0A%20%20%60el_contrato_puede_ser_prorrogado%60%2C%0A%20%20%60fecha_de_notificaci_n_de_prorrogaci_n%60%0AWHERE%0A%20%20caseless_one_of(%60departamento%60%2C%20%22Antioquia%22)%0A%20%20AND%20caseless_one_of(%60ciudad%60%2C%20%22san%20luis%22)"  # Reemplazar con la URL correcta
    response = requests.get(url)
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

    return data[columnas_deseadas]

# Crear pestañas
tab1, tab2 = st.tabs(["Gráficos de Delitos", "Contrataciones"])

with tab1:
    st.header("Gráficos de Delitos en San Luis")

    # Crear una cuadrícula de 3x5 para los gráficos
    for i in range(0, len(info_graficos), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(info_graficos):
                with cols[j]:
                    color = palette[(i + j) % len(palette)]
                    fig = create_chart(info_graficos[i + j]['url'], info_graficos[i + j]['titulo'], color)
                    st.plotly_chart(fig, use_container_width=True)

    # Gráfica adicional de laboratorios destruidos
    st.header("Laboratorios destruidos en San Luis")
    df = load_data("https://www.datos.gov.co/resource/v75m-npi8.csv?$query=SELECT%0A%20%20%60fecha_hecho%60%2C%0A%20%20%60cod_depto%60%2C%0A%20%20%60departamento%60%2C%0A%20%20%60cod_muni%60%2C%0A%20%20%60municipio%60%2C%0A%20%20%60cantidad%60%2C%0A%20%20%60unidad%60%0AWHERE%0A%20%20caseless_one_of(%60departamento%60%2C%20%22antioquia%22)%0A%20%20AND%20caseless_one_of(%60municipio%60%2C%20%22san%20luis%22)%0AORDER%20BY%20%60fecha_hecho%60%20DESC%20NULL%20LAST")
    df['fecha_hecho'] = pd.to_datetime(df['fecha_hecho'])
    df['año'] = df['fecha_hecho'].dt.year
    df_anual = df.groupby('año')['cantidad'].sum().reset_index()
    año_actual = datetime.now().year
    inicio_rango = año_actual - 20
    df_anual_reciente = df_anual[(df_anual['año'] >= inicio_rango) & (df_anual['año'] <= año_actual)]

    fig_lab = px.bar(
        df_anual_reciente,
        x='año',
        y='cantidad',
        labels={'año': 'Año', 'cantidad': 'Cantidad de laboratorios destruidos'},
        title=f'Laboratorios destruidos por año en San Luis, Antioquia ({inicio_rango} - {año_actual})',
        text='cantidad'
    )

    fig_lab.update_layout(
        xaxis_tickangle=-90
    )

    fig_lab.update_traces(marker_color='skyblue', texttemplate='%{text}', textposition='outside')

    st.plotly_chart(fig_lab, use_container_width=True)

with tab2:
    st.header("Contrataciones en San Luis")

    # Cargar y mostrar datos de contrataciones
    contratos_data = load_contratos_data()
    st.dataframe(contratos_data)

# Nota del creador
st.markdown("---")
st.markdown("Creado por John Alexander Echeverry Ocampo, politólogo y analista de datos")

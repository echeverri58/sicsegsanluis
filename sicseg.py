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
    url ="https://www.datos.gov.co/resource/jbjy-vk9h.csv?$query=SELECT%0A%20%20%60nombre_entidad%60%2C%0A%20%20%60nit_entidad%60%2C%0A%20%20%60departamento%60%2C%0A%20%20%60ciudad%60%2C%0A%20%20%60localizaci_n%60%2C%0A%20%20%60orden%60%2C%0A%20%20%60sector%60%2C%0A%20%20%60rama%60%2C%0A%20%20%60entidad_centralizada%60%2C%0A%20%20%60proceso_de_compra%60%2C%0A%20%20%60id_contrato%60%2C%0A%20%20%60referencia_del_contrato%60%2C%0A%20%20%60estado_contrato%60%2C%0A%20%20%60codigo_de_categoria_principal%60%2C%0A%20%20%60descripcion_del_proceso%60%2C%0A%20%20%60tipo_de_contrato%60%2C%0A%20%20%60modalidad_de_contratacion%60%2C%0A%20%20%60justificacion_modalidad_de%60%2C%0A%20%20%60fecha_de_firma%60%2C%0A%20%20%60fecha_de_inicio_del_contrato%60%2C%0A%20%20%60fecha_de_fin_del_contrato%60%2C%0A%20%20%60fecha_de_inicio_de_ejecucion%60%2C%0A%20%20%60fecha_de_fin_de_ejecucion%60%2C%0A%20%20%60condiciones_de_entrega%60%2C%0A%20%20%60tipodocproveedor%60%2C%0A%20%20%60documento_proveedor%60%2C%0A%20%20%60proveedor_adjudicado%60%2C%0A%20%20%60es_grupo%60%2C%0A%20%20%60es_pyme%60%2C%0A%20%20%60habilita_pago_adelantado%60%2C%0A%20%20%60liquidaci_n%60%2C%0A%20%20%60obligaci_n_ambiental%60%2C%0A%20%20%60obligaciones_postconsumo%60%2C%0A%20%20%60reversion%60%2C%0A%20%20%60origen_de_los_recursos%60%2C%0A%20%20%60destino_gasto%60%2C%0A%20%20%60valor_del_contrato%60%2C%0A%20%20%60valor_de_pago_adelantado%60%2C%0A%20%20%60valor_facturado%60%2C%0A%20%20%60valor_pendiente_de_pago%60%2C%0A%20%20%60valor_pagado%60%2C%0A%20%20%60valor_amortizado%60%2C%0A%20%20%60valor_pendiente_de%60%2C%0A%20%20%60valor_pendiente_de_ejecucion%60%2C%0A%20%20%60estado_bpin%60%2C%0A%20%20%60c_digo_bpin%60%2C%0A%20%20%60anno_bpin%60%2C%0A%20%20%60saldo_cdp%60%2C%0A%20%20%60saldo_vigencia%60%2C%0A%20%20%60espostconflicto%60%2C%0A%20%20%60dias_adicionados%60%2C%0A%20%20%60puntos_del_acuerdo%60%2C%0A%20%20%60pilares_del_acuerdo%60%2C%0A%20%20%60urlproceso%60%2C%0A%20%20%60nombre_representante_legal%60%2C%0A%20%20%60nacionalidad_representante_legal%60%2C%0A%20%20%60domicilio_representante_legal%60%2C%0A%20%20%60tipo_de_identificaci_n_representante_legal%60%2C%0A%20%20%60identificaci_n_representante_legal%60%2C%0A%20%20%60g_nero_representante_legal%60%2C%0A%20%20%60presupuesto_general_de_la_nacion_pgn%60%2C%0A%20%20%60sistema_general_de_participaciones%60%2C%0A%20%20%60sistema_general_de_regal_as%60%2C%0A%20%20%60recursos_propios_alcald_as_gobernaciones_y_resguardos_ind_genas_%60%2C%0A%20%20%60recursos_de_credito%60%2C%0A%20%20%60recursos_propios%60%2C%0A%20%20%60ultima_actualizacion%60%2C%0A%20%20%60codigo_entidad%60%2C%0A%20%20%60codigo_proveedor%60%2C%0A%20%20%60fecha_inicio_liquidacion%60%2C%0A%20%20%60fecha_fin_liquidacion%60%2C%0A%20%20%60objeto_del_contrato%60%2C%0A%20%20%60duraci_n_del_contrato%60%2C%0A%20%20%60nombre_del_banco%60%2C%0A%20%20%60tipo_de_cuenta%60%2C%0A%20%20%60n_mero_de_cuenta%60%2C%0A%20%20%60el_contrato_puede_ser_prorrogado%60%2C%0A%20%20%60fecha_de_notificaci_n_de_prorrogaci_n%60%0AWHERE%0A%20%20caseless_one_of(%60departamento%60%2C%20%22Antioquia%22)%0A%20%20AND%20caseless_one_of(%60ciudad%60%2C%20%22san%20luis%22)"  # Reemplazar con la URL correcta
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

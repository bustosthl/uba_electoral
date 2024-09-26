import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd, numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from streamlit_javascript import st_javascript
from funciones.carga_datos import cargar_textos, cargar_datos_electorales
from funciones.graficos import grafico_participacion, grafico_votos_porcentuales, grafico_consejeros
import global_vars

# tarjeta para métricas
def metric_display(etiqueta, valor):
    st.markdown(f"""
        <div style="
            border: 2px solid {pcolor};
            padding: 10px;
            border-radius: 10px;
            background-color: {pcolor};
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            width: 90%;
            max-width: 300px;
            margin: 10px auto;
        ">
            <h1 style="margin-bottom: 0em; font-size: 3rem;">{valor}</h1>
            <h2 style="margin-top: 0em; font-size: 1.5rem;">{etiqueta}</h2>
        </div>
    """, unsafe_allow_html=True)



# Función para mostrar análisis por facultad
def mostrar_pagina(facultad):
    textos = cargar_textos()
    datos_electorales = cargar_datos_electorales()

    texto_facultad = textos[textos['Facultad'] == facultad]

    st.title(f"{facultad}")
    sub_divider = 'gray'

    if facultad in ["Odontología"]:
        pass
    else:
        st.subheader("Participación", divider=sub_divider)
        st.markdown(f"""<div style="text-align: justify;">{texto_facultad['Texto Participación'].values[0]}</div>""", unsafe_allow_html=True)
        grafico_participacion(datos_electorales, facultad)

    st.subheader("Votos válidos", divider=sub_divider)
    st.markdown(f"""<div style="text-align: justify;">{texto_facultad['Texto Votos Porcentuales'].values[0]}</div>""", unsafe_allow_html=True)

    grafico_votos_porcentuales(datos_electorales, facultad)

    st.subheader("Consejo Directivo", divider=sub_divider)
    st.markdown(f"""<div style="text-align: justify;">{texto_facultad['Texto Consejeros'].values[0]}</div>""", unsafe_allow_html=True)
    grafico_consejeros(datos_electorales, facultad)

# CSS y personalización
st.set_page_config(page_title='Resultados electorales UBA', 
                   #page_icon="chart_with_upwards_trend",
                   page_icon='img/favicon.png',
                   # layout='wide'
                   )

ruta_logo_ext = 'img/uba_electoral.png'


st.markdown("""
    <style>
        ::selection {
            background-color: #80ED99; /* Color de fondo al resaltar */
            color: #303030; /* Color del texto al resaltar */
        }

        /* Para Firefox */
        ::-moz-selection {
            background-color: #80ED99;
            color: #303030;
        }

        /* Estilos específicos para las opciones del menú */
        .nav-link {
            color: #FFFFFF !important;  /* Color de texto por defecto */
        }
        .nav-link:hover {
            background-color: #80ED99 !important;  /* Color de fondo al pasar el mouse */
            color: #303030 !important;  /* Color de texto al pasar el mouse */
        }
        .nav-link-selected {
            background-color: #80ED99 !important;  /* Color de fondo cuando está seleccionada */
            color: #303030 !important;  /* Color del texto cuando está seleccionada */
        }
            
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        /* Cambiar el fondo de las opciones */
        div[data-baseweb="select"] .css-26l3qy-menu {
            background-color: #80ED99 !important;  /* Fondo verde para las opciones */
        }
        /* Cambiar el color del texto en las opciones */
        div[data-baseweb="select"] .css-26l3qy-option {
            color: black !important;  /* Texto negro para las opciones */
        }
        /* Cambiar el fondo y el color del texto de la opción seleccionada */
        div[data-baseweb="select"] .css-26l3qy-option:active {
            background-color: #80ED99 !important;
            color: black !important;
        }
    </style>
""", unsafe_allow_html=True)

fontuse = """
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap');

html, body, div, h1, h2, h3, h4, h5, h6, span, p, li, a, button,code,pre {    
font-family: 'Inter', sans-serif;
}
"""
st.markdown(f'<style>{fontuse}</style>', unsafe_allow_html=True )

pcolor = st.get_option('theme.primaryColor')
bcolor = st.get_option('theme.backgroundColor')
sbcolor = st.get_option('theme.secondaryBackgroundColor')
text_st_color = 'green'
st.image(ruta_logo_ext)
st.logo('img/uba_electoral_logo.png')
width_logos = 50
# Crear el menú superior horizontal
opcion_principal = option_menu(
    menu_title=None,  # Ocultar título de menú
    options=["Inicio", "Análisis por Facultad", "Exploración de Datos"],
    icons=["house", "bar-chart-line", "database"],  # Iconos de las opciones
    menu_icon="cast",  # Icono del menú principal
    default_index=0,  # Seleccionar la primera opción por defecto
    orientation="horizontal",  # Esto hace que el menú sea horizontal
    #styles={"nav-link":{"--hover-color":"#ce1428"}}
    styles={
        "container": {"padding": "10!important", "background-color": sbcolor},
        "nav-link": {
            "font-size": "18px",
            "text-align": "center",
            "margin": "0px",
            "color": "#FFFFFF",  # Color del texto por defecto
            "--hover-color": pcolor,  # Color de fondo al pasar el mouse
        },
        "nav-link-selected": {
            "background-color": pcolor,  # Color de fondo cuando está seleccionada
            "color": bcolor,  # Color del texto cuando está seleccionada
        },
    }
)
# Si se selecciona "Presentación"
if opcion_principal == "Inicio":
    st.title("Análisis de datos electorales")
    st.header(f":{text_st_color}[UBA]")
    
    st.markdown("""
             <div style="text-align: justify;">
             ¡Bienvenidx! Aquí encontrarás un somero análisis de las elecciones en las distintas facultades de la Universidad de
             Buenos Aires. Además, vas a poder explorar los datos con mayor libertad y descargar lo que creas conveniente. 
              </div>
             """, unsafe_allow_html=True)
    
    datos_electorales = cargar_datos_electorales()
    st.divider()

    #st.write('¿Qué vas a encontrar acá?')
    metric_label = 'etiqueta'
    metric_value = 'valor'

    col1, col2, col3 = st.columns(3)
    with col1:
        #metric_display("Elecciones",datos_electorales['Año'].nunique())
        st.metric("Elecciones",datos_electorales['Año'].nunique())
    with col2:
        #metric_display("Facultades",datos_electorales['Facultad'].nunique())
        st.metric("Facultades",datos_electorales['Facultad'].nunique())
    with col3:
        #metric_display("Listas",datos_electorales['Nombre Lista'].nunique())
        st.metric("Listas",datos_electorales['Nombre Lista'].nunique())
    st.divider()

    col1, col2 = st.columns([1,12])
    with col1:
        st.image('img/icon_como.svg', width=width_logos)
    with col2:
        st.subheader(f':{text_st_color}[¿Cómo se utiliza?]')
    if global_vars.isMobile:
        st.warning("""La app está mejor preparada para ser utilizada desde una computadora. 
                    Si estás desde un dispositivo móvil, te recomendamos girar la pantalla cuando 
                    llegues a la parte de los gráficos :)""", icon="⚠️")
    st.markdown("""
            <div style="text-align: justify;">
            Vas a encontrar dos secciones fundamentales: en <b>Análisis por Facultad</b> vas a poder seleccionar la institución de tu interés
            y ver la evolución de los principales resultados de las elecciones a Consejo Directivo en el claustro de estudiantes. La sección se 
            organiza con un primer apartado con la evolución del total de votos; un segundo apartado con el porcentaje de votos válidos obtenidos
            por cada lista y, por último, la cantidad de bancas obtenidas en cada año. ¡Presioná en la leyenda de cada lista para que aparezca (o no) en el gráfico!
            En la segunda sección, <b>Exploración de Datos</b> vas a poder filtrar la base de datos a tu gusto; está disponible para ver en 
            formato de tabla o con un gráfico de líneas. Al final vas a encontrar un <b>botón para descargar los resultados</b> :)
            </div>
            """, unsafe_allow_html=True)
    st.divider()
    
    col1, col2 = st.columns([1,8])
    with col1:
        st.image('img/icon_porque.svg', width=width_logos)
    with col2:
        st.subheader(f':{text_st_color}[¿Por qué una página de resultados electorales?]')
    st.markdown("""
            <div style="text-align: justify;">
            Las elecciones son el momento democrático por excelencia. La Universidad de Buenos Aires se muestra particularmente efervescente 
            durante los procesos electorales y, sin embargo, no posee sus resultados accesibles y al alcance de cualquier persona de la comunidad educativa.
            Quizás por su naturaleza descentralizada, la información se publica en formatos y lugares disímiles en cada una de las casas de estudio. Por eso
            realizamos este esfuerzo: <b>concentrar y disponibilizar la síntesis del ejercicio ciudadano universitario</b>.  
            
            </div>
                """, unsafe_allow_html=True)
    st.divider()
    col1, col2 = st.columns([1,8])
    with col1:
        st.image('img/icon_quienes.svg', width=width_logos)
    with col2:
        st.subheader(f':{text_st_color}[¿Quiénes somos?]')
    st.markdown("""
                <div style="text-align: justify;">
                Somos un grupo de estudiantes y graduados interesados en la democracia universitaria, en los datos accesibles y en convidar el análisis fundamentado a
                cualquier persona interesada. Participaron de este desarrollo: 

                -  Persona1
                -  Persona2
                -  Persona3
                </div>
                """, unsafe_allow_html=True)      
    st.image(ruta_logo_ext)
    

# Si se selecciona "Análisis por Facultad"
elif opcion_principal == "Análisis por Facultad":
    datos_electorales = cargar_datos_electorales()
    facultades = datos_electorales['Facultad'].unique().tolist()
    
        
    st.title("Resultados electorales")
    st.markdown(f"""<div style="text-align: justify;">
                Seleccioná la facultad de tu interés para ver los resultados a Consejo Directivo de las últimas tres elecciones.
                No siempre está accesible la cantidad absoluta de votos, pero estamos trabajando para que disponibilizarla
                en todos los años para todas las facultades.
                </div>""", unsafe_allow_html=True)
    st.markdown('')
    facultad_seleccionada = st.selectbox("Selecciona una facultad", ['General'] + facultades)
    if facultad_seleccionada=="General":
        anio = st.radio("",datos_electorales['Año'].sort_values(ascending=False).unique(), horizontal=True)
        datos_electorales_gral = (datos_electorales[datos_electorales['Año']==anio]
                                  .sort_values(['Facultad','Votos'], ascending=False)
                                  .drop_duplicates(subset=['Facultad','Año'])
                                  .sort_values('%', ascending=False))
        zipped = zip(datos_electorales_gral['Facultad'], datos_electorales_gral['Nombre Lista'], 
        datos_electorales_gral['Votos'], datos_electorales_gral['%'])

        st.title('Listas ganadoras en el 2024')
        for facultad, lista, votos, porcentaje in zipped:
            st.header(f':{text_st_color}[{facultad}]', divider=False)
            col2, col3, col4 = st.columns([4,1,1])
            col2.metric("Lista", lista)
            try:
                col3.metric("Votos", int(votos))
            except:
                pass
            col4.metric("%", round(porcentaje,1))
            st.divider()
            
    else:
        mostrar_pagina(facultad_seleccionada)

# Si se selecciona "Exploración de Datos"
elif opcion_principal == "Exploración de Datos":
    st.title("Exploración de Datos")
    st.markdown(f"""<div style="text-align: justify;">
                Acá vas a poder explorar libremente los datos electorales, para la facultad y año que desees. 
                En la mayoría de los casos vas a poder ver cantidad absoluta de votos. Más abajo vas a tener disponible
                una visualización gráfica de las listas, la tabla resultante y, al final de este mismo apartado, 
                <b>un botón para descargar en CSV los resultados que estés mirando</b>. 
                </div>""", unsafe_allow_html=True)
    datos_electorales = cargar_datos_electorales()
    facultades = datos_electorales['Facultad'].unique().tolist()
    min_año, max_año = datos_electorales['Año'].min(),datos_electorales['Año'].max()
    valores = ['Votos', '%']

    col1, col2, col3 = st.columns(3)
    with col1:
        facultad_seleccionada = st.multiselect("Facultad", facultades, default=facultades[:2],  placeholder="elegí una opción")
    with col2:
        año_seleccionado = st.slider("Año", min_año, max_año, (min_año, max_año))
    with col3:
        valor_seleccionado = st.selectbox("Valor a ver", valores)

    filtro = (datos_electorales['Facultad'].isin(facultad_seleccionada))
    filtro &= (datos_electorales['Año'] >= año_seleccionado[0]) & (datos_electorales['Año'] <= año_seleccionado[1])
    
    df_filtrado = datos_electorales[filtro]
    
    if facultad_seleccionada:
        df_pivot = (df_filtrado
                    .pivot_table(index=['Año','nombre_clean','color'], values=valor_seleccionado, aggfunc='sum')
                    .reset_index()
                    .sort_values(['Año',valor_seleccionado], ascending=False))
        
        fig = px.line(df_pivot, x='Año', y=valor_seleccionado, color='nombre_clean', text='nombre_clean',
                title=f'Explorador gráfico de resultados electorales',
                markers=True, labels={'Año': 'Año', 'nombre_clean': 'Lista'})

        for lista in df_pivot['nombre_clean'].unique():
            color = df_pivot[df_pivot['nombre_clean'] == lista]['color'].values[0]
            fig.for_each_trace(
                lambda trace: trace.update(line_color=color, textfont=dict(color=color, size=1)) if trace.name == lista else ()
                )
        fig.update_traces(marker=dict(size=10))
        fig.update_traces(
        hovertemplate='<b>Lista</b>: %{text}<br>' +
                      '<b>Año</b>: %{x}<br>' +
                      '<b>Porcentaje de Votos</b>: %{y:,}<extra></extra>',
                      textfont=dict(size=1))
        showlegend=True
        if global_vars.isMobile:
            showlegend=False
        fig.update_layout(
            showlegend=showlegend,  # Ocultar la leyenda 
            margin=dict(r=0),  # Ajustar margen
        )
        st.markdown("")
        col0, col1, col2,_ = st.columns([1,1,1,3])
        with col0:
            st.text("Referencias: ")
        with col1:
            if st.button("mostrar"):
                fig.update_layout(showlegend=True)
        with col2:
            if st.button("ocultar"):
                fig.update_layout(showlegend=False)
        st.plotly_chart(fig)

    dic = {"%": "{:.2f}".format,"Votos":"{:.0f}".format,
           "Año":"{:.0f}".format,"Bancas":"{:.0f}".format}
    cols_drop=['color','filtrar','nombre_clean']
    st.dataframe(df_filtrado.drop(columns=cols_drop).style.format(dic), hide_index=True)
    # Función para convertir a CSV
    @st.cache_data
    def convertir_a_csv(df):
        return df.to_csv(index=True).encode('utf-8')
    csv_long = convertir_a_csv(df_filtrado.drop(columns=cols_drop))
    st.subheader("Descargar datos")
    descarga = st.download_button(label="Presiona para descargar", data=csv_long,
                       file_name='datos_filtrados.csv',mime='text/csv')
    
    if descarga:
        st.balloons()


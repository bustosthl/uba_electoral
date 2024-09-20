import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from streamlit_javascript import st_javascript

# Cargar los textos de análisis desde el archivo Excel
def cargar_textos():
    textos = pd.read_excel("textos_analisis.xlsx")
    return textos

# Simulación de un dataframe con los datos electorales por facultad
def cargar_datos_electorales():
    datos = pd.read_excel('uba_cd_estudiantes.xlsx', sheet_name='base')
    return datos

# Graficar funciones
def grafico_participacion(df, facultad):
    df = df[df['Facultad'] == facultad]
    df = df.pivot_table(index='Año', values='Votos', aggfunc='sum').reset_index()
    # Crear el gráfico de líneas con Plotly
    fig = px.line(df, x='Año', y='Votos', 
              title=f'Votos totales en {facultad}', 
              markers=True, 
              labels={'Votos': 'Cantidad de Votos', 'Año': ''})
    
    fig.update_traces(line=dict(color=color_linea, shape='spline'), marker=dict(size=12), text=df['Votos'])
    fig.update_traces(mode="lines+markers+text", textposition="top center")
    fig.update_yaxes(range=[0, df['Votos'].max()*1.2])
    st.plotly_chart(fig)

def grafico_votos_porcentuales(df, facultad, y='%'):

    df = df[df['Facultad'] == facultad]
    df = (df.pivot_table(index=['Año','nombre_clean','color'], values=y, aggfunc='sum')
          .reset_index()
          .sort_values(['Año',y], ascending=False)
          )
    
    fig = px.line(df, x='Año', y=y, color='nombre_clean',
              title=f'% de votos válidos por lista en {facultad}',
              markers=True, labels={y: 'Porcentaje de Votos', 'Año': 'Año', 'nombre_clean': 'Lista'})
    #fig.update_yaxes(range=[0, 100])
    for lista in df['nombre_clean'].unique():
        color = df[df['nombre_clean'] == lista]['color'].values[0]
        fig.for_each_trace(
            lambda trace: trace.update(line_color=color) if trace.name == lista else ()
            )
    fig.update_traces(marker=dict(size=10))
    fig.update_xaxes(title_text=None)

    fig.update_layout(
        showlegend=True,  # Ocultar la leyenda por defecto
        margin=dict(r=0),  # Ajustar margen
    )
    st.markdown("")
    col0, col1, col2,_ = st.columns([1,1,1,3])
    with col0:
        st.markdown("Leyenda: ")
    with col1:
        if st.button("mostrar"):
            fig.update_layout(showlegend=True)
    with col2:
        if st.button("ocultar"):
            fig.update_layout(showlegend=False)
    st.plotly_chart(fig)


def grafico_consejeros_apiladas(df, facultad):
    df = df[df['Facultad'] == facultad].dropna(subset=['Bancas'])

    fig = px.bar(df, x='Año', y='Bancas', color='nombre_clean',
                 title=f'Bancas obtenidas por lista en {facultad}',
             labels={'Bancas': 'Cantidad de bancas', 'Año': 'Año', 'nombre_clean': 'Lista'},
             text='Bancas')  # Muestra el número de consejeros en la barra
    
    for lista in df['nombre_clean'].unique():
        color = df[df['nombre_clean'] == lista]['color'].values[0]
        fig.for_each_trace(
            lambda trace: trace.update(marker_color=color) if trace.name == lista else ()
        )
    fig.update_xaxes(type='category', categoryorder='array', categoryarray=df['Año'].sort_values().unique())
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
                      legend_title=dict(text="Lista", side="left"))
    st.plotly_chart(fig)

def grafico_consejeros(df, facultad):
    # Filtrar los datos por facultad y eliminar filas sin bancas
    df = df[df['Facultad'] == facultad].dropna(subset=['Bancas'])
    
    # Expandir las filas según la cantidad de bancas
    df_expanded = df.loc[df.index.repeat(df['Bancas'])].copy().sort_values('nombre_clean')

    # Asignar la posición de la banca (1, 2, 3, 4) dentro de cada año
    df_expanded['Posicion Banca'] = df_expanded.groupby(['Año']).cumcount() + 1
    
    # Crear el gráfico de puntos (scatter plot) con puntos más grandes
    fig = px.scatter(df_expanded, x='Año', y='Posicion Banca', color='nombre_clean',
                     title=f'Bancas obtenidas por lista en {facultad}',
                     labels={'Posicion Banca': 'Bancas', 'Año': 'Año', 'nombre_clean': 'Lista'},
                     hover_data=['Bancas'],
                     size_max=40)  # Aumentar el tamaño máximo de los puntos

    # Asignar colores según la lista
    for lista in df_expanded['nombre_clean'].unique():
        color = df_expanded[df_expanded['nombre_clean'] == lista]['color'].values[0]
        fig.for_each_trace(
            lambda trace: trace.update(marker_color=color, marker=dict(size=40)) if trace.name == lista else ()
        )
    
    # Configuración del eje x para mostrar los años en orden
    fig.update_xaxes(type='category', categoryorder='array', categoryarray=df_expanded['Año'].sort_values().unique())
    #fig.update_traces(marker=dict(size=40, symbol='square'))
    # Eliminar la cuadrícula, ticks y el eje Y
    fig.update_yaxes(showgrid=False, zeroline=False, showline=False, showticklabels=False)
    
    # Ajustar el diseño de la leyenda y desactivar la interacción del mouse (zoom)
    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        legend_title=dict(text="Lista", side="left"),
        yaxis=dict(tickvals=[1, 2, 3, 4]),
        xaxis=dict(showgrid=False),  # Eliminar la cuadrícula del eje X
        dragmode=False,  # Desactivar el modo de arrastre (sin zoom)
        hovermode="closest",  # Mantener el hover de la información
        plot_bgcolor=None,  # Quitar el fondo blanco, usar el fondo predeterminado
    )

    # Desactivar zoom con el mouse, pero mantener los botones de descarga
    fig.update_layout(
        modebar_remove=['zoom', 'zoomIn', 'zoomOut', 'autoScale', 'lasso2d', 'select2d','pan'],
        modebar_add=['resetScale2d']
    )
    fig.update_xaxes(title_text=None)
    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)

# Función para mostrar análisis por facultad
def mostrar_pagina(facultad):
    textos = cargar_textos()
    datos_electorales = cargar_datos_electorales()
    
    texto_facultad = textos[textos['Facultad'] == facultad]

    st.title(f"Resultados Electorales: {facultad}")

    st.subheader("Participación", divider='rainbow')
    st.markdown(f"""<div style="text-align: justify;">{texto_facultad['Texto Participación'].values[0]}</div>""", unsafe_allow_html=True)
    grafico_participacion(datos_electorales, facultad)

    st.subheader("Votos válidos", divider='rainbow')
    st.markdown(f"""<div style="text-align: justify;">{texto_facultad['Texto Votos Porcentuales'].values[0]}</div>""", unsafe_allow_html=True)

    grafico_votos_porcentuales(datos_electorales, facultad)

    st.subheader("Consejo Directivo", divider='rainbow')
    st.markdown(f"""<div style="text-align: justify;">{texto_facultad['Texto Consejeros'].values[0]}</div>""", unsafe_allow_html=True)
    grafico_consejeros(datos_electorales, facultad)

# CSS y personalización
st.set_page_config(page_title='Resultados electorales UBA', 
                   page_icon="chart_with_upwards_trend",
                   # layout='wide'
                   )

st_theme = st_javascript("""window.getComputedStyle(window.parent.document.getElementsByClassName("stApp")[0]).getPropertyValue("color-scheme")""")
if st_theme == "dark":
    color_linea = 'white'
else:
    color_linea = 'black'

def get_device_type():
    user_agent = st.experimental_user  # Obtener el User-Agent
    if any(mobile in user_agent for mobile in ['iPhone', 'Android', 'webOS', 'BlackBerry', 'iPad']):
        return 'mobile'
    else:
        return 'desktop'

# Determinar el tipo de dispositivo
device_type = get_device_type()

# Guardar el resultado en session_state para su uso posterior
st.session_state["device_type"] = device_type

st.write(st.session_state['device_type'])
# Crear el menú superior horizontal
opcion_principal = option_menu(
    menu_title=None,  # Ocultar título de menú
    options=["Inicio", "Análisis por Facultad", "Exploración de Datos"],
    icons=["house", "bar-chart-line", "database"],  # Iconos de las opciones
    menu_icon="cast",  # Icono del menú principal
    default_index=0,  # Seleccionar la primera opción por defecto
    orientation="horizontal"  # Esto hace que el menú sea horizontal
)

# Si se selecciona "Presentación"
if opcion_principal == "Inicio":
    st.title("Análisis de datos electorales - UBA")
    st.markdown("""
             <div style="text-align: justify;">
             ¡Bienvenidx! Aquí encontrarás un somero análisis de las elecciones en las distintas facultades de la Universidad de
             Buenos Aires. Además, vas a poder explorar los datos con mayor libertad y descargar lo que creas conveniente. 
              </div>
             """, unsafe_allow_html=True)
    
    datos_electorales = cargar_datos_electorales()
    st.divider()
    st.write('¿Qué vas a encontrar acá?')

    col1, col2, col3 = st.columns(3)
    col1.metric("Elecciones",  datos_electorales['Año'].nunique(), 1)
    col2.metric("Facultades", datos_electorales['Facultad'].nunique(),4)
    col3.metric("Listas", datos_electorales['Nombre Lista'].nunique(), "20%")
    st.divider()

    st.subheader('¿Cómo se utiliza?')
    st.markdown("""
            <div style="text-align: justify;">
            Vas a encontrar dos secciones fundamentales: en <b>Análisis por Facultad</b> vas a poder seleccionar la institución de tu interés
            y ver la evolución de los principales resultados de las elecciones a Consejo Directivo en el claustro de estudiantes. La sección se 
            organiza con un primer apartado con la evolución del total de votos; un segundo apartado con el porcentaje de votos válidos obtenidos
            por cada lista y, por último, la cantidad de bancas obtenidas en cada año. ¡Presioná en la leyenda de cada lista para que aparezca (o no) en el gráfico!
            En la segunda sección, <b>Exploración de Datos</b> vas a poder filtrar la base de datos a tu gusto; está disponible para ver en 
            formato de tabla o con un gráfico de líneas. Al final vas a encontrar un botón para descargar los resultados :)
            </div>
            """, unsafe_allow_html=True)
    st.divider()
    st.subheader('¿Por qué una página de resultados electorales UBA?')
    st.markdown("""
            <div style="text-align: justify;">
            Las elecciones son el momento democrático por excelencia. La Universidad de Buenos Aires se muestra particularmente efervescente 
            durante los procesos electorales y, sin embargo, no posee sus resultados accesibles y al alcance de cualquier persona de la comunidad educativa.
            Quizás por su naturaleza descentralizada, la información se publica el formatos y lugares disímiles en cada una de las casas de estudio. Por eso
            realizamos este esfuerzo: <b>concentrar y disponibilizar la síntesis del ejercicio ciudadano universitario</b>.  
            
            </div>
                """, unsafe_allow_html=True)
    st.divider()
    st.subheader('¿Quiénes somos?')
    st.markdown("""
                <div style="text-align: justify;">
                Somos un grupo de estudiantes y graduados interesados en la democracia universitaria, en los datos accesibles y en convidar el análisis fundamentado a
                cualquier persona interesada. Participaron de este desarrollo: 

                -  Persona1
                -  Persona2
                -  Persona3
                </div>
                """, unsafe_allow_html=True)      
# Si se selecciona "Análisis por Facultad"
elif opcion_principal == "Análisis por Facultad":
    datos_electorales = cargar_datos_electorales()
    facultades = datos_electorales['Facultad'].unique()
    
    facultad_seleccionada = st.selectbox("Selecciona una facultad", facultades)
    mostrar_pagina(facultad_seleccionada)

# Si se selecciona "Exploración de Datos"
elif opcion_principal == "Exploración de Datos":
    st.title("Exploración de Datos")
    st.write("Aquí puedes explorar libremente los datos electorales.")
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
        
        fig = px.line(df_pivot, x='Año', y=valor_seleccionado, color='nombre_clean',
                title=f'Explorador gráfico de resultados electorales',
                markers=True, labels={'Año': 'Año', 'nombre_clean': 'Lista'})

        for lista in df_pivot['nombre_clean'].unique():
            color = df_pivot[df_pivot['nombre_clean'] == lista]['color'].values[0]
            fig.for_each_trace(
                lambda trace: trace.update(line_color=color) if trace.name == lista else ()
                )
        fig.update_traces(marker=dict(size=10))
        st.plotly_chart(fig)

    st.write(df_filtrado.drop(columns=['color']))
    # Función para convertir a CSV
    @st.cache_data
    def convertir_a_csv(df):
        return df.to_csv(index=True).encode('utf-8')
    csv_long = convertir_a_csv(df_filtrado.drop(columns=['color']))
    st.subheader("Descargar datos")
    st.download_button(label="Presiona para descargar", data=csv_long,file_name='datos_filtrados.csv',mime='text/csv')

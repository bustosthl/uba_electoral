import streamlit as st
import plotly.express as px
import pandas as pd, numpy as np
import global_vars


# Graficar funciones
def grafico_participacion(df, facultad):
    df = df[df['Facultad'] == facultad]
    df = df.pivot_table(index='Año', values='Votos', aggfunc='sum').reset_index().replace(0,np.nan).dropna()
    
    if len(df)==0:
        pass
    else:
        # Crear el gráfico de líneas con Plotly
        fig = px.bar(df, x='Año', y='Votos', 
                title=f'Votos totales en {facultad}', 
               # markers=True, 
                labels={'Votos': 'Cantidad de Votos', 'Año': ''})
        
        fig.update_traces(text=df['Votos'], width=0.4,
                          #marker_color=global_vars.color_linea, 
                          marker_color = global_vars.pcolor,
                          textfont=dict(size=18), textposition='outside')
        fig.update_xaxes(type='category', categoryorder='array', categoryarray=df['Año'].sort_values().unique())
#fig.update_traces(line=dict(color=global_vars.color_linea, shape='spline'), marker=dict(size=12), text=df['Votos'])
        #fig.update_traces(mode="lines+markers+text", textposition="top center")
        fig.update_yaxes(range=[0, df['Votos'].max()*1.2])
        fig.update_traces(
            hovertemplate='<b>Año</b>: %{x}<br>' +
                        '<b>Votoss</b>: %{y:,}<extra></extra>'
        )
        fig.update_layout(
            modebar_remove=['zoom', 'zoomIn', 'zoomOut', 'autoScale', 'lasso2d', 'select2d','pan'],
            modebar_add=['resetScale2d'],
            dragmode=False,  # Desactivar el modo de arrastre (sin zoom)
            )
        st.plotly_chart(fig)
        
def grafico_participacion_lineas(df, facultad):
    df = df[df['Facultad'] == facultad]
    df = df.pivot_table(index='Año', values='Votos', aggfunc='sum').reset_index().replace(0,np.nan).dropna()
    
    if len(df)==0:
        pass
    else:
        # Crear el gráfico de líneas con Plotly
        fig = px.line(df, x='Año', y='Votos', 
                title=f'Votos totales en {facultad}', 
                markers=True, 
                labels={'Votos': 'Cantidad de Votos', 'Año': ''})
        
        fig.update_traces(line=dict(color=global_vars.color_linea, shape='spline'), marker=dict(size=12), text=df['Votos'])
        fig.update_traces(mode="lines+markers+text", textposition="top center")
        fig.update_yaxes(range=[0, df['Votos'].max()*1.2])
        fig.update_traces(
            hovertemplate='<b>Año</b>: %{x}<br>' +
                        '<b>Votoss</b>: %{y:,}<extra></extra>'
        )
        fig.update_layout(
            modebar_remove=['zoom', 'zoomIn', 'zoomOut', 'autoScale', 'lasso2d', 'select2d','pan'],
            modebar_add=['resetScale2d'],
            dragmode=False,  # Desactivar el modo de arrastre (sin zoom)
            )
        st.plotly_chart(fig)

def grafico_votos_porcentuales(df, facultad, isMobile, y='%',):
    df = df[df['Facultad'] == facultad]
    df = (df.pivot_table(index=['Año','nombre_clean','color'], values=y, aggfunc='sum')
          .reset_index()
          .sort_values(['Año',y], ascending=False)
          )

    fig = px.line(df, x='Año', y=y, color='nombre_clean',text='nombre_clean',
              title=f'% de votos válidos por lista en {facultad}',
              markers=True, 
              labels={y: 'Porcentaje de Votos', 'Año': 'Año', 'nombre_clean': 'Lista'})
    #fig.update_yaxes(range=[0, 100])
    for lista in df['nombre_clean'].unique():
        color = df[df['nombre_clean'] == lista]['color'].values[0]
        fig.for_each_trace(
            lambda trace: trace.update(line_color=color, textfont=dict(color=color, size=1)) if trace.name == lista else ()
            )
    fig.update_traces(marker=dict(size=10), textfont=dict(size=1), line=dict(shape='spline'))
    fig.update_xaxes(type='category', categoryorder='array', categoryarray=df['Año'].sort_values().unique())
    fig.update_xaxes(title_text=None)
    # Personalizar el tooltip
    fig.update_traces(
        hovertemplate='<b>Lista</b>: %{text}<br>' +
                      '<b>Año</b>: %{x}<br>' +
                      '<b>Porcentaje de Votos</b>: %{y:,}<extra></extra>'
    )
    showlegend=True
    if isMobile:
        showlegend=False
    fig.update_layout(
        showlegend=showlegend,  # Ocultar la leyenda 
        margin=dict(r=0),  # Ajustar margen
    )
    fig.update_layout(
        modebar_remove=['zoom', 'zoomIn', 'zoomOut', 'autoScale', 'lasso2d', 'select2d','pan'],
        modebar_add=['resetScale2d'],
        dragmode=False,  # Desactivar el modo de arrastre (sin zoom)

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
                     text='nombre_clean',
                     size_max=40)  # Aumentar el tamaño máximo de los puntos

    # Asignar colores según la lista
    for lista in df_expanded['nombre_clean'].unique():
        color = df_expanded[df_expanded['nombre_clean'] == lista]['color'].values[0]
        fig.for_each_trace(
            lambda trace: trace.update(marker_color=color, marker=dict(size=40), textfont=dict(color=color, size=1)) if trace.name == lista else ()
        )
    
    # Configuración del eje x para mostrar los años en orden
    fig.update_xaxes(type='category', categoryorder='array', categoryarray=df_expanded['Año'].sort_values().unique())
    fig.update_traces(marker=dict(size=40, symbol='circle')) # https://plotly.com/python/marker-style/#:~:text=The%20basic%20symbols%20are%3A%20circle,open%22%20to%20a%20symbol%20name.
    # Eliminar la cuadrícula, ticks y el eje Y
    fig.update_yaxes(showgrid=False, zeroline=False, showline=False, showticklabels=False)
    fig.update_traces(
        hovertemplate='<b>Lista</b>: %{text}<br>' +
                      '<b>Año</b>: %{x}<br>' +
                      '<b>Porcentaje de Votos</b>: %{y:,}<extra></extra>'
    , textfont=dict(size=1))
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
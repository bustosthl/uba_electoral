import pandas as pd

# Cargar los textos de análisis desde el archivo Excel
def cargar_textos():
    textos = pd.read_excel("textos_analisis.xlsx")
    return textos

# Simulación de un dataframe con los datos electorales por facultad
def cargar_datos_electorales():
    datos = pd.read_excel('uba_cd_estudiantes.xlsx', sheet_name='base')
    return datos
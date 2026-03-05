import pandas as pd

def obtener_datos():

    url = "https://docs.google.com/spreadsheets/d/1AzTSYjoZFs-d3VToTWf1tgju_mVJOkfU/export?format=csv"

    df = pd.read_csv(url)

    return df
# API.py

# ---- IMPORTACIONES ----
import requests
import pandas as pd


# ---- FUNCION QUE YA TENIAS (Google Sheets) ----
def obtener_datos_sheets():
    # tu código existente
    pass


# ---- NUEVA FUNCION DE VALUACION ----
def calcular_valor_terreno(ofertas, terreno_sujeto, construccion_sujeto, valor_m2_valuador):

    valores_m2_terreno = []
    valores_m2_construccion = []
    valores_negociados = []

    for oferta in ofertas:

        terreno = oferta["terreno"]
        construccion = oferta["construccion"]
        precio = oferta["precio"]
        negociacion = oferta["negociacion"]
        precio_m2_const = oferta["precio_m2_const"]

        valor_negociado = precio * (1 - negociacion)

        valor_construccion = construccion * precio_m2_const
        valor_terreno_total = valor_negociado - valor_construccion
        valor_m2_terreno = valor_terreno_total / terreno

        valores_m2_terreno.append(valor_m2_terreno)
        valores_m2_construccion.append(valor_negociado / construccion)
        valores_negociados.append(valor_negociado)

    promedio_m2_terreno = sum(valores_m2_terreno) / len(valores_m2_terreno)
    promedio_m2_construccion = sum(valores_m2_construccion) / len(valores_m2_construccion)
    promedio_negociacion = sum(valores_negociados) / len(valores_negociados)

    valor_terreno_mercado = promedio_m2_terreno * terreno_sujeto
    valor_terreno_valuador = valor_m2_valuador * terreno_sujeto

    return {
        "promedio_m2_terreno": promedio_m2_terreno,
        "promedio_m2_construccion": promedio_m2_construccion,
        "promedio_negociacion": promedio_negociacion,
        "valor_terreno_mercado": valor_terreno_mercado,
        "valor_terreno_valuador": valor_terreno_valuador
    }

import pandas as pd

def obtener_datos():

    url = "https://docs.google.com/spreadsheets/d/1AzTSYjoZFs-d3VToTWf1tgju_mVJOkfU/export?format=csv"

    df = pd.read_csv(url)

    return df

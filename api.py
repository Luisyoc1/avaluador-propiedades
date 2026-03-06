import requests
import json

class InmobiliariaAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.search_url = "https://google.serper.dev/search"

    def buscar_ofertas(self, colonia):
        # Buscamos específicamente en portales de Guatemala
        query = f"venta casa {colonia} Guatemala terreno construcción metros"
        payload = json.dumps({"q": query})
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", self.search_url, headers=headers, data=payload)
        resultados = response.json()
        
        # Aquí procesamos los resultados (esto es una simulación de extracción)
        ofertas_encontradas = []
        for item in resultados.get('organic', [])[:3]: # Traemos las primeras 3
            ofertas_encontradas.append({
                "fuente": item.get('link'),
                "titulo": item.get('title'),
                "snippet": item.get('snippet')
            })
        return ofertas_encontradas

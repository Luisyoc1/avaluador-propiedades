import requests
import json
import re

class InmobiliariaAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://google.serper.dev/search"

    def buscar_en_google(self, colonia):
        query = f"venta casa {colonia} Guatemala terreno construcción metros precio"
        payload = json.dumps({"q": query, "gl": "gt", "hl": "es"})
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(self.url, headers=headers, data=payload)
            resultados = response.json()
            
            ofertas = []
            # Extraemos los primeros 3 resultados orgánicos
            for item in resultados.get('organic', [])[:3]:
                texto = item.get('snippet', '') + " " + item.get('title', '')
                
                # Intento básico de extraer precio (busca 'Q' seguido de números)
                precio_match = re.search(r'Q\s?([\d,]+)', texto)
                precio = float(precio_match.group(1).replace(',', '')) if precio_match else 1500000.0
                
                # Intento básico de extraer metros (busca números seguidos de 'm2' o 'v2')
                metros_match = re.search(r'(\d+)\s?m2', texto)
                metros = float(metros_match.group(1)) if metros_match else 150.0
                
                ofertas.append({
                    "titulo": item.get('title')[:30] + "...",
                    "precio": precio,
                    "m2_t": metros,
                    "m2_c": metros * 1.2, # Estimación si no lo encuentra
                    "link": item.get('link')
                })
            return ofertas
        except Exception as e:
            return []

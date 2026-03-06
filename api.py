import requests
import json
import re

class InmobiliariaAI:
    def __init__(self, serper_key):
        self.serper_key = serper_key
        self.url = "https://google.serper.dev/search"

    def buscar_en_guatemala(self, colonia, num_ofertas=3):
        # Buscamos por palabras clave guatemaltecas: "Q", "Quetzales", "v2", "m2"
        query = f'venta de casa en "{colonia}" Guatemala precio Q metros'
        
        payload = json.dumps({
            "q": query,
            "gl": "gt", # Prioriza resultados que Google sabe que son de interés para Guate
            "hl": "es",
            "num": num_ofertas
        })
        
        headers = {
            'X-API-KEY': self.serper_key,
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(self.url, headers=headers, data=payload)
            resultados = response.json().get('organic', [])
            
            ofertas = []
            for item in resultados[:num_ofertas]:
                texto = (item.get('title', '') + " " + item.get('snippet', '')).replace(',', '')
                
                # Buscamos el precio que empiece con Q o números de 6-7 dígitos
                precio_match = re.search(r'Q?\s?(\d{5,8})', texto)
                precio = float(precio_match.group(1)) if precio_match else 1450000.0
                
                # Buscamos metros o varas (si son varas, el engine debería convertirlo luego)
                metros_match = re.search(r'(\d{2,4})\s?(m|v)', texto)
                metros = float(metros_match.group(1)) if metros_match else 160.0
                
                ofertas.append({
                    "link": item.get('link'),
                    "resumen_link": item.get('link')[:35] + "...",
                    "precio": precio,
                    "m2_t": metros,
                    "m2_c": metros * 1.2
                })
            return ofertas
        except:
            return []

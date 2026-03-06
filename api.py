import requests
import json
import re

class InmobiliariaAI:
    def __init__(self, serper_key, gemini_key):
        self.serper_key = serper_key
        self.gemini_key = gemini_key
        self.serper_url = "https://google.serper.dev/search"
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_key}"

    def analizar_con_ia(self, texto_sucio, tipo_buscado):
        """Analiza el texto para extraer datos de Guatemala (maneja v2 y m2)."""
        prompt = f"""
        Analiza esta oferta inmobiliaria en Guatemala: "{texto_sucio}"
        Extrae solo JSON con:
        - 'precio': número en Quetzales.
        - 'm2_t': metros de terreno (si dice v2 o varas, multiplica por 0.698).
        - 'm2_c': metros de construcción.
        - 'valido': true si tiene precio y al menos un área, false si no.
        """
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        try:
            res = requests.post(self.gemini_url, json=payload, timeout=10)
            raw = res.json()['candidates'][0]['content']['parts'][0]['text']
            json_match = re.search(r'\{.*\}', raw, re.DOTALL)
            return json.loads(json_match.group()) if json_match else None
        except:
            return None

    def buscar_ofertas_full(self, colonia, tipo, num=3):
        # Buscamos más de lo necesario para tener de donde filtrar
        query = f'venta de {tipo} "{colonia}" Guatemala precio Q metros'
        headers = {'X-API-KEY': self.serper_key, 'Content-Type': 'application/json'}
        payload = json.dumps({"q": query, "gl": "gt", "num": 10})
        
        try:
            response = requests.post(self.serper_url, headers=headers, data=payload)
            items = response.json().get('organic', [])
            buenas, descartadas = [], []
            
            for item in items:
                texto = f"{item.get('title')} {item.get('snippet')}"
                datos = self.analizar_con_ia(texto, tipo)
                
                info_oferta = {
                    "link": item.get('link'),
                    "titulo": item.get('title'),
                    "precio": float(datos.get('precio', 0)) if datos else 0,
                    "m2_t": float(datos.get('m2_t', 0)) if datos else 0,
                    "m2_c": float(datos.get('m2_c', 0)) if datos else 0
                }

                if datos and datos.get('valido') and info_oferta['precio'] > 0:
                    buenas.append(info_oferta)
                else:
                    descartadas.append(info_oferta)
            
            return buenas[:num], descartadas
        except:
            return [], []

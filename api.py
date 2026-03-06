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
        prompt_text = f"""
        Analiza esta oferta: "{texto_sucio}"
        Busca específicamente {tipo_buscado}s en Guatemala.
        Devuelve JSON con: 'precio', 'm2_t' (m2), 'm2_c' (m2).
        Si faltan metros o el tipo no coincide, pon 'incompleto': true.
        """
        payload = {"contents": [{"parts": [{"text": prompt_text}]}]}
        try:
            res = requests.post(self.gemini_url, json=payload, timeout=10)
            raw = res.json()['candidates'][0]['content']['parts'][0]['text']
            json_match = re.search(r'\{.*\}', raw, re.DOTALL)
            return json.loads(json_match.group()) if json_match else None
        except:
            return None

    def buscar_ofertas_full(self, colonia, tipo_propiedad, num=3):
        query = f'venta de {tipo_propiedad} en "{colonia}" Guatemala precio Q'
        headers = {'X-API-KEY': self.serper_key, 'Content-Type': 'application/json'}
        payload = json.dumps({"q": query, "gl": "gt", "num": 10})
        
        try:
            response = requests.post(self.serper_url, headers=headers, data=payload)
            items = response.json().get('organic', [])
            validadas = []
            descartadas = []
            
            for item in items:
                texto = f"{item.get('title')} {item.get('snippet')}"
                datos = self.analizar_con_ia(texto, tipo_propiedad)
                
                if datos and not datos.get('incompleto') and datos.get('precio', 0) > 0:
                    validadas.append({
                        "link": item.get('link'),
                        "precio": float(datos.get('precio', 0)),
                        "m2_t": float(datos.get('m2_t', 0)),
                        "m2_c": float(datos.get('m2_c', 0))
                    })
                else:
                    descartadas.append({"titulo": item.get('title'), "link": item.get('link')})
            
            return validadas[:num], descartadas
        except:
            return [], []

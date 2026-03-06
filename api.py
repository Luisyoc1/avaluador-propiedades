import requests
import json
import re

class InmobiliariaAI:
    def __init__(self, serper_key, gemini_key):
        self.serper_key = serper_key
        self.gemini_key = gemini_key
        self.serper_url = "https://google.serper.dev/search"
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_key}"

    def analizar_con_ia(self, texto_sucio):
        """Usa Gemini para extraer datos técnicos exactos del texto de la oferta."""
        prompt = {
            "contents": [{
                "parts": [{
                    "text": f"""Actúa como un valuador experto en Guatemala. 
                    De este texto de una oferta inmobiliaria, extrae los siguientes datos en formato JSON:
                    - 'precio': solo el número (en Quetzales).
                    - 'm2_t': metros cuadrados de terreno. (Si dice varas o v2, conviértelas multiplicando por 0.698).
                    - 'm2_c': metros cuadrados de construcción.
                    Texto: {texto_sucio}
                    Si no encuentras un dato, pon 0."""
                }]
            }]
        }
        try:
            res = requests.post(self.gemini_url, json=prompt)
            raw_text = res.json()['candidates'][0]['content']['parts'][0]['text']
            # Limpiar el JSON de la respuesta de la IA
            json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
            return json.loads(json_match.group()) if json_match else None
        except:
            return None

    def buscar_ofertas(self, colonia, num=3):
        query = f'venta casa "{colonia}" Guatemala terreno construcción m2 precio'
        headers = {'X-API-KEY': self.serper_key, 'Content-Type': 'application/json'}
        payload = json.dumps({"q": query, "gl": "gt", "num": num})
        
        response = requests.post(self.serper_url, headers=headers, data=payload)
        resultados = response.json().get('organic', [])
        
        ofertas_finales = []
        for item in resultados:
            texto_completo = f"{item.get('title')} {item.get('snippet')}"
            # Llamamos al Analista IA
            datos = self.analizar_con_ia(texto_completo)
            
            if datos:
                ofertas_finales.append({
                    "link": item.get('link'),
                    "precio": float(datos.get('precio', 0)) or 1500000.0,
                    "m2_t": float(datos.get('m2_t', 0)) or 150.0,
                    "m2_c": float(datos.get('m2_c', 0)) or 180.0
                })
        return ofertas_finales

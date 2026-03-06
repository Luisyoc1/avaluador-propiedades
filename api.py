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
        Actúa como perito valuador. Analiza esta oferta: "{texto_sucio}"
        
        REGLAS DE DESCARTE:
        1. Si la oferta es un APARTAMENTO y el usuario busca CASA (o viceversa), devuelve: "DESCARTAR".
        2. Si NO hay metros cuadrados de construcción Y NO hay metros/varas de terreno, devuelve: "DESCARTAR".
        
        REGLAS DE EXTRACCIÓN (Si no se descarta):
        - 'precio': en Quetzales (Tasa $1 = Q7.80).
        - 'm2_t': terreno en m2 (Si son v2, multiplica por 0.698).
        - 'm2_c': construcción en m2.
        
        Devuelve estrictamente un JSON o la palabra "DESCARTAR".
        """
        
        payload = {"contents": [{"parts": [{"text": prompt_text}]}]}
        try:
            res = requests.post(self.gemini_url, json=payload, timeout=10)
            raw = res.json()['candidates'][0]['content']['parts'][0]['text']
            if "DESCARTAR" in raw.upper():
                return "DESCARTAR"
            json_match = re.search(r'\{.*\}', raw, re.DOTALL)
            return json.loads(json_match.group()) if json_match else None
        except:
            return None

    def buscar_ofertas(self, colonia, tipo_propiedad, num=3):
        # Refinamos la búsqueda de Google para ser más precisos
        query = f'venta de {tipo_propiedad} en "{colonia}" Guatemala "m2" precio'
        headers = {'X-API-KEY': self.serper_key, 'Content-Type': 'application/json'}
        payload = json.dumps({"q": query, "gl": "gt", "num": num * 2}) # Buscamos el doble para tener de donde descartar
        
        try:
            response = requests.post(self.serper_url, headers=headers, data=payload)
            items = response.json().get('organic', [])
            ofertas_validadas = []
            
            for item in items:
                if len(ofertas_validadas) >= num: break
                
                texto = f"{item.get('title')} {item.get('snippet')}"
                datos = self.analizar_con_ia(texto, tipo_propiedad)
                
                if datos and datos != "DESCARTAR":
                    ofertas_validadas.append({
                        "link": item.get('link'),
                        "precio": float(datos.get('precio', 0)),
                        "m2_t": float(datos.get('m2_t', 0)),
                        "m2_c": float(datos.get('m2_c', 0))
                    })
            return ofertas_validadas
        except:
            return []

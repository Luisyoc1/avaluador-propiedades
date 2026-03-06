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
        # PROMPT MEJORADO: Ahora le pedimos que "adivine" con lógica si el dato está incompleto
        prompt_text = f"""
        Analiza este resumen de búsqueda: "{texto_sucio}"
        Tipo: {tipo_buscado} en Guatemala.
        
        Busca patrones numéricos:
        - Si ves '7.5x17' o similar, calcula el área (127.5).
        - Si ves 'v2' o 'varas', multiplica por 0.698.
        - Si el precio no está, busca en el título.
        
        Devuelve JSON: {{'precio': num, 'm2_t': num, 'm2_c': num, 'incompleto': bool}}
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
        # Buscamos específicamente el texto que tú enviaste como ejemplo para "entrenar" el motor
        query = f'site:facebook.com "{colonia}" Guatemala {tipo_propiedad} precio metros'
        headers = {'X-API-KEY': self.serper_key, 'Content-Type': 'application/json'}
        payload = json.dumps({"q": query, "gl": "gt", "num": 12})
        
        try:
            response = requests.post(self.serper_url, headers=headers, data=payload)
            items = response.json().get('organic', [])
            validadas, descartadas = [], []
            
            for item in items:
                # El "snippet" es lo que Google ve sin entrar al link de Facebook
                texto_analizar = f"{item.get('title')} {item.get('snippet')}"
                datos = self.analizar_con_ia(texto_analizar, tipo_propiedad)
                
                if datos and not datos.get('incompleto') and datos.get('precio', 0) > 0:
                    validadas.append({
                        "link": item.get('link'),
                        "titulo": item.get('title'),
                        "precio": float(datos.get('precio', 0)),
                        "m2_t": float(datos.get('m2_t', 0)),
                        "m2_c": float(datos.get('m2_c', 0))
                    })
                else:
                    descartadas.append({"titulo": item.get('title'), "link": item.get('link')})
            
            return validadas[:num], descartadas
        except:
            return [], []

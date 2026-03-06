import streamlit as st
import pandas as pd
from engine import ValuadorEngine
from api import InmobiliariaAI

st.set_page_config(page_title="Valuador IA Pro GT", layout="wide")
engine = ValuadorEngine()

# --- CONFIGURACIÓN DE APIS ---
# Reemplaza con tu llave de Gemini (Google AI Studio)
SERPER_KEY = "3b154c2742a1d46402531eb080ee2d12d5f167e4"
GEMINI_KEY = "TU_GEMINI_API_KEY_AQUI" 

api_ia = InmobiliariaAI(SERPER_KEY, GEMINI_KEY)

def f_q(v): return f"Q {v:,.2f}"

# Persistencia de datos
if 'ofert_list' not in st.session_state:
    st.session_state.ofert_list = [{"precio": 0, "m2_t": 0, "m2_c": 0, "link": "Manual"}] * 5
if 'n_o' not in st.session_state: st.session_state.n_o = 3

st.title("🏛️ Valuador Pro: Análisis de Lectura Profunda (IA)")

tab1, tab2, tab3 = st.tabs(["🔍 Mercado Inteligente", "🏠 Sujeto", "📈 Indicadores"])

with tab1:
    col_a, col_b = st.columns([3, 1])
    with col_a:
        sector = st.text_input("Sector a Investigar (Guatemala):", "Bosques de la Fontana")
    with col_b:
        if st.button("➕ Oferta") and st.session_state.n_o < 5:
            st.session_state.n_o += 1
            st.rerun()

    if st.button("🚀 Iniciar Escaneo con Analista IA"):
        with st.spinner("Gemini IA analizando descripciones de mercado..."):
            resultados = api_ia.buscar_ofertas(sector, st.session_state.n_o)
            for i, res in enumerate(resultados):
                st.session_state.ofert_list[i] = res
            st.success("Análisis profundo completado.")

    # Renderizado de Ofertas
    cols = st.columns(st.session_state.n_o)
    res_finales = []
    
    for i in range(st.session_state.n_o):
        with cols[i]:
            st.subheader(f"Oferta {i+1}")
            item = st.session_state.ofert_list[i]
            if item['link'] != "Manual": st.caption(f"[Ver Propiedad]({item['link']})")
            
            p = st.number_input("Precio Q", key=f"p{i}", value=float(item['precio']))
            at = st.number_input("M2 Terreno", key=f"at{i}", value=float(item['m2_t']))
            ac = st.number_input("M2 Const.", key=f"ac{i}", value=float(item['m2_c']))
            cc = st.number_input("Expertís M2", key=f"cc{i}", value=3600.0)
            
            res = engine.calcular_residual_oferta(p, at, ac, cc)
            res_finales.append(res)
            st.info(f"Suelo: {f_q(res['m2_tierra_limpia'])}")

    st.divider()
    df = pd.DataFrame(res_finales)
    df.index = [f"Oferta {i+1}" for i in range(len(res_finales))]
    st.table(df.style.format("{:,.2f}"))
    prom_suelo = df['m2_tierra_limpia'].mean()

# --- LAS PESTAÑAS 2 Y 3 AHORA LEERÁN 'prom_suelo' SIN ERRORES ---

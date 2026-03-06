import streamlit as st
import pandas as pd
from engine import ValuadorEngine
from api import InmobiliariaAI

# --- CONFIGURACIÓN E INICIALIZACIÓN ---
st.set_page_config(page_title="Valuador Pro GT", layout="wide")

# Inicializamos estados para evitar NameError
if 'ofertas_v' not in st.session_state: st.session_state.ofertas_v = []
if 'links_d' not in st.session_state: st.session_state.links_d = []

engine = ValuadorEngine()
S_KEY = "3b154c2742a1d46402531eb080ee2d12d5f167e4"
G_KEY = "AIzaSyDiJ0t5ZOO8f1wODihSrd31lxR69yxnUSs"
api_ia = InmobiliariaAI(S_KEY, G_KEY)

st.title("🏛️ Sistema de Valuación Homogenizada")

t1, t2, t3, t4 = st.tabs(["🔍 Mercado", "🔗 Rescate de Links", "🏠 Sujeto", "📈 Indicadores"])

# --- TAB 1: MERCADO ---
with t1:
    col_bus, col_tipo = st.columns([3, 1])
    with col_bus: sector = st.text_input("Ubicación:", "Bosques de la Fontana")
    with col_tipo: tipo_p = st.selectbox("Tipo:", ["Casa", "Apartamento"])
    
    if st.button("🚀 Buscar y Analizar"):
        with st.spinner("IA analizando mercado..."):
            buenas, malas = api_ia.buscar_ofertas_full(sector, tipo_p)
            st.session_state.ofertas_v = buenas
            st.session_state.links_d = malas
            st.rerun()

    if st.session_state.ofertas_v:
        res_calc = []
        cols = st.columns(len(st.session_state.ofertas_v))
        for i, item in enumerate(st.session_state.ofertas_v):
            with cols[i]:
                st.subheader(f"Oferta {i+1}")
                st.caption(f"[Ver Link]({item['link']})")
                p = st.number_input(f"Precio Q", key=f"p{i}", value=item['precio'])
                at = st.number_input(f"M2 Terreno", key=f"t{i}", value=item['m2_t'])
                ac = st.number_input(f"M2 Const.", key=f"c{i}", value=item['m2_c'])
                res = engine.calcular_residual_oferta(p, at, ac, 3600)
                res_calc.append(res)
        
        st.divider()
        df_res = pd.DataFrame(res_calc)
        st.table(df_res.style.format("{:,.2f}"))
    else:
        st.info("💡 Realiza una búsqueda para comenzar.")

# --- TAB 2: RESCATE (Para links como el de tu imagen) ---
with t2:
    st.header("🔗 Enlaces con Información Pendiente")
    st.write("Si la IA no pudo entrar (ej. Facebook), ábrelo tú y mete los datos aquí:")
    
    for i, link in enumerate(st.session_state.links_d):
        with st.expander(f"Rescatar: {link['titulo'][:60]}..."):
            st.markdown(f"**Link:** [Abrir Publicación]({link['link']})")
            c1, c2, c3, c4 = st.columns(4)
            with c1: pr = st.number_input("Precio Q", key=f"pr{i}")
            with c2: tr = st.number_input("M2 Terreno", key=f"tr{i}")
            with c3: cr = st.number_input("M2 Const.", key=f"cr{i}")
            with c4:
                if st.button("✅ Validar", key=f"btn{i}"):
                    st.session_state.ofertas_v.append({"link": link['link'], "precio": pr, "m2_t": tr, "m2_c": cr})
                    st.success("¡Movido a Mercado!")

# --- LAS OTRAS TABS (Sujeto e Indicadores) ---
with t3:
    st.write("Panel del Sujeto...")
    # Aquí pegas el código de tu pestaña de sujeto habitual

with t4:
    st.write("Panel de Indicadores...")

import streamlit as st
import pandas as pd
from engine import ValuadorEngine
from api import InmobiliariaAI

st.set_page_config(page_title="Valuador Pro GT", layout="wide")
engine = ValuadorEngine()

S_KEY = "3b154c2742a1d46402531eb080ee2d12d5f167e4"
G_KEY = "AIzaSyDiJ0t5ZOO8f1wODihSrd31lxR69yxnUSs"
api_ia = InmobiliariaAI(S_KEY, G_KEY)

# --- ESTADOS DE SESIÓN ---
if 'lista_o' not in st.session_state: st.session_state.lista_o = []
if 'links_descartados' not in st.session_state: st.session_state.links_descartados = []

st.title("🏛️ Valuador Inteligente con Repositorio de Enlaces")

tab1, tab_links, tab2 = st.tabs(["🔍 Mercado Validado", "🔗 Enlaces Descartados (IA)", "🏠 Sujeto"])

with tab1:
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1: sector = st.text_input("Ubicación:", "Bosques de la Fontana")
    with c2: tipo = st.selectbox("Tipo:", ["Casa", "Apartamento"])
    with c3: 
        if st.button("🚀 Escanear Todo"):
            with st.spinner("Buscando y clasificando..."):
                buenas, malas = api_ia.buscar_ofertas_full(sector, tipo)
                st.session_state.lista_o = buenas
                st.session_state.links_descartados = malas
                st.rerun()

    # Mostrar las "Buenas" (Máximo 3 para comparar)
    if st.session_state.lista_o:
        cols = st.columns(len(st.session_state.lista_o))
        for i, item in enumerate(st.session_state.lista_o):
            with cols[i]:
                st.subheader(f"Oferta Validada #{i+1}")
                st.caption(f"[Abrir Fuente]({item['link']})")
                p = st.number_input(f"Precio Q", key=f"pv{i}", value=item['precio'])
                at = st.number_input(f"M2 Terreno", key=f"atv{i}", value=item['m2_t'])
                ac = st.number_input(f"M2 Const.", key=f"acv{i}", value=item['m2_c'])
                st.info(f"Suelo Residual: Q {engine.calcular_residual_oferta(p, at, ac, 3600)['m2_tierra_limpia']:,.2f}")
    else:
        st.warning("No hay ofertas automáticas completas. Revisa la pestaña de Enlaces Descartados.")

# --- NUEVA PESTAÑA: EL BASURERO DE LINKS ---
with tab_links:
    st.header("Enlaces con información incompleta")
    st.write("La IA no pudo extraer m2 o precios exactos de estos links. Revísalos manualmente:")
    
    if st.session_state.links_descartados:
        for i, link_item in enumerate(st.session_state.links_descartados):
            col_l, col_chk = st.columns([4, 1])
            with col_l:
                # El link cambia de estilo si se marca el checkbox
                st.markdown(f"**{i+1}.** [{link_item['titulo']}]({link_item['link']})")
            with col_chk:
                st.checkbox("Revisado", key=f"chk_{i}")
    else:
        st.info("No hay enlaces descartados aún.")

with tab2:
    st.header("Valuación del Sujeto")
    # (Aquí va el código de la pestaña sujeto que ya teníamos)

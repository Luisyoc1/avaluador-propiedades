import streamlit as st
import pandas as pd
from engine import ValuadorEngine
from api import InmobiliariaAI

st.set_page_config(page_title="Valuador Pro GT", layout="wide")
engine = ValuadorEngine()

S_KEY = "3b154c2742a1d46402531eb080ee2d12d5f167e4"
G_KEY = "AIzaSyDiJ0t5ZOO8f1wODihSrd31lxR69yxnUSs"
api_ia = InmobiliariaAI(S_KEY, G_KEY)

def f_q(v): return f"Q {v:,.2f}"

if 'lista_o' not in st.session_state:
    st.session_state.lista_o = [{"precio": 0.0, "m2_t": 0.0, "m2_c": 0.0, "link": "Manual"}] * 5

st.title("🏛️ Valuador Inteligente: Filtro de Tipología y Datos")

tab1, tab2 = st.tabs(["🔍 Mercado Filtrado", "🏠 Sujeto"])

with tab1:
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        sector = st.text_input("Ubicación:", "Bosques de San Nicolás")
    with col2:
        tipo = st.selectbox("¿Qué buscas?", ["Casa", "Apartamento"])
    with col3:
        n_busqueda = st.slider("Cantidad", 3, 5, 3)

    if st.button("🚀 Escanear y Descartar ofertas irrelevantes"):
        with st.spinner(f"Buscando solo {tipo}s con datos completos..."):
            res_ia = api_ia.buscar_ofertas(sector, tipo, n_busqueda)
            if res_ia:
                # Limpiamos la lista anterior para que no se mezclen
                st.session_state.lista_o = [{"precio": 0.0, "m2_t": 0.0, "m2_c": 0.0, "link": "Manual"}] * 5
                for i, r in enumerate(res_ia):
                    st.session_state.lista_o[i] = r
                st.success(f"Se encontraron {len(res_ia)} ofertas válidas.")
            else:
                st.error("No se encontraron ofertas con datos suficientes en esta zona.")

    cols = st.columns(n_busqueda)
    res_finales = []
    
    for i in range(n_busqueda):
        with cols[i]:
            item = st.session_state.lista_o[i]
            st.subheader(f"Oferta {i+1}")
            if item['link'] != "Manual": st.caption(f"[Ver enlace]({item['link']})")
            
            p = st.number_input("Precio Q", key=f"p{i}", value=float(item['precio']))
            at = st.number_input("M2 Terreno", key=f"at{i}", value=float(item['m2_t']))
            ac = st.number_input("M2 Const.", key=f"ac{i}", value=float(item['m2_c']))
            cc = st.number_input("Expertís", key=f"cc{i}", value=3600.0)
            
            # Solo calculamos si hay datos
            if p > 0 and at > 0:
                res = engine.calcular_residual_oferta(p, at, ac, cc)
                res_finales.append(res)
                st.info(f"Suelo: {f_q(res['m2_tierra_limpia'])}")
            else:
                st.warning("Datos incompletos")

    if res_finales:
        st.divider()
        df = pd.DataFrame(res_finales)
        st.write("### Resumen de Comparativos Validados")
        st.table(df.style.format("{:,.2f}"))

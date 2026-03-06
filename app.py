import streamlit as st
import pandas as pd
from engine import ValuadorEngine
from api import InmobiliariaAI

st.set_page_config(page_title="Valuador Pro GT", layout="wide")
engine = ValuadorEngine()
api_gt = InmobiliariaAI("3b154c2742a1d46402531eb080ee2d12d5f167e4")

def f_q(v): return f"Q {v:,.2f}"

st.title("🏛️ Sistema de Valuación Profesional - Guatemala")

# --- PERSISTENCIA DE DATOS ---
if 'num_o' not in st.session_state: st.session_state.num_o = 3
if 'lista_ofertas' not in st.session_state: 
    st.session_state.lista_ofertas = [{"precio": 1500000.0, "m2_t": 150.0, "m2_c": 180.0, "link": "Manual"} for _ in range(5)]

tab1, tab2, tab3 = st.tabs(["🔍 Buscador de Ofertas", "🏠 Sujeto (Valuación)", "📈 Indicadores"])

# --- PESTAÑA 1: MERCADO ---
with tab1:
    col_b, col_btn = st.columns([3, 1])
    with col_b:
        sector = st.text_input("Sector / Colonia a investigar:", "Bosques de la Fontana")
    with col_btn:
        if st.button("➕ Añadir Oferta") and st.session_state.num_o < 5:
            st.session_state.num_o += 1

    if st.button("🚀 Escanear Mercado en Guatemala"):
        with st.spinner("Buscando en portales, inmobiliarias y Marketplace..."):
            encontrados = api_gt.buscar_en_guatemala(sector, st.session_state.num_o)
            for i, enc in enumerate(encontrados):
                st.session_state.lista_ofertas[i] = enc
            st.success(f"Se actualizaron {len(encontrados)} ofertas de {sector}")

    cols = st.columns(st.session_state.num_o)
    resultados_mkt = []
    
    for i in range(st.session_state.num_o):
        with cols[i]:
            st.subheader(f"Oferta #{i+1}")
            item = st.session_state.lista_ofertas[i]
            if "link" in item and item["link"] != "Manual": 
                st.caption(f"[Ver Propiedad]({item['link']})")
            
            p = st.number_input(f"Precio Q", key=f"p{i}", value=float(item['precio']), format="%.2f")
            at = st.number_input(f"M2 Terreno", key=f"at{i}", value=float(item['m2_t']))
            ac = st.number_input(f"M2 Const.", key=f"ac{i}", value=float(item['m2_c']))
            cc = st.number_input(f"Expertís M2", key=f"cc{i}", value=3600.0)
            
            res = engine.calcular_residual_oferta(p, at, ac, cc)
            resultados_mkt.append(res)
            st.write(f"**Tierra Limpia:** {f_q(res['m2_tierra_limpia'])}")

    df_mkt = pd.DataFrame(resultados_mkt)
    df_mkt.index = [f"Oferta {i+1}" for i in range(len(resultados_mkt))]
    st.dataframe(df_mkt.style.format("{:,.2f}"), use_container_width=True)
    prom_tierra_final = df_mkt['m2_tierra_limpia'].mean()

# --- PESTAÑA 2: SUJETO ---
with tab2:
    st.header("Propiedad de Evaluación")
    c1, c2 = st.columns(2)
    with c1:
        m2_s = st.number_input("Metros Terreno Sujeto", value=156.44)
        v_t_expertis = st.number_input("Valor M2 Suelo (Para Banco)", value=4900.0)
    
    df_const = st.data_editor(pd.DataFrame([
        {"Tipo": "Principal", "M2": 204.20, "Costo_M2": 3850.0},
        {"Tipo": "Pérgola", "M2": 18.5, "Costo_M2": 1800.0}
    ]), num_rows="dynamic", use_container_width=True, key="editor_s")
    
    v_tierra_s = m2_s * v_t_expertis
    v_const_s = (df_const['M2'] * df_const['Costo_M2']).sum()
    total_fisico = v_tierra_s + v_const_s
    st.markdown(f"## Valor Físico Total: {f_q(total_fisico)}")

# --- PESTAÑA 3: INDICADORES ---
with tab3:
    st.header("Resumen y Comparación Final")
    ci1, ci2 = st.columns(2)
    with ci1:
        st.subheader("1. Indexación Histórica")
        v_h = st.number_input("Monto Original Q", value=899706.0)
        a_h = st.number_input("Año", value=2017)
        v_ind = engine.indexar_valor(v_h, a_h)
        st.info(f"Proyectado al 2025: {f_q(v_ind)}")

        st.subheader("2. Rentabilidad Comercial")
        r_m = st.number_input("Renta Mensual Estimada Q", value=3500.0)
        v_renta = engine.calcular_rentabilidad(r_m)
        st.info(f"Por Rentabilidad: {f_q(v_renta)}")

    with ci2:
        st.subheader("Triangulación de Valor")
        val_mkt = (prom_tierra_final * m2_s + v_const_s)
        metodos = ["Costo (Físico)", "Mercado (Zona)", "Histórico (3%)", "Renta (Cap 6%)"]
        valores = [total_fisico, val_mkt, v_ind, v_renta]
        
        df_comp = pd.DataFrame({"Método": metodos, "Valor Q": valores}).set_index("Método")
        st.bar_chart(df_comp)
        st.table(df_comp.style.format("{:,.2f}"))

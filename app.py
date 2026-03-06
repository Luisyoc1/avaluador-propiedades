import streamlit as st
import pandas as pd
from engine import ValuadorEngine

st.set_page_config(page_title="Valuador Pro Guatemala", layout="wide")
engine = ValuadorEngine()

# --- FORMATEO DE NÚMEROS ---
def formato_moneda(valor):
    return f"Q {valor:,.2f}"

st.title("🏛️ Sistema Inteligente de Valuación")

tab_mercado, tab_sujeto, tab_indicadores = st.tabs(["🔍 Búsqueda de Ofertas", "🏠 Sujeto", "📈 Indicadores"])

with tab_mercado:
    st.header("Explorador de Mercado Automático")
    colonia_busqueda = st.text_input("Escribe la Colonia o Sector para buscar ofertas:", "Bosques de la Fontana")
    
    if st.button("🔍 Buscar Ofertas en Tiempo Real"):
        st.warning("Conectando con APIs de búsqueda... (Simulando extracción de datos)")
        # Aquí la API llenaría los datos automáticamente
        st.success(f"Se encontraron 3 ofertas en {colonia_busqueda}")

    col_o1, col_o2, col_o3 = st.columns(3)
    ofertas_data = []

    for i, col in enumerate([col_o1, col_o2, col_o3], 1):
        with col:
            st.subheader(f"Oferta #{i}")
            # El usuario puede ajustar lo que la API encontró
            p = st.number_input(f"Precio Q", key=f"p{i}", value=1500000.0, step=500.0, format="%.2f")
            at = st.number_input(f"M2 Terreno", key=f"at{i}", value=150.0)
            ac = st.number_input(f"M2 Const.", key=f"ac{i}", value=200.0)
            cc = st.number_input(f"Expertís M2 Const (Editable)", key=f"cc{i}", value=3500.0)
            
            res = engine.calcular_residual_oferta(p, at, ac, cc)
            ofertas_data.append(res)
            st.write(f"**Tierra Limpia:** {formato_moneda(res['m2_tierra_limpia'])}")

    st.markdown("### Tabla de Ofertas Encontradas")
    df_ofertas = pd.DataFrame(ofertas_data)
    df_ofertas.index = ['Oferta 1', 'Oferta 2', 'Oferta 3']
    
    # Aplicar formato de comas a toda la tabla
    st.dataframe(df_ofertas.style.format("{:,.2f}"), use_container_width=True)

# --- LAS DEMÁS PESTAÑAS SE MANTIENEN CON EL MISMO MOTOR ---

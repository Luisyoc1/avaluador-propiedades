import streamlit as st
import pandas as pd
from engine import ValuadorEngine
from api import InmobiliariaAPI

# Configuración
st.set_page_config(page_title="Valuador AI Guatemala", layout="wide")
engine = ValuadorEngine()
# AQUÍ USAMOS TU API KEY
api_inmuebles = InmobiliariaAPI("3b154c2742a1d46402531eb080ee2d12d5f167e4")

def formato_q(valor):
    return f"Q {valor:,.2f}"

st.title("🏛️ Sistema de Valuación con IA y Google Search")

# Inicializar estados de sesión para las ofertas si no existen
if 'ofertas_buscadas' not in st.session_state:
    st.session_state.ofertas_buscadas = [
        {"p": 1500000.0, "at": 150.0, "ac": 200.0},
        {"p": 1600000.0, "at": 160.0, "ac": 210.0},
        {"p": 1700000.0, "at": 170.0, "ac": 220.0}
    ]

tab_mercado, tab_sujeto, tab_indicadores = st.tabs(["🔍 Buscador de Ofertas", "🏠 Sujeto", "📈 Indicadores"])

with tab_mercado:
    st.header("Explorador de Mercado Real")
    colonia = st.text_input("Sector a investigar:", "Bosques de la Fontana")
    
    if st.button("🔍 Buscar Ofertas Reales"):
        with st.spinner("Consultando Google y portales inmobiliarios..."):
            resultados = api_inmuebles.buscar_en_google(colonia)
            if resultados:
                for i, res in enumerate(resultados):
                    st.session_state.ofertas_buscadas[i] = {
                        "p": res['precio'],
                        "at": res['m2_t'],
                        "ac": res['m2_c']
                    }
                st.success(f"¡Se actualizaron las ofertas con datos de {colonia}!")
            else:
                st.error("No se pudieron extraer datos automáticos, usa el modo manual.")

    # Columnas de Ofertas
    cols = st.columns(3)
    ofertas_calculadas = []
    
    for i, col in enumerate(cols):
        with col:
            st.subheader(f"Oferta #{i+1}")
            # Estos campos se llenan solos con la API pero puedes corregirlos
            p = st.number_input(f"Precio Q", key=f"p{i}", value=st.session_state.ofertas_buscadas[i]['p'], format="%.2f")
            at = st.number_input(f"M2 Terreno", key=f"at{i}", value=st.session_state.ofertas_buscadas[i]['at'])
            ac = st.number_input(f"M2 Const.", key=f"ac{i}", value=st.session_state.ofertas_buscadas[i]['ac'])
            cc = st.number_input(f"Expertís M2 Const", key=f"cc{i}", value=3500.0)
            
            res = engine.calcular_residual_oferta(p, at, ac, cc)
            ofertas_calculadas.append(res)
            st.info(f"Tierra Limpia: {formato_q(res['m2_tierra_limpia'])}")

    st.markdown("### Resumen de Ofertas Encontradas")
    df = pd.DataFrame(ofertas_calculadas)
    df.index = [f"Oferta {i+1}" for i in range(len(ofertas_calculadas))]
    st.dataframe(df.style.format("{:,.2f}"), use_container_width=True)
    
    prom_tierra_zona = df['m2_tierra_limpia'].mean()
    st.subheader(f"Promedio de la Zona: {formato_q(prom_tierra_zona)}")

# --- Las otras pestañas (Sujeto e Indicadores) se mantienen igual ---

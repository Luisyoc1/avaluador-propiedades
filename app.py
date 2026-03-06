import streamlit as st
from engine import ValuadorEngine

st.set_page_config(page_title="Valuador Pro Guatemala", layout="wide")
engine = ValuadorEngine()

st.title("🏛️ Sistema de Valuación Inmobiliaria")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.header("1. Datos de Mercado (Testigos)")
    # Aquí simulamos la entrada de una oferta (puedes repetir esto para 3)
    p_oferta = st.number_input("Precio Oferta (Q)", value=1545600.0)
    m2_t = st.number_input("M2 Terreno", value=145.0)
    m2_c = st.number_input("M2 Construcción", value=205.0)
    costo_c = st.number_input("Costo m2 Const (Expertís)", value=3600.0)
    
    if st.button("Calcular Oferta"):
        res = engine.calcular_residual_oferta(p_oferta, m2_t, m2_c, costo_c)
        st.success(f"Valor Tierra Limpia: Q{res['m2_tierra_limpia']:,.2f}")

with col2:
    st.header("2. Validación Histórica")
    v_h = st.number_input("Valor Histórico (Hipoteca/Compra)", value=899706.0)
    anio_h = st.number_input("Año del registro", value=2017)
    
    if st.button("Indexar al 3%"):
        v_actual = engine.indexar_valor(v_h, anio_h)
        st.info(f"Valor Proyectado a 2025: Q{v_actual:,.2f}")

st.markdown("---")
st.header("3. Propiedad a Evaluar (Sujeto)")
# Aquí iría el desglose de áreas que mencionaste
st.write("Configura el valor físico final basado en tu criterio de banco.")

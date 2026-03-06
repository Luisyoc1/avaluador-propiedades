import streamlit as st
import pandas as pd
from engine import ValuadorEngine

st.set_page_config(page_title="Valuador Pro Guatemala", layout="wide")
engine = ValuadorEngine()

st.title("🏛️ Sistema de Valuación Homogenizada")
st.markdown("---")

# Creación de Pestañas
tab_mercado, tab_sujeto, tab_historico = st.tabs([
    "🔍 Estudio de Mercado (Testigos)", 
    "🏠 Propiedad a Evaluar (Sujeto)", 
    "📈 Indicadores e Hipotecas"
])

# --- PESTAÑA 1: ESTUDIO DE MERCADO ---
with tab_mercado:
    st.header("Análisis de Ofertas (Facebook / Web)")
    col_t1, col_t2, col_t3 = st.columns(3)
    testigos_data = []

    for i, col in enumerate([col_t1, col_t2, col_t3], 1):
        with col:
            st.subheader(f"Testigo #{i}")
            p = st.number_input(f"Precio Oferta Q", key=f"p{i}", value=1500000.0)
            at = st.number_input(f"M2 Terreno", key=f"at{i}", value=150.0)
            ac = st.number_input(f"M2 Const.", key=f"ac{i}", value=200.0)
            cc = st.number_input(f"Costo M2 Const (Expertís)", key=f"cc{i}", value=3500.0)
            
            res = engine.calcular_residual_oferta(p, at, ac, cc)
            testigos_data.append(res)
            st.info(f"Tierra Limpia: Q{res['m2_tierra_limpia']:,.2f}")

    # Tabla resumen de mercado
    st.markdown("### Resumen de Comparativos")
    df_mercado = pd.DataFrame(testigos_data)
    df_mercado.index = ['Oferta 1', 'Oferta 2', 'Oferta 3']
    st.table(df_mercado.style.format("{:,.2f}"))
    
    prom_tierra = df_mercado['m2_tierra_limpia'].mean()
    st.metric("Promedio Tierra Limpia en la Zona", f"Q {prom_tierra:,.2f}")

# --- PESTAÑA 2: PROPIEDAD A EVALUAR (DINÁMICO) ---
with tab_sujeto:
    st.header("Cálculo del Valor Físico")
    
    c1, c2 = st.columns(2)
    with c1:
        m2_sujeto = st.number_input("Metros de Terreno del Sujeto", value=156.44)
        valor_t_banco = st.number_input("Valor M2 Terreno (Expertís Banco)", value=4500.0)
    
    st.markdown("---")
    st.subheader("Áreas de Construcción")
    
    # Manejo dinámico de filas (Usando st.data_editor para facilidad)
    df_const = st.data_editor(pd.DataFrame([
        {"Tipo": "Principal", "M2": 200.0, "Costo_M2": 3800.0},
        {"Tipo": "Pérgola/Cisterna", "M2": 15.0, "Costo_M2": 1500.0}
    ]), num_rows="dynamic")
    
    # Cálculo Final
    valor_tierra_s = m2_sujeto * valor_t_banco
    valor_const_s = (df_const['M2'] * df_const['Costo_M2']).sum()
    total_fisico = valor_tierra_s + valor_const_s
    
    st.markdown(f"## Valor Físico Total: Q {total_fisico:,.2f}")

# --- PESTAÑA 3: INDICADORES HISTÓRICOS ---
with tab_historico:
    st.header("Validación Histórica e Hipotecaria")
    
    col_h1, col_h2 = st.columns(2)
    with col_h1:
        v_h = st.number_input("Monto Original (Hipoteca/Compra)", value=800000.0)
        a_h = st.number_input("Año del Trámite", value=2015, min_value=1990, max_value=2025)
        
        if st.button("Calcular Indexación (3% anual)"):
            v_indexado = engine.indexar_valor(v_h, a_h)
            st.success(f"Valor Proyectado al 2025: Q {v_indexado:,.2f}")
    
    with col_h2:
        st.write("### Gráfica de Validación")
        # Aquí crearíamos la gráfica comparando total_fisico vs v_indexado vs promedio mercado
        datos_grafica = {
            "Método": ["Costo (Expertís)", "Mercado (Promedio)", "Histórico (3%)"],
            "Valor Q": [total_fisico, (prom_tierra * m2_sujeto + valor_const_s), engine.indexar_valor(v_h, a_h)]
        }
        st.bar_chart(pd.DataFrame(datos_grafica).set_index("Método"))

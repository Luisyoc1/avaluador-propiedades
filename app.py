import streamlit as st
import pandas as pd
from engine import ValuadorEngine

st.set_page_config(page_title="Valuador Pro Guatemala", layout="wide")
engine = ValuadorEngine()

st.title("🏛️ Sistema de Valuación Homogenizada e Indicadores")

# --- 1. CÁLCULOS INICIALES (Para evitar errores de variables no definidas) ---
# Valores por defecto para que la gráfica no truene al iniciar
prom_tierra_zona = 0.0
total_fisico = 0.0
v_ind = 0.0
v_av_ind = 0.0
val_renta = 0.0

# Definición de pestañas
tab_mercado, tab_sujeto, tab_indicadores = st.tabs([
    "🔍 Estudio de Mercado", 
    "🏠 Valor Físico (Sujeto)", 
    "📈 Validación de Indicadores"
])

# --- PESTAÑA 1: ESTUDIO DE MERCADO ---
with tab_mercado:
    st.info("💡 Ingresa 3 ofertas de mercado para obtener el promedio residual.")
    col_t1, col_t2, col_t3 = st.columns(3)
    testigos_data = []

    for i, col in enumerate([col_t1, col_t2, col_t3], 1):
        with col:
            st.subheader(f"Testigo #{i}")
            p = st.number_input(f"Precio Oferta Q", key=f"p{i}", value=1500000.0, step=10000.0)
            at = st.number_input(f"M2 Terreno", key=f"at{i}", value=150.0)
            ac = st.number_input(f"M2 Const.", key=f"ac{i}", value=200.0)
            cc = st.number_input(f"Costo M2 Const (Expertís)", key=f"cc{i}", value=3500.0)
            
            res = engine.calcular_residual_oferta(p, at, ac, cc)
            testigos_data.append(res)
            st.metric("Tierra Limpia", f"Q {res['m2_tierra_limpia']:,.2f}")

    st.markdown("### Resumen Comparativo de Mercado")
    df_mercado = pd.DataFrame(testigos_data)
    df_mercado.index = ['Oferta 1', 'Oferta 2', 'Oferta 3']
    st.dataframe(df_mercado.style.format("{:,.2f}"), use_container_width=True)
    
    prom_tierra_zona = df_mercado['m2_tierra_limpia'].mean()
    st.subheader(f"Promedio Residual de Tierra: Q {prom_tierra_zona:,.2f}")

# --- PESTAÑA 2: VALOR FÍSICO DEL SUJETO ---
with tab_sujeto:
    st.header("Propiedad a Evaluar")
    c1, c2 = st.columns(2)
    with c1:
        m2_sujeto = st.number_input("Metros Cuadrados de Terreno", value=156.44)
        v_t_banco = st.number_input("Valor M2 Terreno (Expertís)", value=4900.0)
    
    st.subheader("Desglose de Construcciones")
    df_const = st.data_editor(pd.DataFrame([
        {"Tipo": "Nivel 1", "M2": 204.20, "Costo_M2": 3850.0},
        {"Tipo": "Pérgola", "M2": 18.5, "Costo_M2": 1800.0}
    ]), num_rows="dynamic", use_container_width=True, key="editor_const")
    
    val_tierra_total = m2_sujeto * v_t_banco
    val_const_total = (df_const['M2'] * df_const['Costo_M2']).sum()
    total_fisico = val_tierra_total + val_const_total
    
    st.markdown(f"## Valor Físico Resultante: Q {total_fisico:,.2f}")

# --- PESTAÑA 3: INDICADORES ---
with tab_indicadores:
    st.header("Validación por Indicadores")
    col_i1, col_i2 = st.columns(2)
    
    with col_i1:
        st.subheader("1. Indexación (3%)")
        v_hist = st.number_input("Monto Hipoteca Original Q", value=899706.0)
        a_hist = st.number_input("Año Origen", value=2017)
        v_ind = engine.indexar_valor(v_hist, a_hist)
        
        v_av_old = st.number_input("Monto Avalúo Anterior Q", value=1000000.0)
        a_av_old = st.number_input("Año Avalúo", value=2018)
        v_av_ind = engine.indexar_valor(v_av_old, a_av_old)

        st.subheader("2. Rentabilidad (6%)")
        renta = st.number_input("Renta Mensual Estimada Q", value=3500.0)
        val_renta = engine.calcular_rentabilidad(renta)

    with col_i2:
        st.subheader("Resumen de Métodos")
        # Aquí creamos la variable df_grafica DENTRO de la pestaña para asegurar que exista
        metodos = ["Físico (Sujeto)", "Mercado (Zona)", "Hipoteca Ind.", "Avalúo Ind.", "Rentabilidad"]
        valores = [total_fisico, (prom_tierra_zona * m2_sujeto + val_const_total), v_ind, v_av_ind, val_renta]
        
        df_grafica = pd.DataFrame({"Método": metodos, "Valor Q": valores})
        st.bar_chart(df_grafica.set_index("Método"))
        st.table(df_grafica.set_index("Método").style.format("{:,.2f}"))

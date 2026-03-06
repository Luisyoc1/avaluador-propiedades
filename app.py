import streamlit as st
import pandas as pd
from engine import ValuadorEngine

st.set_page_config(page_title="Valuador Pro Guatemala", layout="wide")
engine = ValuadorEngine()

st.title("🏛️ Sistema de Valuación Homogenizada e Indicadores")

tab_mercado, tab_sujeto, tab_indicadores = st.tabs([
    "🔍 Estudio de Mercado", 
    "🏠 Valor Físico (Sujeto)", 
    "📈 Validación de Indicadores"
])

# --- PESTAÑA 1 y 2 (Se mantienen con la lógica anterior) ---
# ... (Código de mercado y sujeto aquí) ...

# --- PESTAÑA 3: INDICADORES (EL NUEVO CORAZÓN) ---
with tab_indicadores:
    st.header("Validación por Diferentes Métodos")
    
    col_izq, col_der = st.columns(2)

    with col_izq:
        st.subheader("1. Históricos (Indexación 3%)")
        # Sub-sección para Hipoteca
        with st.expander("Datos de Hipoteca"):
            v_hip = st.number_input("Monto Hipoteca Original", value=899706.0)
            a_hip = st.number_input("Año Hipoteca", value=2017)
            v_hip_ind = engine.indexar_valor(v_hip, a_hip)
            st.write(f"Valor Hipoteca Indexado: **Q {v_hip_ind:,.2f}**")

        # Sub-sección para Avalúo Anterior
        with st.expander("Avalúo Anterior"):
            v_av = st.number_input("Monto Avalúo Anterior", value=1000000.0)
            a_av = st.number_input("Año del Avalúo", value=2018)
            v_av_ind = engine.indexar_valor(v_av, a_av)
            st.write(f"Valor Avalúo Indexado: **Q {v_av_ind:,.2f}**")

        st.subheader("2. Método de Rentabilidad")
        with st.expander("Análisis de Rentas (Cap Rate 6%)"):
            renta_mensual = st.number_input("Renta Mensual Percibida (Q)", value=3500.0)
            v_renta = engine.calcular_rentabilidad(renta_mensual)
            st.write(f"Valor por Rentabilidad: **Q {v_renta:,.2f}**")
            st.caption("Fórmula: (Renta * 12) / 0.06")

    with col_der:
        st.subheader("Resumen de Validación")
        # Aquí definimos los valores para la gráfica (usando valores de las entradas)
        # Nota: total_fisico vendría de la pestaña 2
        datos_grafica = {
            "Método": ["Hipoteca Indexada", "Avalúo Indexado", "Rentabilidad (Cap 6%)"],
            "Valor Q": [v_hip_ind, v_av_ind, v_renta]
        }
        df_grafica = pd.DataFrame(datos_grafica).set_index("Método")
        st.bar_chart(df_grafica)
        
        st.table(df_grafica.style.format("{:,.2f}"))

st.info("💡 Este panel permite comparar si el valor físico está alineado con la historia financiera y la capacidad de generar ingresos de la propiedad.")

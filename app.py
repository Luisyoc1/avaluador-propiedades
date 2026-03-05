import streamlit as st
from api import calcular_oferta

st.title("Evaluador de propiedades")

st.header("Datos de la oferta comparable")

area_terreno = st.number_input("Área de terreno (m2)", value=0.0)
area_construccion = st.number_input("Área de construcción (m2)", value=0.0)
precio_oferta = st.number_input("Precio de oferta", value=0.0)
precio_m2_construccion = st.number_input("Precio m2 construcción", value=0.0)

negociacion = st.slider("Porcentaje de negociación", 0.0, 0.20, 0.10)

if st.button("Calcular valores"):

    resultado = calcular_oferta(
        area_terreno,
        area_construccion,
        precio_oferta,
        negociacion,
        precio_m2_construccion
    )

    st.subheader("Resultados")

    st.write("Valor negociado:", round(resultado["valor_negociado"], 2))
    st.write("Valor m2 terreno:", round(resultado["valor_m2_terreno"], 2))
    st.write("Promedio bruto terreno:", round(resultado["valor_bruto_terreno"], 2))
    st.write("Promedio construcción:", round(resultado["valor_promedio_construccion"], 2))

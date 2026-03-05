import streamlit as st

st.title("Evaluador básico de propiedades")

area_construccion = st.number_input("Metros cuadrados de construcción")
area_terreno = st.number_input("Metros cuadrados de terreno")
precio_m2 = st.number_input("Precio promedio por m2")

if st.button("Calcular valor estimado"):
    valor = area_construccion * precio_m2
    st.write("Valor estimado de la propiedad:", valor)

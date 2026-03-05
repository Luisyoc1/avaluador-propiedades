import streamlit as st
from api import calcular_oferta, calcular_promedios, valorar_propiedad

st.title("Sistema de valuación de propiedades")

st.header("Ofertas comparables")

ofertas = []

for i in range(3):

    st.subheader(f"Oferta {i+1}")

    terreno = st.number_input(f"Terreno oferta {i+1}", value=0.0, key=f"t{i}")
    construccion = st.number_input(f"Construcción oferta {i+1}", value=0.0, key=f"c{i}")
    precio = st.number_input(f"Precio oferta {i+1}", value=0.0, key=f"p{i}")
    precio_m2_const = st.number_input(f"Precio m2 construcción oferta {i+1}", value=0.0, key=f"m{i}")

    negociacion = st.slider(f"Negociación oferta {i+1}",0.0,0.30,0.10,key=f"n{i}")

    if terreno > 0 and construccion > 0:

        resultado = calcular_oferta(terreno,construccion,precio,precio_m2_const,negociacion)
        ofertas.append(resultado)

        st.write(resultado)


if len(ofertas) == 3:

    st.header("Promedios de mercado")

    prom_terreno, prom_const, prom_neg = calcular_promedios(ofertas)

    st.write("Promedio m2 terreno:", prom_terreno)
    st.write("Promedio m2 construcción:", prom_const)
    st.write("Promedio precios negociados:", prom_neg)

    st.header("Propiedad a evaluar")

    terreno_eval = st.number_input("Terreno propiedad evaluada")
    construccion_eval = st.number_input("Construcción propiedad evaluada")
    extras = st.number_input("Extras (pérgola, garaje, etc)",value=0.0)

    if st.button("Calcular valor propiedad"):

        vt, vc, total = valorar_propiedad(
            terreno_eval,
            construccion_eval,
            prom_terreno,
            prom_const,
            extras
        )

        st.header("Resultado")

        st.write("Valor terreno:", vt)
        st.write("Valor construcción:", vc)
        st.write("Valor total estimado:", total)

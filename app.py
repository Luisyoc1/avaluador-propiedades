# ... (Parte superior del código igual)

with t2:
    st.header("🔗 Enlaces con Información Pendiente")
    st.info("Aquí están los links donde Facebook bloqueó a la IA o falta info. Ábrelos tú y completa el dato:")
    
    for i, link in enumerate(st.session_state.links_d):
        with st.expander(f"Revisar: {link['titulo'][:50]}..."):
            st.markdown(f"**Enlace original:** [Haz clic aquí para abrir y cerrar el anuncio de FB]({link['link']})")
            
            c1, c2, c3, c4 = st.columns(4)
            with c1: p_man = st.number_input("Precio Q", key=f"pman_{i}")
            with c2: t_man = st.number_input("M2 Terreno", key=f"tman_{i}")
            with c3: c_man = st.number_input("M2 Const.", key=f"cman_{i}")
            with c4: 
                if st.button("✅ Rescatar y Validar", key=f"btnman_{i}"):
                    # Lo movemos a la lista de validadas
                    nueva_oferta = {
                        "link": link['link'],
                        "precio": p_man,
                        "m2_t": t_man,
                        "m2_c": c_man
                    }
                    st.session_state.ofertas_v.append(nueva_oferta)
                    st.success("¡Oferta rescatada! Revisa la pestaña de Estudio de Mercado.")

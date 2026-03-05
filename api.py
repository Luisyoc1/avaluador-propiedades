def calcular_oferta(area_terreno, area_construccion, precio_oferta, precio_m2_construccion, negociacion):

    # precio negociado
    precio_negociado = precio_oferta * (1 - negociacion)

    # valor construcción
    valor_construccion = area_construccion * precio_m2_construccion

    # valor terreno dentro de la oferta
    valor_terreno = precio_negociado - valor_construccion

    # precio terreno por m2
    valor_m2_terreno = valor_terreno / area_terreno

    # valor construcción por m2 real
    valor_m2_construccion = valor_construccion / area_construccion

    return {
        "precio_negociado": precio_negociado,
        "valor_construccion": valor_construccion,
        "valor_terreno": valor_terreno,
        "valor_m2_terreno": valor_m2_terreno,
        "valor_m2_construccion": valor_m2_construccion
    }


def calcular_promedios(ofertas):

    promedio_m2_terreno = sum(o["valor_m2_terreno"] for o in ofertas) / len(ofertas)
    promedio_m2_construccion = sum(o["valor_m2_construccion"] for o in ofertas) / len(ofertas)
    promedio_negociado = sum(o["precio_negociado"] for o in ofertas) / len(ofertas)

    return promedio_m2_terreno, promedio_m2_construccion, promedio_negociado


def valorar_propiedad(area_terreno, area_construccion, promedio_m2_terreno, promedio_m2_construccion, extras):

    valor_terreno = area_terreno * promedio_m2_terreno
    valor_construccion = area_construccion * promedio_m2_construccion

    valor_total = valor_terreno + valor_construccion + extras

    return valor_terreno, valor_construccion, valor_total

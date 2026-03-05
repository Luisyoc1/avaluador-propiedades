def calcular_oferta(area_terreno, area_construccion, precio_oferta, negociacion, precio_m2_construccion):

    valor_negociado = precio_oferta * (1 - negociacion)

    valor_construccion = area_construccion * precio_m2_construccion

    valor_terreno_total = valor_negociado - valor_construccion

    valor_m2_terreno = valor_terreno_total / area_terreno

    valor_bruto_terreno = valor_negociado / area_terreno

    valor_promedio_construccion = valor_negociado / area_construccion

    return {
        "valor_negociado": valor_negociado,
        "valor_m2_terreno": valor_m2_terreno,
        "valor_bruto_terreno": valor_bruto_terreno,
        "valor_promedio_construccion": valor_promedio_construccion
    }

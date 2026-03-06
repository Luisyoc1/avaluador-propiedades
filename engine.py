import math

class ValuadorEngine:
    def __init__(self, tasa_crecimiento=0.03):
        # El 3% de crecimiento anual que mencionaste
        self.tasa = tasa_crecimiento

    def calcular_residual_oferta(self, precio, m2_t, m2_c, costo_c, f_neg=0.10):
        """Calcula el valor residual de la tierra de una oferta de mercado."""
        precio_neto = precio * (1 - f_neg)
        v_const_total = m2_c * costo_c
        v_terr_residual = precio_neto - v_const_total
        return {
            "p_neto": precio_neto,
            "m2_tierra_limpia": v_terr_residual / m2_t if m2_t > 0 else 0,
            "bruto_t": precio_neto / m2_t if m2_t > 0 else 0,
            "bruto_c": precio_neto / m2_c if m2_c > 0 else 0
        }

    def indexar_valor(self, valor_h, anio_h, anio_a=2025):
        """Trae valores del pasado al presente (Hipotecas o Avalúos anteriores)."""
        n = anio_a - anio_h
        return valor_h * (math.pow(1 + self.tasa, n))

    def calcular_rentabilidad(self, monto_mensual, tasa_cap=0.06):
        """Calcula el valor basado en rentas (Cap Rate 6%)."""
        # (Renta mensual * 12 meses) / 0.06
        return (monto_mensual * 12) / tasa_cap

    def valor_fisico_sujeto(self, m2_t, v_t_banco, lista_areas):
        """Calcula el valor total físico sumando terreno y múltiples áreas de construcción."""
        v_tierra = m2_t * v_t_banco
        v_edificios = sum(a['m2'] * a['costo'] for a in lista_areas)
        return v_tierra + v_edificios
    

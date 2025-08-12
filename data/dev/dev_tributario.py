# Parámetros para consultar cuenta corriente de inmueble
parametros_deuda_inmueble = {
    "p_denominacion_catastral": "311509901200000"  # Denominación catastral del inmueble (solo números)
}

# Comentarios sobre el endpoint de cuenta corriente inmueble
parametros_deuda_inmueble_comentarios = {
    # Este endpoint consulta la cuenta corriente municipal de un inmueble específico
    # Requiere p_denominacion_catastral como parámetro obligatorio
    # La denominación catastral debe contener solo números (validación con regex \d+)
    # Retorna DeudaInmuebleResponseSchema con:
    # - id_deuda_inmueble: identificador de la deuda del inmueble
    # - id_inmueble: identificador del inmueble
    # - obj_dato: datos del objeto
    # - información del propietario (persona física o jurídica):
    #   * id_persona_fisica/id_persona_juridica
    #   * nombre, apellido, cuil (persona física)
    #   * razon_social, cuit (persona jurídica)
    #   * nombre_alt, cuit_alt (datos alternativos)
    # - información del inmueble:
    #   * superficie: superficie total
    #   * sup_descubierta: superficie descubierta
    #   * sup_cubierta: superficie cubierta
    # - información de deuda:
    #   * deuda_historica: deuda histórica
    #   * total_deuda: total de la deuda
    #   * ultima_actualizacion: fecha de última actualización
    # - ctactes_dict: lista de cuotas con detalle de:
    #   * id_ctacte_deu_inmueble, ctacte_id
    #   * id_tipo_impuesto: tipo de impuesto
    #   * año, cuota: año y número de cuota
    #   * nominal, nominalcub: montos nominales
    #   * intereses: intereses aplicados
    #   * total, saldo: montos totales y saldo
    #   * estado: estado de la cuota
    #   * fecha_vencimiento, fecha_pago: fechas relevantes
    #
    # El endpoint requiere permisos específicos (servicio_context 144)
    # URL: /inmuebles/ctacte
    # Método: GET
    # Response: DeudaInmuebleResponseSchema
    #
    # VALIDACIONES:
    # - p_denominacion_catastral debe contener solo números
    # - Si no se encuentran datos, retorna error 404
    # - Consulta información adicional del propietario si existe
}

# Parámetros para consulta de cuenta corriente de rodados
parametros_deuda_rodado = {
    "p_dominio": "A078XAY"  # Dominio/patente del vehículo a consultar
}
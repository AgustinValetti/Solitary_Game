def agregar_caracter(nombre_actual: str
                     ,evento: any
                     ,max_largo: int = 12) -> str:
    """
    Esta funcion verifica que el largo del nombre ingresado sea 
    menor a 12 caracteres, devuelve el nombre actualizado
    """
    if len(nombre_actual) < max_largo and evento.unicode.isprintable():
        return nombre_actual + evento.unicode
    return nombre_actual
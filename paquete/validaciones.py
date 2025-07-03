# validaciones.py

def inicializar_pilas() -> dict:
    """
    Esta función crea el diccionario para las pilas acumuladoras.
    """
    pilas = {
        "oros": [],
        "copas": [],
        "espadas": [],
        "bastos": []
    }
    return pilas

def agregar_caracter(nombre_actual: str, evento: any, max_largo: int = 15) -> str:
    """
    Esta funcion valida la cantidad de caracteres
    """
    if len(nombre_actual) < max_largo and evento.unicode.isprintable():
        return nombre_actual + evento.unicode
    return nombre_actual


import pygame

#tablero
def mostrar_tablero(tablero):
    """
    toma la matriz resultante de la baraja, 
    y la muestra en formato de tablero.
    """
    
    encabezado = "    "
    for i in range(len(tablero)):
        encabezado += f" C{i+1}   "
    print(encabezado)
    print("   " + "------" * len(tablero))

    # filas maximas
    max_filas = 0
    for columna in tablero:
        cantidad = len(columna["boca_abajo"]) + len(columna["boca_arriba"])
        if cantidad > max_filas:
            max_filas = cantidad

    # muestra x fila
    for fila in range(max_filas):
        linea = f"{fila+1:2}"
        for col in tablero:
            ocultas = len(col["boca_abajo"])
            visibles = len(col["boca_arriba"])
            total = ocultas + visibles

            if fila < ocultas:
                carta = "🃏  "
            elif fila < total:
                idx = fila - ocultas
                palo, numero = col["boca_arriba"][idx]
                carta = f"{palo[:2]}-{numero:02}"
            else:
                carta = "⬛"
            linea += f" {carta} "
        print(linea)


#ruta de iamgenes
def obtener_ruta_imagen(carta: tuple) -> str:
    """
    Toma una carta, devuelve la ruta de la imagen
    """
    palo_plural, numero = carta

    equivalencias = {
        "oros": "oro",
        "copas": "copa",
        "espadas": "espada",
        "bastos": "basto"
    }

    palo_singular = equivalencias.get(palo_plural, palo_plural)

    nombre_archivo = f"{numero} de {palo_singular}.jpg"
    ruta = f"cartas/{nombre_archivo}"
    return ruta


# PILAS

def inicializar_pilas()-> dict:
    """
    Esta funcion crea el diccionario para las pilas acumuladoras
    """

    pilas = {
        "oros": [],
        "copas": [],
        "espadas": [],
        "bastos": []
    }

    return pilas


# funcion para agregarle border radius a las imagenes
def redondear_imagen(imagen, ancho, alto, radio_borde=4):
    """
    retonra las imagenes con border radius.
    """
    superficie_redondeada = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    
    # superficie de la carta
    pygame.draw.rect(superficie_redondeada, (255, 255, 255), (0, 0, ancho, alto), border_radius=radio_borde)

    imagen_redimensionada = pygame.transform.scale(imagen, (ancho, alto))
    #border radius
    imagen_redimensionada.blit(superficie_redondeada, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

    return imagen_redimensionada



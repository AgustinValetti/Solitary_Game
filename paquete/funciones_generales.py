import pygame
from globals.variables_globales import *
#tablero
# def mostrar_tablero(tablero):
#     """
#     toma la matriz resultante de la baraja, 
#     y la muestra en formato de tablero.
#     """
    
#     encabezado = "    "
#     for i in range(len(tablero)):
#         encabezado += f" C{i+1}   "
#     print(encabezado)
#     print("   " + "------" * len(tablero))

#     # filas maximas
#     max_filas = 0
#     for columna in tablero:
#         cantidad = len(columna["boca_abajo"]) + len(columna["boca_arriba"])
#         if cantidad > max_filas:
#             max_filas = cantidad

#     # muestra x fila
#     for fila in range(max_filas):
#         linea = f"{fila+1:2}"
#         for col in tablero:
#             ocultas = len(col["boca_abajo"])
#             visibles = len(col["boca_arriba"])
#             total = ocultas + visibles

#             if fila < ocultas:
#                 carta = "🃏  "
#             elif fila < total:
#                 idx = fila - ocultas
#                 palo, numero = col["boca_arriba"][idx]
#                 carta = f"{palo[:2]}-{numero:02}"
#             else:
#                 carta = "⬛"
#             linea += f" {carta} "
#         print(linea)


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





##funciones para el movimiento

def detectar_carta_seleccionada(tablero:list
                                ,pila_mazo_vista:list
                                ,pilas:dict
                                ,mouse_x:int
                                ,mouse_y:int)-> dict | None:
    """
    Esta funcion detecta en donde hizo click el usuario.
    Ultima carta del maazo
    Ultima carta del mazo visible
    Pila acumuladora
    Columnas
    """
    # mazo
    x_mostrar = POS_MAZO_X + ANCHO_CARTA + 20
    y_mostrar = POS_MAZO_Y
    rect_mazo_visible = pygame.Rect(x_mostrar, y_mostrar, ANCHO_CARTA, ALTO_CARTA)

    if rect_mazo_visible.collidepoint(mouse_x, mouse_y) and len(pila_mazo_vista) > 0:
        return {"origen": "mazo", "carta": pila_mazo_vista[-1], "indice": None}

    # ultima carta de la mesa
    for indice_columna, columna in enumerate(tablero):
        x = MARGEN_X + indice_columna * (ANCHO_CARTA + ESPACIO_ENTRE_COLUMNAS)
        y = MARGEN_Y

        # espacio vacio
        if len(columna["boca_abajo"]) == 0 and len(columna["boca_arriba"]) == 0:
            rect_vacio = pygame.Rect(x, y, ANCHO_CARTA, ALTO_CARTA)
            if rect_vacio.collidepoint(mouse_x, mouse_y):
                return {"origen": "mesa", "carta": None, "indice": indice_columna}

        # ultima carta boca arriba
        if len(columna["boca_arriba"]) > 0:
            ultima_carta = columna["boca_arriba"][-1]
            y += SUPERPOSICION_VERTICAL * (len(columna["boca_abajo"]) + len(columna["boca_arriba"]) - 1)
            rect_carta = pygame.Rect(x, y, ANCHO_CARTA, ALTO_CARTA)
            if rect_carta.collidepoint(mouse_x, mouse_y):
                return {"origen": "mesa", "carta": ultima_carta, "indice": indice_columna}

    # pila
    for palo, (x, y) in POS_PILAS.items():
        rect_pila = pygame.Rect(x, y, ANCHO_CARTA, ALTO_CARTA)
        if rect_pila.collidepoint(mouse_x, mouse_y):
            return {"origen": "pila", "carta": None, "indice": palo}

    return None



###mueve cartas


def intentar_mover_a_columna(tablero:list
                             ,indice_origen:int
                             ,carta:str
                             ,destino_indice:int) -> bool:
    """
    Esta funcion intenta mover la carta hacia el lugar elegido.
    Si la columna esta vacia, cualquier carta puede ir
    Si la columna no esta vacia, solo se puede mover si el palo es diferente y el numero es menor.
    """

    palo_carta, numero_carta = carta
    columna_destino = tablero[destino_indice]["boca_arriba"]

    if len(columna_destino) == 0:
        #columna vacia
        columna_destino.append(carta)
        return True
    else:
        palo_carta_superior, numero_carta_superior = columna_destino[-1]

        # palo diferente y numero menor
        if palo_carta_superior != palo_carta and numero_carta_superior == numero_carta + 1:
            columna_destino.append(carta)
            return True

    return False




def intentar_mover_a_pila(pilas:dict
                          ,carta:tuple
                          ,palo_destino:str)-> bool:
    """
    Esta funcion bsuca mover las cartas hacia las pilas.
    si la carta es del mismo palo y el orden es ascendente
    """
    palo_carta, numero_carta = carta
    #palo diferente
    if palo_carta != palo_destino:
        return False  

    pila_actual = pilas[palo_destino]

    if not pila_actual:
        # si no hay anda en la pila solo se permite el ingreso de los 1
        if numero_carta == 1:
            pilas[palo_destino].append(carta)
            return True
        else:
            return False
    else:
        # orden ascendente
        numero_superior = pila_actual[-1]
        if numero_carta == numero_superior + 1:
            pilas[palo_destino].append(carta)
            return True

    return False


#
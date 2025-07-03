import pygame
from constantes.constantes import *
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


##Secuencia de pila matriz
def obtener_secuencia_valida(cartas_boca_arriba:list
                             ,indice_inicial:int) -> list:
    """
    Esta funcion valida si la secuencia de cartas se pueden mover en conjunto
    desde el indice de inicio hasta el final
    Revisando el orden y palo.
    """
    if indice_inicial >= len(cartas_boca_arriba):
        return []
    
    secuencia = [cartas_boca_arriba[indice_inicial]]
    
    # si es ultima carta solo devuelve esa
    if indice_inicial == len(cartas_boca_arriba) - 1:
        return secuencia
    
    # valida de arriba hacia abajo
    i = indice_inicial
    while i < len(cartas_boca_arriba) - 1:
        carta_actual = cartas_boca_arriba[i]
        carta_siguiente = cartas_boca_arriba[i + 1]
        
        palo_actual, num_actual = carta_actual
        palo_siguiente, num_siguiente = carta_siguiente
        
        # valida entre palo  diferente palo y numero siguiente
        if (palo_actual != palo_siguiente and 
            num_actual in ESCALERA_VALIDO and 
            ESCALERA_VALIDO[num_actual] == num_siguiente):
            secuencia.append(carta_siguiente)
            i += 1
        else:
            # si la secuencia no es valida se queda con la ultima carta seleccionada
            return [cartas_boca_arriba[indice_inicial]]
    
    return secuencia




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
        return {"origen": "mazo", "carta": [pila_mazo_vista[-1]], "indice": None}

    # recorre de la ultima carta  ala primera
    cantidad_columnas = len(tablero)
    col = 0
    while col < cantidad_columnas:
        x = MARGEN_X + col * (ANCHO_CARTA + ESPACIO_ENTRE_COLUMNAS)
        y_inicial = MARGEN_Y
        columna = tablero[col]

        cantidad_boca_abajo = len(columna["boca_abajo"])
        cantidad_boca_arriba = len(columna["boca_arriba"])

        # si no hay cartas
        if cantidad_boca_abajo == 0 and cantidad_boca_arriba == 0:
            rect_vacio = pygame.Rect(x, y_inicial, ANCHO_CARTA, ALTO_CARTA)
            if rect_vacio.collidepoint(mouse_x, mouse_y):
                return {"origen": "mesa", "carta": None, "indice": col}

        # busca las cartas boca arriba de la ultima a la primera
        carta_clickeada = None
        indice_clickeado = -1
        
        i = cantidad_boca_arriba - 1
        while i >= 0:
            y_carta = y_inicial + (cantidad_boca_abajo + i) * SUPERPOSICION_VERTICAL
            rect_carta = pygame.Rect(x, y_carta, ANCHO_CARTA, ALTO_CARTA)
            if rect_carta.collidepoint(mouse_x, mouse_y):
                carta_clickeada = columna["boca_arriba"][i]
                indice_clickeado = i
                break
            i -= 1

        # se selecciona la carta y se valida si es valida
        if carta_clickeada is not None:
            cartas_seleccionadas = obtener_secuencia_valida(columna["boca_arriba"], indice_clickeado)
            return {"origen": "mesa", "carta": cartas_seleccionadas, "indice": col}

        col += 1

    # pila
    for palo in pilas:
        x, y = POS_PILAS[palo]
        rect_pila = pygame.Rect(x, y, ANCHO_CARTA, ALTO_CARTA)
        if rect_pila.collidepoint(mouse_x, mouse_y):
            return {"origen": "pila", "carta": None, "indice": palo}

    return None



###mueve cartas


# def intentar_mover_a_columna(tablero:list
#                              ,indice_origen:int
#                              ,carta:str
#                              ,destino_indice:int) -> bool:
#     """
#     Esta funcion intenta mover la carta hacia el lugar elegido.
#     Si la columna esta vacia, cualquier carta puede ir
#     Si la columna no esta vacia, solo se puede mover si el palo es diferente y el numero es menor.
#     """

#     palo_carta, numero_carta = carta
#     columna_destino = tablero[destino_indice]["boca_arriba"]

#     if len(columna_destino) == 0:
#         #columna vacia
#         columna_destino.append(carta)
#         return True
#     else:
#         palo_carta_superior, numero_carta_superior = columna_destino[-1]

#         # palo diferente y numero menor
#         if palo_carta_superior != palo_carta and numero_carta_superior == numero_carta + 1:
#             columna_destino.append(carta)
#             return True
#     return False

def intentar_mover_a_columna(tablero:list
                             ,indice_origen:int
                             ,cartas:str
                             ,destino_indice:int) -> bool:
    """
    Esta funcion mueve entre las columnas las cartas seleccionadas
    """

    if cartas is None or len(cartas) == 0 or cartas[0] is None:
        return False  

    # 
    if indice_origen is not None:
        columna_origen = tablero[indice_origen]["boca_arriba"]
    else:
        #sale del mazo
        columna_origen = None  

    columna_destino = tablero[destino_indice]["boca_arriba"]

    primera_carta = cartas[0]
    palo_carta, numero_carta = primera_carta

    if len(columna_destino) == 0:
        for carta in cartas:
            columna_destino.append(carta)
            if columna_origen is not None:
                columna_origen.remove(carta)
        return True
    else:
        palo_superior, numero_superior = columna_destino[-1]

        if palo_superior != palo_carta:
            if numero_superior in ESCALERA_VALIDO and ESCALERA_VALIDO[numero_superior] == numero_carta:
                for carta in cartas:
                    columna_destino.append(carta)
                    if columna_origen is not None:
                        columna_origen.remove(carta)
                return True

    return False



def intentar_mover_a_pila(pilas:list
                          ,cartas:list
                          ,palo_destino:str)-> bool:
    """
    Esta funcion acumula las cartas en orden ascendente en las pilas

    """
    # muevo solo de a 1 carta a las pilas
    if cartas is None or len(cartas) != 1:  
        return False

    carta = cartas[0]
    if carta is None:
        return False

    palo_carta, numero_carta = carta

    pila = pilas[palo_destino]
    
    if len(pila) == 0:
        # si la pila esta vacia solo se puede poner 1 carta
        if numero_carta == 1 and palo_carta == palo_destino:
            pila.append(carta)
            return True
        else:
            return False
    else:
        ultima_palo, ultima_numero = pila[-1]

        if palo_carta == palo_destino:
            # pilas escalera
            if ultima_numero == 7 and numero_carta == 10:
                pila.append(carta)
                return True

            elif ultima_numero < 7 and numero_carta == ultima_numero + 1:
                pila.append(carta)
                return True

            elif ultima_numero in [10, 11] and numero_carta == ultima_numero + 1:
                pila.append(carta)
                return True
    return False


####### partida finalizada


def finalizar_partida(pilas: dict) -> bool:
    """
    Esta funcion valida el estado
    de la partida
    """
    for palo in ["oros", "copas", "espadas", "bastos"]:
        if len(pilas[palo]) != 10:
            return False
    return True

##bubble sort

def ordenar_ranking(ranking:list)-> list:
    """
    Esta funcion ordena el ranking de menor a mayor
    """
    for i in range(len(ranking)):
        for j in range(0, len(ranking) - i - 1):
            if ranking[j][1] > ranking[j + 1][1]:  
                ranking[j], ranking[j + 1] = ranking[j + 1], ranking[j]
    return ranking
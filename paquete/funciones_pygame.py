import pygame
from constantes.constantes import *

def dibujar_texto_fijo(ventana: pygame.Surface, texto: pygame.Surface, x: int, y: int) -> None:
    """
    dibujo un texto en una posicion.
    """
    ventana.blit(texto, (x, y))

def dibujar_texto_boton(ventana: pygame.Surface, texto: pygame.Surface, boton: pygame.Rect, x: int = 0, y: int = 0) -> None:
    """
    Dibujo de texto centrado en boton
    """
    ventana.blit(texto, (boton.x + x, boton.y + y))

def dibujar_imagen(ventana: pygame.Surface, imagen: pygame.Surface, x: int, y: int) -> None:
    """
    Dibujo de imagen en la posicion de la ventana
    """
    ventana.blit(imagen, (x, y))

def crear_fuente(nombre_fuente: str, tamaño: int) -> pygame.font.Font:
    """
    Crea y retorna font de pygame
    """
    return pygame.font.SysFont(nombre_fuente, tamaño)

def renderizar_texto(fuente: pygame.font.Font, contenido: str, color: tuple[int, int, int]) -> pygame.Surface:
    """
    Render de un texto con la fuente y color
    """
    return fuente.render(contenido, True, color)

def dibujar_boton(ventana: pygame.Surface, boton: pygame.Rect, color: tuple[int, int, int] = (BLANCO), radio_borde: int = 8) -> None:
    """
    Dibujo para botones de la ventana.
    """
    pygame.draw.rect(ventana, color, boton, border_radius=radio_borde)

def dibujar_tablero(
    ventana: pygame.Surface,
    fondo: pygame.Surface,
    tablero: list,
    mazo: list,
    mazo_visible: list,
    pilas: dict,
    imagenes: dict,
    imagen_oculta: pygame.Surface,
    imagenes_pilas_vacias: dict,
    imagen_recarga_mazo: pygame.Surface,
    carta_seleccionada: list | None,
    musica_pausada: bool,
    imagen_reproducir: pygame.Surface,
    imagen_pausar: pygame.Surface,
    boton_volver: pygame.Rect,
    font_opciones: pygame.font.Font
) -> None:
    """
    Dibujo de los elementos del trablero, fondo, columnas, mazo, pilas y boton de la musica.
    Dibuja todos los elementos del tablero de juego: fondo, columnas, mazo.
    """
    ventana.fill(ROJO)
    ventana.blit(fondo, (0, 0))

    # dibujo de boton para volver
    pygame.draw.rect(ventana, AMARILLO, boton_volver, border_radius=8)
    texto_volver = renderizar_texto(font_opciones, "Volver al menú", ROJO)
    rect_texto_volver = texto_volver.get_rect(center=boton_volver.center)
    ventana.blit(texto_volver, rect_texto_volver)

    # dibujo de columnas
    index = 0
    for columna in tablero:
        x = MARGEN_X + index * (ANCHO_CARTA + ESPACIO_ENTRE_COLUMNAS)
        y = MARGEN_Y

        # columna vacia muestra rectangulo
        if len(columna["boca_abajo"]) == 0 and len(columna["boca_arriba"]) == 0:
            pygame.draw.rect(ventana, (180, 180, 180), (x, y, ANCHO_CARTA, ALTO_CARTA), width=1, border_radius=4)
        else:
            # dibujo cartas boca abajo
            for _ in columna["boca_abajo"]:
                pygame.draw.rect(ventana, (180, 180, 180), (x, y, ANCHO_CARTA, ALTO_CARTA), width=1, border_radius=4)
                ventana.blit(imagen_oculta, (x, y))
                y += SUPERPOSICION_VERTICAL

            # cartas boca arriba dibujo
            for carta in columna["boca_arriba"]:
                imagen = imagenes.get(carta, imagen_oculta)
                ventana.blit(imagen, (x, y))

                # resalto de carta seleccionada
                if carta_seleccionada is not None and carta in carta_seleccionada:
                    color_borde = AMARILLO 
                    grosor_borde = 4
                    pygame.draw.rect(ventana, color_borde, (x, y, ANCHO_CARTA, ALTO_CARTA), width=grosor_borde, border_radius=6)
                else:
                    pygame.draw.rect(ventana, (180, 180, 180), (x, y, ANCHO_CARTA, ALTO_CARTA), width=1, border_radius=4)

                y += SUPERPOSICION_VERTICAL

        index += 1

    # dibujo del mazo
    if len(mazo) > 0:
        ventana.blit(imagen_oculta, (POS_MAZO_X, POS_MAZO_Y))
    else:
        # mazo vacio muestra imagen de recargar
        ventana.blit(imagen_recarga_mazo, (POS_MAZO_X + 20, POS_MAZO_Y + 50))

    # dibujo mazo
    if len(mazo_visible) > 0:
        carta = mazo_visible[-1]
        imagen = imagenes.get(carta, imagen_oculta)
        ventana.blit(imagen, (POS_MAZO_X + ANCHO_CARTA + 20, POS_MAZO_Y))

        # resalto carta seleccionada
        if carta_seleccionada is not None and carta in carta_seleccionada:
            color_borde = AMARILLO 
            grosor_borde = 4
        else:
            color_borde = (180, 180, 180)
            grosor_borde = 1

        pygame.draw.rect(
            ventana, color_borde,
            (POS_MAZO_X + ANCHO_CARTA + 20, POS_MAZO_Y, ANCHO_CARTA, ALTO_CARTA),
            width=grosor_borde,
            border_radius=6
        )

    # dibujo pilas
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for palo, pila in pilas.items():
        x, y = POS_PILAS[palo]
        rect_pila = pygame.Rect(x, y, ANCHO_CARTA, ALTO_CARTA)

        if pila:
            carta = pila[-1]
            imagen = imagenes.get(carta, imagen_oculta)
            ventana.blit(imagen, (x, y))
        else:
            imagen_pila_vacia = imagenes_pilas_vacias.get(palo)
            ventana.blit(imagen_pila_vacia, (x, y))

        # resalto de pila seleccionada
        if rect_pila.collidepoint(mouse_x, mouse_y):
            color_borde = AMARILLO 
        else:
            color_borde = (180, 180, 180)

        pygame.draw.rect(ventana, color_borde, rect_pila, width=1, border_radius=4)

    # boton musica
    superficie_boton = pygame.Surface((BOTON_SIZE_X, BOTON_SIZE_Y), pygame.SRCALPHA)
    ventana.blit(superficie_boton, (POS_BOTON_X, POS_BOTON_Y))
    rect_boton_musica = pygame.Rect(POS_BOTON_X, POS_BOTON_Y, BOTON_SIZE_X, BOTON_SIZE_Y)

    if musica_pausada:
        imagen_rect = imagen_reproducir.get_rect(center=rect_boton_musica.center)
        ventana.blit(imagen_reproducir, imagen_rect)
    else:
        imagen_rect = imagen_pausar.get_rect(center=rect_boton_musica.center)
        ventana.blit(imagen_pausar, imagen_rect)


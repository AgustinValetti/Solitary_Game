import pygame
from constantes.constantes import *

def dibujar_texto_fijo(ventana: pygame.Surface, texto: pygame.Surface, x: int, y: int) -> None:
    ventana.blit(texto, (x, y))

def dibujar_texto_boton(ventana: pygame.Surface, texto: pygame.Surface, boton: pygame.Rect, offset_x: int = 0, offset_y: int = 0) -> None:
    ventana.blit(texto, (boton.x + offset_x, boton.y + offset_y))

def dibujar_imagen(ventana: pygame.Surface, imagen: pygame.Surface, x: int, y: int) -> None:
    """
    Dibuja una imagen en la ventana en la posición (x, y).

    Parámetros:
    - ventana: pygame.Surface -> superficie donde se dibuja.
    - imagen: pygame.Surface -> superficie de la imagen cargada.
    - x: int -> coordenada horizontal.
    - y: int -> coordenada vertical.
    """
    ventana.blit(imagen, (x, y))

def crear_fuente(nombre_fuente: str, tamaño: int) -> pygame.font.Font:
    """
    Crea y devuelve una fuente de Pygame.

    Parámetros:
    - nombre_fuente: str -> nombre de la fuente (por ejemplo, 'Bodoni').
    - tamaño: int -> tamaño de la fuente.

    Retorna:
    - pygame.font.Font -> objeto fuente creado.
    """
    return pygame.font.SysFont(nombre_fuente, tamaño)

def renderizar_texto(fuente: pygame.font.Font, contenido: str, color: tuple[int, int, int]) -> pygame.Surface:
    """
    Renderiza un texto con la fuente y color especificados.

    Parámetros:
    - fuente: pygame.font.Font -> fuente a utilizar.
    - contenido: str -> texto a mostrar.
    - color: tuple[int, int, int] -> color del texto en formato RGB.

    Retorna:
    - pygame.Surface -> superficie renderizada con el texto.
    """
    return fuente.render(contenido, True, color)

def dibujar_boton(ventana: pygame.Surface, boton: pygame.Rect, color: tuple[int, int, int] = (255, 255, 255), radio_borde: int = 8) -> None:
    """
    Dibuja un botón en la ventana.

    Parámetros:
    - ventana: pygame.Surface -> superficie donde se dibuja.
    - boton: pygame.Rect -> rectángulo que representa el botón.
    - color: tuple[int, int, int] -> color del botón (por defecto blanco).
    - radio_borde: int -> radio de redondeo de las esquinas (por defecto 8).
    """
    pygame.draw.rect(ventana, color, boton, border_radius=radio_borde)


def dibujar_tablero(
    ventana, fondo, tablero, mazo, mazo_visible, pilas, imagenes, imagen_oculta,
    imagenes_pilas_vacias, imagen_recarga_mazo, carta_seleccionada, musica_pausada,
    imagen_reproducir, imagen_pausar, boton_volver, font_opciones
):
    ventana.fill((30, 0, 0))
    ventana.blit(fondo, (0, 0))

    # Dibujar botón volver
    pygame.draw.rect(ventana, BLANCO, boton_volver, border_radius=8)
    texto_volver = renderizar_texto(font_opciones, "Volver al menú", NEGRO)
    rect_texto_volver = texto_volver.get_rect(center=boton_volver.center)
    ventana.blit(texto_volver, rect_texto_volver)

    # Dibujar columnas
    index = 0
    for columna in tablero:
        x = MARGEN_X + index * (ANCHO_CARTA + ESPACIO_ENTRE_COLUMNAS)
        y = MARGEN_Y

        if len(columna["boca_abajo"]) == 0 and len(columna["boca_arriba"]) == 0:
            pygame.draw.rect(ventana, (180, 180, 180), (x, y, ANCHO_CARTA, ALTO_CARTA), width=1, border_radius=4)
        else:
            for _ in columna["boca_abajo"]:
                pygame.draw.rect(ventana, (180, 180, 180), (x, y, ANCHO_CARTA, ALTO_CARTA), width=1, border_radius=4)
                ventana.blit(imagen_oculta, (x, y))
                y += SUPERPOSICION_VERTICAL

            for carta in columna["boca_arriba"]:
                imagen = imagenes.get(carta, imagen_oculta)
                ventana.blit(imagen, (x, y))

                if carta_seleccionada is not None and carta in carta_seleccionada:
                    color_borde = (255, 203, 24)
                    grosor_borde = 4
                    pygame.draw.rect(ventana, color_borde, (x, y, ANCHO_CARTA, ALTO_CARTA), width=grosor_borde, border_radius=6)
                else:
                    pygame.draw.rect(ventana, (180, 180, 180), (x, y, ANCHO_CARTA, ALTO_CARTA), width=1, border_radius=4)

                y += SUPERPOSICION_VERTICAL

        index += 1

    # Dibujar mazo
    if len(mazo) > 0:
        ventana.blit(imagen_oculta, (POS_MAZO_X, POS_MAZO_Y))
    else:
        ventana.blit(imagen_recarga_mazo, (POS_MAZO_X + 20, POS_MAZO_Y + 50))

    # Dibujar carta del mazo visible
    if len(mazo_visible) > 0:
        carta = mazo_visible[-1]
        imagen = imagenes.get(carta, imagen_oculta)
        ventana.blit(imagen, (POS_MAZO_X + ANCHO_CARTA + 20, POS_MAZO_Y))

        if carta_seleccionada is not None and carta in carta_seleccionada:
            color_borde = (255, 203, 24)
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

    # Dibujar pilas
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

            if rect_pila.collidepoint(mouse_x, mouse_y):
                color_borde = (255, 203, 24)
            else:
                color_borde = (180, 180, 180)

            pygame.draw.rect(ventana, color_borde, rect_pila, width=1, border_radius=4)

    # Dibujar botón de música
    superficie_boton = pygame.Surface((BOTON_SIZE_X, BOTON_SIZE_Y), pygame.SRCALPHA)
    ventana.blit(superficie_boton, (POS_BOTON_X, POS_BOTON_Y))
    rect_boton_musica = pygame.Rect(POS_BOTON_X, POS_BOTON_Y, BOTON_SIZE_X, BOTON_SIZE_Y)

    if musica_pausada:
        imagen_rect = imagen_reproducir.get_rect(center=rect_boton_musica.center)
        ventana.blit(imagen_reproducir, imagen_rect)
    else:
        imagen_rect = imagen_pausar.get_rect(center=rect_boton_musica.center)
        ventana.blit(imagen_pausar, imagen_rect)

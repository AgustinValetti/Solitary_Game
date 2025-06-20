import pygame
from paquete.baraja import generar_baraja
from paquete.mesa import repartir_tablero
from paquete.funciones_generales import *


# Variables globales
size = [1600, 980]
FPS = 120
COLUMNAS = 7
FILAS_MAX = 15  
ANCHO_CARTA = 120
ALTO_CARTA = 180
MARGEN_X = (size[0] * 0.10) 
MARGEN_Y = 280
ESPACIO_ENTRE_COLUMNAS = 70
SUPERPOSICION_VERTICAL = 25
POS_MAZO_X = (size[0] * 0.10) 
POS_MAZO_Y = 60
#posicion pilas
POS_PILAS = {
    "oros":    (725, 60),
    "copas":   (920, 60),
    "espadas": (1110, 60),
    "bastos":  (1300, 60),
}


# Inicio
pygame.init()

fuente = pygame.font.SysFont("Bodoni", 24)

ventana=pygame.display.set_mode(size)
pygame.display.set_caption("Solitario Game")
reloj = pygame.time.Clock()

# mesa
baraja = generar_baraja()
tablero, mazo = repartir_tablero(baraja)
pilas = inicializar_pilas()
# Carga de recursos
imagenes = {}

imagen_oculta = pygame.image.load("cartas/Dorso.jpg").convert_alpha()
imagen_oculta = redondear_imagen(imagen_oculta, ANCHO_CARTA, ALTO_CARTA)

#mazo
if len(mazo) > 0:
    ventana.blit(imagen_oculta, (POS_MAZO_X,
                                POS_MAZO_Y))
else:
    # rectangulo vacio
    pygame.draw.rect(ventana,
                    (0, 0, 0),
                    (POS_MAZO_X,
                    POS_MAZO_Y,
                    ANCHO_CARTA,
                    ALTO_CARTA))


for carta in baraja:
    ruta = obtener_ruta_imagen(carta)
    imagen = pygame.image.load(ruta).convert_alpha()
    imagen_redonda = redondear_imagen(imagen, ANCHO_CARTA, ALTO_CARTA)
    imagenes[carta] = imagen_redonda

# ciclo main
ejecutar = True
while ejecutar:

    lista_eventos = pygame.event.get()

    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            ejecutar = False    

    #  fondo
    ventana.fill((30, 0, 0))

    # visualizacion sobre el fondo

    for index, columna in enumerate(tablero):
        x = MARGEN_X + index * (ANCHO_CARTA + ESPACIO_ENTRE_COLUMNAS)
        y = MARGEN_Y

        # muestra de carta boca abajo
        for _ in columna["boca_abajo"]:
            #  borde
            pygame.draw.rect(
                ventana, (180, 180, 180),
                (x, y,
                ANCHO_CARTA,
                ALTO_CARTA),
                width=1,
                border_radius=4
            )
            # imagenes ocultas
            ventana.blit(imagen_oculta, (x, y))
            y += SUPERPOSICION_VERTICAL

        for carta in columna["boca_arriba"]:
            imagen = imagenes.get(carta, imagen_oculta)

            # borde
            pygame.draw.rect(
                ventana, (180, 180, 180),
                (x, y,
                ANCHO_CARTA,
                ALTO_CARTA),
                width=1,
                border_radius=4
            )

            # imagen
            ventana.blit(imagen, (x, y))
            y += SUPERPOSICION_VERTICAL


    #mazo
    if len(mazo) > 0:
        ventana.blit(imagen_oculta, (POS_MAZO_X, POS_MAZO_Y))

    #pilas
    # mouse para hover 
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for palo, pila in pilas.items():
        x, y = POS_PILAS[palo]
        rect_pila = pygame.Rect(x, y,
                                ANCHO_CARTA,
                                ALTO_CARTA)

        if pila:
            #muestra la ultima carta de la pila si estan uno arriba de la otra
            carta = pila[-1]  
            imagen = imagenes.get(carta, imagen_oculta)
            ventana.blit(imagen, (x, y))
        else:
            # pilas vacias se muestra un borde sin relleno para dar a entender que ahi se puede colocar una carta
            if rect_pila.collidepoint(mouse_x,mouse_y):
                color_borde = (255, 203, 24)
            else:
                color_borde = (180, 180, 180)
            #
            pygame.draw.rect(
                ventana,
                color_borde,
                rect_pila,
                width=1,
                border_radius=4)


    pygame.display.update()

pygame.quit()

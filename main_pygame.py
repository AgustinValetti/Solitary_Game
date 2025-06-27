import pygame
from globals.variables_globales import *
from paquete.baraja import generar_baraja
from paquete.mesa import repartir_tablero
from paquete.funciones_generales import *

# inicio
pygame.init()

fuente = pygame.font.SysFont("Bodoni", 24)

ventana = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Solitario Game")
reloj = pygame.time.Clock()

# Mesa
baraja = generar_baraja()
tablero, mazo = repartir_tablero(baraja)
pilas = inicializar_pilas()
mazo_visible = []

# carga de recursos
imagenes = {}

##Cartas
for carta in baraja:
    ruta = obtener_ruta_imagen(carta)
    imagen = pygame.image.load(ruta)
    imagen_redonda = redondear_imagen(imagen, ANCHO_CARTA, ALTO_CARTA)
    imagenes[carta] = imagen_redonda

#dorso de cartas

imagen_oculta = pygame.image.load("cartas/Dorso.jpg")
imagen_oculta = redondear_imagen(imagen_oculta, ANCHO_CARTA, ALTO_CARTA)
#imagenes pilas
imagenes_pilas_vacias = {
    "oros": redondear_imagen(pygame.image.load("cartas/oro_vacio.jpeg"), ANCHO_CARTA, ALTO_CARTA),
    "copas": redondear_imagen(pygame.image.load("cartas/copa_vacio.jpeg"), ANCHO_CARTA, ALTO_CARTA),
    "espadas": redondear_imagen(pygame.image.load("cartas/espada_vacio.jpeg"), ANCHO_CARTA, ALTO_CARTA),
    "bastos": redondear_imagen(pygame.image.load("cartas/basto_vacio.jpeg"), ANCHO_CARTA, ALTO_CARTA)
}

for imagen in imagenes_pilas_vacias.values():
    imagen.set_alpha(80)  

# Cargar la imagen de fondo
fondo = pygame.image.load("cartas/fondo.jpg").convert()
fondo = pygame.transform.scale(fondo, (SIZE[0], SIZE[1])) 
fondo.set_alpha(60) 

 



# seleccion de carta
carta_seleccionada = None
origen_seleccion = None
columna_seleccionada = None

# ciclo principal
ejecutar = True

while ejecutar:
    lista_eventos = pygame.event.get()
    
    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            ejecutar = False

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            rect_mazo = pygame.Rect(POS_MAZO_X, POS_MAZO_Y, ANCHO_CARTA, ALTO_CARTA)
            
            if rect_mazo.collidepoint(mouse_x, mouse_y):
                if len(mazo) > 0:
                    mazo_visible.append(mazo.pop())
                else:
                    mazo = mazo_visible[::-1]
                    mazo_visible = []

            else:
                seleccion = detectar_carta_seleccionada(tablero, mazo_visible, pilas, mouse_x, mouse_y)
                
                if seleccion:
                    if carta_seleccionada is None:
                        # primero selecciono
                        if seleccion["origen"] in ["mazo", "mesa"]:
                            carta_seleccionada = seleccion["carta"]
                            origen_seleccion = seleccion["origen"]
                            columna_seleccionada = seleccion["indice"]
                    else:
                        # segundo dirijo 
                        if seleccion["origen"] == "mesa":
                            movido = intentar_mover_a_columna(tablero, columna_seleccionada, carta_seleccionada, seleccion["indice"])

                            if movido:
                                if origen_seleccion == "mazo":
                                    mazo_visible.pop()
                                elif origen_seleccion == "mesa":
                                    tablero[columna_seleccionada]["boca_arriba"].remove(carta_seleccionada)
                                    if len(tablero[columna_seleccionada]["boca_abajo"]) > 0 and len(tablero[columna_seleccionada]["boca_arriba"]) == 0:
                                        tablero[columna_seleccionada]["boca_arriba"].append(tablero[columna_seleccionada]["boca_abajo"].pop())

                                carta_seleccionada = None
                                origen_seleccion = None
                                columna_seleccionada = None
                            else:
                                print("Error.")

                        elif seleccion["origen"] == "pila":
                            movido = intentar_mover_a_pila(pilas, carta_seleccionada, seleccion["indice"])

                            if movido:
                                if origen_seleccion == "mazo":
                                    mazo_visible.pop()
                                elif origen_seleccion == "mesa":
                                    tablero[columna_seleccionada]["boca_arriba"].remove(carta_seleccionada)
                                    if len(tablero[columna_seleccionada]["boca_abajo"]) > 0 and len(tablero[columna_seleccionada]["boca_arriba"]) == 0:
                                        tablero[columna_seleccionada]["boca_arriba"].append(tablero[columna_seleccionada]["boca_abajo"].pop())

                                carta_seleccionada = None
                                origen_seleccion = None
                                columna_seleccionada = None
                            else:
                                print("Error")

                        else:
                            carta_seleccionada = None
                            origen_seleccion = None
                            columna_seleccionada = None
                else:
                    carta_seleccionada = None
                    origen_seleccion = None
                    columna_seleccionada = None

    # Fondo
    ventana.fill((30, 0, 0))
    ventana.blit(fondo, (0, 0))  # Superponer imagen con transparencia


    #tablero - cartas boca arriba - boca abajo 
    for index, columna in enumerate(tablero):
        x = MARGEN_X + index * (ANCHO_CARTA + ESPACIO_ENTRE_COLUMNAS)
        y = MARGEN_Y

        if len(columna["boca_abajo"]) == 0 and len(columna["boca_arriba"]) == 0:
            # muestra rectangulo vacio 
            pygame.draw.rect(
                ventana, (180, 180, 180),
                (x, y, ANCHO_CARTA, ALTO_CARTA),
                width=1,
                border_radius=4
            )
        else:
            for _ in columna["boca_abajo"]:
                pygame.draw.rect(
                    ventana, (180, 180, 180),
                    (x, y, ANCHO_CARTA, ALTO_CARTA),
                    width=1,
                    border_radius=4
                )
                ventana.blit(imagen_oculta, (x, y))
                y += SUPERPOSICION_VERTICAL

            for carta in columna["boca_arriba"]:
                imagen = imagenes.get(carta, imagen_oculta)

                # Primero dibujo la carta
                ventana.blit(imagen, (x, y))

                if carta == carta_seleccionada:
                    # Luego dibujo el borde amarillo encima
                    color_borde = (255, 203, 24)
                    grosor_borde = 4

                    pygame.draw.rect(
                        ventana, color_borde,
                        (x, y, ANCHO_CARTA, ALTO_CARTA),
                        width=grosor_borde,
                        border_radius=6
                    )
                else:
                    # Si no está seleccionada, dibujo el borde gris
                    pygame.draw.rect(
                        ventana, (180, 180, 180),
                        (x, y, ANCHO_CARTA, ALTO_CARTA),
                        width=1,
                        border_radius=4
                    )

                y += SUPERPOSICION_VERTICAL

    # muestra de cartas ocultas
    if len(mazo) > 0:
        ventana.blit(imagen_oculta, (POS_MAZO_X, POS_MAZO_Y))
    else:
        pygame.draw.rect(ventana, (0, 0, 0), (POS_MAZO_X, POS_MAZO_Y, ANCHO_CARTA, ALTO_CARTA))

    # muertra de cartas visibles

    if len(mazo_visible) > 0:
        carta = mazo_visible[-1]
        imagen = imagenes.get(carta, imagen_oculta)

        # dibujo
        ventana.blit(imagen, (POS_MAZO_X + ANCHO_CARTA + 20, POS_MAZO_Y))

        # borde de seleccion
        if carta == carta_seleccionada:
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

        

    # muestra de las pilas
    # muestra de las pilas
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for palo, pila in pilas.items():
        x, y = POS_PILAS[palo]
        rect_pila = pygame.Rect(x, y, ANCHO_CARTA, ALTO_CARTA)

        if pila:
            carta = pila[-1]
            imagen = imagenes.get(carta, imagen_oculta)
            ventana.blit(imagen, (x, y))
        else:
            # Mostrar la imagen correspondiente a la pila vacía
            imagen_pila_vacia = imagenes_pilas_vacias.get(palo)
            ventana.blit(imagen_pila_vacia, (x, y))

            if rect_pila.collidepoint(mouse_x, mouse_y):
                color_borde = (255, 203, 24)
            else:
                color_borde = (180, 180, 180)

            pygame.draw.rect(ventana, color_borde, rect_pila, width=1, border_radius=4)
        

    pygame.display.update()
    reloj.tick(30)

pygame.quit()

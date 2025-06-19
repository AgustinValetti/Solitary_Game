import pygame
from paquete.baraja import generar_baraja
from paquete.mesa import repartir_tablero
from paquete.funciones_generales import obtener_ruta_imagen

# Variables globales
FPS = 120
COLUMNAS = 7
FILAS_MAX = 15  
ANCHO_CARTA = 120
ALTO_CARTA = 160
MARGEN_X = 80
MARGEN_Y = 150
ESPACIO_ENTRE_COLUMNAS = 70
SUPERPOSICION_VERTICAL = 35

# Inicio
pygame.init()
ventana = pygame.display.set_mode((1620, 980))
pygame.display.set_caption("Solitario Game")
reloj = pygame.time.Clock()

# mesa
baraja = generar_baraja()
tablero, mazo = repartir_tablero(baraja)

# Carga de recursos
imagenes = {}
imagen_oculta = pygame.image.load("cartas/Dorso.jpg").convert_alpha()

for carta in baraja:
    ruta = obtener_ruta_imagen(carta)
    imagenes[carta] = pygame.image.load(ruta).convert_alpha()

# ciclo main
ejecutar = True
while ejecutar:

    lista_eventos = pygame.event.get()

    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            ejecutar = False    

    #  fondo
    ventana.fill((30, 0, 0))


    pygame.display.update()

pygame.quit()

import pygame

from constantes.constantes import *
from paquete.baraja import *
from paquete.mesa import *
from paquete.validaciones import *
from paquete.funciones_generales import *
from paquete.funciones_pygame import *
from paquete.estados_juego import *
from paquete.funciones_ranking import *
def main():
    """
    inicializa Pygame, carga recursos, manejo del bucle main
    y cambia entre los diferentes estados del juego.
    """
    # Inicialización de Pygame
    pygame.init()
    pygame.mixer.init()

    # Configuración de la ventana y reloj
    ventana = pygame.display.set_mode(SIZE)
    icono = pygame.image.load("cartas/icono.png")  
    pygame.display.set_icon(icono)
    pygame.display.set_caption("Z E U S - S O L I T A R Y")
    reloj = pygame.time.Clock()

    # Cargar de (musica, imagenes de botones, fondo)
    recursos = cargar_recursos_iniciales()
    
    # titulo y musica
    recursos["efecto_titulo"].play()
    
    
    pygame.mixer.music.load(recursos["musica_tablero"])
    pygame.mixer.music.set_volume(0.05)
    pygame.mixer.music.play(-1)

    # estado del menu
    estado_juego = "menu"

    # rectangulos d elos botones
    botones_menu = {
        "jugar": pygame.Rect(SIZE[0] // 2 - 100, 300, 200, 60),
        "ranking": pygame.Rect(SIZE[0] // 2 - 100, 400, 200, 60),
        "salir": pygame.Rect(SIZE[0] // 2 - 100, 500, 200, 60),
        "volver": pygame.Rect(SIZE[0] - 910, 810, 220, 60) 
    }   

    # archivo de ranking
    archivo_ranking = "ranking.csv"

    # inicializa el archivo de ranking si está vacío o no existe, se abre en modo "r+" 
    # para leer y escribir, si no existe se crea y si no hay lineas se crea con los parametros
    with open(archivo_ranking, "r+") as archivo:
        contenido = archivo.read()
        if contenido == "":
            archivo.write("nombre,puntaje\n")

    # variables del estado de juego para jugando y nombre.
    estado_juego_funciones = {
        "tablero": [],
        "mazo": [],
        "pilas": {},
        "mazo_visible": [],
        "carta_seleccionada": None,
        "origen_seleccion": None,
        "columna_seleccionada": None,
        "musica_pausada": False,
        "puntos": 0,
        "cantidad_click": 0,
        "valor_por_click": 100,
        "nombre_ingresado": "",
        "boton_volver": botones_menu["volver"] # boton de estado volver
    }

    # bucle main
    ejecutar = True
    while ejecutar:
        # eventos
        lista_eventos = pygame.event.get()

        # cambio de estados del juego
        if estado_juego == "menu":
            nuevo_estado = manejar_menu(ventana, lista_eventos, recursos, botones_menu)
            if nuevo_estado == "jugando":
                # resteo del juego cada vez que tocamos volver al menu
                estado_juego_funciones["tablero"], estado_juego_funciones["mazo"] = repartir_tablero(generar_baraja())
                estado_juego_funciones["pilas"] = inicializar_pilas()
                estado_juego_funciones["mazo_visible"] = []
                estado_juego_funciones["carta_seleccionada"] = None
                estado_juego_funciones["origen_seleccion"] = None
                estado_juego_funciones["columna_seleccionada"] = None
                estado_juego_funciones["puntos"] = 0
                estado_juego_funciones["cantidad_click"] = 0
                estado_juego_funciones["musica_pausada"] = False
                pygame.mixer.music.unpause() # loop de musica
            estado_juego = nuevo_estado
        elif estado_juego == "jugando":
            estado_juego = manejar_juego(ventana, lista_eventos, recursos, estado_juego_funciones)
        elif estado_juego == "ranking":
            estado_juego = manejar_ranking(ventana, lista_eventos, recursos, archivo_ranking)
        elif estado_juego == "ingresar_nombre":
            estado_juego = manejar_ingresar_nombre(ventana, lista_eventos, recursos, estado_juego_funciones, archivo_ranking)
        
        # rompe el bucle
        if estado_juego == "salir":
            ejecutar = False

        # refresh de pantalla y fps
        pygame.display.update()
        reloj.tick(30)

    # finaliza el programa 
    pygame.quit()

# si existe el archivo __init__ se ejecuta la funcion main
if __name__ == "__main__":
    main()

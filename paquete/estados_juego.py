import pygame
import csv
from constantes.constantes import *
from paquete.baraja import *
from paquete.mesa import *
from paquete.validaciones import *
from paquete.funciones_generales import *
from paquete.funciones_pygame import *
from paquete.funciones_ranking import *

def cargar_recursos_iniciales() -> dict:
    """
    carga de imagenes y sonidos para el juego
    retorna diccionario con llave y valor, con todo cargado
    """
    recursos = {}

    # musica y sonido
    recursos["efecto_titulo"] = pygame.mixer.Sound("sounds/effecto_titulo.mp3")
    recursos["musica_tablero"] = "sounds/MusicaTablero.mp3"

    # imagenes cartas
    baraja_completa = generar_baraja() 
    recursos["imagenes_cartas"] = {}
    for carta in baraja_completa:
        ruta = obtener_ruta_imagen(carta)
        imagen = pygame.image.load(ruta)
        imagen_redonda = redondear_imagen(imagen, ANCHO_CARTA, ALTO_CARTA)
        recursos["imagenes_cartas"][carta] = imagen_redonda

    # dorso cartas
    recursos["imagen_oculta"] = pygame.image.load("cartas/Dorso_2.jpeg")
    recursos["imagen_oculta"] = redondear_imagen(recursos["imagen_oculta"], ANCHO_CARTA, ALTO_CARTA)

    # rectangulos pilas vacias
    recursos["imagenes_pilas_vacias"] = {
        "oros": redondear_imagen(pygame.image.load("cartas/oro_vacio.jpeg"), ANCHO_CARTA, ALTO_CARTA),
        "copas": redondear_imagen(pygame.image.load("cartas/copa_vacio.jpeg"), ANCHO_CARTA, ALTO_CARTA),
        "espadas": redondear_imagen(pygame.image.load("cartas/espada_vacio.jpeg"), ANCHO_CARTA, ALTO_CARTA),
        "bastos": redondear_imagen(pygame.image.load("cartas/basto_vacio.jpeg"), ANCHO_CARTA, ALTO_CARTA)
    }
    for imagen in recursos["imagenes_pilas_vacias"].values():
        imagen.set_alpha(80)

    # fondo
    recursos["fondo"] = pygame.image.load("cartas/fondo.jpg").convert()
    recursos["fondo"] = pygame.transform.scale(recursos["fondo"], (SIZE[0], SIZE[1]))
    recursos["fondo"].set_alpha(60)

    # imagenes para boto de musica transparencia de png con alpha
    recursos["imagen_reproducir"] = pygame.image.load("sounds/boton_de_play.png").convert_alpha()
    recursos["imagen_pausar"] = pygame.image.load("sounds/pausa.png").convert_alpha()
    recursos["imagen_reproducir"] = pygame.transform.smoothscale(recursos["imagen_reproducir"], (BOTON_SIZE_X - 10, BOTON_SIZE_Y - 10))
    recursos["imagen_pausar"] = pygame.transform.smoothscale(recursos["imagen_pausar"], (BOTON_SIZE_X - 10, BOTON_SIZE_Y - 10))

    # iamgen recarga
    recursos["imagen_recarga_mazo"] = pygame.image.load("cartas/recarga.png").convert_alpha()
    recursos["imagen_recarga_mazo"] = pygame.transform.smoothscale(recursos["imagen_recarga_mazo"], (80, 80))

    return recursos

def manejar_menu(ventana: pygame.Surface, lista_eventos: list, recursos: dict, botones_menu: dict) -> str:
    """
    logica y dibujo menu principal
    """
    ventana.fill((30, 0, 0))
    ventana.blit(recursos["fondo"], (0, 0))

    pygame.draw.rect(ventana, AMARILLO, botones_menu["jugar"], border_radius=8)
    pygame.draw.rect(ventana, AMARILLO, botones_menu["ranking"], border_radius=8)
    pygame.draw.rect(ventana, AMARILLO, botones_menu["salir"], border_radius=8)

    font_titulo = crear_fuente("Bodoni", 90)
    font_opciones = crear_fuente("Bodoni", 40)
    texto_titulo = renderizar_texto(font_titulo, "Z E U S    S O L I T A R Y", AMARILLO)
    texto_jugar = renderizar_texto(font_opciones, "Jugar", ROJO)
    texto_ranking = renderizar_texto(font_opciones, "Ranking", ROJO)
    texto_salir = renderizar_texto(font_opciones, "Salir", ROJO)
    dibujar_texto_fijo(ventana, texto_titulo, 450, 120)
    dibujar_texto_boton(ventana, texto_jugar, botones_menu["jugar"], 60, 18)
    dibujar_texto_boton(ventana, texto_ranking, botones_menu["ranking"], 45, 18)
    dibujar_texto_boton(ventana, texto_salir, botones_menu["salir"], 65, 18)

    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            return "salir"
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if botones_menu["jugar"].collidepoint(mouse_x, mouse_y):
                return "jugando"
            elif botones_menu["ranking"].collidepoint(mouse_x, mouse_y):
                return "ranking"
            elif botones_menu["salir"].collidepoint(mouse_x, mouse_y):
                return "salir"
    return "menu"

def manejar_juego(ventana: pygame.Surface, lista_eventos: list, recursos: dict, estado_juego_funciones: dict) -> str:
    """
    manejo de logica y dibujos para los estados, tablero, movimientos, cambio de estado del juego

    """
    # asigno las varibles con las llaves y valores del diccionario
    tablero = estado_juego_funciones["tablero"]
    mazo = estado_juego_funciones["mazo"]
    pilas = estado_juego_funciones["pilas"]
    mazo_visible = estado_juego_funciones["mazo_visible"]
    carta_seleccionada = estado_juego_funciones["carta_seleccionada"]
    origen_seleccion = estado_juego_funciones["origen_seleccion"]
    columna_seleccionada = estado_juego_funciones["columna_seleccionada"]
    musica_pausada = estado_juego_funciones["musica_pausada"]
    puntos = estado_juego_funciones["puntos"]
    cantidad_click = estado_juego_funciones["cantidad_click"]
    valor_por_click = estado_juego_funciones["valor_por_click"]
    
    # botones
    boton_volver = estado_juego_funciones["boton_volver"]
    rect_boton_musica = pygame.Rect(POS_BOTON_X, POS_BOTON_Y, BOTON_SIZE_X, BOTON_SIZE_Y)

    #font
    font_opciones = crear_fuente("Bodoni", 40)

    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            return "salir"

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # logica de boton volver
            if boton_volver.collidepoint(mouse_x, mouse_y):
                #reinicio si vuelvo al menu
                estado_juego_funciones["tablero"], estado_juego_funciones["mazo"] = repartir_tablero(generar_baraja())
                estado_juego_funciones["pilas"] = inicializar_pilas()
                estado_juego_funciones["mazo_visible"] = []
                estado_juego_funciones["carta_seleccionada"] = None
                estado_juego_funciones["origen_seleccion"] = None
                estado_juego_funciones["columna_seleccionada"] = None
                estado_juego_funciones["puntos"] = 0
                estado_juego_funciones["cantidad_click"] = 0
                return "menu"

            #logica para el boton volver
            if rect_boton_musica.collidepoint(mouse_x, mouse_y):
                if musica_pausada:
                    pygame.mixer.music.unpause()
                    estado_juego_funciones["musica_pausada"] = False
                else:
                    pygame.mixer.music.pause()
                    estado_juego_funciones["musica_pausada"] = True
            #contador de clicks
            estado_juego_funciones["cantidad_click"] += 1 

            # logica para el manejo de clicks en el mazo
            rect_mazo = pygame.Rect(POS_MAZO_X, POS_MAZO_Y, ANCHO_CARTA, ALTO_CARTA)
            if rect_mazo.collidepoint(mouse_x, mouse_y):
                if len(mazo) > 0:
                    mazo_visible.append(mazo.pop())
                else:
                    mazo.extend(mazo_visible[::-1]) # pasa las cartas del mazo visible al mazo
                    mazo_visible.clear() # vacia el mazo visible
                #deseleccion de cartas al tocar el mazo
                estado_juego_funciones["carta_seleccionada"] = None
                estado_juego_funciones["origen_seleccion"] = None
                estado_juego_funciones["columna_seleccionada"] = None
            else:
                # detecta seleccion de carta
                seleccion = detectar_carta_seleccionada(tablero, mazo_visible, pilas, mouse_x, mouse_y)

                if seleccion:
                    if carta_seleccionada is None and seleccion["carta"] is not None:
                        estado_juego_funciones["carta_seleccionada"] = seleccion["carta"]
                        estado_juego_funciones["origen_seleccion"] = seleccion["origen"]
                        estado_juego_funciones["columna_seleccionada"] = seleccion["indice"]
                    else:
                        # movimiento para la carta seleccionada
                        movido = False
                        if seleccion["origen"] == "mesa":
                            movido = intentar_mover_a_columna(tablero, columna_seleccionada, carta_seleccionada, seleccion["indice"])
                        elif seleccion["origen"] == "pila":
                            movido = intentar_mover_a_pila(pilas, carta_seleccionada, seleccion["indice"])

                        if movido:
                            # si el movimiento funciona
                            if origen_seleccion == "mazo":
                                mazo_visible.pop()
                            elif origen_seleccion == "mesa" and columna_seleccionada is not None:
                                for carta_movida in carta_seleccionada:
                                    # valida la carta de la columna antes d emover
                                    if carta_movida in tablero[columna_seleccionada]["boca_arriba"]:
                                        tablero[columna_seleccionada]["boca_arriba"].remove(carta_movida)
                                # cambie la carta que esta abajo a boca arriba
                                if len(tablero[columna_seleccionada]["boca_abajo"]) > 0 and len(tablero[columna_seleccionada]["boca_arriba"]) == 0:
                                    tablero[columna_seleccionada]["boca_arriba"].append(tablero[columna_seleccionada]["boca_abajo"].pop())
                            
                            # verifica si la partida continua
                            if finalizar_partida(pilas):
                                estado_juego_funciones["puntos"] = estado_juego_funciones["cantidad_click"] * estado_juego_funciones["valor_por_click"]
                                return "ingresar_nombre"
                        
                        # deseleccion de carta despues de mover
                        estado_juego_funciones["carta_seleccionada"] = None
                        estado_juego_funciones["origen_seleccion"] = None
                        estado_juego_funciones["columna_seleccionada"] = None
                else:
                    #si se clickea en una carta o lugar que no es valido se deselecciona
                    estado_juego_funciones["carta_seleccionada"] = None
                    estado_juego_funciones["origen_seleccion"] = None
                    estado_juego_funciones["columna_seleccionada"] = None


    # dibujo de tablero
    dibujar_tablero(
        ventana, recursos["fondo"], tablero, mazo, mazo_visible, pilas,
        recursos["imagenes_cartas"], recursos["imagen_oculta"], recursos["imagenes_pilas_vacias"],
        recursos["imagen_recarga_mazo"], carta_seleccionada, musica_pausada,
        recursos["imagen_reproducir"], recursos["imagen_pausar"], boton_volver, font_opciones
    )
    
    return "jugando"

def manejar_ranking(ventana: pygame.Surface, lista_eventos: list, recursos: dict, archivo_ranking: str) -> str:
    """
    logica y dibujo de ranking
    return del estado
    """
    mostrar_ranking(ventana, recursos["fondo"], archivo_ranking)

    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            return "salir"
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                return "menu"
    return "ranking"

def manejar_ingresar_nombre(ventana: pygame.Surface, lista_eventos: list, recursos: dict, estado_juego_vars: dict, archivo_ranking: str) -> str:
    """
    logica y dibujo del nombre del jugador
    return del estado
    """
    nombre_ingresado = estado_juego_vars["nombre_ingresado"]
    puntos = estado_juego_vars["puntos"]

    ventana.fill(ROJO)
    ventana.blit(recursos["fondo"], (0, 0))

    font = pygame.font.SysFont(None, 40)
    ganaste_texto = font.render(f"!Felicidades Ganaste! Puntaje: {puntos}", True, AMARILLO)
    texto_input_label = font.render("Ingresa tu nombre:", True, BLANCO)

    ventana.blit(texto_input_label, (700, 280))
    ventana.blit(ganaste_texto, (600, 200))

    font_input = pygame.font.SysFont(None, 50)
    input_box = pygame.Rect(680, 360, 300, 50)
    pygame.draw.rect(ventana, BLANCO, input_box, 2)

    texto_nombre = font_input.render(nombre_ingresado, True, BLANCO)
    ventana.blit(texto_nombre, (input_box.x + 5, input_box.y + 5))

    texto_confirmar = font.render("Presiona ENTER para confirmar", True, BLANCO)
    ventana.blit(texto_confirmar, (610, 460))

    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            return "salir"
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                if len(nombre_ingresado) > 0:
                    agregar_al_ranking(nombre_ingresado, puntos)
                    estado_juego_vars["nombre_ingresado"] = "" # reinicio
                    return "menu"
            elif evento.key == pygame.K_BACKSPACE:
                estado_juego_vars["nombre_ingresado"] = nombre_ingresado[:-1]
            else:
                # limite de caracteres
                if len(nombre_ingresado) < 15:
                    estado_juego_vars["nombre_ingresado"] = agregar_caracter(nombre_ingresado, evento, 15)
    
    return "ingresar_nombre"

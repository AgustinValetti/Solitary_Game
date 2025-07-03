import pygame
import csv
from constantes.constantes import *
from paquete.baraja import generar_baraja
from paquete.mesa import repartir_tablero
from paquete.validaciones import *
from paquete.funciones_generales import *
from paquete.funciones_pygame import *


#inicio
pygame.init()
pygame.mixer.init()

# musica
musica_pausada = False

# Cargar y reproducir efecto primero
efecto = pygame.mixer.Sound("sounds/effecto_titulo.mp3")
efecto.play()

# Esperar a que termine el efecto
tiempo = pygame.time.wait(int(efecto.get_length() * 0))

# Luego iniciar la música de fondo
pygame.mixer.music.load("sounds/MusicaTablero.mp3")  
pygame.mixer.music.set_volume(0.07)
pygame.mixer.music.play(-1)

ventana = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Z E U S - S O L I T A R Y")
reloj = pygame.time.Clock()

# estado del juego
estado_juego = "menu"

# botones del menu
boton_jugar = pygame.Rect(SIZE[0] // 2 - 100, 300, 200, 60)
boton_ranking = pygame.Rect(SIZE[0] // 2 - 100, 400, 200, 60)
boton_salir = pygame.Rect(SIZE[0] // 2 - 100, 500, 200, 60)
boton_volver = pygame.Rect(SIZE[0] // 2 - 100, 820, 220, 60)  # Esquina superior derecha


# archivo de ranking
archivo_ranking = "ranking.csv"

#nombre usuario
nombre_ingresado = ""

puntos = 0


# open archivo en modo lectura
archivo = open(archivo_ranking, "r+")
contenido = archivo.read()

if contenido == "":
    archivo.write("nombre,puntaje\n")

archivo.close()






# mesa
baraja = generar_baraja()
tablero, mazo = repartir_tablero(baraja)
pilas = inicializar_pilas()
mazo_visible = []

##estado de la partida

estado_de_partida = False

#
cantidad_click = 0
valor_por_click = 100

# carga de recursos
imagenes = {}

##cartas
for carta in baraja:
    ruta = obtener_ruta_imagen(carta)
    imagen = pygame.image.load(ruta)
    imagen_redonda = redondear_imagen(imagen, ANCHO_CARTA, ALTO_CARTA)
    imagenes[carta] = imagen_redonda

#dorso
imagen_oculta = pygame.image.load("cartas/Dorso_2.jpeg")
imagen_oculta = redondear_imagen(imagen_oculta, ANCHO_CARTA, ALTO_CARTA)

# pilas
imagenes_pilas_vacias = {
    "oros": redondear_imagen(pygame.image.load("cartas/oro_vacio.jpeg"), ANCHO_CARTA, ALTO_CARTA),
    "copas": redondear_imagen(pygame.image.load("cartas/copa_vacio.jpeg"), ANCHO_CARTA, ALTO_CARTA),
    "espadas": redondear_imagen(pygame.image.load("cartas/espada_vacio.jpeg"), ANCHO_CARTA, ALTO_CARTA),
    "bastos": redondear_imagen(pygame.image.load("cartas/basto_vacio.jpeg"), ANCHO_CARTA, ALTO_CARTA)
}

for imagen in imagenes_pilas_vacias.values():
    imagen.set_alpha(80)  

# fondo
fondo = pygame.image.load("cartas/fondo.jpg").convert()
fondo = pygame.transform.scale(fondo, (SIZE[0], SIZE[1])) 
fondo.set_alpha(60) 

# iamgenes de boton
imagen_reproducir = pygame.image.load("sounds/boton_de_play.png").convert_alpha()
imagen_pausar = pygame.image.load("sounds/pausa.png").convert_alpha()

imagen_reproducir = pygame.transform.smoothscale(imagen_reproducir, (BOTON_SIZE_X - 10, BOTON_SIZE_Y - 10)) 
imagen_pausar = pygame.transform.smoothscale(imagen_pausar, (BOTON_SIZE_X - 10, BOTON_SIZE_Y - 10))

#imagen mazo recarga
imagen_recarga_mazo = pygame.image.load("cartas/recarga.png").convert_alpha()
imagen_recarga_mazo = pygame.transform.smoothscale(imagen_recarga_mazo,( 80 , 80))


# cartas para la seleccion
carta_seleccionada = None
origen_seleccion = None
columna_seleccionada = None

# ciclo main
ejecutar = True


while ejecutar:
    lista_eventos = pygame.event.get()
    
    if estado_juego == "menu":
        tiempo
        ventana.fill((30, 0, 0))
        ventana.blit(fondo, (0, 0))
        
        pygame.draw.rect(ventana,BLANCO, boton_jugar, border_radius=8)
        pygame.draw.rect(ventana,BLANCO, boton_ranking, border_radius=8)
        pygame.draw.rect(ventana,BLANCO, boton_salir, border_radius=8)

        font_titulo = crear_fuente("Bodoni", 90)
        font_opciones = crear_fuente("Bodoni", 40)
        texto_titulo = renderizar_texto(font_titulo, "Z E U S    S O L I T A R Y", AMARILLO)
        texto_jugar = renderizar_texto(font_opciones, "Jugar", NEGRO)
        texto_ranking = renderizar_texto(font_opciones, "Ranking", NEGRO)
        texto_salir = renderizar_texto(font_opciones, "Salir", NEGRO)
        dibujar_texto_fijo(ventana, texto_titulo, 450, 120)
        dibujar_texto_boton(ventana, texto_jugar, boton_jugar, 60, 18)
        dibujar_texto_boton(ventana, texto_ranking, boton_ranking, 45, 18)
        dibujar_texto_boton(ventana, texto_salir, boton_salir, 65, 18)
        
        for evento in lista_eventos:
            ventana.blit(fondo, (0, 0))
            if evento.type == pygame.QUIT:
                ejecutar = False

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if boton_volver.collidepoint(mouse_x, mouse_y):
                        estado_juego = "menu"
                        carta_seleccionada = None
                        origen_seleccion = None
                        columna_seleccionada = None
                        continue  # Vuelve al menú directamente
                for evento in lista_eventos:
                    if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                if boton_jugar.collidepoint(mouse_x, mouse_y):
                    estado_juego = "jugando"
                    efecto_reproducido = False
                    baraja = generar_baraja()
                    tablero, mazo = repartir_tablero(baraja)
                    pilas = inicializar_pilas()
                    mazo_visible = []
                    carta_seleccionada = None
                    origen_seleccion = None
                    columna_seleccionada = None
                    puntos = 0
                    cantidad_click = 0
                    musica_pausada = False
                    
                    


                            

                elif boton_ranking.collidepoint(mouse_x, mouse_y):
                    estado_juego = "ranking"
                    
                elif boton_salir.collidepoint(mouse_x, mouse_y):
                    ejecutar = False

        pygame.display.update()
        reloj.tick(30)
        continue
    if estado_juego == "jugando":  # Solo mostrar cuando estamos jugando

        
        # Crear y dibujar el texto del botón
        font_opciones = crear_fuente("Bodoni", 40)  # Asegúrate de que esta línea esté aquí
        texto_volver = renderizar_texto(font_opciones, "Volver al menú", NEGRO)
        rect_texto_volver = texto_volver.get_rect(center=boton_volver.center)
        
    if estado_juego == "ranking":
        ventana.fill((ROJO))
        ventana.blit(fondo, (0, 0))
        font = pygame.font.SysFont(None, 40)
        titulo = font.render("Ranking", True, (BLANCO))
        ventana.blit(titulo, (750, 150))

        with open(archivo_ranking, newline='') as archivo:
            lineas = list(csv.reader(archivo))
            
            ranking = []
            for i, fila in enumerate(lineas):
                # Saltamos la primera línea (cabecera) por su posición
                if i == 0:
                    continue
                
                # Verificación de datos
                if len(fila) >= 2:  # Asegura que haya al menos 2 columnas
                    nombre = fila[0].strip() if len(fila[0].strip()) > 0 else ""
                    puntaje = fila[1].strip()
                    
                    if puntaje.isdigit():
                        ranking.append([nombre, int(puntaje)])

        y = 200
        for fila in ranking[:5]:
            texto = font.render(f"{fila[0]}: {fila[1]} puntos", True, (AMARILLO))
            ventana.blit(texto, (650, y))
            y += 50

        font_small = pygame.font.SysFont(None, 30)
        texto_volver = font_small.render("Presiona ESC para volver", True, (AMARILLO))
        ventana.blit(texto_volver, (690, 600))

        for evento in lista_eventos:
            if evento.type == pygame.QUIT:
                ejecutar = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    estado_juego = "menu"

        pygame.display.update()
        reloj.tick(30)
        continue


    #menu
    if estado_juego == "ingresar_nombre":
        
        ventana.fill((ROJO))
        ventana.blit(fondo, (0, 0))
        
        font = pygame.font.SysFont(None, 40)
        ganaste = font.render(f"!Felicidades Ganaste! Puntaje: {puntos}", True,(AMARILLO))
        texto = font.render("Ingresa tu nombre:", True, (BLANCO))

        ventana.blit(texto, (700, 280))

        font_input = pygame.font.SysFont(None, 50)
        input_box = pygame.Rect(680, 360, 300, 50)
        pygame.draw.rect(ventana, (BLANCO), input_box, 2)

        texto_nombre = font_input.render(nombre_ingresado, True, (BLANCO))
        ventana.blit(texto_nombre, (685, 365))
        ventana.blit(ganaste, (600, 200))

        texto_confirmar = font.render("Presiona ENTER para confirmar", True, (BLANCO))
        ventana.blit(texto_confirmar, (610, 460))

        for evento in lista_eventos:
            if evento.type == pygame.QUIT:
                ejecutar = False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and len(nombre_ingresado) > 0:

                    
                    
                    # guardo el csv
                    with open(archivo_ranking, "a", newline='') as archivo:
                        escritor = csv.writer(archivo)
                        escritor.writerow([nombre_ingresado, puntos])

                    estado_juego = "menu"
                    nombre_ingresado = ""

                elif evento.key == pygame.K_BACKSPACE:
                    nombre_ingresado = nombre_ingresado[:-1]

                else:
                    nombre_ingresado = agregar_caracter(nombre_ingresado, evento)
        pygame.display.update()
        reloj.tick(30)
        continue

    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            ejecutar = False
        

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            cantidad_click += 1
            ##mazo
            rect_mazo = pygame.Rect(POS_MAZO_X, POS_MAZO_Y, ANCHO_CARTA, ALTO_CARTA)
            
            texto_volver = renderizar_texto(font_opciones, "Volver al menu", NEGRO)
            rect_texto_volver = texto_volver.get_rect(center=boton_volver.center)
            ventana.blit(texto_volver, rect_texto_volver)
            if boton_volver.collidepoint(mouse_x, mouse_y):
                estado_juego = "menu"
            
            # Puedes reiniciar variables del juego aquí si es necesario
                continue
            if rect_mazo.collidepoint(mouse_x, mouse_y):
                if len(mazo) > 0:
                    mazo_visible.append(mazo.pop())
                else:
                    mazo = mazo_visible[::-1]
                    mazo_visible = []

            else:
                seleccion = detectar_carta_seleccionada(tablero, mazo_visible, pilas, mouse_x, mouse_y)

                if seleccion:
                    if carta_seleccionada is None and seleccion["carta"] is not None:
                        carta_seleccionada = seleccion["carta"]
                        origen_seleccion = seleccion["origen"]
                        columna_seleccionada = seleccion["indice"]
                    else:
                        if seleccion["origen"] == "mesa":
                            movido = intentar_mover_a_columna(tablero, columna_seleccionada, carta_seleccionada, seleccion["indice"])

                            if movido:
                                cantidad_click += 1
                                if origen_seleccion == "mazo":
                                    mazo_visible.pop()
                                elif origen_seleccion == "mesa" and columna_seleccionada is not None:

                                    if len(tablero[columna_seleccionada]["boca_abajo"]) > 0 and len(tablero[columna_seleccionada]["boca_arriba"]) == 0:
                                        tablero[columna_seleccionada]["boca_arriba"].append(tablero[columna_seleccionada]["boca_abajo"].pop())

                                carta_seleccionada = None
                                origen_seleccion = None
                                columna_seleccionada = None

                        elif seleccion["origen"] == "pila":
                            movido = intentar_mover_a_pila(pilas, carta_seleccionada, seleccion["indice"])

                            if movido:
                                if origen_seleccion == "mazo":
                                    mazo_visible.pop()
                                elif origen_seleccion == "mesa" and columna_seleccionada is not None:
                                    
                                    for carta in carta_seleccionada:
                                        tablero[columna_seleccionada]["boca_arriba"].remove(carta)
                                    if len(tablero[columna_seleccionada]["boca_abajo"]) > 0 and len(tablero[columna_seleccionada]["boca_arriba"]) == 0:
                                        tablero[columna_seleccionada]["boca_arriba"].append(tablero[columna_seleccionada]["boca_abajo"].pop())

                                carta_seleccionada = None
                                origen_seleccion = None
                                columna_seleccionada = None
                
                # finaliza el juego
                            if finalizar_partida(pilas):
                                puntos = cantidad_click * valor_por_click
                                estado_juego = "ingresar_nombre"

                                
                                



                        else:
                            carta_seleccionada = None
                            origen_seleccion = None
                            columna_seleccionada = None
                else:
                    carta_seleccionada = None
                    origen_seleccion = None
                    columna_seleccionada = None


            #boton
            rect_boton_musica = pygame.Rect(POS_BOTON_X, POS_BOTON_Y, BOTON_SIZE_X, BOTON_SIZE_Y)
            if rect_boton_musica.collidepoint(mouse_x, mouse_y):
                if musica_pausada:
                    pygame.mixer.music.unpause()
                    musica_pausada = False
                else:
                    pygame.mixer.music.pause()
                    musica_pausada = True

    # Fondo
    ventana.fill((ROJO))
    ventana.blit(fondo, (0,0))


    ### visualizaciones

    # columnas
    index = 0  
    for columna in tablero:
        x = MARGEN_X + index * (ANCHO_CARTA + ESPACIO_ENTRE_COLUMNAS)
        y = MARGEN_Y

        if len(columna["boca_abajo"]) == 0 and len(columna["boca_arriba"]) == 0:
            pygame.draw.rect(
                ventana, (AMARILLO),
                (x, y, ANCHO_CARTA, ALTO_CARTA),
                width=1,
                border_radius=4
            )
        else:
            for _ in columna["boca_abajo"]:
                pygame.draw.rect(
                    ventana, (AMARILLO),
                    (x, y, ANCHO_CARTA, ALTO_CARTA),
                    width=1,
                    border_radius=4
                )
                ventana.blit(imagen_oculta, (x, y))
                y += SUPERPOSICION_VERTICAL

            for carta in columna["boca_arriba"]:
                imagen = imagenes.get(carta, imagen_oculta)
                ventana.blit(imagen, (x, y))

                if carta_seleccionada is not None and carta in carta_seleccionada:
                    color_borde = (ROJO)
                    grosor_borde = 4
                    pygame.draw.rect(
                        ventana, color_borde,
                        (x, y, ANCHO_CARTA, ALTO_CARTA),
                        width=grosor_borde,
                        border_radius=6
                    )
                else:
                    pygame.draw.rect(
                        ventana, (AMARILLO),
                        (x, y, ANCHO_CARTA, ALTO_CARTA),
                        width=1,
                        border_radius=4
                    )

                y += SUPERPOSICION_VERTICAL

        index += 1  

    # mazo
    if len(mazo) > 0:
        ventana.blit(imagen_oculta, (POS_MAZO_X, POS_MAZO_Y))
    else:
        ventana.blit(imagen_recarga_mazo,(POS_MAZO_X + 20, POS_MAZO_Y + 50))
        

    # carta
    if len(mazo_visible) > 0:
        carta = mazo_visible[-1]
        imagen = imagenes.get(carta, imagen_oculta)
        ventana.blit(imagen, (POS_MAZO_X + ANCHO_CARTA + 20, POS_MAZO_Y))

        if carta_seleccionada is not None and carta in carta_seleccionada:
            color_borde = (ROJO)
            grosor_borde = 4
        else:
            color_borde = (AMARILLO)
            grosor_borde = 1

        pygame.draw.rect(
            ventana, color_borde,
            (POS_MAZO_X + ANCHO_CARTA + 20, POS_MAZO_Y, ANCHO_CARTA, ALTO_CARTA),
            width=grosor_borde,
            border_radius=6
        )

    # pilas
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
                color_borde = (ROJO)
            else:
                color_borde = (AMARILLO)

            pygame.draw.rect(ventana, color_borde, rect_pila, width=1, border_radius=4)


        #boton
        superficie_boton = pygame.Surface((BOTON_SIZE_X, BOTON_SIZE_Y), pygame.SRCALPHA)

        ventana.blit(superficie_boton, (POS_BOTON_X, POS_BOTON_Y))
        rect_boton_musica = pygame.Rect(POS_BOTON_X, POS_BOTON_Y, BOTON_SIZE_X, BOTON_SIZE_Y)
        if musica_pausada:
            imagen_rect = imagen_reproducir.get_rect(center=rect_boton_musica.center)
            ventana.blit(imagen_reproducir, imagen_rect)
        else:
            imagen_rect = imagen_pausar.get_rect(center=rect_boton_musica.center)
            ventana.blit(imagen_pausar, imagen_rect)

    
        if estado_juego == "jugando":  # Solo mostrar cuando estamos jugando
    # Dibujar el botón volver
            pygame.draw.rect(ventana, ROJO, boton_volver, border_radius=8)
            
            # Crear y dibujar el texto del botón
            font_opciones = crear_fuente("Bodoni", 40)  # Asegúrate de que esta línea esté aquí
            texto_volver = renderizar_texto(font_opciones, "Volver al menu", AMARILLO)
            rect_texto_volver = texto_volver.get_rect(center=boton_volver.center)
            ventana.blit(texto_volver, rect_texto_volver)

    #Update / fps
    pygame.display.update()
    reloj.tick(30)
    continue

pygame.quit()
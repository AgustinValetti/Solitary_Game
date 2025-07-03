import pygame
import csv
from constantes.constantes import BLANCO, AMARILLO, ROJO

def leer_ranking() -> list:
    """
    Lee el archivo del ranking, y devuelve la lista con nombres y puntajes
    """
    ranking_leido = []
    archivo_ranking_path = "ranking.csv"

    with open(archivo_ranking_path, "r", newline='') as archivo:
        lector = csv.reader(archivo)
        
        # salto de primer linea
        bandera = False
        for fila in lector:
            if not bandera:
                bandera = True 
                continue
            
            if len(fila) >= 2:
                nombre = fila[0].strip()
                puntaje_str = fila[1].strip()
                if puntaje_str.isdigit():
                    ranking_leido.append([nombre, int(puntaje_str)])
    return ranking_leido #lista

def guardar_ranking(ranking_a_guardar: list) -> None:
    """
    Guardo el nuevo puntaje y jugador en el ranking
    """
    with open("ranking.csv", "w", newline='') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["nombre", "puntaje"])
        for fila in ranking_a_guardar: #lista recibida
            escritor.writerow(fila)

def ordenar_ranking_ascendente(ranking_original: list) -> list:
    """
    En esta funcion ordeno el ranking en orden descendente
    """
    ranking_copia = list(ranking_original) # copio la lista
    n = len(ranking_copia)
    for i in range(n):
        for j in range(0, n - i - 1):
            if ranking_copia[j][1] > ranking_copia[j + 1][1]:
                ranking_copia[j], ranking_copia[j + 1] = ranking_copia[j + 1], ranking_copia[j]
    return ranking_copia # copia ordenada

def insertar_en_posicion(ranking_actual: list, nombre: str, puntaje: int) -> list:
    """
    Esta funcion agrega una fila al ranking manteniendo el orden
    """
    nueva_fila = [nombre, puntaje]
    
    # Primero se ordena el ranking
    ranking_ordenado = ordenar_ranking_ascendente(ranking_actual) 
    
    ranking_con_nuevo = []
    insertado = False

    for fila in ranking_ordenado:
        # si el nuevo puntaje es menor que el anterior
        if not insertado and puntaje < fila[1]:
            ranking_con_nuevo.append(nueva_fila)
            insertado = True
        ranking_con_nuevo.append(fila)

    if not insertado: # si el nuevo puntaje es mayor
        ranking_con_nuevo.append(nueva_fila)

    return ranking_con_nuevo 

def agregar_al_ranking(nombre: str, puntaje: int) -> None:
    """
    Esta funcion agrega nombre y puntaje
    """
    ranking_actual = leer_ranking() # nueva lista
    ranking_final = insertar_en_posicion(ranking_actual, nombre, puntaje) 
    guardar_ranking(ranking_final) 

def mostrar_ranking(ventana: pygame.Surface, fondo: pygame.Surface, archivo_ranking: str) -> None:
    """
    Funcion que muestra  ranking en pygame
    """
    ventana.fill(ROJO)
    ventana.blit(fondo, (0, 0))

    # fuentes
    font = pygame.font.SysFont(None, 40)
    titulo = font.render("Ranking", True, AMARILLO)
    ventana.blit(titulo, (750, 150))

    # Leer y ejecuta ee ranking
    ranking_data = leer_ranking()
    
    # ordena el ranking
    ranking_data_ordenada = ordenar_ranking_ascendente(ranking_data)

    # muestro los primeros 5
    y_pos = 200
    count = 0
    for entrada in ranking_data_ordenada: 
        if count >= 5:
            break #rompo
        texto = font.render(f"{entrada[0]}: {entrada[1]} puntos", True, AMARILLO)
        ventana.blit(texto, (650, y_pos))
        y_pos += 50
        count += 1

    # texto para volver
    font = pygame.font.SysFont(None, 30)
    texto_volver = font.render("Presiona ESC para volver", True, AMARILLO)
    ventana.blit(texto_volver, (690, 600))
    
    pygame.display.update()


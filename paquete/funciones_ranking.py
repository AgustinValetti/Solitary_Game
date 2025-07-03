
import pygame
import csv
#lectura del ranking
def leer_ranking()-> list:
    ranking = []
    with open("ranking.csv", "r") as archivo:
        lineas = archivo.readlines()
        for linea in lineas[1:]:
            nombre, puntaje = linea.strip().split(",")
            ranking.append([nombre, int(puntaje)])
    return ranking

#guardado de ranking

def guardar_ranking(ranking:list)-> None:
    with open("ranking.csv", "w") as archivo:
        archivo.write("Nombre,Puntaje\n")  

        for fila in ranking:
            linea = ""
            for i in range(len(fila)):
                linea += str(fila[i])
                if i < (len(fila) - 1):
                    linea += ","
            archivo.write(linea + "\n")

# orden 

def insertar_en_posicion(ranking:list
                         ,nombre:str
                         ,puntaje:int)-> list:
    nueva_fila = [nombre, puntaje]
    nuevo_ranking = []
    insertado = False

    for fila in ranking:
        if not insertado and puntaje > fila[1]:  
            nuevo_ranking.append(nueva_fila)
            insertado = True
        nuevo_ranking.append(fila)

    if not insertado:
        nuevo_ranking.append(nueva_fila)

    return nuevo_ranking

# isnertar al ranking

def agregar_al_ranking(nombre:str
                       ,puntaje:int)-> None:
    ranking = leer_ranking()
    ranking = insertar_en_posicion(ranking, nombre, puntaje)
    guardar_ranking(ranking)


def mostrar_ranking(ventana, fondo, archivo_ranking):
    ventana.fill((255, 0, 0))  # ROJO
    ventana.blit(fondo, (0, 0))
    
    # Configuración de fuentes
    font = pygame.font.SysFont(None, 40)
    titulo = font.render("Ranking", True, (255, 255, 255))  # BLANCO
    ventana.blit(titulo, (750, 150))

    # Leer y procesar archivo de ranking
    with open(archivo_ranking, newline='') as archivo:
        lineas = list(csv.reader(archivo))
        
        ranking = []
        # Saltar la primera línea (cabecera)
        i = 1
        while i < len(lineas):
            fila = lineas[i]
            if len(fila) >= 2:  # Verificar que tenga al menos nombre y puntaje
                nombre = fila[0].strip()
                puntaje = fila[1].strip()
                
                if puntaje.isdigit():
                    ranking.append([nombre, int(puntaje)])
            i += 1
        
        # Ordenamiento manual de menor a mayor
        for j in range(len(ranking)):
            for k in range(len(ranking)-1):
                if ranking[k][1] > ranking[k+1][1]:
                    # Intercambiar posiciones
                    temp = ranking[k]
                    ranking[k] = ranking[k+1]
                    ranking[k+1] = temp

    # Mostrar los primeros 5 resultados
    y_pos = 200
    max_resultados = 5
    contador = 0
    
    while contador < max_resultados and contador < len(ranking):
        entrada = ranking[contador]
        texto = font.render(f"{entrada[0]}: {entrada[1]} puntos", True, (255, 255, 0))  # AMARILLO
        ventana.blit(texto, (650, y_pos))
        y_pos += 50
        contador += 1

    # Texto para volver
    font_small = pygame.font.SysFont(None, 30)
    texto_volver = font_small.render("Presiona ESC para volver", True, (255, 255, 0))  # AMARILLO
    ventana.blit(texto_volver, (690, 600))
    
    pygame.display.update()
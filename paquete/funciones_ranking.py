
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

    
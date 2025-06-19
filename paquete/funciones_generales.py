def mostrar_tablero(tablero):
    """
    toma la matriz resultante de la baraja, 
    y la muestra en formato de tablero.
    """
    
    encabezado = "    "
    for i in range(len(tablero)):
        encabezado += f" C{i+1}   "
    print(encabezado)
    print("   " + "------" * len(tablero))

    # filas maximas
    max_filas = 0
    for columna in tablero:
        cantidad = len(columna["boca_abajo"]) + len(columna["boca_arriba"])
        if cantidad > max_filas:
            max_filas = cantidad

    # muestra x fila
    for fila in range(max_filas):
        linea = f"{fila+1:2}"
        for col in tablero:
            ocultas = len(col["boca_abajo"])
            visibles = len(col["boca_arriba"])
            total = ocultas + visibles

            if fila < ocultas:
                carta = "🃏  "
            elif fila < total:
                idx = fila - ocultas
                palo, numero = col["boca_arriba"][idx]
                carta = f"{palo[:2]}-{numero:02}"
            else:
                carta = "⬛"
            linea += f" {carta} "
        print(linea)



def obtener_ruta_imagen(carta: tuple) -> str:
    """
    Toma una carta, devuelve la ruta de la imagen
    """
    palo_plural, numero = carta

    equivalencias = {
        "oros": "oro",
        "copas": "copa",
        "espadas": "espada",
        "bastos": "basto"
    }

    palo_singular = equivalencias.get(palo_plural, palo_plural)

    nombre_archivo = f"{numero} de {palo_singular}.jpg"
    ruta = f"cartas/{nombre_archivo}"
    return ruta
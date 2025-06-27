

def repartir_tablero(baraja:list):
    """
    Reparte la baraja en 7 columnas
    Devuelve el tablero  7 columnas con cartas boca abajo
    y una boca arriba, y tambien el mazo con las cartas
    """
    tablero = []
    indice = 0

    for col in range(7):
        boca_abajo = baraja[indice : indice + col]
        indice += col
        boca_arriba = [baraja[indice]]
        indice += 1
        columna = {
            "boca_abajo": boca_abajo,
            "boca_arriba": boca_arriba
        }
        tablero.append(columna)

    mazo = baraja[indice:]  # lo que queda
    return tablero, mazo

import random

def generar_baraja(usando_48_cartas:bool=False)-> tuple:
    """
    Esta funcion crea la baraja de lista tupla.
    toma como parametro el valor de False por defecto para las 48 cartas
    y en caso de indicar True, genera la baraja de 40 cartas.
    Retorna una tupla
    """
    palos = ["oros", "copas", "espadas", "bastos"]
    
    if usando_48_cartas:
    #Con 8 y 9
        numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  
    #Sin 8 y 9
    else:
        numeros = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]  
    
    baraja = []
    for palo in palos:
        for numero in numeros:
            baraja.append((palo, numero))
    
    random.shuffle(baraja)
    
    return baraja


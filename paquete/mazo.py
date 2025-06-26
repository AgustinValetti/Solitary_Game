def avanzar_mazo(mazo:list
                 ,pila_mazo_vista:list)-> None:
    """
    Saca una carta del mazo.
    """
    if len(mazo) > 0:
        carta = mazo.pop(0)
        pila_mazo_vista.append(carta)
    else:
        pass
# Variables globales
SIZE = [1600, 980]
FPS = 120
COLUMNAS = 7
FILAS_MAX = 15  
ANCHO_CARTA = 120
ALTO_CARTA = 180
MARGEN_X = (SIZE[0] * 0.10) 
MARGEN_Y = 280
ESPACIO_ENTRE_COLUMNAS = 70
SUPERPOSICION_VERTICAL = 45
POS_MAZO_X = (SIZE[0] * 0.10) 
POS_MAZO_Y = 60
POS_DESCARTE_X = (SIZE[0] * 0.210) 
POS_DESCARTE_Y  = 60
#pos pilas
POS_PILAS = {
    "oros":    (725, 60),
    "copas":   (920, 60),
    "espadas": (1110, 60),
    "bastos":  (1300, 60),
}

#escalera para las columnas / pilas
ESCALERA_VALIDO = {
    12: 11,
    11: 10,
    10: 7,
    7: 6,
    6: 5,
    5: 4,
    4: 3,
    3: 2,
    2: 1
}

#pos boton musica
BOTON_SIZE_X = 60
BOTON_SIZE_Y = 60
POS_BOTON_X =  1500
POS_BOTON_Y = 800
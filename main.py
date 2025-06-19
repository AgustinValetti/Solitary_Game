from paquete.baraja import *
from paquete.mesa import *
from paquete.funciones_generales import *



baraja = generar_baraja()

# muestra
print(obtener_ruta_imagen(("copas", 5)))  
print(obtener_ruta_imagen(("espadas", 12)))  
baraja = generar_baraja(True)
tablero, mazo = repartir_tablero(baraja)

# tablero

tablero = mostrar_tablero(tablero)

print(mazo)

"""
Ejercicio 2: Patrón Iterator
Ingeniería de Software II

Implementa un iterador que almacena una cadena de caracteres
y permite recorrerla en sentido directo y reverso.
"""

class IteradorCadena:
    """
    Implementa el patrón Iterator para recorrer una cadena de caracteres
    en sentido directo y reverso.
    """
    
    def __init__(self, cadena):
        """Inicializa el iterador con la cadena a recorrer."""
        self.cadena = cadena
        self.posicion = 0
        self.direccion = 1  # 1 para directo, -1 para reverso
    
    def iterar_directo(self):
        """Recorre la cadena en sentido directo (de izquierda a derecha)."""
        self.direccion = 1
        self.posicion = 0
        resultado = []
        
        while self.posicion < len(self.cadena):
            caracter = self.cadena[self.posicion]
            resultado.append(caracter)
            self.posicion += 1
        
        return resultado
    
    def iterar_reverso(self):
        """Recorre la cadena en sentido reverso (de derecha a izquierda)."""
        self.direccion = -1
        self.posicion = len(self.cadena) - 1
        resultado = []
        
        while self.posicion >= 0:
            caracter = self.cadena[self.posicion]
            resultado.append(caracter)
            self.posicion -= 1
        
        return resultado
    
    def __iter__(self):
        """Hace que la clase sea iterable (iteración directa por defecto)."""
        self.posicion = 0
        self.direccion = 1
        return self
    
    def __next__(self):
        """Obtiene el siguiente elemento en la iteración actual."""
        if self.direccion == 1:
            if self.posicion >= len(self.cadena):
                raise StopIteration
            caracter = self.cadena[self.posicion]
            self.posicion += 1
            return caracter
        else:
            if self.posicion < 0:
                raise StopIteration
            caracter = self.cadena[self.posicion]
            self.posicion -= 1
            return caracter


def main():
    print("=" * 60)
    print("EJERCICIO 2: Iterator")
    print("=" * 60)
    
    # Probar con diferentes cadenas
    cadenas_prueba = ["Ingenieria", "Python", "Software"]
    
    for cadena in cadenas_prueba:
        print(f"\n--- Probando con: '{cadena}' ---")
        iterador = IteradorCadena(cadena)
        
        # Recorrido directo
        resultado_directo = iterador.iterar_directo()
        print(f"Recorrido directo: {resultado_directo}")
        print(f"Como string: '{''.join(resultado_directo)}'")
        
        # Recorrido reverso
        resultado_reverso = iterador.iterar_reverso()
        print(f"Recorrido reverso: {resultado_reverso}")
        print(f"Como string: '{''.join(resultado_reverso)}'")
    
    # Demostración de uso como iterador nativo de Python
    print("\n--- Demostración de uso como iterador nativo (foreach) ---")
    cadena_ejemplo = "Hola"
    print(f"Cadena: '{cadena_ejemplo}'")
    
    print("Recorrido directo con for:")
    for char in IteradorCadena(cadena_ejemplo):
        print(f"  {char}", end=" ")
    
    print("\n\nRecorrido reverso con for:")
    iterador_rev = IteradorCadena(cadena_ejemplo)
    iterador_rev.direccion = -1
    iterador_rev.posicion = len(cadena_ejemplo) - 1
    for char in iterador_rev:
        print(f"  {char}", end=" ")
    print()


if __name__ == "__main__":
    main()
"""
Ejercicio 1: Patrón Cadena de Responsabilidad
Ingeniería de Software II

Se pasan números del 1 al 100 a través de una cadena de manejadores.
Los números primos son consumidos por ConsumidorPrimos.
Los números pares son consumidos por ConsumidorPares.
"""

class Manejador:
    """
    Clase base abstracta para el patrón Cadena de Responsabilidad.
    Define la interfaz común para todos los manejadores.
    """
    
    def __init__(self):
        self.siguiente = None
    
    def establecer_siguiente(self, manejador):
        """Establece el siguiente manejador en la cadena."""
        self.siguiente = manejador
        return manejador
    
    def manejar(self, numero):
        """
        Método principal que maneja el número o lo pasa al siguiente.
        Retorna True si el número fue consumido, False si no.
        """
        if self._puede_consumir(numero):
            self._consumir(numero)
            return True
        elif self.siguiente:
            return self.siguiente.manejar(numero)
        else:
            return False
    
    def _puede_consumir(self, numero):
        """Método a implementar por las subclases para verificar si consumen el número."""
        raise NotImplementedError
    
    def _consumir(self, numero):
        """Método a implementar por las subclases para consumir el número."""
        raise NotImplementedError


class ConsumidorPrimos(Manejador):
    """Consume números primos."""
    
    def _puede_consumir(self, numero):
        """Verifica si el número es primo."""
        if numero < 2:
            return False
        for i in range(2, int(numero ** 0.5) + 1):
            if numero % i == 0:
                return False
        return True
    
    def _consumir(self, numero):
        """Consume el número primo."""
        print(f"  [PRIMO] El número {numero} fue consumido por ConsumidorPrimos")


class ConsumidorPares(Manejador):
    """Consume números pares."""
    
    def _puede_consumir(self, numero):
        """Verifica si el número es par."""
        return numero % 2 == 0
    
    def _consumir(self, numero):
        """Consume el número par."""
        print(f"  [PAR] El número {numero} fue consumido por ConsumidorPares")


def main():
    print("=" * 60)
    print("EJERCICIO 1: Cadena de Responsabilidad")
    print("=" * 60)
    
    # Configurar la cadena de responsabilidad
    consumidor_pares = ConsumidorPares()
    consumidor_primos = ConsumidorPrimos()
    
    # Establecer el orden: primero verifica pares, luego primos
    consumidor_pares.establecer_siguiente(consumidor_primos)
    
    numeros_no_consumidos = []
    
    print("\nProcesando números del 1 al 100:\n")
    
    for numero in range(1, 101):
        if not consumidor_pares.manejar(numero):
            numeros_no_consumidos.append(numero)
            print(f"  [NO CONSUMIDO] El número {numero} no fue consumido por ningún manejador")
    
    print(f"\n--- Resumen ---")
    print(f"Números no consumidos (impares no primos): {numeros_no_consumidos}")
    print(f"Total no consumidos: {len(numeros_no_consumidos)}")


if __name__ == "__main__":
    main()
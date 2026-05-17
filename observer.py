# ejercicio3_observer.py
"""
Ejercicio 3: Patrón Observer
Ingeniería de Software II

Una serie de clases están suscritas, cada clase espera que su propio ID
(una secuencia arbitraria de 4 caracteres) sea expuesta y emitirá un
mensaje cuando el ID emitido y el propio coinciden.
"""

class Observador:
    """
    Clase base para los observadores.
    Cada observador tiene un ID único de 4 caracteres.
    """
    
    def __init__(self, id_):
        """
        Inicializa el observador con su ID de 4 caracteres.
        
        Args:
            id_: String de exactamente 4 caracteres que identifica al observador
        """
        if len(id_) != 4:
            raise ValueError("El ID debe tener exactamente 4 caracteres")
        self.id = id_
    
    def actualizar(self, id_emitido):
        """
        Método llamado cuando el sujeto emite un ID.
        
        Args:
            id_emitido: El ID que fue emitido
        """
        if self.id == id_emitido:
            print(f"  [!] ¡Coincidencia! Observador con ID '{self.id}' recibió su propio ID emitido")
            return True
        return False


class Sujeto:
    """
    Sujeto que mantiene una lista de observadores y les notifica cuando
    se emite un ID.
    """
    
    def __init__(self):
        self.observadores = []
    
    def suscribir(self, observador):
        """Agrega un observador a la lista de suscriptores."""
        self.observadores.append(observador)
        print(f"  Suscrito observador con ID: {observador.id}")
    
    def desuscribir(self, observador):
        """Remueve un observador de la lista de suscriptores."""
        if observador in self.observadores:
            self.observadores.remove(observador)
            print(f"  Desuscrito observador con ID: {observador.id}")
    
    def emitir_id(self, id_):
        """
        Emite un ID y notifica a todos los observadores.
        
        Args:
            id_: El ID a emitir (debe tener 4 caracteres)
        """
        if len(id_) != 4:
            raise ValueError("El ID emitido debe tener exactamente 4 caracteres")
        
        print(f"\n  Emitiendo ID: '{id_}'")
        coincidencias = 0
        
        for observador in self.observadores:
            if observador.actualizar(id_):
                coincidencias += 1
        
        if coincidencias == 0:
            print(f"  No hubo coincidencias para el ID '{id_}'")


def main():
    print("=" * 60)
    print("EJERCICIO 3: Observer")
    print("=" * 60)
    
    # Crear el sujeto (observable)
    sujeto = Sujeto()
    
    # Crear 4 observadores con IDs específicos de 4 caracteres
    observador1 = Observador("ABC1")
    observador2 = Observador("DEF2")
    observador3 = Observador("GHI3")
    observador4 = Observador("JKL4")
    
    # Suscribir los observadores
    print("\n--- Suscribiendo observadores ---")
    sujeto.suscribir(observador1)
    sujeto.suscribir(observador2)
    sujeto.suscribir(observador3)
    sujeto.suscribir(observador4)
    
    # Emitir 8 IDs (4 que coinciden con IDs existentes y 4 que no)
    ids_a_emitir = ["ABC1", "XYZ9", "DEF2", "MNO5", 
                    "GHI3", "PQR6", "JKL4", "STU7"]
    
    print("\n--- Emitiendo IDs ---")
    print("(Los IDs que coinciden son: ABC1, DEF2, GHI3, JKL4)")
    
    for id_ in ids_a_emitir:
        sujeto.emitir_id(id_)
    
    # Resumen
    print("\n--- Resumen ---")
    print(f"Total de observadores suscritos: {len(sujeto.observadores)}")
    print("IDs de observadores suscritos:", [obs.id for obs in sujeto.observadores])
    print("IDs emitidos:", ids_a_emitir)
    print("IDs que coinciden con observadores: ABC1, DEF2, GHI3, JKL4")


if __name__ == "__main__":
    main()
# IS2_taller_scanner_modificado.py
"""
Ejercicio 4: Modificación del programa scanner con memorias
Ingeniería de Software II

Modifica el programa para que además la secuencia de barrido de radios que tiene
incluya la sintonía de una serie de frecuencias memorizadas tanto de AM como de FM.
Las frecuencias estarán etiquetadas como M1, M2, M3 y M4.
Cada memoria podrá corresponder a una radio de AM o de FM en sus respectivas
frecuencias específicas. En cada ciclo de barrido se barrerán las cuatro memorias.
"""

import os

#*--------------------------------------------------------------------
#* Ejemplo de design pattern de tipo state
#*--------------------------------------------------------------------
"""State class: Base State class"""
class State:
    def scan(self):
        self.pos += 1
        if self.pos == len(self.stations):
            self.pos = 0
        print("Sintonizando... Estación {} {}".format(self.stations[self.pos], self.name))
    
    def scan_memories(self):
        """Método base para escanear memorias - será sobrescrito"""
        pass

#*------- Implementa como barrer las estaciones de AM
class AmState(State):
    def __init__(self, radio):
        self.radio = radio
        self.stations = ["1250", "1380", "1510"]
        self.pos = 0
        self.name = "AM"
        
        # Inicializar memorias AM (valores por defecto)
        self.memories = {
            "M1": None,
            "M2": None,
            "M3": None,
            "M4": None
        }

    def toggle_amfm(self):
        print("Cambiando a FM")
        self.radio.state = self.radio.fmstate
    
    def store_memory(self, memory_id, frequency):
        """Almacena una frecuencia en una memoria específica (solo para AM)"""
        if memory_id in self.memories:
            self.memories[memory_id] = frequency
            print(f"  Memoria {memory_id} guardada: AM {frequency} kHz")
        else:
            print(f"  Error: Memoria {memory_id} no válida. Use M1, M2, M3 o M4")
    
    def scan_memories(self):
        """Escanea todas las memorias AM guardadas"""
        print(f"\n--- Escaneando memorias AM ---")
        memories_ordered = ["M1", "M2", "M3", "M4"]
        for memory_id in memories_ordered:
            freq = self.memories[memory_id]
            if freq is not None:
                print(f"Sintonizando memoria {memory_id}: AM {freq} kHz")
            else:
                print(f"Memoria {memory_id}: Vacía (AM)")
        print("--- Fin escaneo memorias AM ---")

#*------- Implementa como barrer las estaciones de FM
"""Separate class for FM state"""
class FmState(State):
    def __init__(self, radio):
        self.radio = radio
        self.stations = ["81.3", "89.1", "103.9"]
        self.pos = 0
        self.name = "FM"
        
        # Inicializar memorias FM (valores por defecto)
        self.memories = {
            "M1": None,
            "M2": None,
            "M3": None,
            "M4": None
        }

    def toggle_amfm(self):
        print("Cambiando a AM")
        self.radio.state = self.radio.amstate
    
    def store_memory(self, memory_id, frequency):
        """Almacena una frecuencia en una memoria específica (solo para FM)"""
        if memory_id in self.memories:
            self.memories[memory_id] = frequency
            print(f"  Memoria {memory_id} guardada: FM {frequency} MHz")
        else:
            print(f"  Error: Memoria {memory_id} no válida. Use M1, M2, M3 o M4")
    
    def scan_memories(self):
        """Escanea todas las memorias FM guardadas"""
        print(f"\n--- Escaneando memorias FM ---")
        memories_ordered = ["M1", "M2", "M3", "M4"]
        for memory_id in memories_ordered:
            freq = self.memories[memory_id]
            if freq is not None:
                print(f"Sintonizando memoria {memory_id}: FM {freq} MHz")
            else:
                print(f"Memoria {memory_id}: Vacía (FM)")
        print("--- Fin escaneo memorias FM ---")

#*--------- Construye la radio con todas sus formas de sintonía
class Radio:
    def __init__(self):
        self.fmstate = FmState(self)
        self.amstate = AmState(self)
        # Inicialmente en FM
        self.state = self.fmstate

    def toggle_amfm(self):
        self.state.toggle_amfm()

    def scan(self):
        self.state.scan()
    
    def scan_memories(self):
        """Escanea las memorias del estado actual"""
        self.state.scan_memories()
    
    def full_scan_cycle(self):
        """Realiza un ciclo completo: barre AM, FM y todas las memorias"""
        print("\n" + "=" * 50)
        print("INICIANDO CICLO COMPLETO DE BARRIDO")
        print("=" * 50)
        
        # Guardar estado actual
        original_state = self.state
        
        # Barrido completo AM
        print("\n--- Modo AM ---")
        self.state = self.amstate
        # Barrer estaciones AM
        for _ in range(len(self.amstate.stations)):
            self.scan()
        # Barrer memorias AM
        self.amstate.scan_memories()
        
        # Barrido completo FM
        print("\n--- Modo FM ---")
        self.state = self.fmstate
        # Barrer estaciones FM
        for _ in range(len(self.fmstate.stations)):
            self.scan()
        # Barrer memorias FM
        self.fmstate.scan_memories()
        
        # Restaurar estado original
        self.state = original_state
        
        print("\n" + "=" * 50)
        print("CICLO COMPLETO FINALIZADO")
        print("=" * 50)
    
    def show_all_memories(self):
        """Muestra todas las memorias guardadas (AM y FM)"""
        print("\n" + "=" * 40)
        print("MEMORIAS GUARDADAS")
        print("=" * 40)
        
        print("\nMemorias AM:")
        memories_ordered = ["M1", "M2", "M3", "M4"]
        for memory_id in memories_ordered:
            freq = self.amstate.memories[memory_id]
            if freq is not None:
                print(f"  {memory_id}: AM {freq} kHz")
            else:
                print(f"  {memory_id}: Vacía")
        
        print("\nMemorias FM:")
        for memory_id in memories_ordered:
            freq = self.fmstate.memories[memory_id]
            if freq is not None:
                print(f"  {memory_id}: FM {freq} MHz")
            else:
                print(f"  {memory_id}: Vacía")
        print("=" * 40)


def configurar_memorias_ejemplo(radio):
    """Configura un ejemplo de memorias para demostración"""
    print("\n" + "=" * 40)
    print("CONFIGURANDO MEMORIAS DE EJEMPLO")
    print("=" * 40)
    
    # Configurar memorias AM
    print("\nConfigurando memorias AM:")
    radio.amstate.store_memory("M1", "750")
    radio.amstate.store_memory("M2", "980")
    radio.amstate.store_memory("M3", "1210")
    radio.amstate.store_memory("M4", "1530")
    
    # Configurar memorias FM
    print("\nConfigurando memorias FM:")
    radio.fmstate.store_memory("M1", "95.5")
    radio.fmstate.store_memory("M2", "100.3")
    radio.fmstate.store_memory("M3", "104.7")
    radio.fmstate.store_memory("M4", "106.9")


#*---------------------
if __name__ == "__main__":
    os.system("clear" if os.name == "posix" else "cls")
    
    print("\n" + "=" * 60)
    print("EJERCICIO 4: RADIO CON MEMORIAS (M1 a M4)")
    print("=" * 60)
    
    # Crear objeto radio
    print("\nCrea un objeto radio")
    radio = Radio()
    
    # Configurar memorias de ejemplo
    configurar_memorias_ejemplo(radio)
    
    # Mostrar todas las memorias configuradas
    radio.show_all_memories()
    
    # Demostración 1: Comportamiento original (scan normal)
    print("\n" + "=" * 40)
    print("DEMOSTRACIÓN 1: COMPORTAMIENTO ORIGINAL")
    print("=" * 40)
    print("\nAcciones originales: 3 scans FM + toggle + 3 scans AM (repetido 2 veces)")
    
    actions = [radio.scan] * 3 + [radio.toggle_amfm] + [radio.scan] * 3
    actions *= 2
    
    print("\nRecorre las acciones ejecutando la acción, el objeto cambia la interfaz según el estado")
    for action in actions:
        action()
    
    # Demostración 2: Escaneo de memorias
    print("\n" + "=" * 40)
    print("DEMOSTRACIÓN 2: ESCANEO DE MEMORIAS")
    print("=" * 40)
    print("\nEscaneando memorias en modo AM:")
    radio.state = radio.amstate
    radio.scan_memories()
    
    print("\nCambiando a FM y escaneando memorias:")
    radio.toggle_amfm()
    radio.scan_memories()
    
    # Demostración 3: Ciclo completo de barrido
    print("\n" + "=" * 40)
    print("DEMOSTRACIÓN 3: CICLO COMPLETO DE BARRIDO")
    print("=" * 40)
    radio.full_scan_cycle()
    
    # Demostración 4: Modificar una memoria
    print("\n" + "=" * 40)
    print("DEMOSTRACIÓN 4: MODIFICAR UNA MEMORIA")
    print("=" * 40)
    print("\nModificando memoria M1 de FM a 99.9 MHz:")
    radio.fmstate.store_memory("M1", "99.9")
    
    print("\nEscaneando memorias FM nuevamente:")
    radio.fmstate.scan_memories()
    
    print("\n" + "=" * 60)
    print("FIN DEL PROGRAMA")
    print("=" * 60)
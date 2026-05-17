# IS2_taller_memory_modificado.py
"""
Ejercicio 5: Modificación del programa Memory con múltiples estados
Ingeniería de Software II

Modifica el programa para que la clase tenga la capacidad de almacenar
hasta 4 estados en el pasado y pueda recuperar los mismos en cualquier orden.
El método undo deberá tener un argumento adicional indicando si se desea
recuperar el inmediato anterior (0) y los anteriores a él (1,2,3).
"""

import os

#*--------------------------------------------------------------------
#* Design pattern memento, ejemplo modificado para múltiples estados
#*-------------------------------------------------------------------

class Memento:
    """Almacena un estado específico del archivo."""
    
    def __init__(self, file, content):
        self.file = file
        self.content = content
        self.version = 0  # Para identificar la versión
    
    def get_content(self):
        """Retorna el contenido guardado."""
        return self.content
    
    def get_file(self):
        """Retorna el nombre del archivo."""
        return self.file


class FileWriterUtility:
    """Clase principal que maneja el contenido y los mementos."""
    
    def __init__(self, file):
        self.file = file
        self.content = ""
        self.version = 0  # Contador de versiones
    
    def write(self, string):
        """Agrega contenido al archivo."""
        self.content += string
        self.version += 1
        print(f"  [VERSIÓN {self.version}] Se escribió: '{string}'")
        print(f"  Contenido actual: '{self.content}'")
    
    def save(self):
        """
        Guarda el estado actual en un memento.
        Retorna el memento creado.
        """
        memento = Memento(self.file, self.content)
        memento.version = self.version
        print(f"  [SAVE] Guardando versión {self.version}: '{self.content}'")
        return memento
    
    def restore(self, memento):
        """
        Restaura un estado específico desde un memento.
        """
        if memento is None:
            print("  [ERROR] No se puede restaurar un memento nulo")
            return False
        
        self.file = memento.get_file()
        self.content = memento.get_content()
        self.version = memento.version
        print(f"  [RESTORE] Restaurado a versión {self.version}: '{self.content}'")
        return True
    
    def get_content(self):
        """Retorna el contenido actual."""
        return self.content
    
    def get_version(self):
        """Retorna la versión actual."""
        return self.version


class FileWriterCaretaker:
    """
    Clase que mantiene el historial de mementos.
    Modificada para almacenar hasta 4 estados en el pasado.
    """
    
    def __init__(self):
        self.historial = []  # Lista de mementos guardados
        self.MAX_HISTORIAL = 4  # Máximo de estados a guardar
        self.current_index = -1  # Índice del estado actual
    
    def save(self, writer):
        """
        Guarda el estado actual del writer en el historial.
        Solo mantiene los últimos MAX_HISTORIAL estados.
        """
        memento = writer.save()
        
        # Si estamos en un punto medio del historial (después de undo),
        # descartamos los estados futuros
        if self.current_index < len(self.historial) - 1:
            print(f"  [CARETAKER] Descartando estados futuros (índice actual: {self.current_index})")
            self.historial = self.historial[:self.current_index + 1]
        
        # Agregar el nuevo memento
        self.historial.append(memento)
        self.current_index += 1
        
        # Mantener solo los últimos MAX_HISTORIAL estados
        if len(self.historial) > self.MAX_HISTORIAL:
            removed = self.historial.pop(0)
            self.current_index -= 1
            print(f"  [CARETAKER] Historial excedió {self.MAX_HISTORIAL}, se eliminó la versión más antigua")
        
        print(f"  [CARETAKER] Historial actual: {len(self.historial)} estados (índice: {self.current_index})")
    
    def undo(self, writer, index=0):
        """
        Restaura un estado anterior según el índice proporcionado.
        
        Args:
            writer: El objeto FileWriterUtility a restaurar
            index: 0 para el inmediato anterior
                   1 para el anterior al inmediato anterior
                   2, 3 para estados más antiguos
        
        Returns:
            bool: True si se pudo restaurar, False en caso contrario
        """
        if not self.historial:
            print("  [CARETAKER] No hay estados guardados para deshacer")
            return False
        
        # Verificar que el índice sea válido (0-3)
        if index < 0 or index > 3:
            print(f"  [CARETAKER] Error: Índice {index} no válido. Use 0, 1, 2 o 3")
            return False
        
        # Calcular la posición en el historial
        # La posición 0 es el estado más antiguo, current_index es el más reciente
        target_position = self.current_index - (index + 1)
        
        if target_position < 0:
            max_index = self.current_index - 1
            print(f"  [CARETAKER] Error: No hay suficientes estados anteriores. Índice máximo disponible: {max_index}")
            return False
        
        # Obtener el memento objetivo
        target_memento = self.historial[target_position]
        
        if index == 0:
            print(f"\n  [CARETAKER] Deshaciendo al estado inmediato anterior (índice {index})")
        else:
            print(f"\n  [CARETAKER] Deshaciendo al estado anterior con índice {index} (saltando {index} estados)")
        
        print(f"  [CARETAKER] Desde versión {writer.get_version()} a versión {target_memento.version}")
        
        # Restaurar el estado
        if writer.restore(target_memento):
            self.current_index = target_position
            print(f"  [CARETAKER] Nuevo índice actual: {self.current_index}")
            return True
        
        return False
    
    def show_history(self):
        """Muestra el historial completo de estados guardados."""
        print("\n" + "=" * 50)
        print("HISTORIAL DE ESTADOS")
        print("=" * 50)
        
        if not self.historial:
            print("  Historial vacío")
        else:
            for i, memento in enumerate(self.historial):
                marker = " -> ACTUAL" if i == self.current_index else ""
                print(f"  Estado {i}: Versión {memento.version} - '{memento.content[:50]}...' (longitud: {len(memento.content)}){marker}")
        
        print("=" * 50)
    
    def get_history_info(self):
        """Retorna información del historial para debugging."""
        return {
            "total": len(self.historial),
            "current_index": self.current_index,
            "max_size": self.MAX_HISTORIAL
        }


def demostrar_undo_con_indices():
    """Función de demostración que muestra el uso de undo con diferentes índices."""
    
    print("\n" + "=" * 60)
    print("DEMOSTRACIÓN: UNDO CON DIFERENTES ÍNDICES")
    print("=" * 60)
    
    caretaker = FileWriterCaretaker()
    writer = FileWriterUtility("demo.txt")
    
    # Crear múltiples versiones
    print("\n--- Creando 5 versiones diferentes ---")
    writer.write("Primera línea\n")
    caretaker.save(writer)
    
    writer.write("Segunda línea\n")
    caretaker.save(writer)
    
    writer.write("Tercera línea\n")
    caretaker.save(writer)
    
    writer.write("Cuarta línea\n")
    caretaker.save(writer)
    
    writer.write("Quinta línea\n")
    caretaker.save(writer)
    
    # Mostrar historial
    caretaker.show_history()
    
    # Demostrar undo con diferentes índices
    print("\n--- Demostración de undo con diferentes índices ---")
    
    # Undo índice 0 (inmediato anterior)
    input("\nPresione Enter para undo con índice 0...")
    caretaker.undo(writer, 0)
    print(f"Contenido actual: '{writer.get_content()}'")
    
    # Undo índice 1 (saltando un estado)
    input("\nPresione Enter para undo con índice 1...")
    caretaker.undo(writer, 1)
    print(f"Contenido actual: '{writer.get_content()}'")
    
    # Undo índice 2 (saltando dos estados)
    input("\nPresione Enter para undo con índice 2...")
    caretaker.undo(writer, 2)
    print(f"Contenido actual: '{writer.get_content()}'")
    
    # Intentar undo con índice inválido
    print("\n--- Probando índices inválidos ---")
    caretaker.undo(writer, 5)  # Índice fuera de rango


def demostrar_limite_historial():
    """Demuestra que el historial solo guarda los últimos 4 estados."""
    
    print("\n" + "=" * 60)
    print("DEMOSTRACIÓN: LÍMITE DE HISTORIAL (MÁXIMO 4 ESTADOS)")
    print("=" * 60)
    
    caretaker = FileWriterCaretaker()
    writer = FileWriterUtility("limite.txt")
    
    # Crear 6 versiones (más que el límite de 4)
    print("\n--- Creando 6 versiones (excediendo el límite de 4) ---")
    for i in range(1, 7):
        print(f"\n>>> Versión {i}:")
        writer.write(f"Línea {i}\n")
        caretaker.save(writer)
        info = caretaker.get_history_info()
        print(f"  Historial: {info['total']}/{info['max_size']} estados (índice: {info['current_index']})")
    
    # Mostrar historial final (solo deberían estar las últimas 4 versiones)
    caretaker.show_history()


def demostrar_undo_y_nuevos_cambios():
    """Demuestra que al hacer nuevos cambios después de undo se descartan estados futuros."""
    
    print("\n" + "=" * 60)
    print("DEMOSTRACIÓN: UNDO + NUEVOS CAMBIOS (DESCARTA ESTADOS FUTUROS)")
    print("=" * 60)
    
    caretaker = FileWriterCaretaker()
    writer = FileWriterUtility("nuevos.txt")
    
    # Crear versiones iniciales
    print("\n--- Creando versiones 1, 2 y 3 ---")
    writer.write("Versión 1\n")
    caretaker.save(writer)
    
    writer.write("Versión 2\n")
    caretaker.save(writer)
    
    writer.write("Versión 3\n")
    caretaker.save(writer)
    
    caretaker.show_history()
    
    # Hacer undo a la versión 1
    print("\n--- Haciendo undo a la versión 1 (índice 1) ---")
    caretaker.undo(writer, 1)
    caretaker.show_history()
    
    # Hacer nuevos cambios
    print("\n--- Haciendo nuevos cambios (debería descartar versiones 2 y 3) ---")
    writer.write("Nueva versión después de undo\n")
    caretaker.save(writer)
    
    caretaker.show_history()


#*--------------------------------------------------------------------
if __name__ == '__main__':
    os.system("clear" if os.name == "posix" else "cls")
    
    print("\n" + "=" * 60)
    print("EJERCICIO 5: MEMENTO CON MÚLTIPLES ESTADOS (MÁXIMO 4)")
    print("=" * 60)
    
    # Demostración principal
    print("\n" + "=" * 40)
    print("DEMOSTRACIÓN PRINCIPAL")
    print("=" * 40)
    
    print("\nCrea un objeto que gestionará las versiones anteriores")
    caretaker = FileWriterCaretaker()
    
    print("\nCrea el objeto cuyo estado se quiere preservar")
    writer = FileWriterUtility("GFG.txt")
    
    print("\nSe graba algo en el objeto y se salva")
    writer.write("Clase de IS2 en UADER\n")
    print(f"Contenido actual: '{writer.get_content()}'")
    caretaker.save(writer)
    caretaker.show_history()
    
    print("\nSe graba información adicional")
    writer.write("Material adicional de la clase de patrones\n")
    print(f"Contenido actual: '{writer.get_content()}'")
    caretaker.save(writer)
    caretaker.show_history()
    
    print("\nSe graba información adicional II")
    writer.write("Material adicional de la clase de patrones II\n")
    print(f"Contenido actual: '{writer.get_content()}'")
    caretaker.save(writer)
    caretaker.show_history()
    
    print("\nSe graba información adicional III")
    writer.write("Material adicional de la clase de patrones III\n")
    print(f"Contenido actual: '{writer.get_content()}'")
    caretaker.save(writer)
    caretaker.show_history()
    
    print("\n" + "-" * 40)
    print("DEMOSTRANDO UNDO CON DIFERENTES ÍNDICES")
    print("-" * 40)
    
    print("\nSe invoca al undo con índice 0 (inmediato anterior)")
    caretaker.undo(writer, 0)
    print(f"Se muestra el estado actual:")
    print(f"  '{writer.get_content()}'")
    
    print("\nSe invoca al undo con índice 1 (saltando un estado)")
    caretaker.undo(writer, 1)
    print(f"Se muestra el estado actual:")
    print(f"  '{writer.get_content()}'")
    
    print("\nSe invoca al undo con índice 2 (saltando dos estados)")
    caretaker.undo(writer, 2)
    print(f"Se muestra el estado actual:")
    print(f"  '{writer.get_content()}'")
    
    # Ejecutar demostraciones adicionales
    print("\n" + "=" * 60)
    print("DEMOSTRACIONES ADICIONALES")
    print("=" * 60)
    
    demostrar_undo_con_indices()
    demostrar_limite_historial()
    demostrar_undo_y_nuevos_cambios()
    
    print("\n" + "=" * 60)
    print("FIN DEL PROGRAMA")
    print("=" * 60)
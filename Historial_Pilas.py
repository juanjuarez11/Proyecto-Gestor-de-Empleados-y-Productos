from datetime import datetime as dt

# 2. La clase Pila (Estructura dinámica)
class PilaHistorial:
    def __init__(self):
        self.__items = []  # Lista interna privada que actúa como pila

    def push(self, historial_objeto):
        self.__items.append(historial_objeto)

    def pop(self):
        if self.es_vacia():
            return None
        return self.__items.pop()

    def es_vacia(self):
        return len(self.__items) == 0
    
    def ultima_accion(self):
        if self.es_vacia():
            return None
        return self.__items[-1]


    def mostrar_historial(self):
        if self.es_vacia():
            print("El historial está vacío.")
            return
        
        # Invertimos la lectura para mostrar el tope primero
        print("\n=== HISTORIAL (De mas reciente a mas antiguo) ===")
        for registro in reversed(self.__items):
            print(registro)


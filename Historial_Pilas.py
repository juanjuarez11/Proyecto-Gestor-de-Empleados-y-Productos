from datetime import datetime as dt
from pruebaJSON import leer_json as lj, guardar_json as gj
import os

# 2. La clase Pila (Estructura dinámica)
class PilaHistorial:
    def __init__(self):
        self.__items = []

    def push(self, historial_objeto):
        self.__items.append(historial_objeto)

    def cargar_historial_json(self, a_nombre = 'historial.json'):
        if not os.path.exists(a_nombre):
            return
            
        historial_json = lj(a_nombre= 'historial')
        if historial_json and isinstance(historial_json, list):
            for historial in historial_json:
                self.push(historial)
                
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
            
                
    def guardar_json(self, a_nombre="historial"):
        gj(a_nombre, self.__items)
        
def generar_n_h(user, accion):
    fecha = dt.today()
    fecha_formateada = fecha.strftime("%d-%m-%Y %H:%M:%S")
    return f"[{fecha_formateada}] {user}: {accion}"
    
def guardar_accion_historial(historial,user, accion):
    N_historial = generar_n_h(user, accion)
    historial.push(N_historial)
    
def registrar_historial(historial,user, accion):
    
    n_accion = generar_n_h(user= user, accion= accion)
    
    guardar_accion_historial(historial= historial, user= user, accion= n_accion)
    
    historial.guardar_json()
    
historial = PilaHistorial()


historial.mostrar_historial()
from datetime import datetime as dt
from Funciones_Proyecto import leer_json as lj, guardar_json as gj
import os

# 2. La clase Pila (Estructura dinámica)
class PilaHistorial:
    def __init__(self):
        self.__items = []

    def push(self, historial_objeto):
        self.__items.append(historial_objeto)

    def cargar_historial_json(self, A_nombre = 'historial.json'):
        if not os.path.exists(A_nombre):
            return
            
        historial_json = lj(A_nombre= 'historial')
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
            
                
    def guardar_json(self, A_nombre="historial"):
        gj(A_nombre, self.__items)
        
def generar_n_a(user, accion):
    fecha = dt.today()
    fecha_formateada = fecha.strftime("%d-%m-%Y %H:%M:%S")
    return f"[{fecha_formateada}] {user}: {accion}"
    
def guardar_accion_historial(historial,user, accion):
    N_historial = generar_n_a(user, accion)
    historial.push(N_historial)
    
def registrar_historial(historial,user, accion):
    
    guardar_accion_historial(historial= historial, user= user, accion= accion)
    
    historial.guardar_json()
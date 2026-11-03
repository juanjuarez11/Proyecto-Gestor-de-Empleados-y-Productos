from datetime import datetime as dt
from Funciones_Proyecto import leer_json as lj, guardar_json as gj
import os

# Modulo encargado de registrar un historial de acciones mediante las pilas (LIFO)
# Primero en entrar es el ultimo en salir.
# El modulo cuenta con una clase(Con 7 metodos funcionales y 1 metodo constructor)
# Cuenta con tres funciones para un registro pas rapido y sencillo.

#____________________________________________________________________________________________________________________________
# La clase Pila (Estructura dinámica)
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
        
# Funcion encargada de generar el historial con el nombre del user y la accion.
#____________________________________________________________________________________________________________________________
def generar_n_a(user, accion):
    fecha = dt.today()
    fecha_formateada = fecha.strftime("%d-%m-%Y %H:%M:%S")
    return f"[{fecha_formateada}] {user}: {accion}"

# Funcion encargada de generar y guardar ese historial 
#____________________________________________________________________________________________________________________________
def guardar_accion_historial(historial,user, accion):
    N_historial = generar_n_a(user, accion)
    historial.push(N_historial)
    
# Funcion encargada de llamar las de arriba y usar una sola fincion para relizar todo el trebajo
#____________________________________________________________________________________________________________________________
def registrar_historial(historial,user, accion):
    
    guardar_accion_historial(historial= historial, user= user, accion= accion)
    
    historial.guardar_json()
#Funciones de Supervisores:
import json, funciones_menu as fm
empleados = fm.leer_json("credenciales")
def ver_datos(datos):
    for dato in datos:
        print("-" * 30)
        for clave, valor in dato.items():
            print(f"{clave}: {valor}")
    print("-" * 30)

def pedir_datos():
    pass


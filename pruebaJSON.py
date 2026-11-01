import json
from datetime import datetime as dt

def leer_json(A_nombre):
    try:
        with open(f"{A_nombre}.json", "r", encoding= "utf-8") as archivo:
            datos = json.load(archivo)
            return datos
    except json.JSONDecodeError:
            print(f"El archivo {A_nombre} está vacío o corrupto.")
            
    except FileNotFoundError:
        print(f'ERROR: El registro de {A_nombre} no existe!!!')
        return False
    
    except Exception:
        print('Error: Ha ocurrido un error inesperado!!!')
            
def guardar_json(A_nombre, datos):
    try:
        with open(f"{A_nombre}.json", "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")

def imprimir_datos(L_datos, A_nombre):
    print(f'======Datos de {A_nombre}======')
    print('=' * 30)
    contador = 0
    for datos in L_datos:
        contador += 1
        print(f'===={A_nombre} {contador}====')
        print('=' * 30)
        for l,i in datos.items():
            print(f'{l}:{i}')
            print('=' * 30)
            
            
def agregar_dato_n(datos, n_dato):
    datos.append(n_dato)
    return datos


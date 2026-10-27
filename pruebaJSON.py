import json
from datetime import datetime as dt

def leer_json(A_nombre):
    try:
        with open(f"{A_nombre}.json", "r") as archivo:
            datos = json.load(archivo)
            return datos
    except FileNotFoundError:
        print(f'ERROR: El registro de {A_nombre} no existe!!!')
        return False
    except Exception:
        print('Error: Ha ocurrido un error inesperado!!!')
            
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
            
def generar_n_h(usuario, accion):
    fecha = dt.today()
    fecha_formateada = fecha.strftime("%d-%m-%Y %H:%M:%S")
    return f"[{fecha_formateada}] {usuario}: {accion}"
    
def regitrar_accion(historial,usuario, accion):
    N_historial = generar_n_h(usuario, accion)
    historial.push(N_historial)
    
def agregar_dato_n(datos, n_dato):
    datos.append(n_dato)
    return datos


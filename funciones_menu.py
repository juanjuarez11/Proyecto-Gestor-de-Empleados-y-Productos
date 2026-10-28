import json
import Funciones_Proyecto as fp
import Gestion_de_personal as Gp
import datetime as dt
import re

def leer_json(A_nombre):
    try:
        with open(f"{A_nombre}.json", "r") as archivo:
            datos = json.load(archivo)
            return datos
    except FileNotFoundError:
        print("ERROR: El registro no fue encontrado!!")
    except Exception:
        print("Error: Ha ocurrido un error inesperado!")

def escribir_json(A_nombre,datos_escribir):
    try:
        with open(f"{A_nombre}"+".json", "w", encoding="utf-8") as archivo:
            json.dump(datos_escribir, archivo, indent= 4, ensure_ascii=False)
    except FileNotFoundError:
        print("Error: El archivo no fue encontrado.")

def validar_categoria(lista,mensaje):
    while True:
        lista.sort()
        categoria = input(mensaje)
        izquierda = 0
        derecha = len(lista) - 1
        while izquierda <= derecha:
            medio = (izquierda + derecha) // 2
            if lista[medio] == categoria:
                print("Categoria válida")
                return categoria
            elif lista[medio] < categoria:
                izquierda = medio + 1
            else:
                derecha = medio - 1
        print("La categoria ingresada no es válida.")
        return validar_categoria(lista,mensaje)

def es_cedula_valida(cedula):
    formato = r"^[0-9]{3}-[0-9]{6}-[0-9]{4}[A-HJ-NP-Y]$"
    return bool(re.fullmatch(formato, cedula))

def validar_imei(mensaje, objeto):
    if objeto:
        while True:
            imei=input(mensaje)
            if all(c.isdigit() for c in imei) and len(imei)==15:
                return imei
            else:
                print('Solo se aceptan numeros y guiones para el carnet!!!')
    else:
        print('\nNo hay registros por el momento!!!')
        return False


def validar_precio():
    while True:
        try:
            precio = fp.decimales("Ingrese el precio del producto: ")
            if precio > 0:
                return precio
            else:
                print("Debe ingresar un precio mayor a 0.")
        except ValueError:
            print("Debe ingresar un valor decimal")

def validar_cantidad():
    while True:
        try:
            cantidad = fp.valor_numerico("Ingrese el stock del producto: ")
            if cantidad > 0:
                return cantidad
            else:
                print("Debe ingresar un stock mayor a 0.")
        except ValueError:
            print("Debe ingresar un valor entero.")
    

def verificar_id_producto_existencia(productos,mensaje):
    while True:
        id_producto=validar_imei(objeto=productos,mensaje=mensaje)
        if all(c.isdigit() for c in id_producto) and id_producto != '':
            existe= any(producto.get("imei")==id_producto for producto in productos)
        
            if existe:
                print("ID ya registrado.")
            else:
                return id_producto
        else:
            print('Solo se aceptan numeros para el ID y no puede estar vacio!!!')



def buscar_id_producto(productos, mensaje):
    if not productos:
        return None
    while True:
        id_producto = validar_imei(objeto=productos, mensaje=mensaje)
        if id_producto is None:
            return None
        producto_encontrado = next((p for p in productos if p["imei"] == id_producto), None)
        
        if producto_encontrado is not None:
            print("¡ID encontrado con éxito.!")
            return producto_encontrado
        else:
            print("ID no encontrado.")
        
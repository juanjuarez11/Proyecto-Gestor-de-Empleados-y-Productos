import json
import Funciones_Proyecto as fp
import Gestion_de_personal as Gp
import datetime as dt
import re, random, string

categorias = ["Celular","Laptop","Computadora de Escritorio","Teclado Alambrico",
              "Teclado Inalambrico","Mouse Alambrico","Mouse Inalambrico"]

marcas_celulares = ["Samsung","Apple","Xiaomi","Google","Huawei","Motorola"]
marcas_laptops_escritorio = ["Lenovo","HP","Dell","Apple","ASUS","MSI"]
marcas_teclados = ["Logitech","Microsoft","Keychron","Razer","Corsair","Redragon","VSG"]
marcas_mouses = ["Logitech","Microsoft","Logitech G","Razer","Corsair","Redragon","SteelSeries"]
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

def buscar_categoria(lista,elemento):
    lista_ordenada = sorted(lista)
    izquierda = 0
    derecha = len(lista) - 1
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        if lista_ordenada[medio].lower() == elemento.lower():
            return lista_ordenada[medio]
        elif lista_ordenada[medio].lower() < elemento.lower():
            izquierda = medio + 1
        else:
            derecha = medio - 1
    return None

def es_categoria_valida(categoria):
    return buscar_categoria(categorias, categoria)

def obtener_marcas_por_categoria(categoria):
    cat = categoria
    
    if cat == "Celular":
        return marcas_celulares
    elif cat == "Laptop" or cat == "Computadora de Escritorio":
        return marcas_laptops_escritorio
    elif cat == "Teclado Alambrico" or cat == "Teclado Inalambrico":
        return marcas_teclados
    elif cat == "Mouse Alambrico" or cat =="Mouse Inalambrico":
        return marcas_mouses
    else:
        return []

def es_marca_valida_para_categoria(categoria, marca):
    lista_marcas = obtener_marcas_por_categoria(categoria)
    if not lista_marcas:
        return False
    else:
        for i in lista_marcas:
            if i == marca:
                return True
    return buscar_categoria(lista_marcas,"Ingrese la categoria: ")

def es_cedula_valida(cedula):
    formato = r"^[0-9]{3}-[0-9]{6}-[0-9]{4}[A-HJ-NP-Y]$"
    return bool(re.fullmatch(formato, cedula))

def asignar_imei():
    numeros = str(string.digits)
    imei = ""
    for i in range(1,16):
        imei+=random.choice(numeros)
    return imei


def validar_precio(mensaje="Ingrese el precio: "):
    while True:
        try:
            p = float(input(mensaje))
            if p > 0:
                return p
        except ValueError:
            return False

def validar_cantidad(mensaje="Ingrese la cantidad: "):
    while True:
        try:
            c = int(input(mensaje))
            if c > 0:
                return c
        except ValueError:
            return False

def asignar_cp(lista):
    codigo_unico = len(lista)+1
    return str(codigo_unico)

        
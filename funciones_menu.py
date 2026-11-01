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

#Manejo de Archivos JSON
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

#Datos de Productos:
def asignar_cp(lista):
    codigo_unico = int(lista[-1]["codigo_unico"]) + 1
    return str(codigo_unico)

def asignar_imei():
    numeros = str(string.digits)
    imei = ""
    for i in range(1,16):
        imei+=random.choice(numeros)
    return imei

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
    resultado = buscar_categoria(lista_marcas,marca)
    return resultado is not None

def validar_precio(p):
    try:
        precio = float(p)
        return precio > 0
    except ValueError:
        return False

def validar_cantidad(c):
    try:
        cantidad = int(c)
        return cantidad > 0
    except ValueError:
        return False

def buscar_producto_cu(productos,cu_buscar):
    for p in productos:
        if p.get("codigo_unico") == cu_buscar:
            return p
    return None

#Calculo de ventas:
def es_cedula_valida(cedula):
    formato = r"^[0-9]{3}-[0-9]{6}-[0-9]{4}[A-HJ-NP-Y]$"
    return bool(re.fullmatch(formato, cedula))

def pedir_y_validar_cedula(mensaje="Ingrese la cédula del cliente: "):
    while True:
        cedula = input(mensaje)
        if es_cedula_valida(cedula):
            return cedula
        else:
            print("Formato de cédula no válido. Intente nuevamente.")

def calcular_venta(producto, cantidad_vendida):
    precio = float(producto.get("precio"))
    subtotal = precio * cantidad_vendida

    return {"codigo":producto.get("codigo_unico"),
            "imei":producto.get("imei"),
            "modelo":producto.get("modelo"),
            "marca":producto.get("marca"),
            "precio":precio,
            "cantidad_vendida":cantidad_vendida,
            "subtotal":subtotal
            }

def descontar_inventario(producto,cant_vender):
    producto["stock"] -=cant_vender

#Actualización de datos de Productos:
def actualizar_datos_productos(productos,c_u,opcion,nuevo_valor):
    producto = buscar_producto_cu(productos,c_u)
    if not producto:
        return False
    match opcion:
        case 1:
            producto["modelo"] = str(nuevo_valor).strip()
        case 2:
            producto["precio"] = float(nuevo_valor)
        case 3:
            producto["stock"] = int(nuevo_valor)
        case _:
            return False
    escribir_json("productos",productos)
    return True

#Guardar datos de productos
def guardar_nuevo_producto(productos, c_p, imei, modelo, categoria, marca, precio, stock):
    nuevo_producto = {
        "codigo_unico": c_p,
        "imei": imei,
        "modelo": modelo,
        "categoria": categoria.capitalize(),
        "marca": marca.capitalize(),
        "precio": precio,
        "stock": stock
    }
    productos.append(nuevo_producto)
    escribir_json("productos", productos)
    return nuevo_producto

#Obtener datos de Arqueo:
def obtener_datos_arqueo():
    historial_ventas = leer_json("ventas") or []
    total_general = sum(venta.get("total",0.0)for venta in historial_ventas)
    return historial_ventas,total_general

#Eliminar Productos:
def eliminar(productos,codigo_unico):
    producto_eliminar = None
    for i in productos:
        if i["codigo_unico"] == codigo_unico:
            producto_eliminar = i
            break

    if producto_eliminar:
        productos.remove(producto_eliminar)
        escribir_json("productos",productos)
        return True
    return False
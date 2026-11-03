import json
import datetime as dt
import re, random, string

categorias = ["Celular","Laptop","Computadora de Escritorio","Teclado Alambrico",
              "Teclado Inalambrico","Mouse Alambrico","Mouse Inalambrico"]

marcas_celulares = ["Samsung","Apple","Xiaomi","Google","Huawei","Motorola"]
marcas_laptops_escritorio = ["Lenovo","HP","Dell","Apple","ASUS","MSI"]
marcas_teclados = ["Logitech","Microsoft","Keychron","Razer","Corsair","Redragon","VSG"]
marcas_mouses = ["Logitech","Microsoft","Logitech G","Razer","Corsair","Redragon","SteelSeries"]

#Manejo de Archivos JSON:
#Carga y lee los datos almacenados en los archivos JSON del sistema.
def leer_json(A_nombre):
    try:
        with open(f"{A_nombre}.json", "r") as archivo:
            datos = json.load(archivo)
            return datos
    except FileNotFoundError:
        print("ERROR: El registro no fue encontrado!!")
    except Exception:
        print("Error: Ha ocurrido un error inesperado!")

#Guarda la información actualizada en formato JSON con codificación UTF-8.
def escribir_json(A_nombre,datos_escribir):
    try:
        with open(f"{A_nombre}"+".json", "w", encoding="utf-8") as archivo:
            json.dump(datos_escribir, archivo, indent= 4, ensure_ascii=False)
    except FileNotFoundError:
        print("Error: El archivo no fue encontrado.")

#Datos de Productos:
#Genera de forma consecutiva el código único para un nuevo producto.
def asignar_cp(lista):
    codigo = int(lista[-1]["codigo_unico"]) + 1
    return str(codigo)

#Genera un código IMEI aleatorio de 15 dígitos.
def asignar_imei():
    numeros = str(string.digits)
    imei = ""
    print(len(imei))
    for i in range(1,16):
        imei+=random.choice(numeros)
    return imei

#Realiza una búsqueda binaria para encontrar un dato específico.
def busqueda_binaria(lista,elemento):
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

#Verifica si una categoría existe dentro de las permitidas.
def es_categoria_valida(categoria):
    return busqueda_binaria(categorias, categoria)

#Retorna la lista de marcas que corresponden a una categoría dada.
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

#Comprueba mediante búsqueda binaria si una marca pertenece legítimamente a la categoría.
def es_marca_valida_para_categoria(categoria, marca):
    lista_marcas = obtener_marcas_por_categoria(categoria)
    if not lista_marcas:
        return False
    resultado = busqueda_binaria(lista_marcas,marca)
    return resultado is not None

#Valida que el precio ingresado sea un número flotante mayor a cero.
def validar_precio(p):
    try:
        precio = float(p)
        return precio > 0
    except ValueError:
        return False

#Comprueba que la cantidad o stock sea un número entero mayor a cero.
def validar_cantidad(c):
    try:
        cantidad = int(c)
        return cantidad > 0
    except ValueError:
        return False

#Busca y retorna un producto específico del inventario usando su código único.
def buscar_producto_cu(productos,cu_buscar):
    for p in productos:
        if p.get("codigo_unico") == cu_buscar:
            return p
    return None

#Calculo de ventas:

#Crea un número correlativo de factura o garantía formateado con ceros a la izquierda (ej. F-001).
def asignar_num(lista,letra):
    if not lista:
        num = 1
    else:
        num = len(lista) + 1
    return f"{letra.upper()}-{num:03d}"

#Calcula la fecha de vencimiento de la garantía sumando días mediante timedelta según la categoría del producto.
def calcular_garantia(categoria):
    fecha_actual = dt.datetime.now()
    if categoria in ["Celular","Laptop","Computadora de Escritorio"]:
        dias_garantia = 360 
    elif categoria in ["Teclado Alambrico","Teclado Inalambrico","Mouse Alambrico","Mouse Inalambrico"]:
        dias_garantia = 7
    else:
        dias_garantia = 30
    fecha_vencimiento = fecha_actual + dt.timedelta(days = dias_garantia)
    return (fecha_actual.strftime("%Y-%m-%d"), fecha_vencimiento.strftime("%Y-%m-%d"))

#Valida mediante expresiones regulares que el formato de la cédula sea correcto.
def es_cedula_valida(cedula):
    formato = r"^[0-9]{3}-[0-9]{6}-[0-9]{4}[A-HJ-NP-Y]$"
    return bool(re.fullmatch(formato, cedula))

#Solicita e insiste en el ingreso de una cédula válida por consola.
def pedir_y_validar_cedula(mensaje="Ingrese la cédula del cliente: "):
    while True:
        cedula = input(mensaje)
        if es_cedula_valida(cedula):
            return cedula
        else:
            print("Formato de cédula no válido. Intente nuevamente.")

#Calcula los subtotales y construye el diccionario con los datos del ítem vendido.
def calcular_venta(producto, cantidad_vendida,fecha_vencimiento):
    precio = float(producto.get("precio"))
    subtotal = precio * cantidad_vendida

    return {"codigo":producto.get("codigo_unico"),
            "fecha_garantia":fecha_vencimiento,
            "imei":producto.get("imei"),
            "modelo":producto.get("modelo"),
            "marca":producto.get("marca"),
            "precio":precio,
            "cantidad_vendida":cantidad_vendida,
            "subtotal":subtotal
            }

#Actualiza y reduce el stock del producto dentro del inventario.
def descontar_inventario(producto,cant_vender):
    producto["stock"] -=cant_vender

#Actualización de datos de Productos:
#Modifica y persiste los cambios de un producto en el JSON.
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
#Agrega un nuevo producto estructurado al inventario y lo guarda en el archivo.
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
#Lee el historial de ventas y calcula el total general acumulado.
def obtener_datos_arqueo():
    historial_ventas = leer_json("ventas") or []
    total_general = sum(venta.get("total",0.0)for venta in historial_ventas)
    return historial_ventas,total_general

#Eliminar Productos:
#Remueve un producto del inventario basándose en su código único.
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
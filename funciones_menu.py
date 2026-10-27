import json
import Funciones_Proyecto as fp
import Gestion_de_personal as Gp
import datetime as dt

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
        print("ERROR: El registro de empleados no existe!")
    except Exception:
        print("Error: Ha ocurrido un error inesperado!")

productos = leer_json("celulares")
def visualizar_inventario(datos):
    print("="*35)
    print(" "*8,"VISUALIZAR INVENTARIO")
    for dato in datos:
        print("="*35)
        for c,v in dato.items():
            print(f"{c}: {v}")

def validar_categoria(lista,mensaje):
    while True:
        lista_ordenada = sorted(lista)
        categoria = input(mensaje)
        izquierda = 0
        derecha = len(lista_ordenada) - 1
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
categoria = validar_categoria(categorias,"Ingrese la categoria: ")
def cambiar_dato():
    print("="*35)
    print("CAMBIAR DATOS DE UN PRODUCTO")

    try:
        producto_buscar = buscar_id_producto(productos,"Ingrese el ID del producto que desea modificar: ")
        
        if producto_buscar:
            print(f"\nProducto encontrado: {producto_buscar["modelo"]}")
            print("¿Qué dato desea modificar?")
            print("1. Modelo")
            print("2. Precio")
            print("3. Cantidad")
            print("4. Marca")
            print("5. Categoria")
            opcion_mod = fp.valor_numerico("Seleccione una opción (1-4): ")

            match opcion_mod:
                case 1:
                    nuevo_modelo = fp.validar_nombre("Ingrese el nuevo modelo: ").strip().title()
                    producto_buscar["modelo"] = nuevo_modelo
                case 2:
                    nuevo_precio = validar_precio()
                    producto_buscar["precio"] = nuevo_precio
                case 3:
                    nueva_cantidad = validar_cantidad()
                    producto_buscar["cantidad"] = nueva_cantidad
                case 4:
                    nueva_marca = input("Ingrese la nueva marca: ").strip().title()
                    producto_buscar["marca"] = nueva_marca
                
                case 5:
                    nueva_categoria = validar_categoria(categorias,"Ingrese la nueva categoria: ")
                    producto_buscar["categoria"] = nueva_categoria

                case _:
                    print("Opción no válida. No se hicieron cambios.")
            escribir_json("productos",productos)
            print("Datos actualizados éxitosamente!!")
            
    except Exception as e:
        print(f"Error: {e}")

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

def escribir_json(A_nombre,datos_escribir):
    try:
        with open(f"{A_nombre}"+".json", "w", encoding="utf-8") as archivo:
            json.dump(datos_escribir, archivo, indent= 4, ensure_ascii=False)
    except FileNotFoundError:
        print("Error: El archivo no fue encontrado.")

emp = [
    {
        "modelo": "Chalino",
        "correo": "Dargs9009 @gmail", 
        "carnet": "6B5F0535",
        "cargo": "supervisor",
        "salario": "22000",
        "estado": "activo"
    },
    {
        "modelo": "Barbanegra",
        "correo": "Barbon9@gmail", 
        "carnet": "5556262",
        "cargo": "empleado",
        "salario": "12000",
        "estado": "activo"
    }
]

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

def agregar_productos():
    try:
        print("="*30)
        print("AGREGAR PRODUCTOS")
        cant = fp.valor_numerico("Cuántos productos desea agregar?: ")
            
        for i in range(1, cant+1):
            print(f"Producto {i}:")

            imei_prod =verificar_id_producto_existencia(productos,"Ingrese el IMEI del producto: ")
        
            modelo = input("Modelo: ").title()

            precio = validar_precio()

            cantidad = validar_cantidad()
            marca = input("Marca: ").title()
            categoria = input("Categoria: ").title()

            producto = {
                "imei": imei_prod,
                "modelo": modelo,
                "precio": precio,
                "cantidad": cantidad,
                "marca": marca,
                "categoria":categoria}
            productos.append(producto)

        escribir_json("productos",productos)
        print("PRODUCTOS AGREGADOS CON EXITO")
        print("="*30)
    except Exception as e:
        print(f"Error: {e}")

def imprimir_factura(detalle_venta, total_general, fecha):
    print("\n" + "="*55)
    print(" "*18, "FACTURA DE VENTA")
    print(f" Fecha y hora: {fecha}")
    print("="*55)
    print(f"{'PRODUCTO':<20} | {'CANT':<5} | {'PRECIO':<10} | {'SUBTOTAL':<10}")
    print("-" * 55)
    
    for item in detalle_venta:
        modelo = item["modelo"]
        marca = item["marca"]
        cant = item["cantidad_vendida"]
        precio = item["precio"]
        subtotal = item["subtotal"]
        print(f"{marca} | {modelo:<20} | {cant:<5} | C${precio:<9.2f} | C${subtotal:<9.2f}")
        
    print("-" * 55)
    print(f"TOTAL A PAGAR: C${total_general:.2f}")
    print("="*55)
    print("¡GRACIAS POR SU COMPRA!")
    print("="*55 + "\n")

def realizar_venta(productos):
    print("="*35)
    print(" "*9,"REALIZAR VENTA")
    print("="*35)
    detalle_venta = []
    total_venta = 0
    continuar = True
    nombre_cliente = fp.validar_nombre("Ingrese el modelo del cliente: ")
    
    while continuar:
        producto = buscar_id_producto(productos,"Ingrese el ID del producto a vender: ")

        if producto is None:
            break

        imei_prod = producto["imei"]
        modelo = producto["modelo"]
        precio = producto["precio"]
        cantidad = producto["cantidad"]
        print(f"Producto: {modelo} | Precio: C${precio} | Existencias actuales: {cantidad}")

        cant_vender = fp.valor_numerico("Cuantas unidades desear vender?: ")
        if cant_vender <= 0:
            print("Error. Ese cantidad no es válida")
        elif cant_vender > producto["cantidad"]:
            print(f"Error: No hay suficiente stock. Unidades disponibles {producto["cantidad"]}")
            
        else:
            producto["cantidad"] -= cant_vender
            subtotal = cant_vender * precio
            total_venta += subtotal
            
            producto_vendido = {"imei":imei_prod,
                                "modelo":modelo,
                                "precio":precio,
                                "cantidad_vendida":cant_vender,
                                "subtotal":subtotal
                                }
            detalle_venta.append(producto_vendido)
            print("¡Producto agregado a la venta con éxito!")
        continuar = fp.s_n("Desea agregar otro producto a la venta?: ")

    if detalle_venta:
        escribir_json("celulares", productos)
        fecha_actual = dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        nueva_venta = {
            "cliente":nombre_cliente,
            "fecha": fecha_actual,
            "detalle": detalle_venta,
            "total": total_venta    
        }

        historial_ventas = leer_json("ventas")
        if historial_ventas is None:
            historial_ventas = []

        historial_ventas.append(nueva_venta)
        escribir_json("ventas",historial_ventas)
        imprimir_factura(detalle_venta, total_venta,fecha_actual)
    else:
        print("No se registró ninguna venta.")

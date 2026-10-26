import json
import Funciones_Proyecto as fp
import Gestion_de_personal as Gp
import datetime as dt

def leer_json(A_nombre):
    try:
        with open(f"{A_nombre}.json", "r") as archivo:
            datos = json.load(archivo)
            return datos
    except FileNotFoundError:
        print('ERROR: El registro de empleados no existe!!!')
    except Exception:
        print('Error: Ha ocurrido un error inesperado!!!')

productos = leer_json("celulares")
def visualizar_inventario(datos):
    print("="*35)
    print(" "*8,"VISUALIZAR INVENTARIO")
    for dato in datos:
        print("="*35)
        for c,v in dato.items():
            print(f"{c}: {v}")


def cambiar_dato(productos=productos):
    print("="*35)
    print("CAMBIAR DATOS DE UN PRODUCTO")

    try:
        id_buscar = buscar_id_producto(productos,"Ingrese el ID del producto que desea modificar: ")
        
        if id_buscar:
            print(f"\nProducto encontrado: {id_buscar["nombre"]}")
            print("¿Qué dato desea modificar?")
            print("1. Nombre")
            print("2. Precio")
            print("3. Cantidad")
            print("4. Descripción")
            opcion_mod = fp.valor_numerico("Seleccione una opción (1-4): ")

            match opcion_mod:
                case 1:
                    nuevo_nombre = fp.validar_nombre("Ingrese el nuevo nombre: ").strip().title()
                    id_buscar["nombre"] = nuevo_nombre
                case 2:
                    while True:
                        nuevo_precio = fp.decimales("Ingrese el nuevo precio: ")
                        if nuevo_precio < 0:
                            print("ERROR. No se acepta este valor")
                        else:
                            id_buscar["precio"] = nuevo_precio
                            break
                case 3:
                    while True:
                        nueva_cantidad = fp.valor_numerico("Ingrese la nueva cantidad: ")
                        if nueva_cantidad <= 0:
                            print("ERROR. No se acepta un valor negativo o igual a 0.")
                        else:
                            id_buscar["cantidad"] = nueva_cantidad
                            break
                case 4:
                    nueva_desc = input("Ingrese la nueva descripción: ").strip().title()
                    id_buscar["descripcion"] = nueva_desc
                case _:
                    print("Opción no válida. No se hicieron cambios.")
            escribir_json("productos",productos)
            print("Datos actualizados éxitosamente!!")
            
    except Exception as e:
        print(f"Error: {e}")

def verificar_id_producto_existencia(productos,mensaje):
    while True:
        id_producto=validar_id(objeto=productos,mensaje=mensaje)
        if all(c.isdigit() for c in id_producto) and id_producto != '':
            existe= any(producto.get("id")==id_producto for producto in productos)
        
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
        id_producto = validar_id(objeto=productos, mensaje=mensaje)
        if id_producto is None:
            return None
        producto_encontrado = next((p for p in productos if p["id"] == id_producto), None)
        
        if producto_encontrado is not None:
            print("¡ID encontrado con éxito.!")
            return producto_encontrado
        else:
            print("ID no encontrado.")
        

def validar_id(mensaje, objeto):
    if objeto:
        while True:
            id=input(mensaje)
            if all(c.isdigit() or c == '-' for c in id):
                return id
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

def actualizar_json(A_nombre,datos_escribir):
    try:
        with open(f"{A_nombre}"+".jsonl", "a", encoding="utf-8") as archivo:
            archivo.write(json.dumps(datos_escribir) + "\n")
    except FileNotFoundError:
        print("Error: El archivo no fue encontrado.")
emp = [
    {
        "nombre": "Chalino",
        "correo": "Dargs9009 @gmail", 
        "carnet": "6B5F0535",
        "cargo": "supervisor",
        "salario": "22000",
        "estado": "activo"
    },
    {
        "nombre": "Barbanegra",
        "correo": "Barbon9@gmail", 
        "carnet": "5556262",
        "cargo": "empleado",
        "salario": "12000",
        "estado": "activo"
    }
]

def ver_datos_emp():
    for empleado in emp:
        print("-" * 30)
        for clave, valor in empleado.items():
            print(f"{clave}: {valor}")
    print("-" * 30)

def agregar_productos():
    try:
        print("="*30)
        print("AGREGAR PRODUCTOS")
        cant = fp.valor_numerico("Cuántos productos desea agregar?: ")
            
        for i in range(1, cant+1):
            print(f"Producto {i}:")

            id_prod =verificar_id_producto_existencia(productos,"Ingrese el ID del producto: ")
        
            nombre = input("Nombre: ").title()

            while True:
                precio = fp.decimales("Precio: ")
                if precio < 0:
                    print("ERROR. No se acepta un precio negativo")
                else:
                    break

            while True:
                cantidad = fp.valor_numerico("Cantidad: ")
                if cantidad <= 0:
                    print("ERROR. No se acepta este valor.")
                else:
                    break
            descrip = input("Descripción: ").title()
            producto = {
                "id": id_prod,
                "nombre": nombre,
                "precio": precio,
                "cantidad": cantidad,
                "descripcion": descrip}
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
        nombre = item["nombre"]
        cant = item["cantidad_vendida"]
        precio = item["precio"]
        subtotal = item["subtotal"]
        print(f"{nombre:<20} | {cant:<5} | C${precio:<9.2f} | C${subtotal:<9.2f}")
        
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
    nombre_cliente = fp.validar_nombre("Ingrese el nombre del cliente: ")
    
    while continuar:
        producto = buscar_id_producto(productos,"Ingrese el ID del producto a vender: ")

        if producto is None:
            break

        id_prod = producto["id"]
        nombre = producto["nombre"]
        precio = producto["precio"]
        cantidad = producto["cantidad"]
        print(f"Producto: {nombre} | Precio: C${precio} | Existencias actuales: {cantidad}")

        cant_vender = fp.valor_numerico("Cuantas unidades desear vender?: ")
        if cant_vender <= 0:
            print("Error. Ese cantidad no es válida")
        elif cant_vender > producto["cantidad"]:
            print(f"Error: No hay suficiente stock. Unidades disponibles {producto["cantidad"]}")
            
        else:
            producto["cantidad"] -= cant_vender
            subtotal = cant_vender * precio
            total_venta += subtotal
            
            producto_vendido = {"codigo":id_prod,
                                "nombre":nombre,
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

import json, funciones_menu as fm, datetime as dt, Funciones_Proyecto as fp
productos = fm.leer_json("credenciales")
categorias = ["Celular","Laptop","Computadora de Escritorio","Teclado Alambrico",
              "Teclado Inalambrico","Mouse Alambrico","Mouse Inalambrico"]

marcas_celulares = ["Samsung","Apple","Xiaomi","Google","Huawei","Motorola"]
marcas_laptops_escritorio = ["Lenovo","HP","Dell","Apple","ASUS","MSI"]
marcas_teclados = ["Logitech","Microsoft","Keychron","Razer","Corsair","Redragon","VSG"]
marcas_mouses = ["Logitech","Microsoft","Logitech G","Razer","Corsair","Redragon","SteelSeries"]
productos = fm.leer_json("productos")
#Funciones de Supervisores:

def ver_datos(datos, titulo="REGISTROS"):
    print(f"\n--- {titulo} ---")
    if not datos:
        print("No hay registros disponibles para mostrar.")
        print("-" * (len(titulo) + 8))
        return
    for indice, item in enumerate(datos, 1):
        print(f"\n[{indice}] Registro:")
        for clave, valor in item.items():
            # Mostramos la clave formateada y su respectivo valor
            print(f"  - {clave.capitalize()}: {valor}")
    print("-" * (len(titulo) + 8))

def pedir_y_validar_cedula(mensaje="Ingrese la cédula del cliente: "):
    while True:
        cedula = input(mensaje)
        if fm.es_cedula_valida(cedula):
            return cedula
        else:
            print("Formato de cédula no válido. Intente nuevamente.")

def realizar_venta(productos):
    print("="*35)
    print(" "*9,"REALIZAR VENTA")
    print("="*35)
    detalle_venta = []
    total_venta = 0
    continuar = True
    nombre_cliente = fp.validar_nombre("Ingrese el modelo del cliente: ")
    cedula_cliente = pedir_y_validar_cedula()

    while continuar:
        producto = fm.buscar_id_producto(productos,"Ingrese el IMEI del producto a vender: ")

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
        fm.escribir_json("celulares", productos)
        fecha_actual = dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        nueva_venta = {
            "modelo":nombre_cliente,
            "cedula":cedula_cliente,
            "fecha": fecha_actual,
            "detalle": detalle_venta,
            "total": total_venta
        }

        historial_ventas = fm.leer_json("ventas")
        if historial_ventas is None:
            historial_ventas = []

        historial_ventas.append(nueva_venta)
        fm.escribir_json("ventas",historial_ventas)
        imprimir_factura(nombre_cliente,cedula_cliente,detalle_venta, total_venta,fecha_actual)
    else:
        print("No se registró ninguna venta.")

def imprimir_factura(modelo,cedula,detalle_venta, total_general, fecha):
    print("\n" + "="*55)
    print(" "*18, "FACTURA DE VENTA")
    print(f" Fecha y hora: {fecha}")
    print(f" Cliente: {modelo}")
    print(f" Cédula de Identidad: {cedula}")
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

def agregar_productos(productos):
    print("\n--- AGREGAR NUEVO PRODUCTO ---")
    
    c_p = fm.asignar_cp(productos)

    imei = fm.asignar_imei()
    modelo =input("Ingrese el modelo del producto: ")
    
    
    while True:
            print(f"Categorías disponibles: {', '.join(fm.categorias)}")
            categoria_ingresada = input("Ingrese la categoría del producto: ").strip()
            categoria_encontrada = fm.es_categoria_valida(categoria_ingresada)
            
            if categoria_encontrada:
                categoria = categoria_encontrada
                print(f"¡Categoría válida: {categoria}!")
                break
            else: 
                print("ERROR: La categoría ingresada no es válida. Intente nuevamente.")

    marcas_permitidas = fm.obtener_marcas_por_categoria(categoria)
    
    while True:
        print(f"Marcas permitidas para '{categoria.capitalize()}': {', '.join(marcas_permitidas)}")
        marca = input("Ingrese la marca del producto: ").strip()
        
        if fm.es_marca_valida_para_categoria(categoria, marca):
            break
        print(f"ERROR: La marca '{marca}' no es válida para la categoría '{categoria}'. Intente nuevamente.")

    # 3. Precio y Stock (con tus validaciones puras anteriores)
    precio = fm.validar_precio()

    cantidad = fm.validar_cantidad()

    # 4. Crear el diccionario y agregarlo
    nuevo_producto = {
        "codigo_unico":c_p,
        "imei": imei,
        "modelo": modelo,
        "categoria": categoria.capitalize(),
        "marca": marca.capitalize(),
        "precio": precio,
        "stock": cantidad
    }

    productos.append(nuevo_producto)
    print(nuevo_producto)
    print(f"¡Producto '{modelo}' agregado exitosamente al inventario con validación binaria!")

    fm.escribir_json("productos",productos)

def cambiar_dato(productos):
    print("="*35)
    print("CAMBIAR DATOS DE UN PRODUCTO")

    try:
        producto_buscar = fm.buscar_id_producto(productos,"Ingrese el IMEI del producto que desea modificar: ")
        
        if producto_buscar:
            print(f"\nProducto encontrado: {producto_buscar["modelo"]}")
            print("¿Qué dato desea modificar?")
            print("1. Modelo")
            print("2. Precio")
            print("3. Cantidad")
            print("4. Categoria")
            print("5. Marca")
            opcion_mod = fp.valor_numerico("Seleccione una opción (1-4): ")

            match opcion_mod:
                case 1:
                    nuevo_modelo = input("Ingrese el nuevo modelo: ")
                    producto_buscar["modelo"] = nuevo_modelo
                case 2:
                    nuevo_precio = fm.validar_precio()
                    producto_buscar["precio"] = nuevo_precio
                case 3:
                    nueva_cantidad = fm.validar_cantidad()
                    producto_buscar["cantidad"] = nueva_cantidad
                case 4:
                    nueva_categoria = fm.validar_categoria(categorias,"Ingrese la nueva categoria: ")
                    producto_buscar["categoria"] = nueva_categoria
                    
                case 5:
                    nueva_marca = input("Ingrese la nueva marca: ").strip().title()
                    producto_buscar["marca"] = nueva_marca

                case _:
                    print("Opción no válida. No se hicieron cambios.")
            fm.escribir_json("productos",productos)
            print("Datos actualizados éxitosamente!!")
            
    except Exception as e:
        print(f"Error: {e}")

def eliminar(productos,codigo_unico):
    producto_eliminar = None
    for i in productos:
        if i["codigo_unico"] == codigo_unico:
            producto_eliminar = i
            break

    if producto_eliminar:
        productos.remove(producto_eliminar)
        fm.escribir_json("productos",productos)
        return True
    
    return False

def proceso_eliminar(productos):
    while True:
        print("\n--- ELIMINAR PRODUCTO ---")
        codigo_unico = input("Ingrese el código único del producto a eliminar: ")

        if codigo_unico.lower() == 'salir':
            print("Operación de eliminación cancelada.")
            return False
        
        eliminado = eliminar(productos, codigo_unico)
        
        if eliminado:
            print("¡Producto eliminado exitosamente del inventario!")
            return True
        else:
            print("ERROR: No se encontró ningún producto con ese código único.")
            opcion = fp.s_n("¿Desea intentar con otro código? (s/n): ")
            if opcion != 's':
                print("Saliendo del módulo de eliminación...")
                return False

#Funciones de Cajero:
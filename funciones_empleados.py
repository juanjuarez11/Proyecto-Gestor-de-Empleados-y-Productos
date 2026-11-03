import funciones_menu as fm, datetime as dt, Funciones_Proyecto as fp
from funciones_menu import categorias
productos = fm.leer_json("credenciales")

productos = fm.leer_json("productos")

#funciones de Empleados:
#Funciones de Supervisor:
#Gestiona la interfaz interactiva para ingresar los datos de un nuevo producto en el inventario.
def agregar_productos(productos):
    print("\n--- AGREGAR NUEVO PRODUCTO ---")
    
    c_p = fm.asignar_cp(productos)

    imei = fm.asignar_imei()
    modelo =input("Ingrese el modelo del producto: ")
    
    
    while True:
        print(f"Categorías disponibles: {', '.join(categorias)}")
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

    while True:
        precio_ingresado = input("Ingrese el precio: ").strip()
        if fm.validar_precio(precio_ingresado):
            precio = float(precio_ingresado)
            break
        print("ERROR: El precio debe ser un número válido mayor a 0. Intente nuevamente.")

    while True:
        cantidad_ingresada = input("Ingrese la stock: ").strip()
        if fm.validar_cantidad(cantidad_ingresada):
            stock = int(cantidad_ingresada)
            break
        print("ERROR: La stock debe ser un número entero mayor a 0. Intente nuevamente.")

    nuevo_producto = fm.guardar_nuevo_producto(productos,c_p,imei,modelo,categoria,marca,precio,stock)
    if nuevo_producto:
        print(f"¡Producto '{modelo}' agregado exitosamente al inventario con validación binaria!")
    else:
        print("ERROR: No se agregó el producto.")

#Controla el flujo por consola para eliminar un producto utilizando su código único.
def proceso_eliminar(productos):
    while True:
        print("\n--- ELIMINAR PRODUCTO ---")
        codigo_unico = input("Ingrese el código único del producto a eliminar: ")

        if codigo_unico.lower() == 'salir':
            print("Operación de eliminación cancelada.")
            return False
        
        eliminado = fm.eliminar(productos, codigo_unico)
        
        if eliminado:
            print("¡Producto eliminado exitosamente del inventario!")
            return True
        else:
            print("ERROR: No se encontró ningún producto con ese código único.")
            opcion = fp.s_n("¿Desea intentar con otro código? (s/n): ")
            if opcion != 's':
                print("Saliendo del módulo de eliminación...")
                return False

#Permite seleccionar y modificar el modelo, precio o stock de un producto existente.
def cambiar_dato(productos):
    print("\n"+"="*35)
    print("   CAMBIAR DATO DE UN PRODUCTO")
    print("="*35)
    
    codigo = input("Ingrese el Código único del producto que desea modificar:  ")

    producto = fm.buscar_producto_cu(productos,codigo)
    if not producto:
        print("ERROR: No se encontró ningún producto con ese código.")
        return
    
    print(f"\nProducto encontrado: {producto["modelo"]}")
    print("¿Qué dato desea modificar?")
    print("1. Modelo")
    print("2. Precio")
    print("3. Cantidad")
    opcion_mod = fp.valor_numerico("Seleccione una opción (1-3): ")

    match opcion_mod:
        case 1:
            nuevo_valor = input("Ingrese el nuevo modelo: ")
            if not nuevo_valor:
                print("ERROR: El modelo no puede estar vacío.")
        case 2:
            while True:
                nuevo_precio = input("Ingrese el nuevo precio: ").strip()
                if fm.validar_precio(nuevo_precio):
                    nuevo_valor = float(nuevo_precio)
                    break
                print("ERROR: El precio debe ser un número válido mayor a 0.")
        case 3:
            while True:
                nueva_cantidad = input("Ingrese la nueva cantidad: ").strip()
                if fm.validar_cantidad(nueva_cantidad):
                    nuevo_valor = int(nueva_cantidad)
                    break
                print("ERROR: La cantidad debe ser un número válido mayor a 0.")
        case _:
            print("Opción no válida. No se hicieron cambios.")
    actualizado = fm.actualizar_datos_productos(productos,codigo,opcion_mod,nuevo_valor)
    if actualizado:
        print("Datos actualizados y guardados éxitosamente!!")
    else:
        print("ERROR: Ocurrió un problema al actualizar el producto.")
        return False



#Funciones de Cajero:
#Administra el proceso interactivo de venta de uno o varios productos, 
# calculando totales y generando facturas y garantías.
def realizar_venta(productos):
    print("="*35)
    print(" "*9,"REALIZAR VENTA")
    print("="*35)

    detalle_venta = []
    total_venta = 0

    historial_ventas = fm.leer_json("ventas") or []
    n_fact = fm.asignar_num(historial_ventas,"F")
    n_garantia = fm.asignar_num(historial_ventas,"G")

    nombre_cliente = fp.validar_nombre("Ingrese el nombre del cliente: ")
    cedula_cliente = fm.pedir_y_validar_cedula()

    while True:
        codigo_unico = input("Ingrese el codigo único del producto a vender (o 'cerrar' para cancelar la venta): ")

        if codigo_unico.lower() == "cerrar":
            break

        producto = fm.buscar_producto_cu(productos,codigo_unico)
        if not producto:
            print("ERROR: No se encontró ningún producto con ese Código.")
            continue

        imei_prod = producto["imei"]
        modelo = producto["modelo"]
        precio = producto["precio"]
        categoria = producto["categoria"]
        stock = producto["stock"]
        print(f"Codigo: {codigo_unico} | IMEI: {imei_prod} | Producto: {modelo} | Precio: C${precio} | Existencias actuales: {stock}\n")

        cant_vender = fp.valor_numerico("Cuantas unidades desear vender?: ")
        if cant_vender <= 0:
            print("Error. Ese stock no es válida")
        elif cant_vender > producto["stock"]:
            print(f"Error: No hay suficiente stock. Unidades disponibles {producto["stock"]}")
            
        else:
            fecha,fecha_vencimiento = fm.calcular_garantia(categoria)
            hora = dt.datetime.now().strftime("%I:%M:%S %p")
            item_vendido = fm.calcular_venta(producto,cant_vender,fecha_vencimiento)
            detalle_venta.append(item_vendido)
            
            fm.descontar_inventario(producto,cant_vender)
            total_venta+=item_vendido["subtotal"]
            print(f"¡Producto agregado a la venta con éxito! (Subtotal: C${item_vendido["subtotal"]:.2f})")

        if not fp.s_n("Desea agregar otro producto a la venta?: "):
            break

    if detalle_venta:
        fm.escribir_json("productos", productos)
        nueva_venta = {
            "factura":n_fact,
            "n_garantia":n_garantia,
            "cliente":nombre_cliente,
            "cedula":cedula_cliente,
            "fecha_actual": fecha,
            "hora": hora,
            "detalle": detalle_venta,
            "total": total_venta
        }

        historial_ventas.append(nueva_venta)
        fm.escribir_json("ventas",historial_ventas)
        imprimir_factura(n_fact,n_garantia,fecha,hora,nombre_cliente,cedula_cliente,detalle_venta, total_venta)
    else:
        print("No se registró ninguna venta.")

#Muestra en pantalla el comprobante detallado de la venta con sus respectivos precios y fechas de garantía.
def imprimir_factura(n_fact,n_garantia,fecha_actual,hora,cliente,cedula,detalle_venta, total_general):
    print("\n" + "="*55)
    print(" "*18, f"FACTURA DE VENTA {n_fact}")
    print(f" Fecha y hora: {fecha_actual +" "+ hora}")
    print(f"Número de Garantía: {n_garantia}")
    print(f" Cliente: {cliente}")
    print(f" Cédula de Identidad: {cedula}")
    print("="*55)
    print(f"{'PRODUCTO':<22} | {'CANT':<5} | {'PRECIO':<10} | {'SUBTOTAL':<10}")
    print("-" * 55)
    
    for item in detalle_venta:
        modelo = item["modelo"]
        marca = item["marca"]
        cant = item["cantidad_vendida"]
        precio = item["precio"]
        subtotal = item["subtotal"]
        fecha_vencimiento = item["fecha_garantia"]
        print(f"{marca} | {modelo:<20} | {cant:<5} | C${precio:<9.2f} | C${subtotal:<9.2f}")
        print(f"Fecha de Vencimiento de Garantía: {fecha_vencimiento}")

    print("-" * 55)
    print(f"TOTAL A PAGAR: C${total_general:.2f}")
    print("="*55)
    print("¡GRACIAS POR SU COMPRA!")
    print("="*55 + "\n")

#Muestra el desglose de todas las transacciones registradas y el monto total acumulado en caja.
def realizar_arqueo():
    print("\n" + "="*45)
    print(" "*15 + "ARQUEO DE CAJA")
    print("="*45)

    historial_ventas,total_general = fm.obtener_datos_arqueo()
    if not historial_ventas:
        print("No hay registros de ventas en el sistema.")
        print("="*45)
        return
    for indice,venta in enumerate(historial_ventas,1):
        fecha_actual = venta.get("fecha_actual", "Fecha no registrada")
        hora = venta.get("hora")
        cliente = venta.get("cliente", "General")
        total_venta = venta.get("total", 0.0)

        print(f"\n[Venta #{indice}]")
        print(f"  • Fecha y hora : {fecha_actual +" "+hora}")
        print(f"  • Cliente      : {cliente}")
        print(f"  • Subtotal     : C${total_venta:.2f}")
        
        print("  • Productos:")
        for item in venta.get("detalle", []):
            marca = item.get("marca", "")
            modelo = item.get("modelo", "")
            cant = item.get("cantidad_vendida", 0)
            sub = item.get("subtotal", 0.0)
            print(f"    - {marca} {modelo} (x{cant}) -> C${sub:.2f}")

    print("\n" + "="*45)
    print(f" TOTAL ACUMULADO EN VENTAS: C${total_general:.2f}")
    print("="*45 + "\n")

#Va en Funciones_Proyecto
#Permite visualizar los datos que se encuentra en una lista de diccionarios,
#pasandole como parametros una lista de diccionarios y un titulo para especificar
#que tipo de registro es
def ver_datos(datos, titulo):
    print(f"\n--- {titulo} ---")
    if not datos:
        print("No hay registros disponibles para mostrar.")
        print("-" * (len(titulo) + 8))
        return
    for indice, item in enumerate(datos, 1):
        print(f"\n[{indice}] Registro:")
        for clave, valor in item.items():
            print(f"  - {clave.capitalize()}: {valor}")
    print("-" * (len(titulo) + 8))
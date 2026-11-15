import funciones_menu_servicio_tecnico as funciones # las funciones de cada opcion del menu


#    Orden por secciones
#
#    1. PANTALLA DEL MENU
#    2. EJECUTAR EL MENU
#
#    Este modulo es solo el menu: lo que se ve y el ciclo que pide la opcion.


# ==============================================================
# SECCION 1: PANTALLA DEL MENU
# ==============================================================


def mostrar_titulo(texto):
    """
    Que hace: muestra un titulo para saber en que parte del menu se esta.
    Como funciona: imprime el texto centrado entre dos lineas de "=".
    """
    print()
    print("=" * 40)
    print(texto.center(40))
    print("=" * 40)


def mostrar_menu():
    """
    Que hace: muestra las opciones del servicio tecnico.
    Como funciona: imprime el titulo y las opciones numeradas.
    """
    mostrar_titulo("SERVICIO TECNICO")
    print("  1. Recibir equipo con ticket de compra")
    print("  2. Buscar orden por numero de orden")
    print("  3. Actualizar estado")
    print("  4. Mostrar ordenes abiertas")
    print("  5. Mostrar ordenes cerradas")
    print("  0. Volver a la tienda")
    print("-" * 40)


# ==============================================================
# SECCION 2: EJECUTAR EL MENU
# ==============================================================


def ejecutar_menu(tickets_tienda, ordenes):
    """
    Que hace: es el menu principal; el sistema de la tienda lo llama con las facturas y las ordenes.
    Como funciona: repite el menu y llama a la funcion de la opcion elegida hasta que se escribe 0.
    """
    funciones.preparar_ordenes(ordenes)

    while True:
        mostrar_menu()
        opcion = funciones.pedir_opcion("Seleccione: ", ["0", "1", "2", "3", "4", "5"])

        if opcion == "0":
            print("Volviendo al sistema de la tienda.")
            return

        elif opcion == "1":
            mostrar_titulo("RECIBIR EQUIPO")
            funciones.recibir_equipo_y_guardar(tickets_tienda, ordenes)

        elif opcion == "2":
            mostrar_titulo("BUSCAR ORDEN")
            funciones.buscar_y_mostrar_orden(ordenes)

        elif opcion == "3":
            mostrar_titulo("ACTUALIZAR ESTADO")
            funciones.actualizar_orden_y_guardar(ordenes)

        elif opcion == "4":
            mostrar_titulo("ORDENES ABIERTAS")
            funciones.mostrar_ordenes_abiertas(ordenes)

        elif opcion == "5":
            mostrar_titulo("ORDENES CERRADAS")
            funciones.mostrar_ordenes_cerradas(ordenes)
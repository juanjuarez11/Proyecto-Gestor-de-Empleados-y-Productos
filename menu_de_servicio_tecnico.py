import funciones_menu_servicio_tecnico as funciones #Este modulo solo conoce a funciones_menu_servicio_tecnico, que a su vez usa a validaciones_servicio_tecnico


#    Orden por secciones
#
#    1. PANTALLA DEL MENU DE SERVICIO TECNICO
#    2. EJECUTAR EL MENU
#
#    Este modulo es solo el menu: lo que se ve en pantalla y el ciclo que
#    pregunta la opcion. El trabajo de cada opcion lo hacen las funciones
#    de funciones_menu_servicio_tecnico.


# ==============================================================
# SECCION 1: PANTALLA DEL MENU DE SERVICIO TECNICO
#
# Estas funciones se encargan de mostrar el titulo y las
# opciones del menu de servicio tecnico.
# ==============================================================


def mostrar_titulo(texto):
    """
    Que hace: muestra un titulo para que el usuario sepa en que parte del menu esta.
    Como funciona: imprime una linea de "=", el texto centrado y otra linea de "=".
    """
    print()
    print("=" * 40)
    print(texto.center(40))
    print("=" * 40)



def mostrar_menu():
    """
    Que hace: muestra las opciones principales del servicio tecnico.
    Como funciona: imprime el titulo y las opciones numeradas. Solo las muestra,
    la opcion elegida se lee en ejecutar_menu.
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
#
# Esta funcion se encarga de repetir el menu y de llamar a la
# funcion de la opcion elegida.
# ==============================================================


def ejecutar_menu(tickets_tienda, ordenes):
    """
    Que hace: es el menu principal del servicio tecnico. El sistema de la tienda lo
    llama y le entrega la lista de facturas y la lista de ordenes.
    Como funciona: al iniciar deja lista la lista de ordenes (preparar_ordenes).
    Luego muestra el menu, pide una opcion y llama a la funcion que le
    corresponde (1 recibir equipo, 2 buscar orden, 3 actualizar estado, 4 ordenes
    abiertas, 5 ordenes cerradas). Con 0 termina y regresa al sistema de la
    tienda. No sabe nada del archivo: guardar las ordenes lo hacen las funciones
    de las opciones 1 y 3.
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
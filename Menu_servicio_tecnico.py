import Funciones_menu_servicio_tecnico as funciones
import Almacenamiento_ordenes_servicio_tecnico as almacenamiento
import Vista_servicio_tecnico as vista


def ejecutar_menu(tickets_tienda, ordenes):
    """
    Que hace: es el menu principal del servicio tecnico. El sistema de la tienda lo
    llama y le entrega la lista de facturas y la lista de ordenes.
    Como funciona: al iniciar carga las ordenes guardadas en el archivo .json (si
    la lista llega vacia). Luego repite: muestra el menu, pide una opcion y llama
    a la funcion que le corresponde (1 recibir equipo, 2 buscar orden, 3 actualizar
    estado, 4 ordenes abiertas, 5 ordenes cerradas). Despues de recibir un equipo
    o actualizar un estado guarda las ordenes en el archivo. Con 0 termina y
    regresa al sistema de la tienda.
    """
    if len(ordenes) == 0:
        ordenes.extend(almacenamiento.cargar_ordenes())

    while True:
        funciones.mostrar_menu()
        opcion = funciones.pedir_opcion("Seleccione: ", ["0", "1", "2", "3", "4", "5"])

        if opcion == "0":
            print("Volviendo al sistema de la tienda.")
            return

        elif opcion == "1":
            funciones.mostrar_titulo("RECIBIR EQUIPO")
            funciones.recibir_equipo(tickets_tienda, ordenes)
            almacenamiento.guardar_ordenes(ordenes)

        elif opcion == "2":
            funciones.mostrar_titulo("BUSCAR ORDEN")
            funciones.buscar_y_mostrar_orden(ordenes)

        elif opcion == "3":
            funciones.mostrar_titulo("ACTUALIZAR ESTADO")
            funciones.actualizar_orden(ordenes)
            almacenamiento.guardar_ordenes(ordenes)

        elif opcion == "4":
            funciones.mostrar_titulo("ORDENES ABIERTAS")
            vista.mostrar_ordenes_abiertas(ordenes)

        elif opcion == "5":
            funciones.mostrar_titulo("ORDENES CERRADAS")
            vista.mostrar_ordenes_cerradas(ordenes)
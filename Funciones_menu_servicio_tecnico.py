import Servicio_tecnico as servicio
import Vista_servicio_tecnico as vista


# ============================================================
# PANTALLA DEL MENU
# ============================================================


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


# ============================================================
# FUNCIONES COMUNES PARA PEDIR DATOS (las usan varias opciones)
# ============================================================


def pedir_opcion(mensaje, opciones):
    """
    Que hace: pide al usuario elegir una opcion de una lista y no lo deja avanzar
    hasta que escriba una valida.
    Como funciona: repite la pregunta hasta que lo escrito (sin espacios sobrantes)
    este en la lista de opciones. Si no lo esta, avisa y vuelve a preguntar.
    """
    while True:
        opcion = input(mensaje).strip()
        if opcion in opciones:
            return opcion
        print("Opcion no valida. Intente de nuevo.")


def pedir_falla(mensaje):
    """
    Que hace: pide la descripcion de una falla. Sirve para la falla que dice el
    cliente y para la que encuentra el tecnico, solo cambia el mensaje.
    Como funciona: repite la pregunta mientras el texto este vacio. Devuelve la
    falla escrita. Con 0 cancela y devuelve None.
    """
    while True:
        falla = input(mensaje).strip()
        if falla == "0":
            return None
        if falla != "":
            return falla
        print("La falla no puede quedar vacia. Describa el problema.")


def pedir_orden_existente(ordenes):
    """
    Que hace: pide un numero de orden y no avanza hasta que exista. Se usa al
    buscar y al actualizar una orden, para no repetir el mismo codigo.
    Como funciona: repite la pregunta hasta que buscar_orden encuentre la orden y
    la devuelve. Con 0 cancela y devuelve None.
    """
    while True:
        ticket = input("Numero de orden (0 para cancelar): ").strip()
        if ticket == "0":
            return None
        orden = servicio.buscar_orden(ordenes, ticket)
        if orden is not None:
            return orden
        print("No se encontro esa orden. Verifique el numero e intentelo de nuevo.")


# ============================================================
# OPCION 1: RECIBIR EQUIPO
# ============================================================


def pedir_factura(tickets_tienda):
    """
    Que hace: pide el codigo de factura del cliente y devuelve su registro de
    compra.
    Como funciona: repite la pregunta hasta que el codigo exista en las facturas
    (lo busca con buscar_ticket_compra). Con 0 cancela y devuelve None.
    """
    while True:
        codigo = input("Codigo unico de factura (0 para cancelar): ").strip()
        if codigo == "0":
            return None
        registro = servicio.buscar_ticket_compra(tickets_tienda, codigo)
        if registro is not None:
            return registro
        print("Verifique el ticket e intentelo de nuevo, o escriba 0 para cancelar.")


def pedir_ticket_garantia(registro):
    """
    Que hace: pide el ticket de garantia y comprueba que sea el de esa factura.
    Como funciona: repite la pregunta hasta que validar_ticket_garantia lo acepte.
    Devuelve True si coincide. Con 0 cancela y devuelve False.
    """
    while True:
        ticket = input("Ticket de garantia (0 para cancelar): ").strip()
        if ticket == "0":
            return False
        if servicio.validar_ticket_garantia(registro, ticket):
            return True
        print("Revise el ticket de garantia e intentelo de nuevo, o escriba 0 para cancelar.")


def recibir_equipo(tickets_tienda, ordenes):
    """
    Que hace: registra el ingreso de un equipo a servicio tecnico, desde que se
    pide la factura hasta que se crea la orden.
    Como funciona: solo coordina, cada paso lo hace otra funcion. Si un paso se
    cancela o falla, termina sin crear la orden. Los pasos son: 1) pedir la
    factura, 2) pedir el ticket de garantia, 3) revisar que la garantia este
    vigente, 4) revisar que el equipo no tenga una orden abierta, 5) mostrar los
    datos del equipo y pedir la falla del cliente, 6) crear la orden y mostrarla.
    """
    registro = pedir_factura(tickets_tienda)
    if registro is None:
        print("Registro cancelado. Volviendo al menu de servicio tecnico.")
        return

    if not pedir_ticket_garantia(registro):
        print("Registro cancelado. Volviendo al menu de servicio tecnico.")
        return
    if not servicio.validar_garantia_vigente(registro):
        print("No se puede registrar este equipo. Puede intentar con otra factura.")
        return

    abierta = servicio.buscar_orden_abierta(ordenes, registro["codigo_factura"])
    if abierta is not None:
        print(f"Este equipo ya fue recibido, tiene la orden {abierta['ticket']} abierta "
              f"({abierta['estado']}).")
        return

    vista.mostrar_datos_equipo(registro)
    falla = pedir_falla("Falla reportada por el cliente (0 para cancelar): ")
    if falla is None:
        print("Registro cancelado. Volviendo al menu de servicio tecnico.")
        return

    orden = servicio.crear_orden(ordenes, registro, falla)
    vista.mostrar_detalle(orden)


# ============================================================
# OPCION 2: BUSCAR ORDEN
# ============================================================


def buscar_y_mostrar_orden(ordenes):
    """
    Que hace: es la opcion "Buscar orden" del menu. Muestra los datos de una orden.
    Como funciona: pide el numero con pedir_orden_existente y, si la encuentra, la
    muestra con vista.mostrar_detalle. Si el usuario cancela, avisa y termina.
    """
    orden = pedir_orden_existente(ordenes)
    if orden is None:
        print("Busqueda cancelada. Volviendo al menu de servicio tecnico.")
        return
    vista.mostrar_detalle(orden)


# ============================================================
# OPCION 3: ACTUALIZAR ESTADO
# ============================================================


def pedir_dias_garantia():
    """
    Que hace: pide cuantos dias de garantia se dan al entregar un equipo reparado,
    de 0 hasta el maximo permitido (MAX_DIAS_GARANTIA).
    Como funciona: primero arma una lista con los dias validos escritos como texto
    ("0", "1", ... "30"). Luego repite la pregunta hasta que lo escrito este en esa
    lista. Devuelve los dias como numero entero.
    """
    dias_validos = []
    for dias in range(servicio.MAX_DIAS_GARANTIA + 1):
        dias_validos.append(str(dias))

    while True:
        texto = input(f"Dias de garantia (0 a {servicio.MAX_DIAS_GARANTIA}, 0 si no aplica): ").strip()
        if texto in dias_validos:
            return int(texto)
        print(f"Ingrese un numero entero entre 0 y {servicio.MAX_DIAS_GARANTIA}.")


def elegir_estado(estados):
    """
    Que hace: muestra los estados a los que puede pasar una orden y deja elegir uno.
    Como funciona: imprime los estados numerados desde 1 y guarda esos numeros en
    una lista. Pide el numero con pedir_opcion y, como las listas empiezan en 0,
    devuelve el estado de la posicion (numero elegido - 1).
    """
    opciones = []
    numero = 1
    print("\nEstados disponibles:")
    for estado in estados:
        print(f"  {numero}. {estado}")
        opciones.append(str(numero))
        numero = numero + 1
    seleccion = pedir_opcion("Nuevo estado: ", opciones)
    return estados[int(seleccion) - 1]


def actualizar_orden(ordenes):
    """
    Que hace: es la opcion "Actualizar estado" del menu. Cambia el estado de una
    orden respetando el flujo permitido.
    Como funciona: 1) pide la orden. 2) muestra su estado y los estados a los que
    puede pasar (si no tiene ninguno, esta cerrada y termina). 3) segun el estado
    elegido: "Diagnosticado" pide la falla encontrada por el tecnico, "No reparado"
    pide la solucion del cliente, "Entregado" pide los dias de garantia, y los
    demas solo cambian el estado. 4) muestra la orden actualizada.
    """
    orden = pedir_orden_existente(ordenes)
    if orden is None:
        print("Actualizacion cancelada. Volviendo al menu de servicio tecnico.")
        return

    print(f"Estado actual de la orden {orden['ticket']}: {orden['estado']}")
    estados = servicio.ESTADOS[orden["estado"]]
    if len(estados) == 0:
        print("Esta orden ya esta cerrada, no se puede cambiar su estado.")
        return

    nuevo_estado = elegir_estado(estados)
    if nuevo_estado == "Diagnosticado":
        print(f"\nFalla reportada por el cliente: {orden['falla']}")
        falla_encontrada = pedir_falla("Falla encontrada por el tecnico (0 para cancelar): ")
        if falla_encontrada is None:
            print("Actualizacion cancelada. Volviendo al menu de servicio tecnico.")
            return
        servicio.registrar_diagnostico(orden, falla_encontrada)

    elif nuevo_estado == "No reparado":
        print("\nEl cliente puede elegir:")
        for numero in servicio.SOLUCIONES:
            print(f"  {numero}. {servicio.SOLUCIONES[numero]}")
        solucion = pedir_opcion("Solucion elegida: ", ["1", "2"])
        servicio.marcar_no_reparado(orden, solucion)

    else:
        if nuevo_estado == "Entregado":
            dias = pedir_dias_garantia()
            servicio.actualizar_estado(orden, nuevo_estado, dias)
        else:
            servicio.actualizar_estado(orden, nuevo_estado)

    vista.mostrar_detalle(orden)
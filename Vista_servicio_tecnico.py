import Servicio_tecnico as servicio


# ============================================================
# MOSTRAR UNA ORDEN
# ============================================================


def mostrar_detalle(orden):
    """
    Que hace: muestra en pantalla todos los datos de una orden, como una tarjeta.
    Como funciona: imprime los datos que siempre existen (ticket, ticket de
    compra, IMEI, falla reportada y estado). Los demas solo se imprimen si ya
    tienen contenido: la falla encontrada, la solucion del cliente y los datos de
    entrega (fecha y garantia con su fecha de vencimiento, o "sin garantia").
    """
    print("-" * 40)
    print(f"Ticket: {orden['ticket']}")
    print(f"Ticket de compra: {orden['ticket_compra']}")
    print(f"IMEI/serie: {orden['imei_serie']}")
    print(f"Falla reportada: {orden['falla']}")
    if orden["falla_encontrada"] != "":
        print(f"Falla encontrada: {orden['falla_encontrada']}")
    print(f"Estado: {orden['estado']}")
    
    if orden["solucion"] != "":
        print(f"Solucion: {orden['solucion']}")
        
    if orden["fecha_entrega"] != "":
        print(f"Fecha de entrega: {orden['fecha_entrega']}")
        if orden["dias_garantia"] > 0:
            print(
                f"Garantia: {orden['dias_garantia']} dias "
                f"(vence el {orden['fecha_vencimiento']})"
            )
        else:
            print("Garantia: sin garantia")
    print("-" * 40)


# ============================================================
# MOSTRAR LISTAS DE ORDENES
# ============================================================


def mostrar_ordenes_abiertas(ordenes):
    """
    Que hace: muestra las ordenes abiertas, o sea las que todavia pueden cambiar
    de estado.
    Como funciona: recorre las ordenes y muestra con mostrar_detalle las que
    tienen estados siguientes en "ESTADOS". Si no hay ninguna, avisa.
    """
    hay_abiertas = False
    for orden in ordenes:
        if len(servicio.ESTADOS[orden["estado"]]) > 0:
            mostrar_detalle(orden)
            print()
            hay_abiertas = True

    if not hay_abiertas:
        print("No hay ordenes abiertas.")


def mostrar_ordenes_cerradas(ordenes):
    """
    Que hace: muestra las ordenes cerradas (Entregado y No reparado), que ya no
    pueden cambiar de estado.
    Como funciona: recorre las ordenes y muestra con mostrar_detalle las que no
    tienen estados siguientes en "ESTADOS". Si no hay ninguna, avisa.
    """
    hay_cerradas = False
    for orden in ordenes:
        if len(servicio.ESTADOS[orden["estado"]]) == 0:
            mostrar_detalle(orden)
            print()
            hay_cerradas = True

    if not hay_cerradas:
        print("No hay ordenes cerradas.")


# ============================================================
# MOSTRAR DATOS DEL EQUIPO (al recibirlo)
# ============================================================


def mostrar_datos_equipo(registro):
    """
    Que hace: muestra los datos del equipo que vienen en la factura, para que el
    tecnico confirme que es el equipo correcto.
    Como funciona: recorre los campos de la factura y los imprime, menos los datos
    de control (codigos y fechas), que no son del equipo.
    """
    print("\nDatos del equipo encontrados en la tienda:")
    print("-" * 40)
    for campo in registro:
        if campo not in (
            "ticket",
            "codigo_factura",
            "ticket_garantia",
            "fecha_factura",
            "garantia_hasta",
        ):
            print(f"  {campo}: {registro[campo]}")
    print("-" * 40)
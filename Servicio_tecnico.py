from datetime import date, timedelta

# Cada estado y los estados a los que puede pasar.
# Si la lista esta vacia, la orden esta cerrada.
ESTADOS = {
    "En diagnostico": ["Diagnosticado"],
    "Diagnosticado": ["Esperando repuesto", "Reparado", "No reparado"],
    "Esperando repuesto": ["En diagnostico", "No reparado"],
    "Reparado": ["Entregado"],
    "No reparado": [],
    "Entregado": [],
}

# Maximo de dias de garantia que se pueden dar al entregar un equipo reparado
MAX_DIAS_GARANTIA = 30

# Opciones del cliente cuando su equipo no se pudo reparar
SOLUCIONES = {
    "1": "Cambio por equipo del mismo precio o modelo",
    "2": "Reposicion total del dinero",
}


# ============================================================
# BUSCAR (ordenes y facturas)
# ============================================================


def buscar_orden(ordenes, ticket):
    """
    Que hace: busca una orden por su numero de ticket (ejemplo: T-001).
    Como funciona: pasa lo escrito a mayuscula (t-001 se busca como T-001),
    recorre la lista y compara el ticket de cada orden.
    Devuelve la orden si la encuentra, o None si no existe.
    """
    ticket = ticket.upper()
    for orden in ordenes:
        if orden["ticket"] == ticket:
            return orden
    return None


def buscar_orden_abierta(ordenes, ticket_compra):
    """
    Que hace: revisa si un equipo ya tiene una orden abierta (que todavia puede
    cambiar de estado). El equipo se identifica por el codigo de su factura.
    Como funciona: recorre las ordenes y busca una con ese codigo de factura cuyo
    estado tenga estados siguientes en "ESTADOS".
    Devuelve esa orden, o None si no tiene ninguna abierta.
    """
    for orden in ordenes:
        if orden["ticket_compra"] == ticket_compra and len(ESTADOS[orden["estado"]]) > 0:
            return orden
    return None


def buscar_ticket_compra(tickets_tienda, ticket_compra):
    """
    Que hace: busca en las facturas de la tienda la que tiene el codigo escrito.
    Como funciona: pasa el codigo a mayuscula y lo compara con el campo
    codigo_factura de cada factura.
    Devuelve la factura si la encuentra; si no, avisa y devuelve None.
    """
    codigo = ticket_compra.upper()
    for registro in tickets_tienda:
        if registro["codigo_factura"] == codigo:
            return registro

    print("El codigo de factura no existe en el registro de facturas.")
    return None


# ============================================================
# VALIDAR GARANTIA
# ============================================================


def validar_ticket_garantia(registro, ticket_garantia):
    """
    Que hace: comprueba que el ticket de garantia escrito sea el de esa factura.
    Como funciona: compara lo escrito (en mayuscula) con el campo ticket_garantia
    de la factura. Si no coinciden, avisa y devuelve False. Si son iguales,
    devuelve True.
    """
    if registro["ticket_garantia"] != ticket_garantia.upper():
        print("El ticket de garantia no coincide con el registrado en la factura.")
        return False
    return True


def validar_garantia_vigente(registro):
    """
    Que hace: dice si la garantia de la factura todavia sirve.
    Como funciona: convierte el campo garantia_hasta (texto AAAA-MM-DD) a fecha y
    la compara con la de hoy. Si ya paso, avisa y devuelve False. Si vence hoy o
    despues, devuelve True.
    """
    fecha_vencimiento = date.fromisoformat(registro["garantia_hasta"])
    if fecha_vencimiento < date.today():
        print("La garantia de este ticket ya vencio.")
        return False
    return True


# ============================================================
# CREAR LA ORDEN (al recibir el equipo)
# ============================================================


def crear_orden(ordenes, registro_compra, falla):
    """
    Que hace: registra un equipo en servicio tecnico creando su orden.
    Como funciona: genera el ticket de la orden (T-001, T-002...) segun cuantas
    ordenes hay, arma la orden en estado "En diagnostico" con los datos de la
    factura y la falla del cliente, y la agrega a la lista.
    Devuelve la orden creada.
    """
    numero = len(ordenes) + 1
    ticket_orden = "T-" + str(numero).zfill(3)  # zfill rellena con ceros: 1 -> 001

    orden = {
        "ticket": ticket_orden,
        "ticket_compra": registro_compra["codigo_factura"],
        "imei_serie": str(registro_compra["imei"]),
        "falla": falla,
        "falla_encontrada": "",
        "estado": "En diagnostico",
        "solucion": "",
        "fecha_entrega": "",
        "dias_garantia": 0,
        "fecha_vencimiento": "",
    }
    ordenes.append(orden)
    print(f"Orden registrada. Ticket: {orden['ticket']}")
    return orden


# ============================================================
# CAMBIAR EL ESTADO DE LA ORDEN
# ============================================================


def actualizar_estado(orden, nuevo_estado, dias_garantia=0):
    """
    Que hace: cambia el estado de una orden (Esperando repuesto, En diagnostico,
    Reparado o Entregado).
    Como funciona: guarda el nuevo estado en la orden. Si es "Entregado", guarda
    tambien la fecha de entrega, los dias de garantia que se dieron y la fecha en
    que vence esa garantia.
    """
    orden["estado"] = nuevo_estado
    if nuevo_estado == "Entregado":
        hoy = date.today()
        orden["fecha_entrega"] = hoy.strftime("%d/%m/%Y")
        orden["dias_garantia"] = dias_garantia
        vencimiento = hoy + timedelta(days=dias_garantia)
        orden["fecha_vencimiento"] = vencimiento.strftime("%d/%m/%Y")

    print(f"Estado actualizado: {nuevo_estado}")


def registrar_diagnostico(orden, falla_encontrada):
    """
    Que hace: pasa la orden a "Diagnosticado" y guarda la falla que encontro el
    tecnico, que puede ser distinta a la que dijo el cliente.
    Como funciona: guarda la falla en la orden y cambia el estado.
    """
    orden["falla_encontrada"] = falla_encontrada
    orden["estado"] = "Diagnosticado"
    print(f"Estado actualizado: Diagnosticado. Falla encontrada: {falla_encontrada}")


def marcar_no_reparado(orden, opcion):
    """
    Que hace: cierra la orden como "No reparado" y guarda lo que elige el cliente
    (cambio de equipo o devolucion del dinero). Esta orden ya no se entrega.
    Como funciona: busca la opcion elegida en SOLUCIONES, la guarda en la orden y
    cambia el estado.
    """
    orden["solucion"] = SOLUCIONES[opcion]
    orden["estado"] = "No reparado"
    print(f"Estado actualizado: No reparado. Solucion: {orden['solucion']}")
import json #Usamos json para guardar y recuperar las órdenes en un archivo
import os # Y os para saber si ese archivo ya existe
from datetime import date, timedelta #Usamos date para comparar fechas y timedelta para sumar los días de garantía a la fecha de entrega


#    Oden por secciones
#
#    1. DATOS DEL SERVICIO TECNICO
#    2. GUARDAR Y LEER LAS ORDENES (ARCHIVO .JSON)
#    3. BUSCAR ORDENES Y FACTURAS
#    4. VALIDAR LA GARANTIA
#    5. CREAR ORDENES Y CAMBIAR SU ESTADO
#    6. MOSTRAR INFORMACION EN PANTALLA
#    7. PEDIR DATOS AL USUARIO
#    8. OPCION 1 DEL MENU: RECIBIR EQUIPO
#    9. OPCION 2 DEL MENU: BUSCAR ORDEN
#   10. OPCION 3 DEL MENU: ACTUALIZAR ESTADO
#   11. PANTALLA DEL MENU DE SERVICIO TECNICO


# ==============================================================
# SECCION 1: DATOS DEL SERVICIO TECNICO
#
# Estos son los datos que usan todas las funciones: los
# estados, las soluciones y el limite de garantia.
# ==============================================================


# Cada estado y los estados a los que puede pasar.
# Si la lista esta vacia, la orden esta cerrada.
ESTADOS = {
    "En diagnostico": ["Diagnosticado"],
    "Diagnosticado": ["Esperando repuesto", "Reparado", "No reparado"],
    "Esperando repuesto": ["En diagnostico"],
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

# Archivo donde se guardan las ordenes (queda en la carpeta donde se ejecuta el programa)
ARCHIVO_ORDENES = "ordenes_servicio_tecnico.json"


# ==============================================================
# SECCION 2: GUARDAR Y LEER LAS ORDENES (ARCHIVO .JSON)
#
# Estas funciones se encargan de guardar las ordenes en un
# archivo y de leerlas al abrir el programa.

# ==============================================================


def cargar_ordenes():
    """
    Que hace: lee del archivo .json las ordenes guardadas (abiertas y cerradas)
    para recuperarlas al abrir el programa.
    Como funciona: si el archivo no existe (primera vez) devuelve una lista vacia.
    Si existe, lo abre y json.load convierte su contenido en la lista de ordenes.
    Si el archivo esta danado (json.load da ValueError), avisa y devuelve una
    lista vacia.
    """
    if not os.path.exists(ARCHIVO_ORDENES): # utiliza libreria os para buscar la ruta de ARCHIVOS ORDENES
                                            #
        return []

    try:
        with open(ARCHIVO_ORDENES, "r", encoding="utf-8") as archivo:
            # encoding=
            # utf-8 hace que el programa entienda los acentos y la ñ
            ordenes = json.load(archivo)
        return ordenes
    except ValueError:
        print("El archivo de ordenes esta danado. Se inicia sin ordenes guardadas.")
        return []


def guardar_ordenes(ordenes):
    """
    Que hace: escribe en el archivo .json todas las ordenes, para que no se
    pierdan al cerrar el programa.
    Como funciona: abre el archivo para escribir y json.dump guarda en el la lista
    de ordenes. Con indent=4 el archivo queda ordenado y con ensure_ascii=False se
    guardan bien las tildes y la ñ. Si no se puede escribir (disco lleno, sin
    permisos), avisa y el programa sigue funcionando.
    """
    try:
        with open(ARCHIVO_ORDENES, "w", encoding="utf-8") as archivo:
            json.dump(ordenes, archivo, indent=4, ensure_ascii=False)
    except OSError:
        print("Aviso: no se pudieron guardar las ordenes en el archivo.")


# ==============================================================
# SECCION 3: BUSCAR ORDEN, ORDENES ABIERTAS Y FACTURAS
#
# Estas funciones se encargan de buscar una orden y de buscar
# una factura de la tienda.
# ==============================================================


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
    estado tenga estados siguientes en ESTADOS.
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


# ==============================================================
# SECCION 4: VALIDAR LA GARANTIA
#
# Estas funciones se encargan de validar el ticket de garantia
# y que la garantia no este vencida.
# ==============================================================


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


# ==============================================================
# SECCION 5: CREAR ORDENES Y CAMBIAR SU ESTADO
#
# Estas funciones se encargan de crear una orden y de cambiar
# su estado, tambien registra el diagnostico y cierra la orden
# con la funcion no reparado
# ==============================================================


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


# ==============================================================
# SECCION 6: MOSTRAR INFORMACION EN PANTALLA
#
# Estas funciones se encargan de mostrar en pantalla las
# ordenes y los datos del equipo.
# ==============================================================


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


def mostrar_ordenes_abiertas(ordenes):
    """
    Que hace: muestra las ordenes abiertas, o sea las que todavia pueden cambiar
    de estado.
    Como funciona: recorre las ordenes y muestra con mostrar_detalle las que
    tienen estados siguientes en ESTADOS. Si no hay ninguna, avisa.
    """
    hay_abiertas = False
    for orden in ordenes:
        if len(ESTADOS[orden["estado"]]) > 0:
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
    tienen estados siguientes en ESTADOS. Si no hay ninguna, avisa.
    """
    hay_cerradas = False
    for orden in ordenes:
        if len(ESTADOS[orden["estado"]]) == 0:
            mostrar_detalle(orden)
            print()
            hay_cerradas = True

    if not hay_cerradas:
        print("No hay ordenes cerradas.")


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


# ==============================================================
# SECCION 7: PEDIR DATOS AL USUARIO
#
# Estas funciones se encargan de pedir datos y no dejan
# avanzar hasta que sean validos. Las usan varias opciones del
# menu.
# ==============================================================


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
        orden = buscar_orden(ordenes, ticket)
        if orden is not None:
            return orden
        print("No se encontro esa orden. Verifique el numero e intentelo de nuevo.")


def pedir_dias_garantia():
    """
    Que hace: pide cuantos dias de garantia se dan al entregar un equipo reparado,
    de 0 hasta el maximo permitido (MAX_DIAS_GARANTIA).
    Como funciona: primero arma una lista con los dias validos escritos como texto
    ("0", "1", ... "30"). Luego repite la pregunta hasta que lo escrito este en esa
    lista. Devuelve los dias como numero entero.
    """
    dias_validos = []
    for dias in range(MAX_DIAS_GARANTIA + 1):
        dias_validos.append(str(dias))

    while True:
        texto = input(f"Dias de garantia (0 a {MAX_DIAS_GARANTIA}, 0 si no aplica): ").strip()
        if texto in dias_validos:
            return int(texto)
        print(f"Ingrese un numero entero entre 0 y {MAX_DIAS_GARANTIA}.")


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


# ==============================================================
# SECCION 8: OPCION 1 DEL MENU: RECIBIR EQUIPO
#
# Estas funciones se encargan de recibir un equipo y crear su
# orden.
# ==============================================================


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
        registro = buscar_ticket_compra(tickets_tienda, codigo)
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
        if validar_ticket_garantia(registro, ticket):
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
    if not validar_garantia_vigente(registro):
        print("No se puede registrar este equipo. Puede intentar con otra factura.")
        return

    abierta = buscar_orden_abierta(ordenes, registro["codigo_factura"])
    if abierta is not None:
        print(f"Este equipo ya fue recibido, tiene la orden {abierta['ticket']} abierta "
              f"({abierta['estado']}).")
        return

    mostrar_datos_equipo(registro)
    falla = pedir_falla("Falla reportada por el cliente (0 para cancelar): ")
    if falla is None:
        print("Registro cancelado. Volviendo al menu de servicio tecnico.")
        return

    orden = crear_orden(ordenes, registro, falla)
    mostrar_detalle(orden)


# ==============================================================
# SECCION 9: OPCION 2 DEL MENU: BUSCAR ORDEN
#
# Estas funciones se encargan de buscar una orden y mostrarla.
# ==============================================================


def buscar_y_mostrar_orden(ordenes):
    """
    Que hace: es la opcion "Buscar orden" del menu. Muestra los datos de una orden.
    Como funciona: pide el numero con pedir_orden_existente y, si la encuentra, la
    muestra con mostrar_detalle. Si el usuario cancela, avisa y termina.
    """
    orden = pedir_orden_existente(ordenes)
    if orden is None:
        print("Busqueda cancelada. Volviendo al menu de servicio tecnico.")
        return
    mostrar_detalle(orden)


# ==============================================================
# SECCION 10: OPCION 3 DEL MENU: ACTUALIZAR ESTADO
#
# Estas funciones se encargan de cambiar el estado de una
# orden.
# ==============================================================


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
    
    
    estados = ESTADOS[orden["estado"]]
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
        registrar_diagnostico(orden, falla_encontrada)

    elif nuevo_estado == "No reparado":
        print("\nEl cliente puede elegir:")
        for numero in SOLUCIONES:
            print(f"  {numero}. {SOLUCIONES[numero]}")
        solucion = pedir_opcion("Solucion elegida: ", ["1", "2"])
        marcar_no_reparado(orden, solucion)

    else:
        if nuevo_estado == "Entregado":
            dias = pedir_dias_garantia()
            actualizar_estado(orden, nuevo_estado, dias)
        else:
            actualizar_estado(orden, nuevo_estado)

    mostrar_detalle(orden)


# ==============================================================
# SECCION 11: PANTALLA DEL MENU DE SERVICIO TECNICO
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
import json #Usamos json para guardar y recuperar las órdenes en un archivo
import os # Y os para saber si ese archivo ya existe
from datetime import date, timedelta #Usamos date para la fecha de entrega y timedelta para sumar los días de garantía a esa fecha
from Validaciones_servicio_tecnico import (
    validar_garantia_vigente,
    pedir_opcion,
    pedir_falla,
    pedir_dias_garantia,
    pedir_ticket_garantia,
    pedir_dato_existente,
) # Las validaciones de los datos de entrada viven en su propio modulo


#    Orden por secciones
#
#    1. DATOS DEL SERVICIO TECNICO
#    2. GUARDAR Y LEER LAS ORDENES (ARCHIVO .JSON)
#    3. BUSCAR ORDENES Y FACTURAS
#    4. CREAR ORDENES Y CAMBIAR SU ESTADO
#    5. MOSTRAR INFORMACION EN PANTALLA
#    6. PEDIR DATOS AL USUARIO
#    7. OPCION 1 DEL MENU: RECIBIR EQUIPO
#    8. OPCION 2 DEL MENU: BUSCAR ORDEN
#    9. OPCION 3 DEL MENU: ACTUALIZAR ESTADO
#
#    Este modulo tiene las funciones que hacen el trabajo de cada opcion del
#    menu. Importa a validaciones_servicio_tecnico (las validaciones de los datos de entrada)
#    y lo usa menu_servicio_tecnico (la pantalla y el ciclo del menu).
#
#    Regla del archivo: las funciones de logica (buscar, crear, cambiar
#    estado) NO imprimen nada, solo devuelven un resultado. Los mensajes
#    los imprimen las funciones de pedir datos, las de mostrar y las
#    opciones del menu (las que coordinan). Pedir datos y revisar lo que
#    se escribe es trabajo del modulo validaciones_servicio_tecnico.


# ==============================================================
# SECCION 1: DATOS DEL SERVICIO TECNICO
#
# Estos son los datos que usan todas las funciones: los
# estados y las soluciones.
# ==============================================================


# Cada estado y los estados a los que puede pasar.
# Si la lista esta vacia, la orden esta cerrada.
estados = {
    "En diagnostico": ["Diagnosticado"],
    "Diagnosticado": ["Esperando repuesto", "Reparado", "No reparado"],
    "Esperando repuesto": ["En diagnostico"],
    "Reparado": ["Entregado"],
    "No reparado": [],
    "Entregado": [],
}

# Opciones del cliente cuando su equipo no se pudo reparar
soluciones = {
    "1": "Cambio por equipo del mismo precio o modelo",
    "2": "Reposicion total del dinero",
}

# Archivo donde se guardan las ordenes (queda en la carpeta donde se ejecuta el programa)
archivo_de_ordenes = "ordenes_servicio_tecnico.json"

# Campos de la factura que son de control y no se muestran como datos del equipo
campos_control = (
    "ticket",
    "codigo_factura",
    "ticket_garantia",
    "fecha_factura",
    "garantia_hasta",
)


# ==============================================================
# SECCION 2: GUARDAR Y LEER LAS ORDENES (ARCHIVO .JSON)
#
# Estas funciones se encargan de guardar las ordenes en un
# archivo y de leerlas al abrir el programa. Cada una tiene una
# funcion que hace el trabajo con el archivo (sin imprimir) y
# otra que avisa al usuario si algo salio mal.
# ==============================================================


def leer_archivo_ordenes():
    """
    Que hace: lee del archivo .json las ordenes guardadas (abiertas y cerradas).
    Como funciona: si el archivo no existe (primera vez) devuelve una lista vacia.
    Si existe, lo abre y json.load convierte su contenido en la lista de ordenes.
    Si el archivo esta danado (json.load da ValueError) devuelve None. No imprime nada.
    """
    if not os.path.exists(archivo_de_ordenes): # comprueba si el archivo donde se guardan las ordenes existe
        return []

    try:
        with open(archivo_de_ordenes, "r", encoding="utf-8") as archivo:
            # encoding=utf-8 hace que el programa entienda los acentos y la ñ
            ordenes = json.load(archivo) # transforma el texto en una estructura de python
        return ordenes
    except ValueError:
        return None



def escribir_archivo_ordenes(ordenes):
    """
    Que hace: escribe en el archivo .json todas las ordenes.
    Como funciona: abre el archivo para escribir y json.dump guarda en el la lista
    de ordenes. Con indent=4 el archivo queda ordenado y con ensure_ascii=False se
    guardan bien las tildes y la ñ. Devuelve True si se pudo escribir y False si
    no (disco lleno, sin permisos). No imprime nada.
    """
    try:
        with open(archivo_de_ordenes, "w", encoding="utf-8") as archivo:
            json.dump(ordenes, archivo, indent=4, ensure_ascii=False)
        return True
    except OSError:
        return False



def cargar_ordenes():
    """
    Que hace: recupera las ordenes guardadas al abrir el programa y avisa si el
    archivo esta danado.
    Como funciona: pide la lista a leer_archivo_ordenes. Si el archivo esta danado
    avisa y devuelve una lista vacia para que el programa siga funcionando.
    """
    ordenes = leer_archivo_ordenes()
    if ordenes is None:
        print("El archivo de ordenes esta danado. Se inicia sin ordenes guardadas.")
        return []
    return ordenes



def guardar_ordenes(ordenes):
    """
    Que hace: guarda todas las ordenes para que no se pierdan al cerrar el
    programa y avisa si no se pudo.
    Como funciona: le pide a escribir_archivo_ordenes que guarde la lista. Si no
    se pudo escribir, avisa y el programa sigue funcionando.
    """
    if not escribir_archivo_ordenes(ordenes):
        print("Aviso: no se pudieron guardar las ordenes en el archivo.")



def preparar_ordenes(ordenes):
    """
    Que hace: deja lista la lista de ordenes al abrir el menu.
    Como funciona: si la lista llega vacia, le agrega las ordenes guardadas en el
    archivo (cargar_ordenes). Si ya trae ordenes, no la toca.
    """
    if len(ordenes) == 0:
        ordenes.extend(cargar_ordenes())



# ==============================================================
# SECCION 3: BUSCAR ORDEN, ORDENES ABIERTAS Y FACTURAS
#
# Estas funciones se encargan de saber si una orden esta abierta,
# de buscar una orden, de filtrar ordenes y de buscar una factura
# de la tienda. Ninguna imprime mensajes.
# ==============================================================


def esta_abierta(orden):
    """
    Que hace: dice si una orden esta abierta, o sea si todavia puede cambiar de
    estado. Es la unica regla de "abierta/cerrada" del programa.
    Como funciona: mira los estados siguientes de la orden en estados. Devuelve
    True si tiene alguno (abierta) y False si la lista esta vacia (cerrada).
    """
    return len(estados[orden["estado"]]) > 0



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
    Como funciona: recorre las ordenes y busca una con ese codigo de factura que
    este abierta (esta_abierta).
    Devuelve esa orden, o None si no tiene ninguna abierta.
    """
    for orden in ordenes:
        if orden["ticket_compra"] == ticket_compra and esta_abierta(orden):
            return orden
    return None



def filtrar_ordenes(ordenes, abiertas):
    """
    Que hace: separa las ordenes abiertas de las cerradas.
    Como funciona: recorre las ordenes y guarda en una lista nueva las que
    coinciden con lo pedido: abiertas=True devuelve las abiertas y
    abiertas=False devuelve las cerradas. Devuelve esa lista (puede quedar vacia).
    """
    resultado = []
    for orden in ordenes:
        if esta_abierta(orden) == abiertas:
            resultado.append(orden)
    return resultado



def buscar_ticket_compra(tickets_tienda, ticket_compra):
    """
    Que hace: busca en las facturas de la tienda la que tiene el codigo escrito.
    Como funciona: pasa el codigo a mayuscula y lo compara con el campo
    codigo_factura de cada factura.
    Devuelve la factura si la encuentra, o None si no existe.
    """
    codigo = ticket_compra.upper()
    for registro in tickets_tienda:
        if registro["codigo_factura"] == codigo:
            return registro
    return None



# ==============================================================
# SECCION 4: CREAR ORDENES Y CAMBIAR SU ESTADO
#
# Estas funciones se encargan de crear una orden y de cambiar
# su estado, tambien registra el diagnostico, la entrega y cierra
# la orden con la funcion no reparado. No imprimen mensajes.
# ==============================================================


def generar_ticket(ordenes):
    """
    Que hace: inventa el numero de ticket de la siguiente orden (T-001, T-002...).
    Como funciona: cuenta cuantas ordenes hay, le suma 1 y rellena con ceros
    hasta tener 3 digitos (zfill: 1 -> 001). Devuelve el ticket como texto.
    """
    numero = len(ordenes) + 1
    return "T-" + str(numero).zfill(3)



def crear_orden(ticket, registro_compra, falla):
    """
    Que hace: arma la orden de un equipo que entra a servicio tecnico.
    Como funciona: crea la orden en estado "En diagnostico" con el ticket que
    recibe, los datos de la factura y la falla del cliente. Solo la devuelve:
    quien la llama es el que la agrega a la lista (con agregar_orden).
    """
    orden = {
        "ticket": ticket,
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
    return orden



def agregar_orden(ordenes, orden):
    """
    Que hace: agrega una orden nueva a la lista de ordenes.
    Como funciona: la pone al final de la lista (append).
    """
    ordenes.append(orden)



def actualizar_estado(orden, nuevo_estado):
    """
    Que hace: cambia el estado de una orden (Esperando repuesto, En diagnostico,
    Diagnosticado, Reparado, No reparado o Entregado).
    Como funciona: guarda el nuevo estado en la orden. Nada mas: los datos extra
    de cada estado los guardan las funciones de abajo.
    """
    orden["estado"] = nuevo_estado



def registrar_diagnostico(orden, falla_encontrada):
    """
    Que hace: pasa la orden a "Diagnosticado" y guarda la falla que encontro el
    tecnico, que puede ser distinta a la que dijo el cliente.
    Como funciona: guarda la falla en la orden y cambia el estado.
    """
    orden["falla_encontrada"] = falla_encontrada
    actualizar_estado(orden, "Diagnosticado")



def formatear_fecha(fecha):
    """
    Que hace: convierte una fecha al formato que se guarda y se muestra en las
    ordenes (dia/mes/anio, ejemplo: 30/10/2026).
    Como funciona: usa strftime con el formato "%d/%m/%Y". Devuelve el texto.
    """
    return fecha.strftime("%d/%m/%Y")



def registrar_entrega(orden, dias_garantia):
    """
    Que hace: pasa la orden a "Entregado" y guarda los datos de la entrega.
    Como funciona: cambia el estado y guarda la fecha de entrega (hoy), los dias
    de garantia que se dieron y la fecha en que vence esa garantia (hoy mas los
    dias de garantia). Las fechas se guardan con formatear_fecha.
    """
    hoy = date.today()
    vencimiento = hoy + timedelta(days=dias_garantia)
    actualizar_estado(orden, "Entregado")
    orden["fecha_entrega"] = formatear_fecha(hoy)
    orden["dias_garantia"] = dias_garantia
    orden["fecha_vencimiento"] = formatear_fecha(vencimiento)



def marcar_no_reparado(orden, opcion):
    """
    Que hace: cierra la orden como "No reparado" y guarda lo que elige el cliente
    (cambio de equipo o devolucion del dinero). Esta orden ya no se entrega.
    Como funciona: busca la opcion elegida en soluciones, la guarda en la orden y
    cambia el estado.
    """
    orden["solucion"] = soluciones[opcion]
    actualizar_estado(orden, "No reparado")



# ==============================================================
# SECCION 5: MOSTRAR INFORMACION EN PANTALLA
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



def mostrar_lista_ordenes(lista_ordenes, mensaje_vacio):
    """
    Que hace: muestra una lista de ordenes, una tras otra.
    Como funciona: recorre la lista y muestra cada orden con mostrar_detalle. Si
    la lista esta vacia, imprime el mensaje que recibio.
    """
    if len(lista_ordenes) == 0:
        print(mensaje_vacio)
        return

    for orden in lista_ordenes:
        mostrar_detalle(orden)
        print()



def mostrar_ordenes_abiertas(ordenes):
    """
    Que hace: muestra las ordenes abiertas, o sea las que todavia pueden cambiar
    de estado.
    Como funciona: pide las abiertas a filtrar_ordenes y las muestra con
    mostrar_lista_ordenes. Si no hay ninguna, avisa.
    """
    abiertas = filtrar_ordenes(ordenes, True)
    mostrar_lista_ordenes(abiertas, "No hay ordenes abiertas.")



def mostrar_ordenes_cerradas(ordenes):
    """
    Que hace: muestra las ordenes cerradas (Entregado y No reparado), que ya no
    pueden cambiar de estado.
    Como funciona: pide las cerradas a filtrar_ordenes y las muestra con
    mostrar_lista_ordenes. Si no hay ninguna, avisa.
    """
    cerradas = filtrar_ordenes(ordenes, False)
    mostrar_lista_ordenes(cerradas, "No hay ordenes cerradas.")



def mostrar_datos_equipo(registro):
    """
    Que hace: muestra los datos del equipo que vienen en la factura, para que el
    tecnico confirme que es el equipo correcto.
    Como funciona: recorre los campos de la factura y los imprime, menos los datos
    de control (campos_control), que no son del equipo.
    """
    print("\nDatos del equipo encontrados en la tienda:")
    print("-" * 40)
    for campo in registro:
        if campo not in campos_control:
            print(f"  {campo}: {registro[campo]}")
    print("-" * 40)



def mostrar_estados(estados_posibles):
    """
    Que hace: muestra los estados a los que puede pasar una orden, numerados.
    Como funciona: imprime cada estado con su numero, empezando desde 1.
    """
    print("\nEstados disponibles:")
    numero = 1
    for estado in estados_posibles:
        print(f"  {numero}. {estado}")
        numero = numero + 1



# ==============================================================
# SECCION 6: PEDIR DATOS AL USUARIO
#
# Estas funciones se encargan de pedir datos que hay que buscar
# en las ordenes o en las facturas. Las que solo revisan lo
# escrito estan en el modulo validaciones_servicio_tecnico.
# ==============================================================


def pedir_orden_existente(ordenes):
    """
    Que hace: pide un numero de orden y no avanza hasta que exista. Se usa al
    buscar y al actualizar una orden, para no repetir el mismo codigo.
    Como funciona: le pasa a pedir_dato_existente la funcion buscar_orden y la
    lista de ordenes. Devuelve la orden encontrada. Con 0 cancela y devuelve None.
    """
    return pedir_dato_existente(
        "Numero de orden (0 para cancelar): ",
        buscar_orden,
        ordenes,
        "No se encontro esa orden. Verifique el numero e intentelo de nuevo.",
    )



def elegir_estado(estados_posibles):
    """
    Que hace: deja elegir uno de los estados a los que puede pasar una orden.
    Como funciona: guarda en una lista los numeros de las opciones (1, 2, 3...).
    Pide el numero con pedir_opcion y, como las listas empiezan en 0, devuelve el
    estado de la posicion (numero elegido - 1). Los estados se muestran antes con
    mostrar_estados.
    """
    opciones = []
    for numero in range(1, len(estados_posibles) + 1):
        opciones.append(str(numero))
    seleccion = pedir_opcion("Nuevo estado: ", opciones)
    return estados_posibles[int(seleccion) - 1]



# ==============================================================
# SECCION 7: OPCION 1 DEL MENU: RECIBIR EQUIPO
#
# Estas funciones se encargan de recibir un equipo y crear su
# orden.
# ==============================================================


def pedir_factura(tickets_tienda):
    """
    Que hace: pide el codigo de factura del cliente y devuelve su registro de
    compra.
    Como funciona: le pasa a pedir_dato_existente la funcion buscar_ticket_compra y
    la lista de facturas. Si el codigo no existe, avisa. Con 0 cancela y devuelve
    None.
    """
    return pedir_dato_existente(
        "Codigo unico de factura (0 para cancelar): ",
        buscar_ticket_compra,
        tickets_tienda,
        "El codigo de factura no existe en el registro de facturas.\n"
        "Verifique el ticket e intentelo de nuevo, o escriba 0 para cancelar.",
    )



def recibir_equipo(tickets_tienda, ordenes):
    """
    Que hace: registra el ingreso de un equipo a servicio tecnico, desde que se
    pide la factura hasta que se crea la orden.
    Como funciona: solo coordina, cada paso lo hace otra funcion. Si un paso se
    cancela o falla, termina sin crear la orden. Los pasos son: 1) pedir la
    factura, 2) pedir el ticket de garantia, 3) revisar que la garantia este
    vigente, 4) revisar que el equipo no tenga una orden abierta, 5) mostrar los
    datos del equipo y pedir la falla del cliente, 6) crear la orden, agregarla
    a la lista y mostrarla.
    """
    registro = pedir_factura(tickets_tienda)
    if registro is None:
        print("Registro cancelado. Volviendo al menu de servicio tecnico.")
        return

    if not pedir_ticket_garantia(registro):
        print("Registro cancelado. Volviendo al menu de servicio tecnico.")
        return
    if not validar_garantia_vigente(registro):
        print("La garantia de este ticket ya vencio.")
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

    orden = crear_orden(generar_ticket(ordenes), registro, falla)
    agregar_orden(ordenes, orden)
    print(f"Orden registrada. Ticket: {orden['ticket']}")
    mostrar_detalle(orden)



def recibir_equipo_y_guardar(tickets_tienda, ordenes):
    """
    Que hace: es la opcion 1 completa del menu: recibe un equipo y guarda las
    ordenes en el archivo.
    Como funciona: llama a recibir_equipo y despues a guardar_ordenes.
    """
    recibir_equipo(tickets_tienda, ordenes)
    guardar_ordenes(ordenes)



# ==============================================================
# SECCION 8: OPCION 2 DEL MENU: BUSCAR ORDEN
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
# SECCION 9: OPCION 3 DEL MENU: ACTUALIZAR ESTADO
#
# Estas funciones se encargan de cambiar el estado de una
# orden. Cada estado que pide datos extra tiene su propia
# funcion, y actualizar_orden solo las coordina.
# ==============================================================


def procesar_diagnostico(orden):
    """
    Que hace: pide la falla que encontro el tecnico y pasa la orden a "Diagnosticado".
    Como funciona: muestra la falla que dijo el cliente, pide la falla encontrada
    y la guarda con registrar_diagnostico. Devuelve True si se hizo el cambio y
    False si el usuario cancelo.
    """
    print(f"\nFalla reportada por el cliente: {orden['falla']}")
    falla_encontrada = pedir_falla("Falla encontrada por el tecnico (0 para cancelar): ")
    if falla_encontrada is None:
        return False
    registrar_diagnostico(orden, falla_encontrada)
    return True



def procesar_no_reparado(orden):
    """
    Que hace: pide lo que elige el cliente cuando su equipo no se pudo reparar y
    cierra la orden como "No reparado".
    Como funciona: muestra las opciones de soluciones, pide la eleccion con
    pedir_opcion y la guarda con marcar_no_reparado.
    """
    print("\nEl cliente puede elegir:")
    for numero in soluciones:
        print(f"  {numero}. {soluciones[numero]}")
    solucion = pedir_opcion("Solucion elegida: ", list(soluciones))
    marcar_no_reparado(orden, solucion)



def procesar_entrega(orden):
    """
    Que hace: pide los dias de garantia y pasa la orden a "Entregado".
    Como funciona: pide los dias con pedir_dias_garantia y los guarda con
    registrar_entrega.
    """
    dias = pedir_dias_garantia()
    registrar_entrega(orden, dias)



def aplicar_cambio_estado(orden, nuevo_estado):
    """
    Que hace: hace el cambio al estado elegido, pidiendo los datos extra que ese
    estado necesite.
    Como funciona: "Diagnosticado" pide la falla encontrada, "No reparado" pide
    la solucion del cliente, "Entregado" pide los dias de garantia y los demas
    solo cambian el estado. Devuelve True si se hizo el cambio y False si el
    usuario cancelo.
    """
    if nuevo_estado == "Diagnosticado":
        return procesar_diagnostico(orden)
    if nuevo_estado == "No reparado":
        procesar_no_reparado(orden)
    elif nuevo_estado == "Entregado":
        procesar_entrega(orden)
    else:
        actualizar_estado(orden, nuevo_estado)
    return True



def actualizar_orden(ordenes):
    """
    Que hace: es la opcion "Actualizar estado" del menu. Cambia el estado de una
    orden respetando el flujo permitido.
    Como funciona: 1) pide la orden. 2) muestra su estado y revisa que este
    abierta (si esta cerrada, avisa y termina). 3) muestra los estados a los que
    puede pasar (mostrar_estados) y deja elegir uno (elegir_estado). 4) hace el
    cambio con aplicar_cambio_estado.
    5) muestra la orden actualizada.
    """
    orden = pedir_orden_existente(ordenes)
    if orden is None:
        print("Actualizacion cancelada. Volviendo al menu de servicio tecnico.")
        return
    print(f"Estado actual de la orden {orden['ticket']}: {orden['estado']}")

    if not esta_abierta(orden):
        print("Esta orden ya esta cerrada, no se puede cambiar su estado.")
        return

    estados_posibles = estados[orden["estado"]]
    mostrar_estados(estados_posibles)
    nuevo_estado = elegir_estado(estados_posibles)
    if not aplicar_cambio_estado(orden, nuevo_estado):
        print("Actualizacion cancelada. Volviendo al menu de servicio tecnico.")
        return

    print(f"Estado actualizado: {orden['estado']}")
    mostrar_detalle(orden)



def actualizar_orden_y_guardar(ordenes):
    """
    Que hace: es la opcion 3 completa del menu: actualiza el estado de una orden y
    guarda las ordenes en el archivo.
    Como funciona: llama a actualizar_orden y despues a guardar_ordenes.
    """
    actualizar_orden(ordenes)
    guardar_ordenes(ordenes)
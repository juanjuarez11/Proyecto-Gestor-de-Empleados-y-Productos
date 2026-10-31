from datetime import date #Usamos date para comparar la fecha de vencimiento de la garantia con la de hoy


#    Orden por secciones
#
#    1. DATOS DE LAS VALIDACIONES
#    2. VALIDAR LA GARANTIA
#    3. VALIDAR LO QUE ESCRIBE EL USUARIO
#    4. PEDIR DATOS VALIDOS AL USUARIO
#
#    Este modulo no importa a ningun otro modulo del programa.
#    Aqui estan todas las validaciones de los datos de entrada. Las
#    secciones 2 y 3 solo revisan y devuelven True o False (no imprimen ni
#    piden nada). La seccion 4 pide los datos con input, usa esas validaciones
#    y no deja avanzar hasta que lo escrito sea valido.


# ==============================================================
# SECCION 1: DATOS DE LAS VALIDACIONES
#
# Este es el dato que usan las validaciones de entrada.
# ==============================================================


# Maximo de dias de garantia que se pueden dar al entregar un equipo reparado
max_dia_garantia = 30


# ==============================================================
# SECCION 2: VALIDAR LA GARANTIA
#
# Estas funciones se encargan de validar el ticket de garantia
# y que la garantia no este vencida.
# ==============================================================


def validar_ticket_garantia(registro, ticket_garantia):
    """
    Que hace: comprueba que el ticket de garantia escrito sea el de esa factura.
    Como funciona: compara lo escrito (en mayuscula) con el campo ticket_garantia
    de la factura. Devuelve True si son iguales y False si no coinciden.
    """
    return registro["ticket_garantia"] == ticket_garantia.upper()



def validar_garantia_vigente(registro):
    """
    Que hace: dice si la garantia de la factura todavia sirve.
    Como funciona: convierte el campo garantia_hasta (texto AAAA-MM-DD) a fecha y
    la compara con la de hoy. Si ya paso, devuelve False. Si vence hoy o
    despues, devuelve True.
    """
    fecha_vencimiento = date.fromisoformat(registro["garantia_hasta"])
    return fecha_vencimiento >= date.today()



# ==============================================================
# SECCION 3: VALIDAR LO QUE ESCRIBE EL USUARIO
#
# Estas funciones se encargan de revisar un texto ya escrito.
# Solo devuelven True o False.
# ==============================================================


def es_cancelar(texto):
    """
    Que hace: dice si el usuario escribio 0 para cancelar.
    Como funciona: compara el texto con "0". Devuelve True si es igual y False
    si no.
    """
    return texto == "0"



def validar_opcion(texto, opciones):
    """
    Que hace: dice si lo escrito es una de las opciones permitidas.
    Como funciona: busca el texto en la lista de opciones. Devuelve True si esta
    y False si no.
    """
    return texto in opciones



def validar_falla(texto):
    """
    Que hace: dice si la descripcion de una falla es valida.
    Como funciona: una falla es valida si no esta vacia. Devuelve True si tiene
    texto y False si esta vacia.
    """
    return texto != ""



def validar_dias_garantia(texto):
    """
    Que hace: dice si lo escrito sirve como dias de garantia, de 0 hasta el
    maximo permitido (max_dia_garantia).
    Como funciona: primero arma una lista con los dias validos escritos como texto
    ("0", "1", ... "30"). Luego busca el texto en esa lista. Devuelve True si
    esta y False si no.
    """
    dias_validos = []
    for dias in range(max_dia_garantia + 1):
        dias_validos.append(str(dias))
    return texto in dias_validos



# ==============================================================
# SECCION 4: PEDIR DATOS VALIDOS AL USUARIO
#
# Estas funciones se encargan de pedir datos y no dejan
# avanzar hasta que sean validos. Cada una hace tres cosas por
# separado: leer lo escrito (leer_texto), revisarlo (las
# validaciones de arriba) y avisar si esta mal (el print).
# ==============================================================


def leer_texto(mensaje):
    """
    Que hace: lee lo que escribe el usuario. Es la unica funcion del programa que
    usa input para leer texto libre.
    Como funciona: muestra el mensaje, lee lo escrito y le quita los espacios
    sobrantes del principio y del final (strip). No revisa nada.
    """
    return input(mensaje).strip()



def pedir_opcion(mensaje, opciones):
    """
    Que hace: pide al usuario elegir una opcion de una lista y no lo deja avanzar
    hasta que escriba una valida.
    Como funciona: repite la pregunta hasta que validar_opcion acepte lo escrito
    (leido con leer_texto). Si no lo acepta, avisa y vuelve a preguntar.
    """
    while True:
        opcion = leer_texto(mensaje)
        if validar_opcion(opcion, opciones):
            return opcion
        print("Opcion no valida. Intente de nuevo.")



def pedir_falla(mensaje):
    """
    Que hace: pide la descripcion de una falla. Sirve para la falla que dice el
    cliente y para la que encuentra el tecnico, solo cambia el mensaje.
    Como funciona: repite la pregunta hasta que validar_falla acepte lo escrito.
    Devuelve la falla escrita. Con 0 cancela y devuelve None.
    """
    while True:
        falla = leer_texto(mensaje)
        if es_cancelar(falla):
            return None
        if validar_falla(falla):
            return falla
        print("La falla no puede quedar vacia. Describa el problema.")



def pedir_dias_garantia():
    """
    Que hace: pide cuantos dias de garantia se dan al entregar un equipo reparado,
    de 0 hasta el maximo permitido (max_dia_garantia).
    Como funciona: repite la pregunta hasta que validar_dias_garantia acepte lo
    escrito. Devuelve los dias como numero entero.
    """
    while True:
        texto = leer_texto(f"Dias de garantia (0 a {max_dia_garantia}, 0 si no aplica): ")
        if validar_dias_garantia(texto):
            return int(texto)
        print(f"Ingrese un numero entero entre 0 y {max_dia_garantia}.")



def pedir_ticket_garantia(registro):
    """
    Que hace: pide el ticket de garantia y comprueba que sea el de esa factura.
    Como funciona: repite la pregunta hasta que validar_ticket_garantia lo acepte.
    Si no coincide, avisa. Devuelve True si coincide. Con 0 cancela y devuelve False.
    """
    while True:
        ticket = leer_texto("Ticket de garantia (0 para cancelar): ")
        if es_cancelar(ticket):
            return False
        if validar_ticket_garantia(registro, ticket):
            return True
        print("El ticket de garantia no coincide con el registrado en la factura.")
        print("Revise el ticket de garantia e intentelo de nuevo, o escriba 0 para cancelar.")



def pedir_dato_existente(mensaje, buscar, datos, mensaje_error):
    """
    Que hace: pide un dato (un numero de orden, un codigo de factura...) y no deja
    avanzar hasta que exista. Sirve para cualquier dato que se tenga que buscar en
    una lista, solo cambian el mensaje y la funcion de busqueda.
    Como funciona: recibe la funcion "buscar" (por ejemplo buscar_orden) y la lista
    "datos" donde buscar. Repite la pregunta hasta que buscar(datos, texto) encuentre
    algo y lo devuelve. Si no existe, imprime mensaje_error. Con 0 cancela y
    devuelve None. Asi este modulo no necesita importar las funciones de busqueda.
    """
    while True:
        texto = leer_texto(mensaje)
        if es_cancelar(texto):
            return None
        encontrado = buscar(datos, texto)
        if encontrado is not None:
            return encontrado
        print(mensaje_error)
        
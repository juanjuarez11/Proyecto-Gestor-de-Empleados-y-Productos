from datetime import date # date: la fecha de hoy, para revisar si la garantia vencio


#    Orden por secciones
#
#    1. DATOS DE LAS VALIDACIONES
#    2. VALIDAR LA GARANTIA
#    3. VALIDAR LO QUE ESCRIBE EL USUARIO
#    4. PEDIR DATOS VALIDOS AL USUARIO
#
#    Este modulo no importa a ningun otro. Las secciones 2 y 3 solo devuelven
#    True o False. La seccion 4 pide datos con input hasta que sean validos.


# ==============================================================
# SECCION 1: DATOS DE LAS VALIDACIONES
# ==============================================================


# Maximo de dias de garantia que se pueden dar al entregar un equipo
max_dia_garantia = 30


# ==============================================================
# SECCION 2: VALIDAR LA GARANTIA
# ==============================================================


def validar_ticket_garantia(registro, ticket_garantia):
    """
    Que hace: comprueba que el ticket de garantia sea el de esa factura.
    Como funciona: compara lo escrito (en mayuscula) con el de la factura.
    """
    return registro["ticket_garantia"] == ticket_garantia.upper()


def validar_garantia_vigente(registro):
    """
    Que hace: dice si la garantia de la factura todavia sirve.
    Como funciona: compara la fecha garantia_hasta con la de hoy (True si no paso).
    """
    fecha_vencimiento = date.fromisoformat(registro["garantia_hasta"])
    return fecha_vencimiento >= date.today()


# ==============================================================
# SECCION 3: VALIDAR LO QUE ESCRIBE EL USUARIO
# ==============================================================


def es_cancelar(texto):
    """
    Que hace: dice si el usuario escribio 0 para cancelar.
    Como funciona: compara el texto con "0".
    """
    return texto == "0"


def validar_opcion(texto, opciones):
    """
    Que hace: dice si lo escrito es una de las opciones permitidas.
    Como funciona: busca el texto en la lista de opciones.
    """
    return texto in opciones


def validar_falla(texto):
    """
    Que hace: dice si la descripcion de una falla es valida.
    Como funciona: es valida si no esta vacia.
    """
    return texto != ""


def validar_dias_garantia(texto):
    """
    Que hace: dice si lo escrito sirve como dias de garantia (de 0 a max_dia_garantia).
    Como funciona: arma la lista de dias validos como texto y busca el texto ahi.
    """
    dias_validos = []
    for dias in range(max_dia_garantia + 1):
        dias_validos.append(str(dias))
    return texto in dias_validos


# ==============================================================
# SECCION 4: PEDIR DATOS VALIDOS AL USUARIO
# ==============================================================


def leer_texto(mensaje):
    """
    Que hace: lee lo que escribe el usuario
    Como funciona: muestra el mensaje y quita los espacios sobrantes (strip).
    """
    return input(mensaje).strip()


def pedir_opcion(mensaje, opciones):
    """
    Que hace: pide elegir una opcion de una lista hasta que sea valida.
    Como funciona: repite la pregunta hasta que validar_opcion acepte lo escrito.
    """
    while True:
        opcion = leer_texto(mensaje)
        if validar_opcion(opcion, opciones):
            return opcion
        print("Opcion no valida. Intente de nuevo.")


def pedir_falla(mensaje):
    """
    Que hace: pide la descripcion de una falla (la del cliente o la del tecnico).
    Como funciona: repite hasta que validar_falla acepte; con 0 cancela y devuelve None.
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
    Que hace: pide los dias de garantia al entregar un equipo (0 a max_dia_garantia).
    Como funciona: repite hasta que validar_dias_garantia acepte; devuelve un entero.
    """
    while True:
        texto = leer_texto(f"Dias de garantia (0 a {max_dia_garantia}, 0 si no aplica): ")
        if validar_dias_garantia(texto):
            return int(texto)
        print(f"Ingrese un numero entero entre 0 y {max_dia_garantia}.")


def pedir_ticket_garantia(registro):
    """
    Que hace: pide el ticket de garantia y comprueba que sea el de la factura.
    Como funciona: repite hasta que validar_ticket_garantia acepte; con 0 devuelve False.
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
    Que hace: pide un dato (orden, factura...) hasta que exista en una lista.
    Como funciona: usa la funcion "buscar" que recibe; con 0 cancela y devuelve None.
    """
    while True:
        texto = leer_texto(mensaje)
        if es_cancelar(texto):
            return None
        encontrado = buscar(datos, texto)
        if encontrado is not None:
            return encontrado
        print(mensaje_error)

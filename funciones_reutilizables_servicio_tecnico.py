import json # guardar y leer las ordenes en un archivo
import os # saber si ese archivo ya existe



archivo_de_ordenes = "ordenes_servicio_tecnico.json" # archivo donde se guardan las ordenes


def leer_archivo_ordenes():
    """
    Que hace: lee las ordenes guardadas en el archivo .json.
    Como funciona: sin archivo devuelve []; si esta danado devuelve None. No imprime.
    """
    if not os.path.exists(archivo_de_ordenes): # comprueba si el archivo existe,si no, empezamos con una lista vacia
        return []

    try:
        with open(archivo_de_ordenes, "r", encoding="utf-8") as archivo:
            # utf-8: para soportar los acentos y eñes
            ordenes = json.load(archivo) # convierte el archivo json en lista/diccionario
        return ordenes
    except json.JSONDecodeError: # el archivo esta danado (json invalido)
        return None


def escribir_archivo_ordenes(ordenes):
    """
    Que hace: escribe todas las ordenes en el archivo .json.
    Como funciona: json.dump guarda la lista; devuelve True si pudo y False si no.
    """
    try:
        with open(archivo_de_ordenes, "w", encoding="utf-8") as archivo:# se abre el archivo en modo escritura
            json.dump(ordenes, archivo, indent=4, ensure_ascii=False) # indent=4 da formato ordenado y legible; ensure_ascii=False: guarda tildes y ñ
        return True                                                   #ensure_ascii=False evita convertir tildes y eñe en codigos extraños
    except OSError: # no se pudo escribir (disco lleno, sin permisos)
        return False


def generar_ticket(ordenes):
    """
    Que hace: crea el ticket de la siguiente orden (T-001, T-002...).
    Como funciona: cuenta las ordenes, suma 1 y rellena con ceros (zfill: 1 -> 001).
    """
    numero = len(ordenes) + 1 # siguiente numero de orden
    return "T-" + str(numero).zfill(3) # zfill(3) rellena con ceros: 1 -> 001
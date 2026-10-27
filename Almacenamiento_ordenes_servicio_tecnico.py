import json
import os

# Archivo donde se guardan las ordenes (queda en la carpeta donde se ejecuta el programa)
ARCHIVO_ORDENES = "ordenes_servicio_tecnico.json"


# ============================================================
# LEER DEL ARCHIVO
# ============================================================


def cargar_ordenes():
    """
    Que hace: lee del archivo .json las ordenes guardadas (abiertas y cerradas)
    para recuperarlas al abrir el programa.
    Como funciona: si el archivo no existe (primera vez) devuelve una lista vacia.
    Si existe, lo abre y json.load convierte su contenido en la lista de ordenes.
    Si el archivo esta danado (json.load da ValueError), avisa y devuelve una
    lista vacia.
    """
    if not os.path.exists(ARCHIVO_ORDENES): #if not os.path.exists comprueba si el archivo ordenes se encuentra en el disco
        return []

    try:
        with open(ARCHIVO_ORDENES, "r", encoding="utf-8") as archivo:
            ordenes = json.load(archivo)
        return ordenes
    except ValueError:
        print("El archivo de ordenes esta danado. Se inicia sin ordenes guardadas.")
        return []


# ============================================================
# ESCRIBIR EN EL ARCHIVO
# ============================================================


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
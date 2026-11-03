import json, os
#___________________________________________________________________________________________________________________________
def decimales(mensaje):
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print('ERROR: Debe ingresar un numero!!!')
#___________________________________________________________________________________________________________________________
def valor_numerico(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print('ERROR: Debe ingresar un numero entero!!!')
#___________________________________________________________________________________________________________________________
def letras(mensaje):
    while True:
        entrada=input(mensaje).strip()
        
        if all(c.isalpha() or c.isspace()for c in entrada) and entrada!='':
            return entrada.title()
        else:
            print('Error: No puede contener numeros ni estar vacio.')
#___________________________________________________________________________________________________________________________
def numeros_con_guiones(mensaje):
    while True:
        entrada=input(mensaje).strip()
        
        if all(c.isdigit() or c=='-' for c in entrada) and entrada !='':
            return entrada
        else:
            print('ERROR: Solo se aceptan numeros y guiones!!!')
#___________________________________________________________________________________________________________________________
def validar_Fecha(mensaje):
    while True:
        Fecha = numeros_con_guiones(mensaje)
        if len(Fecha) != 10 or Fecha[2] != '-' or Fecha[5] != '-'and all(c.isdigit or c == '-' for c in Fecha):
            print('La fecha debe cumplir con el formato dd-mm-aaaa')
        else:
            return Fecha
#___________________________________________________________________________________________________________________________
def validar_nombre(mensaje):
    while True:
            nombre=letras(mensaje)
            if len (nombre) < 3 or len(nombre) > 50:
                print('El nombre debe tener entre 3 y 50 caracteres')
            else:
                return nombre.title()
#____________________________________________________________________________________________________________________________
def leer_json(A_nombre):
    
    if not os.path.exists(f'{A_nombre}.json'):
        return []
    
    try:
        with open(f"{A_nombre}.json", "r", encoding= "utf-8") as archivo:
            datos = json.load(archivo)
            return datos
    except json.JSONDecodeError:
            print(f"El archivo {A_nombre} está vacío o corrupto.")
            
    except FileNotFoundError:
        print(f'ERROR: El registro de {A_nombre} no existe!!!')
        return False
    
    except Exception:
        print('Error: Ha ocurrido un error inesperado!!!')
#____________________________________________________________________________________________________________________________
def guardar_json(A_nombre, datos):
    try:
        with open(f"{A_nombre}.json", "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")
#____________________________________________________________________________________________________________________________
def imprimir_datos(l_datos):
        
    claves = list(l_datos[0].keys())
    
    ancho_columna = 18  # Espacio fijo para cada celda
    ancho_total = len(claves) * (ancho_columna + 3)
    
    print('-' * max(ancho_total, 50))
    header_str = " | ".join([f"{str(clave).capitalize():<{ancho_columna}}" for clave in claves])
    print(header_str)
    print('-' * max(ancho_total, 50))
    
    for item in l_datos:
        # Extraemos los valores en el mismo orden de las claves
        valores = [str(item.get(clave, "")) for clave in claves]
        fila_str = " | ".join([f"{val:<{ancho_columna}}" for val in valores])
        print(fila_str)
        
    print('-' * max(ancho_total, 50))
    return True
#____________________________________________________________________________________________________________________________
def agregar_dato_n(datos, n_dato):
    datos.append(n_dato)
    return datos
#____________________________________________________________________________________________________________________________
def generar_ticket(ordenes):
    """
    Que hace: crea el ticket de la siguiente orden (T-001, T-002...).
    Como funciona: cuenta las ordenes, suma 1 y rellena con ceros (zfill: 1 -> 001).
    """
    numero = len(ordenes) + 1 # siguiente numero de orden
    return "T-" + str(numero).zfill(3) # zfill(3) rellena con ceros: 1 -> 001
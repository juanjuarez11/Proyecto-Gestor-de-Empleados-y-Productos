import json
import maskpass
import time
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
def texto_con_guiones(mensaje):
    while True:
        entrada=input(mensaje).strip()
        
        if all(c.isdigit() or c=='-' for c in entrada) and entrada !='':
            return entrada
        else:
            print('ERROR: Solo se aceptan numeros y guiones!!!')
#___________________________________________________________________________________________________________________________
def validar_Fecha(mensaje):
    while True:
        Fecha=texto_con_guiones(mensaje)
        if len(Fecha) != 10 or Fecha[2] != '-' or Fecha[5] != '-':
            print('La fecha debe cumplir con el formato dd-mm-aaaa')
        else:
            return Fecha
#___________________________________________________________________________________________________________________________
def validar_anio(mensaje):
    while True:
        anio=valor_numerico(mensaje)
        if anio>=1600 and anio<=2026:
            return anio
        else:
            print('El año no es valido o no esta en el rango establecido!!!')
#___________________________________________________________________________________________________________________________
def verificar_id_libros(libros,mensaje):
    while True:
        id_libro=input(mensaje)
        if all(c.isdigit() for c in id_libro) and id_libro != '':
            existe= any(l["id"] == id_libro for l in libros)        
            if existe:
                print("¡Error: El ID del libro que está tratando de registrar ya se encuentra asignado!")
                continue
            else:
                return id_libro
        else:
            print('Error: Solo se aceptan numeros para el ID y no puede estar vacio!!!')
#___________________________________________________________________________________________________________________________
def verificar_id_usuario(usuarios,mensaje):
    while True:
        id_usuario=validar_id(objeto=usuarios, mensaje=mensaje)
        if  all(c.isdigit() for c in id_usuario) and id_usuario != '':
            existe= any(usuario['id']==id_usuario for usuario in usuarios)
        
            if existe:
                print("¡Error: El ID de usuario que está tratando de registrar ya se encuentra asignado!")
            else:
                return id_usuario
        else:
            print('Solo se aceptan numeros para el ID y no puede estar vacio!!!')
#___________________________________________________________________________________________________________________________
def validar_nombre(mensaje):
    while True:
            nombre=letras(mensaje)
            if len (nombre) < 3 or len(nombre) > 50:
                print('El nombre debe tener entre 3 y 50 caracteres')
            else:
                return nombre.title()
#___________________________________________________________________________________________________________________________
def validar_grado(mensaje):
    while True:
        grado=input(mensaje).lower()
        partes = grado.split()
        if len(partes) == 2:
            numero, palabra = partes
            if numero.isdigit and palabra == 'grado':
                return grado
            else:
                print('Error: el grado debe comenzar con números y terminar con la palabra grado !!!')
        else:
            print('Error: el grado debe cumplir con el formato NN grado !!!')
#___________________________________________________________________________________________________________________________
def validar_id(mensaje, objeto):
    if objeto:
        while True:
            carnet=input(mensaje)
            if all(c.isdigit or c == '-' for c in carnet):
                return carnet
            else:
                print('Solo se aceptan numeros y guiones para el carnet!!!')
    else:
        print('\nNo hay registros por el momento!!!')
        return False
#___________________________________________________________________________________________________________________________
def verificar_id_usuario_existencia(usuarios,mensaje):
    while True:
        id_usuario=input(mensaje)
        if all(c.isdigit() for c in id_usuario) and id_usuario != '':
            existe= any(usuario['id']==id_usuario for usuario in usuarios)
        
            if existe:
                return id_usuario
            else:
                print('El ID no esta registrado')
        else:
            print('Solo se aceptan numeros para el ID y no puede estar vacio!!!')
#___________________________________________________________________________________________________________________________
def verificar_id_libro_existencia(libros,mensaje):
    while True:
        id_libro=input(mensaje)
        if all(c.isdigit() for c in id_libro) and id_libro != '':
            existe= any(libro['id']==id_libro for libro in libros)
        
            if existe:
                return id_libro
            else:
                print('El ID no esta registrado')
        else:
            print('Solo se aceptan numeros para el ID y no puede estar vacio!!!')
#___________________________________________________________________________________________________________________________
def s_n(mensaje):
    while True:
        res=input(mensaje).lower()
        if res == 's' or res == 'n':
            if res == 's':
                return True
            if res == 'n':
                return False
        else:
            print('ERROR: Solo se acepta S o N como respuesta!!!')
#____________________________________________________________________________________________________________________________
def validar_empleado():
    try:
        with open("credenciales.json", "r") as archivo:
            lista_empleados = json.load(archivo)
    except FileNotFoundError:
        print('ERROR: El registro de empleados no existe!!!')
    except Exception:
        print('Error: Ha ocurrido un error inesperado!!!')
        
    intentos_nombre = 3
    acceso_concedido = False

    while intentos_nombre > 0:
        nombre = validar_nombre("Ingrese su nombre y apellido: ")
        nombre_encontrado = None
        for i in lista_empleados:
            if nombre == i["nombre"]:
                nombre_encontrado = i
                break
        if nombre_encontrado is not None and nombre_encontrado['cargo'] == 'supervisor':
            print(f"Nombre Encontrado: {nombre}")
            intentos_carnet = 3
            while intentos_carnet > 0:
                try:
                    carnet = input("Por favor, Ingrese su carnet: ")
                    if str(carnet) == str(nombre_encontrado["carnet"]):
                        print("CARNET CORRECTO. INICIANDO SESIÓN....")
                        acceso_concedido = True
                        break
                    else:
                        intentos_carnet-=1
                        print(f"CARNET INCORRECTO. Intentos restantes: {intentos_carnet}")
                except TypeError:
                    print("Carnet no reconocido")

            if acceso_concedido:
                return True
        elif nombre_encontrado == None:    
            intentos_nombre -= 1
            print(f"ERROR: {nombre} no está en la lista de empleados o no es supervisor. Intentos restantes: {intentos_nombre}")
        elif nombre_encontrado :
            pass
#____________________________________________________________________________________________________________________________
def validar_admin():
    try:
        with open(f"administrador.json", "r") as archivo:
            lista_administradores = json.load(archivo)
    except FileNotFoundError:
        print('ERROR: El registro de administradores no existe!!!')
        
    intentos_username = 3
    acceso_concedido = False

    while intentos_username > 0:
        username = input("Ingrese su nombre de usuario: ")
        username_encontrado = None
        for i in lista_administradores:
            if username == i["username"]:
                username_encontrado = i
                break
        if username_encontrado is not None:
            print(f"Usuario Encontrado: {username}")
            intentos_password = 3
            while intentos_password > 0:
                password = maskpass.askpass(prompt="Por favor, Ingrese su contraseña: ", mask='●')
                if str(password) == str(username_encontrado["password"]):
                    print("INICIANDO SESIÓN....")
                    
                    acceso_concedido = True
                    break
                else:
                    intentos_password-=1
                    print(f"CONTRASEÑA INCORRECTA. Intentos restantes: {intentos_password}")
            if acceso_concedido:
                break
        else:
            intentos_username -= 1
            print(f"ERROR: {username} no está en la lista de empleados. Intentos restantes: {intentos_username}")
#____________________________________________________________________________________________________________________________
def bloqueo():
    
    try:
        with open('t_bloqueo.txt' , 'r') as tb:
            t_bloqueo = int(tb)
    except FileNotFoundError:
        print('Error: Archivo de bloqueo no encontrado!!!')
    except Exception:
        print('Error en general en el bloqueo!!!')
    tiempo_actual = time.time()
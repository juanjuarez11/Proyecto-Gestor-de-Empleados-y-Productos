import json
import maskpass
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
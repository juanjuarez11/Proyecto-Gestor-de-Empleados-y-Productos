import json, time, maskpass as mp, os
from datetime import datetime, timedelta

# Este es el modulo encargado de los bloqueos y validacion de datos de empleados y admins.
# Se cuanta co 7 funciones de dicadas completamente en seguridad del programa.

# Funcion encargada de verificar si hay un bloqueo sin concluir.
#____________________________________________________________________________________________________________________________
def verificar_bloqueo():
    try:
        with open("bloqueo.json", "r") as archivo:
            datos = json.load(archivo)
            expiracion = datetime.fromisoformat(datos["expiracion"])
            ahora = datetime.now()
            
            if ahora < expiracion:
                segundos_restantes = int((expiracion - ahora).total_seconds())
                return True, segundos_restantes
                
    except (FileNotFoundError, json.JSONDecodeError):
        pass
        
    return False, 0

# Funcion encargada de guardar un bloqueo en json
#____________________________________________________________________________________________________________________________
def guardar_bloqueo():
    expiracion = datetime.now() + timedelta(seconds=20)
    with open("bloqueo.json", "w") as archivo:
        json.dump({"expiracion": expiracion.isoformat()}, archivo)
    
# Funcion encargada de ocultar los password y carnets.
#____________________________________________________________________________________________________________________________
def ocultar_escritura(mensaje):
    dato = mp.askpass(prompt=mensaje, mask='●')
    return dato

# Funcion encargada de ejecutar un bloqueo pendiente.
#____________________________________________________________________________________________________________________________
def bloqueo_pendiente(bloqueo, segundos):
    
    if bloqueo:
        print(f"ACCESO DENEGADO: Sistema bloqueado temporalmente.")
        for i in range(segundos + 1):
            print(f"Desbloqueo en {segundos} segundos. ", end='\r')
            time.sleep(1)
            segundos -= 1
        print()
        return
    else:
        return
    
# Funcion encargada de buscar el admin o empleado.
#____________________________________________________________________________________________________________________________
def validar_perfil(l_credenciales, clave_user, clave_c, user, credencial):
    for i in l_credenciales:
        if i[clave_user] == user and i[clave_c] == credencial:
            return i
        else:
            continue
    return False

# Funcion encargada de validar el acceso por cargos
#____________________________________________________________________________________________________________________________
def validar_acceso(exito,usuario):
    if exito:
        
        if usuario.get("estado") == "inactivo":
            print("Acceso denegado: Su usuario está inactivo.")
            return False
            
        cargo = usuario.get("cargo")
        if cargo is None:
            print("Acceso concedido como Administrador.")
            return True
            
        elif cargo in ["supervisor", "cajero", "tecnico"]:
            print(f"Acceso concedido con cargo: {cargo}")
            return True
            
        else:
            print("Acceso denegado: No tiene un cargo autorizado.")
            return False

# Funcion principal que se encarga de solicitar los datos
#____________________________________________________________________________________________________________________________
def login(l_credenciales, t_user, t_credencial):
    
    while True:
        
        os.system('cls' if os.name == 'nt' else 'clear')
        bloqueo,segundos = verificar_bloqueo()
        
        bloqueo_pendiente(bloqueo=bloqueo, segundos=segundos)
        
        if bloqueo:
            os.system('cls' if os.name == 'nt' else 'clear')
        
        for i in range(3):
            
            contador = i + 1
            print('\n' + f'===============Intento {contador}================')
            print('\n' + '=' * 40 + '\n')
            
            user = input(f'- Ingrese su {t_user}: ')
            print('\n' + '=' * 40 + '\n')
            
            credencial = ocultar_escritura(f'- Ingrese su {t_credencial}: ')
            print('\n' + '=' * 40 + '\n')
            
            perfil=validar_perfil(l_credenciales= l_credenciales, clave_user= t_user, clave_c= t_credencial, user= user, credencial= credencial)
            
            if perfil:
                
                if validar_acceso(exito= True, usuario= perfil) != True:
                    continue
                
                else:
                    return perfil,True
                
            else:
                print(f'Error: {t_user} o {t_credencial} es incorrecto!!!')
                print(f'Le quedan {3 - contador} intento/s')
            
        else:
            guardar_bloqueo()
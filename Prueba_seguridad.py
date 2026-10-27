import pruebaJSON as pj
import Bloqueo_Seguridad as bs

admins = pj.leer_json(A_nombre='Administrador')

def validar(admins, usser, contrasena):
    for i in admins:
        if i['username'] == usser and i['password'] == contrasena:
            return True
        else:
            continue
    return False

while True:
    bloqueo,segundos=bs.verificar_bloqueo()

    bs.bloqueo_pendiente(bloqueo=bloqueo, segundos=segundos)
    

    for i in range(3):
        
        contador = i + 1
        print(f'Intento {contador}')
        
        usser = input('Ingrese su usuario: ')
        contrasena = bs.ocultar_escritura('Ingrese su contrasena: ')
        
        if validar(admins=admins, usser=usser,contrasena=contrasena):
            print('SISTEMA DESBLOQUEADO')
            break
        else:
            print('Error: La contrasena o el usuario es incorrecto!!!')
            print(f'Le quedan {3 - contador} intento/s')
    
    else:
        bs.guardar_bloqueo()
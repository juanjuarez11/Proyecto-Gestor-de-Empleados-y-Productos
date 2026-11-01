import json
from datetime import datetime, timedelta
import time
import maskpass as mp
from Funciones_Proyecto import letras
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

def guardar_bloqueo():
    expiracion = datetime.now() + timedelta(seconds=20)
    with open("bloqueo.json", "w") as archivo:
        json.dump({"expiracion": expiracion.isoformat()}, archivo)
    

def ocultar_escritura(mensaje):
    dato = mp.askpass(prompt=mensaje, mask='●')
    return dato

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
    
def validar_perfil(l_credenciales, clave_user, clave_c, user, credencial):
    for i in l_credenciales:
        if i[clave_user] == user and i[clave_c] == credencial:
            return True
        else:
            continue
    return False
    
def inicio_secion_seguro(l_credenciales, t_user, t_credencial):
    
    while True:
        bloqueo,segundos = verificar_bloqueo()

        bloqueo_pendiente(bloqueo=bloqueo, segundos=segundos)
        

        for i in range(3):
            
            contador = i + 1
            print('\n' + f'======Intento {contador}======')
            print('\n' + '=' * 40 + '\n')
            
            user = input(f'Ingrese su {t_user}: ')
            print('\n' + '=' * 40 + '\n')
            
            credencial = ocultar_escritura(f'Ingrese su {t_credencial}: ')
            print('\n' + '=' * 40 + '\n')
            
            if validar_perfil(l_credenciales= l_credenciales, clave_user= t_user, clave_c= t_credencial, user= user, credencial= credencial):
                print(f'======Bienvenido {user}======')
                return True
                
            else:
                print(f'Error: {t_user} o {t_credencial} es incorrecto!!!')
                print(f'Le quedan {3 - contador} intento/s')
        
        else:
            guardar_bloqueo()
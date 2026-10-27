import json
from datetime import datetime, timedelta
import time
import maskpass as mp
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
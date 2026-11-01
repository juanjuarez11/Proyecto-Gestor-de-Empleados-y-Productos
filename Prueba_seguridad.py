import pruebaJSON as pj
import Bloqueo_Seguridad as bs

admins = pj.leer_json(A_nombre='Administrador')
inicio_sesion = False

if bs.inicio_secion_seguro(l_credenciales=admins, t_user='username', t_credencial='password'):
    inicio_sesion = True
    
while inicio_sesion:
    print('Se inicio sesion con exito')
    break
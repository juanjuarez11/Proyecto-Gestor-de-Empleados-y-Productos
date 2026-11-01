import pruebaJSON as pj
import Bloqueo_Seguridad as bs

admins = pj.leer_json(A_nombre='Administrador')
inicio_sesion = False

user,inicio_secion = bs.inicio_secion_seguro(l_credenciales=admins, t_user='username', t_credencial='password')

while inicio_secion:
    print(f'======Bienvenido {user}======')
    break

import pruebaJSON as pj
import Bloqueo_Seguridad as bs

emp = pj.leer_json(A_nombre='Empleados')
inicio_sesion = False

user,cargo,inicio_sesion = bs.inicio_sesion_seguro(l_credenciales=emp, t_user='nombre', t_credencial='carnet')

while inicio_sesion:
    print(f'======Bienvenido {user}======')
    print(cargo)
    break

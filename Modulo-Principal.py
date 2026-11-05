import Bloqueo_Seguridad as bs
from Funciones_Proyecto import leer_json as lj, s_n
import menus
import Historial_Pilas as hp

def ejecutar_proceso():
    
    adminitradores = lj(A_nombre= 'Administrador')
    empleados = lj(A_nombre= 'Empleados')
    productos = lj(A_nombre= 'Productos')
    ventas = lj(A_nombre= 'Ventas')
    historial = hp.PilaHistorial()
    historial.cargar_historial_json()
    while True:
        print('----------------INICIO SESION----------------')
        print()
        print(" - Administrador.")
        print(" - Empleado.")
        print(" - Cerrar.")
        print()
        user = bs.validar_tipo_user('Como desea iniciar sesion: ')
        print()
        
        match user:
            case 'Administrador':
                t_user= 'username'
                t_clave = 'password'
                l_credenciales = adminitradores
            case 'Empleado':
                t_user = 'nombre'
                t_clave = 'carnet'
                l_credenciales = empleados
            case 'Cerrar':
                exit()
            case False:
                continue
        
        perfil,inicio_sesion = bs.login(l_credenciales= l_credenciales, t_user= t_user , t_credencial= t_clave)
        user_p = perfil[t_user]
        cargo = bs.validar_acceso_cargo(usuario= perfil, exito= inicio_sesion)
        print('-' * 70)
        print()
        
        while inicio_sesion:
            hp.registrar_historial(historial= historial, user=user_p , accion= f'Inicio sesion como {cargo}')
            
            if menus.menus(historial=historial, user= perfil[t_user], cargo= cargo, productos= productos,ventas=ventas,empleados=empleados) != True:
                break

ejecutar_proceso()
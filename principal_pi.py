import Funciones_Proyecto as fp, funciones_inicio_sesion as fis, funciones_menu as f

def mostrar_menu_inicio():
    print("=" * 20)
    print("INICIO DE SESIÓN")
    print("=" * 20)
    print("1. Iniciar como Administrador.")
    print("2. Iniciar como Empleado.")
    print("3. Cerrar sistema.")
    return fp.letras("Ingrese una opción (administrador/empleado/cerrar): ").strip().lower()

def procesar_login_admin(administradores):
    exito,cargo_encontrado =fis.validar_inicio_sesion(administradores,"username","password")
    if exito:
        print("Sesión de administrador iniciada correctamente.")
        return cargo_encontrado
    else:
        print("No se pudo iniciar sesión como administrador. Intente nuevamente.\n")
        return None

def procesar_login_empleado(empleados):
    exito,cargo_encontrado = fis.validar_inicio_sesion(empleados,"nombre","carnet")
    if exito:
        print(f"Sesión iniciada correctamente como: {cargo_encontrado}")
        return cargo_encontrado
    else:
        print("No se pudo iniciar sesión como empleado. Intente nuevamente.\n")
        return None

def ejecutar_proceso():
    empleados = f.leer_json("credenciales")
    administradores = f.leer_json("administrador")
    while True:
        res = mostrar_menu_inicio()
        if not res:
            print("Opción no valida.\n")
            continue
        if res in ["empleado","emp"]:
            if procesar_login_empleado(empleados):
                break
        elif res in ["administrador","admin"]:
            if procesar_login_admin(administradores):
                break
                
        elif res in ["cerrar","c"]:
            print("Cerrando sistema...")
            break

        else:
            print("Opción no válida.\n")

    return res
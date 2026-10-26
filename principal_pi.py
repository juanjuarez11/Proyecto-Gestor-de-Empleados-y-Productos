import Funciones_Proyecto as fp, funciones_inicio_sesion as fis, funciones_menu as f
empleados = f.leer_json("credenciales")
administradores = f.leer_json("administrador")
def ejecutar_proceso():
    print("=" * 20)
    print("INICIO DE SESIÓN")
    print("=" * 20)

    while True:
        print("1. Iniciar como Administrador.")
        print("2. Iniciar como Empleado.")
        print("3. Cerrar sistema.")
        res = fp.letras("Ingrese una opción (administrador/empleado/cerrar): ").strip().lower()
        
        if res:    
            if res == "empleado" or res=="emp":
                if fis.validar_inicio_sesion(empleados,"nombre","carnet"):
                    print("Sesión de empleado iniciada correctamente.")
                    break 
                else:
                    print("No se pudo iniciar sesión como empleado. Intente nuevamente.\n")
                    
            elif res == "administrador" or res=="admin":
                if fis.validar_inicio_sesion(administradores,"username","password"):
                    print("Sesión de administrador iniciada correctamente.")
                    break 
                else:
                    print("No se pudo iniciar sesión como administrador. Intente nuevamente.\n")
                    
            elif res == "cerrar" or res=="c":
                print("Cerrando sistema...")
                break

        else:
            print("Opción no válida.\n")

    return res
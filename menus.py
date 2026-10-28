from principal_pi import ejecutar_proceso
from Gestion_de_personal import admin
import Funciones_Proyecto as fp, funciones_menu as fm

productos = fm.leer_json("productos")

def menu():
    while True:
        cargo = ejecutar_proceso()

        if cargo == "administrador":
            menu_administradores()
        elif cargo == "supervisor":
            menu_supervisor() 
        elif cargo == "cajero":
            menu_cajero() 
        elif cargo == "tecnico":
            menu_tecnico()      
        elif cargo == "cerrar":
            break
        else:
            print("Opción no válida o sesión no autorizada.\n")

def menu_administradores():
        while True:
            print("---BIENVENIDO AL SISTEMA---")
            print("Opciones de Administrador: ")
            print("1. Busqueda y Actualización de Empleados")
            print("2. Dar de Alta Empleados")
            print("3. Dar de Baja Empleados")
            print("4. Salir del Sistema")
            opcion = fp.valor_numerico("Escoja una opción (1-4): ")
            match opcion:
                case 1:
                    admin.Busqueda_actualizacion()
                case 2:
                    admin.Alta_integ()
                case 3:
                    admin.Baja_empleado()
                case 4:
                    print("Saliendo del sistema...")
                    break

def menu_supervisor():
        while True:
            print("\n" + "="*25)
            print("   MENÚ DE SUPERVISOR")
            print("="*25)
            print("1. Visualizar datos de empleados.")
            print("2. Agregar productos.")
            print("3. Eliminar productos.")
            print("4. Cambiar datos de productos.")
            print("5. Cerrar Sesión.")
            
            opcion = fp.valor_numerico("Ingrese una opción (1-5): ")
            match opcion:
                case 1:
                    fm.ver_datos(fm.emp) if hasattr(fm, 'ver_datos') else print("Función no disponible")
                case 2:
                    fm.agregar_productos()
                case 3:
                    pass  
                    fm.cambiar_dato()
                case 5:
                    print("Cerrando sesión de supervisor...")
                    break
                case _:
                    print("Opción no válida.")
            
def menu_cajero():
    while True:
        print("\n" + "="*25)
        print("     MENÚ DE CAJERO")
        print("="*25)
        print("1. Realizar Venta.")
        print("2. Visualizar Inventario.")
        print("3. Cerrar Sesión.")
        opcion = fp.valor_numerico("Ingrese una opción (1-3): ")
        match opcion:
            case 1:
                fm.realizar_venta(productos)
            case 2:
                fm.visualizar_inventario(productos)
            case 3:
                print("Saliendo del sistema...")
                break
            case _:
                print("Opción no válida.")
        

def menu_tecnico():
    while True:
        print("\n" + "="*25)
        print("     MENÚ DE TÉCNICO")
        print("="*25)
        print("1. (Módulo en desarrollo)")
        print("2. (Módulo en desarrollo)")
        print("3. Cerrar Sesión.")
        opcion = fp.valor_numerico("Ingrese una opción (1-3): ")
        match opcion:
            case 1:
                pass
            case 2:
                pass
            case 3:
                print("Saliendo del sistema...")
                break
            case _:
                print("Opción no válida.")  
               
if __name__ == "__main__":
    menu()

from principal_pi import ejecutar_proceso
from Gestion_de_personal import admin
import Funciones_Proyecto as fp, funciones_menu as fm, funciones_empleados as fe

productos = fm.leer_json("productos")
empleados = fm.leer_json("credenciales")
productos = fm.leer_json("productos")
#Controla el flujo principal de ejecución y redirige al menú correspondiente según el rol autenticado.
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

#Despliega las opciones de gestión, alta y baja de personal para los administradores.
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

#Muestra el menú interactivo para el control de inventario y datos de empleados.
def menu_supervisor():
        while True:
            print("\n" + "="*25)
            print("   MENÚ DE SUPERVISOR")
            print("="*25)
            print("1. Visualizar datos de empleados.")
            print("2. Visualizar Inventario.")
            print("3. Agregar productos.")
            print("4. Eliminar productos.")
            print("5. Cambiar datos de productos.")
            print("6. Cerrar Sesión.")
            
            opcion = fp.valor_numerico("Ingrese una opción (1-6): ")
            match opcion:
                case 1:
                    fe.ver_datos(empleados,"EMPLEADOS")
                case 2:
                    fe.ver_datos(productos,"INVENTARIO")
                case 3:
                    fe.agregar_productos(productos)
                case 4:
                    fe.proceso_eliminar(productos)
                case 5:  
                    fe.cambiar_dato(productos)
                case 6:
                    print("Cerrando sesión de supervisor...")
                    break
                case _:
                    print("Opción no válida.")

#Presenta las opciones accesibles para los cajeros, incluyendo ventas, inventario y arqueo.          
def menu_cajero():
    while True:
        print("\n" + "="*25)
        print("     MENÚ DE CAJERO")
        print("="*25)
        print("1. Realizar Venta.")
        print("2. Visualizar Inventario.")
        print("3. Realizar Arqueo de Caja.")
        print("4. Cerrar Sesión.")
        opcion = fp.valor_numerico("Ingrese una opción (1-4): ")
        match opcion:
            case 1:
                fe.realizar_venta(productos)
            case 2:
                fp.ver_datos(productos,"INVENTARIO")
            case 3:
                fe.realizar_arqueo()
            case 4:
                print("Saliendo del sistema...")
                break
            case _:
                print("Opción no válida.")
        
#Despliega el menú correspondiente al rol de técnico.
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

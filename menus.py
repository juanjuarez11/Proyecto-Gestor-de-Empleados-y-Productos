from principal_pi import ejecutar_proceso
from Gestion_de_personal import admin
import Funciones_Proyecto as fp, funciones_menu as fm

productos = fm.leer_json("celulares")
def menu():
    while True:
        global res
        res = ejecutar_proceso()
        if res == "administrador" or  res=="admin":
            menu_administradores()
        elif res == "empleado" or res=="emp":
            menu_empleados()      
        elif res == "cerrar" or "c":
            break

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

def menu_empleados():
        while True:
            print("---BIENVENIDO AL SISTEMA---")
            print("Opciones de Empleado")
            print("1. Supervisor")
            print("2. Cajero")
            print("3. Técnico")
            print("4. Salir")
            cargo = fp.valor_numerico("Elija una opción (1-4): ")
            match cargo:
                case 1:
                    while True:
                        print("="*25)
                        print("Opciones de Supervisor:")
                        print("-"*25)
                        print("1. Visualizar datos de empleados.")
                        print("2. Agregar productos.")
                        print("3. Eliminar productos.")
                        print("4. Cambiar datos de productos.")
                        print("5. Salir.")
                        opcion = fp.valor_numerico("Ingrese una opción (1-5): ")
                        match opcion:
                            case 1:
                                fm.ver_datos_emp()
                            case 2:
                                fm.agregar_productos()
                            case 3:
                                pass
                            case 4:
                                fm.cambiar_dato()
                            case 5:
                                print("Saliendo del sistema...")
                                break
                            case _:
                                print("Opción no válida.")

                case 2:
                    while True:
                        print("="*25)
                        print("Opciones de Cajero:")
                        print("-"*25)
                        print("1. Realizar Venta.")
                        print("2. Visualizar Inventario.")
                        print("3. Salir.")
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
                        

                case 3:
                    while True:
                        print("="*25)
                        print("Opciones de Técnico:")
                        print("-"*25)
                        print("1. ")
                        print("2. ")
                        print("3. Salir.")
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
                case 4:
                    print("Saliendo..")
                    break                
if __name__ == "__main__":
    menu()

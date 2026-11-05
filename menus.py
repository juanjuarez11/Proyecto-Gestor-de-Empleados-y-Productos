import Funciones_Proyecto as fp, funciones_empleados as fe, Gestion_de_personal as gp
from Historial_Pilas import registrar_historial as rh
#Controla el flujo principal de ejecución y redirige al menú correspondiente según el rol autenticado.

def menus(historial, user, cargo, empleados, productos, ventas):
    while True:

        if cargo == "administrador":
            if menu_administradores(historial= historial, user= user, empleados= empleados) != True:
                return False
        elif cargo == "supervisor":
            if menu_supervisor(historial= historial, user= user, empleados= empleados, productos= productos) != True:
                return False
        elif cargo == "cajero":
            if menu_cajero(historial= historial,user= user, productos=productos, ventas= ventas) != True:
                return False

#Despliega las opciones de gestión, alta y baja de personal para los administradores.
def menu_administradores(historial, user, empleados):
        while True:
            print("---BIENVENIDO AL SISTEMA---")
            print("Opciones de Administrador: ")
            print("1. Busqueda y Actualización de Empleados")
            print("2. Dar de Alta Empleados")
            print("3. Dar de Baja Empleados")
            print("4. Visualizar Empleados")
            print("5. Salir del Sistema")
            opcion = fp.valor_numerico("Escoja una opción (1-5): ")
            match opcion:
                case 1:
                    exito = gp.Actualizar_datos(empleados= empleados)
                    if exito:
                        rh(historial=historial, user= user, accion='Actualizo un empleado')
                case 2:
                    exito = gp.Alta_integ(empleados= empleados)
                    if exito:
                        rh(historial=historial, user= user, accion='Registro un nuevo empleado')
                case 3:
                    exito = gp.Baja_empleado(empleados= empleados)
                    if exito:
                        rh(historial=historial, user= user, accion='Elimino un empleado')
                case 4:
                    fp.imprimir_datos(l_datos=empleados)
                    rh(historial=historial, user= user, accion='Reviso datos de los empleados')
                case 5:
                    print("Saliendo del sistema...")
                    rh(historial=historial, user= user, accion='Cerro sesion')
                    return False
                case _:
                    print('Error: Opcion no valida')
                    if fp.s_n('De Volver al menu de administrador: ') != True:
                        return False

#Muestra el menú interactivo para el control de inventario y datos de empleados.
def menu_supervisor(historial, user, empleados,productos):
        while True:
            print("\n" + "="*25)
            print("----------MENÚ DE SUPERVISOR----------")
            print("="*25)
            print()
            print("1. Visualizar datos de empleados.")
            print("2. Visualizar Inventario.")
            print("3. Agregar productos.")
            print("4. Eliminar productos.")
            print("5. Cambiar datos de productos.")
            print("6. Cerrar Sesión.")
            print()
            opcion = fp.valor_numerico("Ingrese una opción (1-6): ")
            match opcion:
                case 1:
                    fp.imprimir_datos(l_datos= empleados)
                    rh(historial=historial, user= user, accion='Reviso datos de los empleados')
                case 2:
                    fp.imprimir_datos(l_datos= productos)
                    rh(historial=historial, user= user, accion='Reviso datos de los productos')
                case 3:
                    exito = fe.agregar_productos(productos= productos)
                    if exito:
                        rh(historial=historial, user= user, accion='Registro un nuevo producto')
                case 4:
                    exito = fe.proceso_eliminar(productos= productos)
                    if exito:
                        rh(historial=historial, user= user, accion='Elimino un producto')
                case 5:  
                    fe.cambiar_dato(productos= productos)
                    rh(historial=historial, user= user, accion='Actualizo un producto')
                case 6:
                    print("Cerrando sesión de supervisor...")
                    rh(historial=historial, user= user, accion='Cerro sesion')
                    return False
                case _:
                    print("Opción no válida.")

#Presenta las opciones accesibles para los cajeros, incluyendo ventas, inventario y arqueo.          
def menu_cajero(historial, user, productos, ventas):
    while True:
        print("\n" + "="*25)
        print("----------MENÚ DE CAJERO----------")
        print("="*25)
        print()
        print("1. Realizar Venta.")
        print("2. Visualizar Inventario.")
        print("3. Realizar Arqueo de Caja.")
        print("4. Cerrar Sesión.")
        print()
        opcion = fp.valor_numerico("Ingrese una opción (1-4): ")
        match opcion:
            case 1:
                exito = fe.realizar_venta(productos=productos, ventas= ventas)
                if exito:
                    rh(historial=historial, user= user, accion='Realizo una venta')
            case 2:
                fp.imprimir_datos(l_datos=productos)
                rh(historial=historial, user= user, accion='Reviso datos de los productos')
            case 3:
                exito = fe.realizar_arqueo()
                if exito:
                    rh(historial=historial, user= user, accion='Realizo un arqueo')
            case 4:
                print("Saliendo del sistema...")
                rh(historial=historial, user= user, accion='Cerro sesion')
                return False
            case _:
                print("Opción no válida.")
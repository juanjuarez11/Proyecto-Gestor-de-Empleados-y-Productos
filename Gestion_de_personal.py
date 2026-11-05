import Funciones_Proyecto as f_original
import Logica_GE as logic
import Actualizaciones_GE as actualizacion

# Modulo de funciones del Administrador
# Contiene 3 funciones exclusivas para administradores.

# Funcion para el regirtro de empleados.
def Alta_integ(empleados):
    print("\n--- REGISTRO DE NUEVO INTEGRANTE ---\n")

    while True:
        # 1. Validación de Nombre
        nom = f_original.letras("Nombre completo del integrante: ")
        if logic.val_Two(clave="nombre", valor=nom, empleados=empleados):
            print(f"{nom} ya se encuentra registrado.\n")
            if f_original.s_n("¿Desea intentarlo de nuevo? S/N: "):
                continue
        
            return
        print("")

        # 2. Validación de Correo (Formato y Duplicidad)
        print("Formato esperado: Username@gmail.com")
        while True:
            correo = input("Correo: ").strip().lower()
            if not logic.val_formato_correo(correo):
                print("El correo no cumple con el formato requerido.\n")
                continue
            if logic.val_Two(clave="correo", valor=correo, empleados=empleados):
                print("Este correo ya se encuentra registrado.\n")
                continue
            break
        print("")

            # 3. Validación de Carnet
        carnet =logic.asignar_carnet(empleados=empleados)

        # 4. Validación de Cargo
        print("Cargos disponibles: ---Supervisor---Asistente---Presentador---Limpieza---Cajero---")
        print('-' * 70)
        cargo = f_original.letras("Cargo: ")
        print('-' * 70)
        if not logic.val_cargo(cargo=cargo):
            print("El cargo ingresado no es válido.\n")
            if f_original.s_n("¿Desea intentarlo de nuevo? S/N: "):
                continue
            return
        print("")
        # Asignación automática de salario según el cargo
        salario = logic.asig_salario(cargo=cargo)

        # 5. Validación de Estado
        print("Estados disponibles: ---activo---inactivo---")
        estado = f_original.letras("Estado: ")
        if not logic.val_estado(estado):
            print(" El estado ingresado no es válido.\n")
            if f_original.s_n("¿Desea intentarlo de nuevo? (S/N): "):
                continue
            return

        # 6. Guardar el registro en la lista y en el JSON
        logic.registrar(nom, correo, carnet, cargo, str(salario), estado, empleados)
        if f_original.s_n('Desea volver a registrar otro empleado (S/N): ') != True:
            break
    
# Funicion para eliminar empleados.
def Baja_empleado(empleados):
    print("\n--- DAR DE BAJA A EMPLEADO ---\n")
    while True:
        print('-' * 70)
        carnet = f_original.valor_numerico("Carnet del empleado a eliminar: ")
        print('-' * 70)
        print()

        # 1. Validar si el carnet existe usando la capa de negocio
        if not logic.val_Two(clave="carnet", valor=str(carnet), empleados=empleados):
            print(f"El carnet {carnet} no le pertenece a ningún empleado.\n")
            if f_original.s_n("¿Desea intentarlo de nuevo? S/N: "):
                continue
            return
        
        # 2. Eliminar el registro (la función logic.eliminar se encarga de borrarlo y actualizar el JSON)
        logic.eliminar(str(carnet), empleados)
        print("Empleado eliminado exitosamente.\n")
        if f_original.s_n('Desea eliminar otro empleado : ') != True:
            break
    
# Funcion para actualizar los datos de los empleados.
def Actualizar_datos(empleados):
    print("\n--- ACTUALIZAR DATOS DE EMPLEADO ---\n")
    
    while True:
        print('-' * 70)
        carnet = f_original.valor_numerico(
            "Ingrese el carnet del usuario a modificar: "
        )
        print('-' * 70)
        print()
        
        # 1. Verificar si el carnet existe
        if not logic.val_Two(clave="carnet", valor=str(carnet), empleados=empleados):
            print(f"El carnet {carnet} no le pertenece a ningún empleado.\n")
            if f_original.s_n("¿Desea intentarlo de nuevo? S/N: "):
                continue
            return
            
        # 2. Bucle para permitir múltiples modificaciones al mismo empleado
        while True:
            print("\nCampos disponibles: --nombre--correo--cargo--carnet--salario--estado--")
            print('-' * 70)
            deseo = f_original.letras("Qué dato desea modificar: ").lower()
            print('-' * 70)
            print()
            
            match deseo:
                case "nombre":
                    actualizacion.actualizar_nombre(empleados=empleados,carnet=str(carnet))
                case "correo":
                    actualizacion.actualizar_correo(empleados=empleados,carnet=str(carnet))
                case "carnet":
                    actualizacion.actualizar_carnet(empleados=empleados,carnet=str(carnet))
                case "cargo":
                    actualizacion.actualizar_cargo(empleados=empleados,carnet=str(carnet))
                case "salario":
                    actualizacion.actualizar_salario(empleados=empleados,carnet=str(carnet))
                case "estado":
                    actualizacion.actualizar_estado(empleados=empleados,carnet=str(carnet))
                case _:
                    print("Opción de dato inválida.")
                    if f_original.s_n("¿Desea intentarlo de nuevo? S/N: "):
                        continue
                    break
        # Preguntar si desea modificar otro dato del mismo empleado
            if f_original.s_n("¿Desea modificar otro dato? S/N: "):
                continue
            break
        break
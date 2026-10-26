import Funciones_Proyecto as f_original
import Funciones_personal as f_n
import json
with open("credenciales.json","r")as archivo:
    empleados=json.load(archivo)
def Alta_integ(empleados):
  print("\n--- REGISTRO DE NUEVO INTEGRANTE ---")

  while True:
    # 1. Validación de Nombre
    nom = f_original.letras("Nombre completo del integrante: ")
    if f_n.val_Two(clave="nombre", valor=nom, empleados=empleados):
      print(f"{nom} ya se encuentra registrado.\n")
      if f_original.s_n("¿Desea intentarlo de nuevo? S/N: "):
        continue
      return

    # 2. Validación de Correo (Formato y Duplicidad)
    print("Formato esperado: Username@gmail.com")
    while True:
        correo = input("Correo: ").strip().lower()
        if not f_n.val_formato_correo(correo):
            print("El correo no cumple con el formato requerido.\n")
            continue
        if f_n.val_Two(clave="correo", valor=correo, empleados=empleados):
            print("Este correo ya se encuentra registrado.\n")
            continue
        break

    # 3. Validación de Carnet
    carnet = f_original.valor_numerico("Carnet: ")
    if f_n.val_Two(clave="carnet", valor=carnet, empleados=empleados):
        print(f"El carnet {carnet} ya se encuentra registrado.\n")
        if f_original.s_n("¿Desea intentarlo de nuevo? S/N: "):
            continue
        return

    # 4. Validación de Cargo
    print("Cargos disponibles: ---Supervisor---Tecnico---Cajero---")
    cargo = f_original.letras("Cargo: ")
    if not f_n.val_cargo(cargo=cargo):
        print("El cargo ingresado no es válido.\n")
        if f_original.s_n("¿Desea intentarlo de nuevo? S/N: "):
            continue
        return

    # Asignación automática de salario según el cargo
    salario = f_n.asig_salario(cargo=cargo)

    # 5. Validación de Estado
    print("Estados disponibles: ---activo---inactivo---")
    estado = f_original.letras("Estado: ")
    if not f_n.val_estado(estado):
        print(" El estado ingresado no es válido.\n")
        if f_original.s_n("¿Desea intentarlo de nuevo? S/N: "):
            continue
        return

    # 6. Guardar el registro en la lista y en el JSON
    f_n.registrar(nom, correo, carnet, cargo, salario, estado, empleados)
    break
def Baja_empleado(empleados):
  print("\n--- DAR DE BAJA A EMPLEADO ---")
  while True:
    carnet = f_original.valor_numerico("Carnet del empleado a eliminar: ")

    # 1. Validar si el carnet existe usando la capa de negocio
    if not f_n.val_Two(clave="carnet", valor=carnet, empleados=empleados):
      print(f"El carnet {carnet} no le pertenece a ningún empleado.\n")
      if f_original.s_n("¿Desea intentarlo de nuevo? S/N: "):
        continue
      return

    # 2. Eliminar el registro (la función f_n.eliminar se encarga de borrarlo y actualizar el JSON)
    f_n.eliminar(carnet, empleados)
    print("Empleado eliminado exitosamente.\n")
    break
def Actualizar_datos(empleados):
  print("\n--- ACTUALIZAR DATOS DE EMPLEADO ---")

  while True:
    carnet = f_original.valor_numerico(
        "Ingrese el carnet del usuario a modificar: "
    )

    # 1. Verificar si el carnet existe
    if not f_n.val_Two(clave="carnet", valor=carnet, empleados=empleados):
        print(f"El carnet {carnet} no le pertenece a ningún empleado.\n")
        if f_original.s_n("¿Desea intentarlo de nuevo? S/N: "):
            continue
        return

    # 2. Bucle para permitir múltiples modificaciones al mismo empleado
    while True:
        print("\nCampos disponibles: --nombre--correo--cargo--carnet--salario--estado--")
        deseo = f_original.letras("Qué dato desea modificar: ").lower()

        match deseo:
            case "nombre":
                nom = f_original.letras("Nuevo nombre: ")
                if f_n.val_Two(clave="nombre", valor=nom, empleados=empleados):
                    print(f"{nom} ya se encuentra registrado.\n")
                    if f_original.s_n("¿Desea intentarlo de nuevo? S/N: "):
                        continue
                    break
                dic = f_n.cambiar("nombre", nuevo_valor=nom,
                    empleados=empleados, carnet=carnet)
                f_n.imprimir(dic)

            case "correo":
                print("Formato esperado: Username@gmail.com")
                while True:
                    correo = input("Nuevo correo: ").strip().lower()
                    if not f_n.val_formato_correo(correo):
                        print("El correo no cumple con el formato requerido.\n")
                        continue
                    if f_n.val_Two(clave="correo", valor=correo, empleados=empleados):
                            print(" Este correo ya se encuentra registrado.\n")
                            continue
                    break
                dic = f_n.cambiar(
                    dato="correo",
                    nuevo_valor=correo,
                    empleados=empleados,
                    carnet=carnet,
                )
                f_n.imprimir(dic)

            case "carnet":
                nuevo_carnet = f_original.valor_numerico("Ingrese el nuevo carnet: ")
                if f_n.val_Two(clave="carnet", valor=nuevo_carnet, empleados=empleados):
                    print(f"❌ El carnet {nuevo_carnet} ya está en uso.\n")
                    if f_original.s_n("¿Desea intentarlo de nuevo? S/N: "):
                        continue
                    break
                dic = f_n.cambiar(
                    dato="carnet",
                    nuevo_valor=nuevo_carnet,
                    empleados=empleados,
                    carnet=carnet,
                )
                f_n.imprimir(dic)
                carnet = nuevo_carnet  # Actualizamos el carnet activo en el ciclo

            case "cargo":
                print("Cargos disponibles: ---Supervisor---Tecnico---Cajero---")
                cargo = f_original.letras("Nuevo cargo: ")
                if not f_n.val_cargo(cargo=cargo):
                    print(" El cargo ingresado es inválido.\n")
                    if f_original.s_n("¿Desea intentarlo de nuevo? S/N: "):
                        continue
                    break
                dic = f_n.cambiar(dato="cargo", nuevo_valor=cargo, empleados=empleados, carnet=carnet)
                f_n.imprimir(dic)

            case "salario":
                sal = f_original.valor_numerico("Ingrese el nuevo salario: ")
                if not f_n.val_salario(salario=sal):
                    print(" Salario fuera de rango (debe estar entre 10000 y 20000).\n")
                    if f_original.s_n("¿Desea intentarlo de nuevo? S/N: "):
                        continue
                    break
                dic = f_n.cambiar(
                    dato="salario", nuevo_valor=sal, empleados=empleados, carnet=carnet
                )
                f_n.imprimir(dic)

            case "estado":
                print("Estados disponibles: ---activo---inactivo---")
                estado = f_original.letras("Nuevo estado: ")
                if not f_n.val_estado(estado=estado):
                    print(" El estado ingresado es inválido.\n")
                    if f_original.s_n("¿Desea intentarlo de nuevo? S/N: "):
                        continue
                    break
                dic = f_n.cambiar(
                    dato="estado",
                    nuevo_valor=estado,
                    empleados=empleados,
                    carnet=carnet,
                )
                f_n.imprimir(dic)

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
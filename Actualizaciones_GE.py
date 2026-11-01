import Funciones_Proyecto as f_original
import Logica_GE as logic


# Muestra en formato clave-valor los datos del empleado
def imprimir(i):
    print("\n")
    for e, o in i.items():
        print(f"{e}: {o}")
    print("\n")

def actualizar_nombre(empleados, carnet):
    while True:
        nom = f_original.letras("Nuevo nombre: ")
        if logic.val_Two(clave="nombre", valor=nom, empleados=empleados):
            print(f"{nom} ya se encuentra registrado.\n")
            if f_original.s_n("¿Desea intentarlo de nuevo? S/N: "):
                continue
            break
        dic = logic.cambiar("nombre", nuevo_valor=nom, empleados=empleados, carnet=carnet)
        imprimir(dic)
        return

def actualizar_correo(empleados, carnet):
    print("Formato esperado: Username@gmail.com")
    while True:
        correo = input("Nuevo correo: ").strip().lower()
        if not logic.val_formato_correo(correo):
            print("El correo no cumple con el formato requerido.\n")
            continue
        if logic.val_Two(clave="correo", valor=correo, empleados=empleados):
            print(" Este correo ya se encuentra registrado.\n")
            continue
        break
    dic = logic.cambiar(
        dato="correo",
        nuevo_valor=correo,
        empleados=empleados,
        carnet=carnet,
    )
    imprimir(dic)

def actualizar_carnet(empleados, carnet):
    while True:
        nuevo_carnet = f_original.valor_numerico("Ingrese el nuevo carnet: ")
        if logic.val_Two(clave="carnet", valor=nuevo_carnet, empleados=empleados):
            print(f" El carnet {nuevo_carnet} ya está en uso.\n")
            if f_original.s_n("¿Desea intentarlo de nuevo? S/N: "):
                continue
            break
        dic = logic.cambiar(
            dato="carnet",
            nuevo_valor=nuevo_carnet,
            empleados=empleados,
            carnet=carnet,
        )
        imprimir(dic)
        carnet = nuevo_carnet  
        return

def actualizar_cargo(empleados, carnet):
    while True:
        print("Cargos disponibles: ---Supervisor---Tecnico---Cajero---")
        cargo = f_original.letras("Nuevo cargo: ")
        if not logic.val_cargo(cargo=cargo):
            print(" El cargo ingresado es inválido.\n")
            if f_original.s_n("¿Desea intentarlo de nuevo? S/N: "):
                continue
            break
        dic = logic.cambiar(dato="cargo", nuevo_valor=cargo, empleados=empleados, carnet=carnet)
        imprimir(dic)
        return

def actualizar_salario(empleados, carnet):
    while True:
        sal = f_original.valor_numerico("Ingrese el nuevo salario: ")
        if not logic.val_salario(salario=sal):
            print(" Salario fuera de rango (debe estar entre 10000 y 20000).\n")
            if f_original.s_n("¿Desea intentarlo de nuevo? S/N: "):
                continue
            break
        dic = logic.cambiar(
            dato="salario", nuevo_valor=sal, empleados=empleados, carnet=carnet
        )
        imprimir(dic)
        return

def actualizar_estado(empleados, carnet):
    while True:
        print("Estados disponibles: ---activo---inactivo---")
        estado = f_original.letras("Nuevo estado: ")
        if not logic.val_estado(estado=estado):
            print(" El estado ingresado es inválido.\n")
            if f_original.s_n("¿Desea intentarlo de nuevo? S/N: "):
                continue
            break
        dic = logic.cambiar(
            dato="estado",
            nuevo_valor=estado,
            empleados=empleados,
            carnet=carnet,
        )
        imprimir(dic)
        return
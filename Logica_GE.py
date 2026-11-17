from Funciones_Proyecto import guardar_json
import re
import random, string
# Verifica si el valor ya se encuentra en lista.
def val_Two(clave, valor, empleados):
    for e in empleados:
        if e.get(clave) == valor:
            return True
    return False

# Valida si el cargo ingresado pertenece a los permitidos.
def val_cargo(cargo):
    cargos_validos = ["supervisor", "cajero", "limpieza", "asistente", "presentador", "tecnico"]
    return cargo.lower() in cargos_validos

# Retorna el salario predeterminado según el cargo.
def asig_salario(cargo):
    salarios = {"supervisor": 17000, "asistente": 14000, "cajero": 13000, "presentador": 10000, "limpieza": 9000}
    return salarios.get(cargo.lower(), 0)

# Valida que el salario esté dentro del rango permitido (10k - 20k).
def val_salario(salario):
    return 10000 <= salario <= 20000

# Valida que el estado sea activo o inactivo
def val_estado(estado):
    estados_validos = ["activo", "inactivo"]
    return estado.lower() in estados_validos

# Valida estrictamente el formato del correo mediante regex.
def val_formato_correo(correo):
    patron = r"^.+@gmail.com$"
    return bool(re.match(patron, correo.strip()))



# 3. CAPA DE OPERACIONES DE DATOS (Modifican la lista):

# Agrega un nuevo registro a la lista en memoria.
def registrar(nombre, correo, carnet, cargo, salario, estado, empleados):
    nuevo_registro = {
        "nombre": nombre,
        "correo": correo,
        "carnet": carnet,
        "cargo": cargo,
        "salario": salario,
        "estado": estado,
    }
    empleados.append(nuevo_registro)
    guardar_json(A_nombre='Empleados',datos=empleados)
    return True

# Elimina un empleado de la lista según su carnet.
def eliminar(carnet, empleados):
    for i in empleados:
        if i["carnet"] == carnet:
            empleados.remove(i)
            guardar_json(A_nombre='Empleados',datos=empleados)
            return True
    return False

# Modifica un atributo específico de un empleado y guarda los cambios.
def cambiar(dato, nuevo_valor, empleados, carnet):
    for i in empleados:
        if i["carnet"] == carnet:
            i[dato] = nuevo_valor
            guardar_json(A_nombre='Empleados',datos=empleados)
            return i
    return None

def asignar_carnet(empleados):
    while True:
        caracteres = string.ascii_uppercase + string.digits
        
        carnet = ''.join(random.choice(caracteres) for i in range(8))
        if val_Two(clave='carnet', valor= carnet, empleados= empleados) != True:
            return carnet
        else:
            continue
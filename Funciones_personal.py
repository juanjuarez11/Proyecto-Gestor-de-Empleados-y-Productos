import json
import re
def val_Two(clave, valor, empleados):
  """Verifica si un valor ya existe en una clave específica de los empleados."""
  for e in empleados:
    if e.get(clave) == valor:
      return True
  return False


def val_cargo(cargo):
  """Valida si el cargo pertenece a los permitidos."""
  cargos_validos = ["supervisor", "tecnico", "cajero"]
  return cargo.lower() in cargos_validos


def asig_salario(cargo):
  """Retorna el salario predeterminado según el cargo."""
  salarios = {"supervisor": 17000, "tecnico": 14000, "cajero": 13000}
  return salarios.get(cargo.lower(), 0)


def val_salario(salario):
  """Valida que el salario esté dentro del rango permitido (10k - 20k)."""
  return 10000 <= salario <= 20000


def val_estado(estado):
  """Valida que el estado sea activo o inactivo."""
  estados_validos = ["activo", "inactivo"]
  return estado.lower() in estados_validos


def val_formato_correo(correo):
  """Valida estrictamente el formato del correo mediante regex."""
  patron = r"^.+@gmail.com$"
  return bool(re.match(patron, correo.strip()))


# ==========================================
# 2. CAPA DE PERSISTENCIA (Manejo de archivos)
# ==========================================


def guardar_credenciales(empleados, archivo="credenciales.json"):
  """Guarda la lista de empleados en el archivo JSON de forma segura."""
  with open(archivo, "w", encoding="utf-8") as f:
    json.dump(empleados, f, ensure_ascii=False, indent=4)


# ==========================================
# 3. CAPA DE OPERACIONES DE DATOS (Modifican la lista)
# ==========================================


def registrar(nombre, correo, carnet, cargo, salario, estado, empleados):
  """Agrega un nuevo registro a la lista en memoria."""
  nuevo_registro = {
      "nombre": nombre,
      "correo": correo,
      "carnet": carnet,
      "cargo": cargo,
      "salario": salario,
      "estado": estado,
  }
  empleados.append(nuevo_registro)
  guardar_credenciales(empleados)
  return True


def eliminar(carnet, empleados):
  """Elimina un empleado de la lista según su carnet."""
  for i in empleados:
    if i["carnet"] == carnet:
      empleados.remove(i)
      guardar_credenciales(empleados)
      return True
  return False


def cambiar(dato, nuevo_valor, empleados, carnet):
  """Modifica un atributo específico de un empleado y guarda los cambios."""
  for i in empleados:
    if i["carnet"] == carnet:
      i[dato] = nuevo_valor
      guardar_credenciales(empleados)
      return i
  return None
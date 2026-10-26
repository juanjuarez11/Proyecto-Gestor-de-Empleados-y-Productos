administradores = [
    {
        "nombre": "Pepito Alvarado",
        "correo": "pepitoElMejor@gmail", 
        "identificacion": "1ABC2345",
        "salario": "30000",
        "estado": "Activo"
    }
]

emp = [
    {
        "nombre": "Chalino",
        "correo": "Dargs9009 @gmail", 
        "identificacion": "6B5F0535",
        "cargo": "supervisor",
        "salario": "22000",
        "estado": "activo"
    },
    {
        "nombre": "Barbanegra",
        "correo": "Barbon9@gmail", 
        "identificacion": "5556262",
        "cargo": "empleado",
        "salario": "12000",
        "estado": "activo"
    }
]

class Administradores:
    def __init__(self):
        pass

    def Busqueda_actualizacion(self):
        while True:
            try:
                print("\n1- Visualizar los perfiles\n" \
                      "2- Actualizar un dato\n" \
                      "3- Salir")
                opcion = int(input("Elija una opción: "))
                
                match opcion:
                    case 1:
                        for empleado in emp:
                            print("-" * 30)
                            for clave, valor in empleado.items():
                                print(f"{clave}: {valor}")
                        print("-" * 30)

                    case 2:
                        encontrado = False
                        codigo = input("Ingrese la identificación del empleado: ")
                        for U in emp:
                            if U["identificacion"].lower() == codigo.lower():
                                encontrado = True
                                print("Parámetros:\nnombre - correo - identificacion - cargo - estado - salario")
                                op = input("Ingrese el parámetro a modificar: ").lower()
                                
                                if op in ["nombre", "correo", "identificacion", "cargo", "estado", "salario"]:
                                    val = input("Nuevo valor: ")
                                    U[op] = val
                                    print("¡Modificación exitosa!")
                                else:
                                    print("Parámetro no válido.")
                                break
                        
                        if not encontrado:
                            print("Identificación errónea.")

                    case 3:
                        print("Saliendo...")
                        return
                    case _:
                        print("Opción no válida.")
            except Exception as e:
                print(f"Ha ocurrido un error: {e}")
    def Alta_integ(self):
        while True:
            try:
                nom = input("Nombre completo del integrante: ")
                correo = input("Correo: ")
                identificacion = input("Código de identificación: ")
                estado = input("Su estado: ")
                salario = input("Salario: ")
                cargo = input("Su cargo asignado (empleado/supervisor): ").lower()
                
                if cargo not in ["empleado", "supervisor"]:
                    print(f"Error! '{cargo}' no es un cargo válido.")
                    continue
                
                # Validación de duplicados
                duplicado = False
                for C in emp:
                    if C["nombre"].lower() == nom.lower():
                        print(f"Error! {nom} ya se encuentra registrado.")
                        duplicado = True
                        break
                    elif C["correo"].lower() == correo.lower():
                        print(f"Error! {correo} ya se encuentra registrado.")
                        duplicado = True
                        break
                    elif C["identificacion"].lower() == identificacion.lower():
                        print(f"Error! {identificacion} ya se encuentra registrado.")
                        duplicado = True
                        break
                
                if duplicado:
                    continue

                nuevo_registro = {
                    "nombre": nom,
                    "correo": correo,
                    "identificacion": identificacion,
                    "cargo": cargo,
                    "salario": salario,
                    "estado": estado
                }
                emp.append(nuevo_registro)
                print("¡Empleado registrado con éxito!")
                break
            except Exception as e:
                print(f"Ha ocurrido un error: {e}")

    def Baja_empleado(self):
        while True:
            try:
                identificacion = input("Ingrese el código de identificación de quien desea dar de baja: ")
                encontrado = False
                for i in emp:
                    if i["identificacion"].lower() == identificacion.lower():
                        emp.remove(i)
                        print(f"Se ha eliminado a {i['nombre']} correctamente.")
                        encontrado = True
                        return emp
                
                if not encontrado:
                    print(f"Error! {identificacion} no corresponde a ningún Integrante.")
            except Exception as e:
                print(f"Ha ocurrido un error: {e}")

admin = Administradores()

import json
import maskpass
import funciones_menu as f

empleados = f.leer_json("credenciales")
administradores = f.leer_json("administrador")

#____________________________________________________________________________________________________________________________
def validar_inicio_sesion(lista,nombre,clave):
    try: 
        intentos_username = 3

        while intentos_username > 0:
            username = input("Ingrese su nombre de usuario: ")
            username_encontrado = None
            
            for i in lista:
                if username == i[nombre]:
                    username_encontrado = i
                    break

            if username_encontrado is not None:
                print(f"Usuario Encontrado: {username}")
                intentos_password = 3

                while intentos_password > 0:
                    password = maskpass.askpass(prompt="Por favor, Ingrese su contraseña: ",mask="●")
                    if str(password) == str(username_encontrado[clave]):
                        print("CONTRASEÑA CORRECTA. INICIANDO SESIÓN....")
                        return True
                    else:
                        intentos_password -= 1
                        print(f"CONTRASEÑA INCORRECTA. Intento/os restantes: {intentos_password}")
                
                print("Se han agotado los intentos de contraseña.")
                return False
            
            else:
                intentos_username -= 1
                print(f"ERROR: {username} no está en la lista de administradores. Intento/os restantes: {intentos_username}")
        
        print("Se han agotado los intentos de usuario.")
        return False

    except Exception as e:
        print(f"Error: {e}")
        return False
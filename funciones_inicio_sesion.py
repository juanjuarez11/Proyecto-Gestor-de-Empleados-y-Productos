import json
import maskpass
import funciones_menu as f

empleados = f.leer_json("credenciales")
administradores = f.leer_json("administrador")

def buscar_usuario(lista_usuarios, username_ingresado, campo_nombre):
    for usuario in lista_usuarios:
        if username_ingresado == usuario.get(campo_nombre):
            return usuario
    return None

def verificar_password(usuario, password_ingresada, campo_clave):
    if usuario and str(password_ingresada) == str(usuario.get(campo_clave)):
        return True
    return False

def validar_inicio_sesion(lista, nombre_campo, clave_campo,es_admin=False):
    try: 
        intentos_username = 3

        while intentos_username > 0:
            username = input("Ingrese su nombre de usuario: ")
            
            usuario_encontrado = buscar_usuario(lista, username, nombre_campo)

            if usuario_encontrado is not None:
                print(f"Usuario Encontrado: {username}")
                intentos_password = 3

                while intentos_password > 0:
                    password = maskpass.askpass(prompt="Por favor, Ingrese su contraseña: ", mask="●")
                    
                    if verificar_password(usuario_encontrado, password, clave_campo):
                        print("CONTRASEÑA CORRECTA. INICIANDO SESIÓN....")
                        if es_admin:
                            return True,"administrador"
                        else:
                            cargo =usuario_encontrado.get("cargo","empleado").lower()
                            return True,cargo
                    else:
                        intentos_password -= 1
                        print(f"CONTRASEÑA INCORRECTA. Intento/os restantes: {intentos_password}")
                
                print("Se han agotado los intentos de contraseña.")
                return False, None
            
            else:
                intentos_username -= 1
                print(f"ERROR: {username} no está en los registros. Intento/os restantes: {intentos_username}")
        
        print("Se han agotado los intentos de usuario.")
        return False, None

    except Exception as e:
        print(f"Error: {e}")
        return False, None
# ------------ autenticacion.py ------------
import os
import sys
import getpass
from hashlib import sha256

ARCHIVO_USUARIOS = "usuarios.txt"

# --- Funciones Auxiliares para Entrada de Datos ---
def _get_input_stripped(prompt, min_len=0, max_len=None, is_alphanum=False, valid_options=None):
    """Obtiene una entrada de usuario validada."""
    while True:
        value = input(prompt).strip()
        if not value and min_len > 0:
            print("La entrada no puede estar vacía.")
            continue
        if max_len is not None and len(value) > max_len:
            print(f"La entrada debe tener máximo {max_len} caracteres.")
            continue
        if is_alphanum and not value.isalnum():
            print("La entrada debe ser alfanumérica.")
            continue
        if valid_options is not None and value.lower() not in valid_options:
            print(f"Opción no válida. Elija entre: {', '.join(valid_options)}.")
            continue
        return value

def _get_password(prompt, min_len=6):
    """Obtiene una contraseña segura con confirmación."""
    while True:
        password = getpass.getpass(prompt)
        if len(password) < min_len:
            print(f"La contraseña debe tener al menos {min_len} caracteres.")
            continue
        confirm_password = getpass.getpass("Confirme contraseña: ")
        if password == confirm_password:
            return password
        print("Las contraseñas no coinciden.")

def _get_validated_choice(prompt, options):
    """Obtiene una opción válida de una lista de opciones."""
    while True:
        choice = input(prompt).strip().lower()
        if choice in options:
            return choice
        print("Opción no válida. Intente de nuevo.")

# --- Funciones de Utilidad para Archivos ---
def encriptar_contrasena(contrasena):
    """Encripta la contraseña usando SHA-256."""
    return sha256(contrasena.encode()).hexdigest()

def _cargar_usuarios():
    """Carga todos los usuarios del archivo."""
    usuarios = []
    if os.path.exists(ARCHIVO_USUARIOS):
        with open(ARCHIVO_USUARIOS, "r") as f:
            for linea in f:
                if linea.strip():
                    datos = linea.strip().split("|")
                    if len(datos) < 5: # Mínimo 5 campos (usuario, hash, nombre, rol, estado)
                        print(f"[ADVERTENCIA] Formato de línea incorrecto en '{ARCHIVO_USUARIOS}': {linea.strip()}. Saltando.")
                        continue
                    permisos_especiales = datos[5].split(',') if len(datos) > 5 and datos[5] else []
                    usuarios.append({
                        'usuario': datos[0], 'contrasena': datos[1], 'nombre': datos[2],
                        'rol': datos[3], 'estado': datos[4], 'permisos_especiales': permisos_especiales
                    })
    return usuarios

def _guardar_usuarios(usuarios):
    """Guarda la lista de usuarios en el archivo."""
    try:
        with open(ARCHIVO_USUARIOS, "w") as f:
            for u in usuarios:
                permisos_str = ','.join(u['permisos_especiales'])
                f.write(f"{u['usuario']}|{u['contrasena']}|{u['nombre']}|{u['rol']}|{u['estado']}|{permisos_str}\n")
    except IOError as e:
        print(f"[ERROR] Error de E/S al guardar usuarios: {str(e)}")
        print("Asegúrate de tener permisos de escritura en este directorio.")
        sys.exit(1) # Salir si no se pueden guardar los usuarios

# --- Funciones Principales de Autenticación ---
def inicializar_sistema():
    """Inicializa el sistema creando el usuario admin si no existe."""
    if not os.path.exists(ARCHIVO_USUARIOS) or os.stat(ARCHIVO_USUARIOS).st_size == 0:
        try:
            with open(ARCHIVO_USUARIOS, "w") as f:
                contrasena_plana = "1234"
                contrasena_encriptada = encriptar_contrasena(contrasena_plana)
                f.write(f"admin|{contrasena_encriptada}|Administrador|admin|activo|\n")
            print("\nSistema inicializado correctamente.")
            print("Usuario 'admin' creado automáticamente con contraseña '1234'.")
            print("¡IMPORTANTE: Cambia esta contraseña después del primer acceso!")
        except Exception as e:
            print(f"Error al inicializar sistema: {str(e)}")
            sys.exit(1)

def iniciar_sesion():
    """Permite a un usuario iniciar sesión."""
    inicializar_sistema()
    print("\n=== INICIO DE SESIÓN ===")
    print("NOTA: La contraseña no se mostrará mientras escribe.\n")

    for intentos in range(3, 0, -1):
        try:
            usuario = _get_input_stripped("Usuario: ", min_len=1)
            contrasena_ingresada = getpass.getpass("Contraseña: ")
            contrasena_hash_ingresada = encriptar_contrasena(contrasena_ingresada)

            usuarios = _cargar_usuarios() # Recargar usuarios para asegurar la última versión
            usuario_encontrado = next((u for u in usuarios if u['usuario'] == usuario), None)

            if usuario_encontrado:
                if usuario_encontrado['contrasena'] == contrasena_hash_ingresada:
                    if usuario_encontrado['estado'] == 'activo':
                        print(f"\n¡Bienvenido(a), {usuario_encontrado['nombre']}!")
                        return usuario_encontrado
                    else:
                        print("\nError: Cuenta inactiva.")
                        return None
                else:
                    print("\nError: Contraseña incorrecta.")
            else:
                print(f"Usuario '{usuario}' no encontrado.")
            
            if intentos > 1:
                print(f"Credenciales incorrectas. Intentos restantes: {intentos - 1}")
        except KeyboardInterrupt:
            print("\nOperación cancelada por el usuario.")
            sys.exit(0)
        except Exception as e:
            print(f"\nError inesperado durante el inicio de sesión: {str(e)}")

    print("\nDemasiados intentos fallidos. Por seguridad, el sistema se cerrará.")
    sys.exit(1)

def verificar_permiso(usuario_actual, permiso_requerido):
    """Verifica si el usuario actual tiene el permiso requerido."""
    if not usuario_actual or not isinstance(usuario_actual, dict):
        return False
        
    permisos_por_rol = {
        'admin': ['registrar', 'modificar', 'eliminar', 'reportes', 'ventas', 'inventario', 'compras', 'bajas', 'devoluciones', 'usuarios', 'eliminar_articulos', 'modificar_precios', 'ver_reportes_detallados'],
        'inventario': ['registrar', 'modificar', 'reportes', 'inventario', 'compras', 'bajas'],
        'ventas': ['ventas', 'devoluciones', 'reportes'],
        'reportes': ['reportes']
    }
    
    rol = usuario_actual.get('rol', '')
    permisos_especiales = usuario_actual.get('permisos_especiales', [])

    return permiso_requerido in permisos_por_rol.get(rol, []) or permiso_requerido in permisos_especiales

# --- Funciones de Gestión de Usuarios ---
def registrar_usuario():
    """Permite registrar un nuevo usuario."""
    print("\nREGISTRO DE NUEVO USUARIO")
    
    while True:
        usuario = _get_input_stripped("Nombre de usuario (5-15 caracteres alfanuméricos): ", min_len=5, max_len=15, is_alphanum=True)
        usuarios = _cargar_usuarios()
        if any(u['usuario'] == usuario for u in usuarios):
            print("Este nombre de usuario ya existe.")
            continue
        break
    
    contrasena_hash = encriptar_contrasena(_get_password("Contraseña (mínimo 6 caracteres): "))
    nombre_completo = _get_input_stripped("Nombre completo del usuario: ", max_len=50)
    rol = _get_validated_choice("Rol (admin, inventario, ventas, reportes): ", ['admin', 'inventario', 'ventas', 'reportes'])
    
    nuevo_usuario = {'usuario': usuario, 'contrasena': contrasena_hash, 'nombre': nombre_completo,
                     'rol': rol, 'estado': 'activo', 'permisos_especiales': []}
    
    usuarios.append(nuevo_usuario)
    _guardar_usuarios(usuarios)
    print(f"\nUsuario registrado exitosamente: {usuario} ({rol})")

def modificar_permisos():
    """Permite a un administrador modificar los permisos especiales de un usuario."""
    print("\nMODIFICAR PERMISOS DE USUARIO")
    usuarios = _cargar_usuarios()
    if not usuarios:
        print("No hay usuarios registrados.")
        return
    
    print("\nUsuarios registrados:")
    for u in usuarios:
        permisos_actuales = ', '.join(u['permisos_especiales']) if u['permisos_especiales'] else 'Ninguno'
        print(f"Usuario: {u['usuario']} - Rol: {u['rol']} - Estado: {u['estado']} - Permisos: {permisos_actuales}")
    
    usuario_sel = _get_input_stripped("\nIngrese el nombre de usuario a modificar permisos (o dejar vacío para cancelar): ")
    if not usuario_sel: return

    usuario_a_modificar = next((u for u in usuarios if u['usuario'] == usuario_sel), None)
    if not usuario_a_modificar:
        print("Usuario no encontrado.")
        return
    
    print(f"\nModificando permisos para: {usuario_a_modificar['usuario']} (Rol: {usuario_a_modificar['rol']})")
    print("1. Permiso para eliminar artículos ('eliminar_articulos')")
    print("2. Permiso para modificar precios ('modificar_precios')")
    print("3. Permiso para ver reportes detallados ('ver_reportes_detallados')")
    print("4. Todos los permisos anteriores")
    print("5. Quitar todos los permisos especiales")
    
    permiso_opcion = _get_validated_choice("Seleccione el permiso a otorgar/quitar (1-5): ", [str(i) for i in range(1, 6)])
    
    permisos_map = {
        '1': ['eliminar_articulos'],
        '2': ['modificar_precios'],
        '3': ['ver_reportes_detallados'],
        '4': ['eliminar_articulos', 'modificar_precios', 'ver_reportes_detallados'],
        '5': []
    }
    usuario_a_modificar['permisos_especiales'] = permisos_map[permiso_opcion]
    _guardar_usuarios(usuarios)
    print(f"\nPermisos para {usuario_a_modificar['usuario']} actualizados exitosamente.")
    print(f"Nuevos permisos especiales: {', '.join(usuario_a_modificar['permisos_especiales']) if usuario_a_modificar['permisos_especiales'] else 'Ninguno'}")

def cambiar_estado_usuario():
    """Permite a un administrador cambiar el estado de un usuario."""
    print("\nCAMBIAR ESTADO DE USUARIO")
    usuarios = _cargar_usuarios()
    if not usuarios:
        print("No hay usuarios registrados.")
        return
    
    print("\nUsuarios registrados:")
    for u in usuarios:
        print(f"Usuario: {u['usuario']} - Rol: {u['rol']} - Estado: {u['estado']}")
    
    usuario_sel = _get_input_stripped("\nIngrese el nombre de usuario a cambiar estado (o dejar vacío para cancelar): ")
    if not usuario_sel: return

    usuario_a_modificar = next((u for u in usuarios if u['usuario'] == usuario_sel), None)
    if not usuario_a_modificar:
        print("Usuario no encontrado.")
        return
    if usuario_a_modificar['usuario'] == 'admin':
        print("No se puede cambiar el estado del usuario 'admin'.")
        return
    
    print(f"\nEstado actual de {usuario_a_modificar['usuario']}: {usuario_a_modificar['estado']}")
    nuevo_estado = _get_validated_choice("Nuevo estado (activo/inactivo): ", ['activo', 'inactivo'])
    
    usuario_a_modificar['estado'] = nuevo_estado
    _guardar_usuarios(usuarios)
    print(f"\nEstado de {usuario_a_modificar['usuario']} actualizado a '{nuevo_estado}' exitosamente.")

def restablecer_contrasena():
    """Permite a un administrador restablecer la contraseña de un usuario."""
    print("\nRESTABLECER CONTRASEÑA DE USUARIO")
    usuarios = _cargar_usuarios()
    if not usuarios:
        print("No hay usuarios registrados.")
        return
    
    print("\nUsuarios registrados:")
    for u in usuarios:
        print(f"Usuario: {u['usuario']} - Rol: {u['rol']}")
    
    usuario_sel = _get_input_stripped("\nIngrese el nombre de usuario para restablecer contraseña (o dejar vacío para cancelar): ")
    if not usuario_sel: return

    usuario_a_modificar = next((u for u in usuarios if u['usuario'] == usuario_sel), None)
    if not usuario_a_modificar:
        print("Usuario no encontrado.")
        return
    
    nueva_contrasena_hash = encriptar_contrasena(_get_password("Ingrese la nueva contraseña (mínimo 6 caracteres): "))
    usuario_a_modificar['contrasena'] = nueva_contrasena_hash
    _guardar_usuarios(usuarios)
    print(f"\nContraseña de {usuario_a_modificar['usuario']} restablecida exitosamente.")

def menu_usuarios(usuario_actual):
    """Muestra el menú de gestión de usuarios (solo para admin)."""
    if usuario_actual['rol'] != 'admin':
        print("No tiene permisos para acceder a la gestión de usuarios.")
        return

    while True:
        print("\n--- GESTIÓN DE USUARIOS ---")
        print("1. Registrar nuevo usuario")
        print("2. Modificar permisos de usuario")
        print("3. Cambiar estado de usuario (activo/inactivo)")
        print("4. Restablecer contraseña de usuario")
        print("5. Volver al menú principal")

        opcion = _get_validated_choice("Seleccione una opción: ", [str(i) for i in range(1, 6)])

        if opcion == '1':
            registrar_usuario()
        elif opcion == '2':
            modificar_permisos()
        elif opcion == '3':
            cambiar_estado_usuario()
        elif opcion == '4':
            restablecer_contrasena()
        elif opcion == '5':
            break

if __name__ == "__main__":
    # Solo para pruebas de autenticación independiente
    usuario_logueado = iniciar_sesion()
    if usuario_logueado:
        print("\nSesión iniciada con éxito.")
        print(f"Detalles: {usuario_logueado}")
        print(f"Tiene permiso 'ventas': {verificar_permiso(usuario_logueado, 'ventas')}")
        print(f"Tiene permiso 'eliminar_articulos': {verificar_permiso(usuario_logueado, 'eliminar_articulos')}")
        if usuario_logueado['rol'] == 'admin':
            menu_usuarios(usuario_logueado)
    else:
        print("\nFallo en el inicio de sesión.")
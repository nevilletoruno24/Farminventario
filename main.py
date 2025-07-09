# ------------ main.py ------------
import os
import sys
from autenticacion import iniciar_sesion, verificar_permiso

def mostrar_menu_principal(usuario_actual):
    """Muestra el menú principal según los permisos del usuario"""
    print(f"\n=== SISTEMA DE INVENTARIO ===")
    print(f"Usuario: {usuario_actual['nombre']} ({usuario_actual['rol']})")
    print("\nOpciones disponibles:")
    
    # Construir opciones basadas en permisos
    opciones = []
    
    # Opción 1: Gestión de Artículos
    if verificar_permiso(usuario_actual, 'registrar') or verificar_permiso(usuario_actual, 'modificar'):
        opciones.append(("1", "Gestión de Artículos (Registrar/Modificar)"))
    
    # Opción 3: Reportes (siempre visible si tiene permiso)
    if verificar_permiso(usuario_actual, 'reportes'):
        opciones.append(("2", "Reportes"))
    
    # Opción 4: Gestión de Compras
    if verificar_permiso(usuario_actual, 'compras'):
        opciones.append(("3", "Gestión de Compras"))
    
    # Opción 5: Gestión de Bajas
    if verificar_permiso(usuario_actual, 'bajas'):
        opciones.append(("4", "Gestión de Bajas"))
    
    # Opción 6: Gestión de Devoluciones
    if verificar_permiso(usuario_actual, 'devoluciones'):
        opciones.append(("5", "Gestión de Devoluciones"))
    
    # Opción 6: Eliminar Artículos
    if verificar_permiso(usuario_actual, 'eliminar_articulos'):
        opciones.append(("6", "Eliminar Artículos"))
    
    # Opción 7: Facturación (reemplaza a Gestión de Ventas)
    if verificar_permiso(usuario_actual, 'ventas'):
        opciones.append(("7", "Facturación"))
    
    # Mostrar opciones disponibles
    for numero, texto in opciones:
        print(f"{numero}. {texto}")
    
    # Opción de gestión de usuarios solo para admin
    if usuario_actual['rol'] == 'admin':
        print("U. Gestión de Usuarios")
    
    # Opción de salida
    print("S. Salir")
    return [op[0] for op in opciones]  # Retornar solo los números de opción

def main():
    """Función principal del sistema de inventario."""
    usuario_actual = iniciar_sesion()

    if not usuario_actual:
        print("No se pudo iniciar sesión. Saliendo del programa.")
        sys.exit(1)

    while True:
        opciones_validas = mostrar_menu_principal(usuario_actual)
        opcion = input("\nSeleccione una opción: ").strip().upper()

        try:
            if opcion == "1" and "1" in opciones_validas:
                from registroDeArticulos import registrar_articulo
                registrar_articulo()
            
            elif opcion == "2" and "2" in opciones_validas:
                from reporteInventario import menu_reportes
                menu_reportes()
            
            elif opcion == "3" and "3" in opciones_validas:
                from registroDeCompras import registrar_compra
                registrar_compra(usuario_actual)
            
            elif opcion == "4" and "4" in opciones_validas:
                from bajasInventario import registrar_baja
                registrar_baja(usuario_actual)
            
            elif opcion == "5" and "5" in opciones_validas:
                from devoluciones import registrar_devolucion
                registrar_devolucion(usuario_actual)
            
            elif opcion == "6" and "6" in opciones_validas:
                from eliminarArticulos import eliminar_articulo
                eliminar_articulo()
            
            elif opcion == "7" and "7" in opciones_validas:
                from ventas import generar_factura
                generar_factura()
            
            elif opcion == "U" and usuario_actual['rol'] == 'admin':
                from autenticacion import menu_usuarios
                menu_usuarios(usuario_actual)
            
            elif opcion == "S":
                print("\nSaliendo del sistema...")
                break
            
            else:
                print("\nOpción no válida o no permitida para su rol. Intente de nuevo.")
        
        except ImportError as e:
            print(f"\nError: No se pudo cargar el módulo - {str(e)}")
            print("Verifique que el archivo exista y tenga la función requerida.")

        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()
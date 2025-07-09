# ------------ reporteInventario.py ------------
import os
from datetime import datetime

ARCHIVO_INVENTARIO = "inventario.txt"
ARCHIVO_HISTORICO_BAJAS = "bajas.txt"
ARCHIVO_HISTORICO_ELIMINACIONES = "historial_eliminaciones.txt"
ARCHIVO_FACTURAS = "facturas.txt"
ARCHIVO_DEVOLUCIONES = "devoluciones.txt"
ARCHIVO_COMPRAS = "compras.txt"

def mostrar_menu_reportes():
    """Muestra el menú de opciones de reportes"""
    print("\n=== MENÚ DE REPORTES ===")
    print("1. Reporte de inventario actual")
    print("2. Reporte de artículos dados de baja")
    print("3. Reporte de artículos eliminados")
    print("4. Reporte de facturas emitidas")
    print("5. Reporte de devoluciones")
    print("6. Reporte de compras")
    print("7. Reporte general consolidado")
    print("8. Volver al menú principal")
    
    while True:
        opcion = input("Seleccione una opción (1-8): ").strip()
        if opcion in ['1', '2', '3', '4', '5', '6', '7', '8']:
            return opcion
        print("Opción no válida. Intente de nuevo.")

def leer_archivo(nombre_archivo):
    """Función auxiliar para leer archivos con manejo de errores"""
    try:
        if os.path.exists(nombre_archivo):
            with open(nombre_archivo, 'r', encoding='utf-8') as f:
                return [linea.strip() for linea in f if linea.strip()]
        return []
    except Exception as e:
        print(f"\nError al leer {nombre_archivo}: {str(e)}")
        return []

def generar_reporte_inventario():
    """Genera un reporte del inventario actual"""
    lineas = leer_archivo(ARCHIVO_INVENTARIO)
    if not lineas:
        print("\nNo hay artículos registrados en el inventario.")
        return
    
    print("\n=== REPORTE DE INVENTARIO ACTUAL ===")
    print("-" * 120)
    print("{:<12} {:<30} {:<20} {:<10} {:<10} {:<20} {:<20}".format(
        "Código", "Nombre", "Categoría", "Precio", "Stock", "Vencimiento", "Proveedor"))
    print("-" * 120)
    
    for linea in lineas:
        datos = linea.split("|")
        if len(datos) >= 5:  # Validar que tenga los campos mínimos
            print("{:<12} {:<30} {:<20} {:<10.2f} {:<10} {:<20} {:<20}".format(
                datos[0], datos[1], datos[2], 
                float(datos[3]), int(datos[4]), 
                datos[5] if len(datos) > 5 else "N/A", 
                datos[6] if len(datos) > 6 else "N/A"))
    
    print("-" * 120)
    print(f"Total de artículos: {len(lineas)}")

def generar_reporte_bajas():
    """Genera un reporte de artículos dados de baja"""
    lineas = leer_archivo(ARCHIVO_HISTORICO_BAJAS)
    if not lineas:
        print("\nNo hay registros de bajas.")
        return
    
    print("\n=== REPORTE DE BAJAS ===")
    print("-" * 100)
    print("{:<12} {:<30} {:<10} {:<20} {:<15} {:<15}".format(
        "Código", "Nombre", "Cantidad", "Motivo", "Fecha", "Usuario"))
    print("-" * 100)
    
    for linea in lineas:
        datos = linea.split("|")
        if len(datos) >= 6:  # Validar que tenga todos los campos necesarios
            print("{:<12} {:<30} {:<10} {:<20} {:<15} {:<15}".format(
                datos[0], datos[1], datos[2], datos[3], datos[4], datos[5]))
    
    print("-" * 100)
    print(f"Total de bajas registradas: {len(lineas)}")

def generar_reporte_eliminaciones():
    """Genera un reporte de artículos eliminados"""
    lineas = leer_archivo(ARCHIVO_HISTORICO_ELIMINACIONES)
    if not lineas:
        print("\nNo hay registros de eliminaciones.")
        return
    
    print("\n=== REPORTE DE ELIMINACIONES ===")
    print("-" * 120)
    print("{:<12} {:<30} {:<20} {:<15} {:<15}".format(
        "Código", "Nombre", "Fecha Eliminación", "Usuario", "Motivo"))
    print("-" * 120)
    
    for linea in lineas:
        datos = linea.split("|")
        if len(datos) >= 5:
            print("{:<12} {:<30} {:<20} {:<15} {:<15}".format(
                datos[0], datos[1], datos[2], datos[3], datos[4]))
    
    print("-" * 120)
    print(f"Total de artículos eliminados: {len(lineas)}")

def generar_reporte_facturas():
    """Genera un reporte de facturas emitidas"""
    lineas = leer_archivo(ARCHIVO_FACTURAS)
    if not lineas:
        print("\nNo hay facturas registradas.")
        return
    
    print("\n=== REPORTE DE FACTURAS ===")
    print("-" * 120)
    print("{:<30} {:<35} {:<15} {:<20} {:<10} {:<15}".format(
        "Fecha", "Cliente", "Código", "Producto", "Cantidad", "Total"))
    print("-" * 120)
    
    for linea in lineas:
        if linea.strip():  # Verificar que la línea no esté vacía
            partes = [p.strip() for p in linea.split("|")]
            if len(partes) >= 6:  # Verificar que tenga todos los campos necesarios
                fecha = partes[0]
                cliente = partes[1].split(":")[1].strip() if ":" in partes[1] else partes[1]
                codigo = partes[2].split(":")[1].strip() if ":" in partes[2] else partes[2]
                producto = partes[3].split(":")[1].strip() if ":" in partes[3] else partes[3]
                cantidad = partes[4].split(":")[1].strip() if ":" in partes[4] else partes[4]
                total = partes[5].split(":")[1].strip() if ":" in partes[5] else partes[5]
                
                print("{:<30} {:<35} {:<15} {:<20} {:<10} {:<15}".format(
                    fecha, cliente, codigo, producto, cantidad, total))
    
    print("-" * 120)
    print(f"Total de facturas emitidas: {len([l for l in lineas if l.strip()])}")

def generar_reporte_devoluciones():
    """Genera un reporte de devoluciones"""
    lineas = leer_archivo(ARCHIVO_DEVOLUCIONES)
    if not lineas:
        print("\nNo hay devoluciones registradas.")
        return
    
    print("\n=== REPORTE DE DEVOLUCIONES ===")
    print("-" * 120)
    print("{:<20} {:<10} {:<20} {:<20} {:<10} {:<15}".format(
        "Fecha", "Factura", "Cliente", "Producto", "Cantidad", "Total"))
    print("-" * 120)
    
    for linea in lineas:
        if linea.strip():  # Verificar que la línea no esté vacía
            # Parsear los datos con etiquetas
            datos = linea.split("|")
            devolucion = {}
            
            for dato in datos:
                if dato.startswith("Fecha:"):
                    devolucion['fecha'] = dato.split(":")[1].strip()
                elif dato.startswith("Factura:"):
                    devolucion['factura'] = dato.split(":")[1].strip()
                elif dato.startswith("Cliente:"):
                    devolucion['cliente'] = dato.split(":")[1].strip()
                elif dato.startswith("Producto:"):
                    devolucion['producto'] = dato.split(":")[1].strip()
                elif dato.startswith("Cantidad:"):
                    devolucion['cantidad'] = dato.split(":")[1].strip()
                elif dato.startswith("Total:") and not dato.startswith("Total Devolucion:"):
                    devolucion['total'] = dato.split(":")[1].strip()
            
            # Mostrar la devolución si se pudo parsear correctamente
            if devolucion:
                print("{:<20} {:<10} {:<20} {:<20} {:<10} {:<15}".format(
                    devolucion.get('fecha', 'N/A'),
                    devolucion.get('factura', 'N/A'),
                    devolucion.get('cliente', 'N/A'),
                    devolucion.get('producto', 'N/A'),
                    devolucion.get('cantidad', 'N/A'),
                    devolucion.get('total', 'N/A')))
    
    print("-" * 120)
    print(f"Total de devoluciones registradas: {len([l for l in lineas if l.strip()])}")

def generar_reporte_compras():
    """Genera un reporte de compras realizadas"""
    lineas = leer_archivo(ARCHIVO_COMPRAS)
    if not lineas:
        print("\nNo hay compras registradas.")
        return
    
    print("\n=== REPORTE DE COMPRAS ===")
    print("-" * 120)
    print("{:<12} {:<30} {:<15} {:<15} {:<15} {:<15}".format(
        "Código", "Proveedor", "Cantidad", "Precio", "Total", "Fecha"))
    print("-" * 120)
    
    for linea in lineas:
        datos = linea.split("|")
        if len(datos) >= 6:
            try:
                precio = float(datos[3])
                cantidad = int(datos[2])
                total = precio * cantidad
                print("{:<12} {:<30} {:<15} {:<15.2f} {:<15.2f} {:<15}".format(
                    datos[0], datos[1], cantidad, precio, total, datos[5]))
            except ValueError:
                continue
    
    print("-" * 120)
    print(f"Total de compras registradas: {len(lineas)}")

def generar_reporte_general():
    """Genera un reporte consolidado con toda la información"""
    print("\n=== REPORTE GENERAL CONSOLIDADO ===")
    
    # 1. Inventario
    inv = leer_archivo(ARCHIVO_INVENTARIO)
    print("\n1. INVENTARIO:")
    print(f"  - Artículos registrados: {len(inv)}")
    
    # 2. Bajas
    bajas = leer_archivo(ARCHIVO_HISTORICO_BAJAS)
    print("\n2. BAJAS:")
    print(f"  - Artículos dados de baja: {len(bajas)}")
    
    # 3. Eliminaciones
    elim = leer_archivo(ARCHIVO_HISTORICO_ELIMINACIONES)
    print("\n3. ELIMINACIONES:")
    print(f"  - Artículos eliminados: {len(elim)}")
    
    # 4. Facturas
    facturas = [l for l in leer_archivo(ARCHIVO_FACTURAS) if l.startswith("Fecha:")]
    print("\n4. FACTURAS:")
    print(f"  - Facturas emitidas: {len(facturas)}")
    
    # 5. Devoluciones
    devol = [l for l in leer_archivo(ARCHIVO_DEVOLUCIONES) if "|" in l]
    print("\n5. DEVOLUCIONES:")
    print(f"  - Devoluciones registradas: {len(devol)}")
    
    # 6. Compras
    compras = leer_archivo(ARCHIVO_COMPRAS)
    print("\n6. COMPRAS:")
    print(f"  - Compras realizadas: {len(compras)}")
    
    print("\nReporte generado exitosamente")

def menu_reportes():
    """Maneja el menú de reportes"""
    while True:
        opcion = mostrar_menu_reportes()
        
        if opcion == '1':
            generar_reporte_inventario()
        elif opcion == '2':
            generar_reporte_bajas()
        elif opcion == '3':
            generar_reporte_eliminaciones()
        elif opcion == '4':
            generar_reporte_facturas()
        elif opcion == '5':
            generar_reporte_devoluciones()
        elif opcion == '6':
            generar_reporte_compras()
        elif opcion == '7':
            generar_reporte_general()
        elif opcion == '8':
            break
        
        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    menu_reportes()
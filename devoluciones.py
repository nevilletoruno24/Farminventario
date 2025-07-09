# ------------ devoluciones.py ------------
import os
from datetime import datetime
from main import mostrar_menu_principal

ARCHIVO_FACTURAS = "facturas.txt"
ARCHIVO_DEVOLUCIONES = "devoluciones.txt"
ARCHIVO_INVENTARIO = "inventario.txt"
ARCHIVO_HISTORICO_DEVOLUCIONES = "historico_devoluciones.txt"


def verificar_archivo():
    return os.path.exists(ARCHIVO_FACTURAS)


def buscar_factura(numero_factura, cliente):
    """Busca facturas por número o cliente"""
    
    facturas = []
    
    with open(ARCHIVO_FACTURAS, "r") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:  # Saltar líneas vacías
                continue
                
            # Parsear la línea completa de la factura
            datos = linea.split("|")
            
            # Extraer información de la factura
            factura = {}
            producto = {}
            
            # Contador para distinguir entre total de factura y total de producto
            total_count = 0
            
            for dato in datos:
                if dato.startswith("Fecha:"):
                    factura['fecha'] = dato.split(":")[1].strip()
                elif dato.startswith("Cliente:"):
                    factura['cliente'] = dato.split(":")[1].strip()
                elif dato.startswith("Total:") and not dato.startswith("Total Producto:"):
                    factura['total'] = float(dato.split(":")[1].strip())
                elif dato.startswith("Codigo:"):
                    factura['numero'] = int(dato.split(":")[1].strip())
                elif dato.startswith("Producto:"):
                    producto['nombre'] = dato.split(":")[1].strip()
                elif dato.startswith("Cantidad:"):
                    producto['cantidad'] = int(dato.split(":")[1].strip())
                elif dato.startswith("Total:") and len(datos) > 4:  # Total del producto
                    producto['total'] = float(dato.split(":")[1].strip())
            
            # Agregar el producto a la factura
            if producto:
                factura['productos'] = [producto]
                facturas.append(factura)
    
    # Filtrar resultados
    resultados = []
    for fact in facturas:
        # Filtro por número de factura
        if numero_factura and fact.get('numero', 0) == numero_factura:
            resultados.append(fact)
        # Filtro por cliente (búsqueda parcial, case-insensitive)
        elif cliente and cliente.lower() in fact.get('cliente', '').lower():
            resultados.append(fact)
    
    return resultados if resultados else None

def registrar_devolucion(usuario_actual):

    print("\nREGISTRO DE DEVOLUCIÓN")
    
    
    # Opción de búsqueda
    print("\nBuscar factura por:")
    print("1. Número de factura")
    print("2. Nombre del cliente")
    
    
    while True:
        opcion = input("Seleccione una opción (1-3): ").strip()
        if opcion in ['1', '2']:
            break

    if not verificar_archivo():
        print("El archivo factura no existe!")
    else:
        if opcion == '1':
            while True:
                try:
                    numero = int(input("Número de factura: "))
                    break
                except ValueError:
                    print("Ingrese un número válido.")
        
            facturas = buscar_factura(numero_factura=numero,cliente="")
            
        else:
            cliente = input("Nombre del cliente: ").strip()
            facturas = buscar_factura(cliente=cliente,numero_factura=0)
        
    
    if not facturas:
        print("No se encontraron facturas con los criterios de búsqueda.")
        
    
    # Mostrar facturas encontradas
    print("\nFACTURAS ENCONTRADAS:")
    for i, fact in enumerate(facturas, 1):
        print(f"\n{i}. Factura N° {fact['numero']} - Cliente: {fact['cliente']}")
        print(f"Fecha: {fact['fecha']} - Total: S/ {fact['total']:.2f}")
        print("Productos:")
        for prod in fact['productos']:
            precio_unitario = prod.get('total', 0) / prod.get('cantidad', 1) if prod.get('cantidad', 0) > 0 else 0
            print(f"  - {prod['nombre']} (Cantidad: {prod['cantidad']}, Total: S/ {prod.get('total', 0):.2f})")
    
    # Seleccionar factura
    while True:
        try:
            seleccion = int(input("\nSeleccione la factura (número) o 0 para cancelar: "))
            if 0 <= seleccion <= len(facturas):
                break
            print("Selección inválida.")
        except ValueError:
            print("Ingrese un número válido.")
    
    if seleccion == 0:
        print("Operación cancelada.")
        return
    
    factura_seleccionada = facturas[seleccion-1]
    
    # Seleccionar productos a devolver
    productos_devolver = []
    print("\nSeleccione los productos a devolver:")
    for i, prod in enumerate(factura_seleccionada['productos'], 1):
        precio_unitario = prod.get('total', 0) / prod.get('cantidad', 1) if prod.get('cantidad', 0) > 0 else 0
        print(f"{i}. {prod['nombre']} - Cantidad: {prod['cantidad']} - Total: S/ {prod.get('total', 0):.2f}")
    
    while True:
        seleccion_productos = input("\nIngrese los números de productos a devolver (separados por comas) o 0 para cancelar: ").strip()
        if seleccion_productos == '0':
            print("Operación cancelada.")
            return
        
        try:
            indices = [int(idx.strip())-1 for idx in seleccion_productos.split(",") if idx.strip().isdigit()]
            if all(0 <= idx < len(factura_seleccionada['productos']) for idx in indices):
                break
            print("Algunos números de producto no son válidos.")
        except ValueError:
            print("Formato incorrecto. Use números separados por comas.")
    
    # Validar cantidades a devolver
    productos_devolucion = []
    for idx in indices:
        producto = factura_seleccionada['productos'][idx]
        
        while True:
            try:
                cantidad = int(input(f"Cantidad a devolver de {producto['nombre']} (máx {producto['cantidad']}): "))
                if 0 < cantidad <= producto['cantidad']:
                    break
                print(f"La cantidad debe estar entre 1 y {producto['cantidad']}")
            except ValueError:
                print("Ingrese un número válido.")
        
        precio_unitario = producto.get('total', 0) / producto.get('cantidad', 1) if producto.get('cantidad', 0) > 0 else 0
        productos_devolucion.append({
            'nombre': producto['nombre'],
            'codigo': producto.get('codigo', ''),
            'cantidad': cantidad,
            'precio': precio_unitario,
            'total': precio_unitario * cantidad
        })
    
    # Motivo de devolución
    while True:
        motivo = input("\nMotivo de la devolución: ").strip()
        if motivo:
            break
        print("El motivo no puede estar vacío.")
    
    # Registrar devolución
    fecha_devolucion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Guardar en archivo de devoluciones
    with open(ARCHIVO_DEVOLUCIONES, "a") as f:
        f.write(f"Fecha: {fecha_devolucion}|Factura: {factura_seleccionada['numero']}|")
        f.write(f"Cliente: {factura_seleccionada['cliente']}|Motivo: {motivo}|")
        
        # Escribir productos devueltos
        for prod in productos_devolucion:
            f.write(f"Producto: {prod['nombre']}|Cantidad: {prod['cantidad']}|")
            f.write(f"Precio: {prod['precio']:.2f}|Total: {prod['total']:.2f}|")
        
        f.write(f"Total Devolucion: {sum(p['total'] for p in productos_devolucion):.2f}\n")
    
    # Actualizar inventario (devolver productos al stock)
    actualizar_inventario_devolucion(productos_devolucion)
    
    print(f"\nDevolución registrada exitosamente.")
    print(f"Total devuelto: S/ {sum(p['total'] for p in productos_devolucion):.2f}")
    
    input("\nPresione Enter para continuar...")


def actualizar_inventario_devolucion(productos_devolucion):
    """Actualiza el inventario cuando se registra una devolución"""
    
    if not os.path.exists(ARCHIVO_INVENTARIO):
        print("Archivo de inventario no encontrado.")
        return
    
    # Leer inventario actual
    inventario = []
    with open(ARCHIVO_INVENTARIO, "r") as f:
        for linea in f:
            linea = linea.strip()
            if linea:
                # Parsear el formato con etiquetas
                datos = linea.split("|")
                item = {}
                for dato in datos:
                    if dato.startswith("Código:"):
                        item['codigo'] = dato.split(":")[1].strip()
                    elif dato.startswith("Nombre:"):
                        item['nombre'] = dato.split(":")[1].strip()
                    elif dato.startswith("Cantidad:"):
                        item['cantidad'] = int(dato.split(":")[1].strip())
                    elif dato.startswith("Precio:"):
                        item['precio'] = float(dato.split(":")[1].strip())
                
                if item:  # Solo agregar si se pudo parsear correctamente
                    inventario.append(item)
    
    # Actualizar cantidades
    for prod_dev in productos_devolucion:
        for item in inventario:
            if item['nombre'].lower() == prod_dev['nombre'].lower():
                item['cantidad'] += prod_dev['cantidad']
                break
    
    # Guardar inventario actualizado
    with open(ARCHIVO_INVENTARIO, "a") as f:
        for item in inventario:
            f.write(f"Código: {item['codigo']}|Nombre: {item['nombre']}|")
            f.write(f"Cantidad: {item['cantidad']}|Precio: {item['precio']:.2f}\n")
    
    print("Inventario actualizado con los productos devueltos.")
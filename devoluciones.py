import os
from datetime import datetime
from main import mostrar_menu_principal

ARCHIVO_FACTURAS = "facturas.txt"
ARCHIVO_DEVOLUCIONES = "devoluciones.txt"
ARCHIVO_INVENTARIO = "inventario.txt"

def verificar_archivo():
    return os.path.exists(ARCHIVO_FACTURAS)

def buscar_factura(numero_factura, cliente):
    facturas = []

    with open(ARCHIVO_FACTURAS, "r") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue

            datos = linea.split("|")
            factura = {}
            producto = {}

            for dato in datos:
                if dato.startswith("Fecha:"):
                    factura['fecha'] = dato.split(":")[1].strip()
                elif dato.startswith("Cliente:"):
                    factura['cliente'] = dato.split(":")[1].strip()
                elif dato.startswith("Codigo:"):
                    try:
                        factura['numero'] = int(dato.split(":")[1].strip())
                    except ValueError:
                        factura['numero'] = 0
                elif dato.startswith("Producto:"):
                    producto['nombre'] = dato.split(":")[1].strip()
                elif dato.startswith("Cantidad:"):
                    try:
                        producto['cantidad'] = int(dato.split(":")[1].strip())
                    except:
                        producto['cantidad'] = 0
                elif dato.startswith("Precio:"):
                    try:
                        producto['precio'] = float(dato.split(":")[1].strip())
                    except:
                        producto['precio'] = 0.0
                elif dato.startswith("Total:"):
                    try:
                        producto['total'] = float(dato.split(":")[1].strip())
                    except:
                        producto['total'] = producto.get('precio', 0.0) * producto.get('cantidad', 0)

            if producto:
                factura['productos'] = [producto]
                facturas.append(factura)

    resultados = []
    for fact in facturas:
        if numero_factura and fact.get('numero', 0) == numero_factura:
            resultados.append(fact)
        elif cliente and cliente.lower() in fact.get('cliente', '').lower():
            resultados.append(fact)

    return resultados if resultados else None

def registrar_devolucion(usuario_actual):
    print("\nREGISTRO DE DEVOLUCIÓN")

    print("\nBuscar factura por:")
    print("1. Número de factura")
    print("2. Nombre del cliente")

    while True:
        opcion = input("Seleccione una opción (1-2): ").strip()
        if opcion in ['1', '2']:
            break

    if not verificar_archivo():
        print("El archivo factura no existe!")
        return

    if opcion == '1':
        while True:
            try:
                numero = int(input("Número de factura: "))
                break
            except ValueError:
                print("Ingrese un número válido.")
        facturas = buscar_factura(numero_factura=numero, cliente="")
    else:
        cliente = input("Nombre del cliente: ").strip()
        facturas = buscar_factura(cliente=cliente, numero_factura=0)

    if not facturas:
        print("No se encontraron facturas con los criterios de búsqueda.")
        return

    print("\nFACTURAS ENCONTRADAS:")
    for i, fact in enumerate(facturas, 1):
        print(f"\n{i}. Factura N° {fact['numero']} - Cliente: {fact['cliente']}")
        print(f"Fecha: {fact['fecha']}")
        print("Productos:")
        for prod in fact['productos']:
            print(f"  - {prod['nombre']} (Cantidad: {prod['cantidad']}, Precio: C$/ {prod.get('precio', 0):.2f}, Total: C$/ {prod.get('total', 0):.2f})")

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

    factura_seleccionada = facturas[seleccion - 1]

    productos_devolver = []
    print("\nSeleccione los productos a devolver:")
    for i, prod in enumerate(factura_seleccionada['productos'], 1):
        print(f"{i}. {prod['nombre']} - Cantidad: {prod['cantidad']} - Precio: C$/ {prod.get('precio', 0):.2f}")

    while True:
        seleccion_productos = input("\nIngrese los números de productos a devolver (separados por comas) o 0 para cancelar: ").strip()
        if seleccion_productos == '0':
            print("Operación cancelada.")
            return

        try:
            indices = [int(idx.strip()) - 1 for idx in seleccion_productos.split(",") if idx.strip().isdigit()]
            if all(0 <= idx < len(factura_seleccionada['productos']) for idx in indices):
                break
            print("Algunos números de producto no son válidos.")
        except ValueError:
            print("Formato incorrecto. Use números separados por comas.")

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

        precio_unitario = producto.get('precio', 0.0)
        total = precio_unitario * cantidad
        productos_devolucion.append({
            'nombre': producto['nombre'],
            'cantidad': cantidad,
            'precio': precio_unitario,
            'total': total
        })

    while True:
        motivo = input("\nMotivo de la devolución: ").strip()
        if motivo:
            break
        print("El motivo no puede estar vacío.")

    fecha_devolucion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(ARCHIVO_DEVOLUCIONES, "a") as f:
        f.write(f"Fecha: {fecha_devolucion}|Factura: {factura_seleccionada['numero']}|")
        f.write(f"Cliente: {factura_seleccionada['cliente']}|Motivo: {motivo}|")
        for prod in productos_devolucion:
            f.write(f"Producto: {prod['nombre']}|Cantidad: {prod['cantidad']}|")
            f.write(f"Precio: {prod['precio']:.2f}|Total: {prod['total']:.2f}|")
        f.write(f"Total Devolucion: {sum(p['total'] for p in productos_devolucion):.2f}\n")

    actualizar_inventario_devolucion(productos_devolucion)

    print(f"\nDevolución registrada exitosamente.")
    print(f"Total devuelto: C$/ {sum(p['total'] for p in productos_devolucion):.2f}")
    input("\nPresione Enter para continuar...")

def actualizar_inventario_devolucion(productos_devolucion):
    if not os.path.exists(ARCHIVO_INVENTARIO):
        print("Archivo de inventario no encontrado.")
        return

    inventario_actual = []
    with open(ARCHIVO_INVENTARIO, "r") as f:
        for linea in f:
            datos = linea.strip().split("|")
            if len(datos) >= 5:
                inventario_actual.append(datos)

    for prod_dev in productos_devolucion:
        for art in inventario_actual:
            if art[1].lower() == prod_dev['nombre'].lower():
                art[4] = str(int(art[4]) + prod_dev['cantidad'])
                break

    with open(ARCHIVO_INVENTARIO, "w") as f:
        for art in inventario_actual:
            f.write("|".join(art) + "\n")

    print("Inventario actualizado con los productos devueltos.")

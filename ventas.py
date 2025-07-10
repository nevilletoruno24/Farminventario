import os
from datetime import datetime

ARCHIVO_INVENTARIO = "inventario.txt"
ARCHIVO_FACTURAS = "facturas.txt"

def buscar_articulo(codigo):
    if not os.path.exists(ARCHIVO_INVENTARIO):
        return None
    
    with open(ARCHIVO_INVENTARIO, "r") as f:
        for linea in f:
            datos = linea.strip().split("|")
            if datos[0] == codigo:
                return {
                    'codigo': datos[0],
                    'nombre': datos[1],
                    'precio': float(datos[3]),
                    'stock': int(datos[4])
                }
    return None

def actualizar_stock(codigo, cantidad_vendida):
    articulos = []
    actualizado = False
    
    with open(ARCHIVO_INVENTARIO, "r") as f:
        for linea in f:
            datos = linea.strip().split("|")
            if datos[0] == codigo:
                nuevo_stock = int(datos[4]) - cantidad_vendida
                if nuevo_stock < 0:
                    return False
                datos[4] = str(nuevo_stock)
                articulos.append("|".join(datos) + "\n")
                actualizado = True
            else:
                articulos.append(linea)
    
    if actualizado:
        with open(ARCHIVO_INVENTARIO, "w") as f:
            f.writelines(articulos)
        return True
    return False

def generar_factura():
    print("\nGENERACIÓN DE FACTURA")
    
    while True:
        nombre_cliente = input("Nombre del cliente: ").strip()
        if nombre_cliente:
            break
        print("El nombre del cliente no puede estar vacío.")
    
    productos = []

    while True:
        print("\nIngrese los datos del producto (deje el código vacío para terminar):")
        codigo = input("Código del artículo: ").strip()
        if not codigo:
            break
        
        articulo = buscar_articulo(codigo)
        if not articulo:
            print("Artículo no encontrado.")
            continue
        
        print(f"Artículo: {articulo['nombre']} - Precio: {articulo['precio']} - Stock: {articulo['stock']}")
        
        while True:
            try:
                cantidad = int(input("Cantidad a vender: "))
                if cantidad <= 0:
                    print("La cantidad debe ser mayor a 0.")
                elif cantidad > articulo['stock']:
                    print(f"No hay suficiente stock. Disponible: {articulo['stock']}")
                else:
                    break
            except ValueError:
                print("Ingrese un número entero válido.")
        
        subtotal = articulo['precio'] * cantidad
        igv = subtotal * 0.15
        total = subtotal + igv
        
        fecha_factura = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        productos.append({
            "fecha": fecha_factura,
            "cliente": nombre_cliente,
            "producto": [{
                'codigo': articulo['codigo'],
                'nombre': articulo['nombre'],
                'precio': articulo['precio'],
                'cantidad': cantidad,
                'subtotal': subtotal,
                'igv': igv,
                'total': total
            }]
        })

    if not productos:
        print("No se agregaron productos a la factura.")
        return

    print("\nFACTURA")
    print(f"Cliente: {nombre_cliente}")
    print("-" * 80)
    print("{:<10} {:<20} {:<10} {:<10} {:<10} {:<10} {:<10}".format(
        "Código","Producto", "Precio", "Cantidad", "Subtotal","IVA", "Total"))
    print("-" * 80)
    
    for prod in productos:
        p = prod['producto'][0]
        print("{:<10} {:<20} {:<10.2f} {:<10} {:<10.2f} {:<10.2f} {:<10.2f}".format(
            p["codigo"], p["nombre"], p["precio"], p["cantidad"], p["subtotal"], p["igv"], p["total"]
        ))
    
    print("-" * 80)
    print(f"TOTAL A PAGAR: C$/ {sum(p['producto'][0]['total'] for p in productos):.2f}")
    
    for prod in productos:
        if not actualizar_stock(prod['producto'][0]["codigo"], prod['producto'][0]["cantidad"]):
            print(f"Error al actualizar stock para {prod['producto'][0]['nombre']}")

    codigo_factura = obtener_codigo()
    with open(ARCHIVO_FACTURAS, "a") as f:
        for prod in productos:
            f.write(f"Fecha: {prod['fecha']}|Cliente: {prod['cliente']}|Codigo: {codigo_factura}|")
            for producto in prod['producto']:
                f.write(
                    f"Producto: {producto['nombre']}|Cantidad: {producto['cantidad']}|"
                    f"Precio: {producto['precio']:.2f}|Total: {producto['total']:.2f}|\n"
                )
    
    print("\nFactura generada y guardada exitosamente.")

def obtener_codigo():
    try:
        with open(ARCHIVO_FACTURAS, "r") as f:
            return len([linea for linea in f if linea.strip()]) + 1
    except FileNotFoundError:
        return 1


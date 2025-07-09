# ------------ facturacion.py ------------
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
                    return False  # No hay suficiente stock
                datos[4] = str(nuevo_stock)
                linea_actualizada = "|".join(datos) + "\n"
                articulos.append(linea_actualizada)
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
    
    # Solicitar datos del cliente
    while True:
        nombre_cliente = input("Nombre del cliente: ").strip()
        if nombre_cliente:
            break
        print("El nombre del cliente no puede estar vacío.")
    
    productos = []

    # Solicitar productos
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
        
        # Validar cantidad
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
        
        # Calcular valores
        subtotal = articulo['precio'] * cantidad
        igv = subtotal * 0.15
        total = subtotal + igv
        
        fecha_factura = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # Agregar a la lista de productos
        productos.append({
            "fecha":fecha_factura,
            "cliente":nombre_cliente,
            "producto":[{
                'codigo': articulo['codigo'],
                'nombre': articulo['nombre'],
                'precio': articulo['precio'],
                'cantidad': cantidad,
                'subtotal': subtotal,
                'igv': igv,
                'total': total
            }]})
        
        
    
    if not productos:
        print("No se agregaron productos a la factura.")
        return
    
    # Mostrar factura
    print("\nFACTURA")
    print(f"Cliente: {nombre_cliente}")
    print("-" * 80)
    print("{:<10} {:<20} {:<10} {:<10} {:<10} {:<10} {:<10}".format(
        "Código","Producto", "Precio", "Cantidad", "Subtotal","iva", "Total"))
    print("-" * 80)
    
    for prod in productos:
        print("{:<10} {:<20} {:<10.2f} {:<10} {:<10.2f} {:<10.2f} {:<10}".format(
            obtener_codigo(),
            prod['producto'][0]["nombre"],
            prod['producto'][0]["precio"],
            prod['producto'][0]["cantidad"],
            prod['producto'][0]["subtotal"],
            prod["producto"][0]["igv"],
            prod['producto'][0]["total"]
        ))
    
    print("-" * 80)
    print(f"TOTAL A PAGAR: C$/ {total:.2f}")
    
    # Actualizar stock y guardar factura
    for prod in productos:
        if not actualizar_stock(prod['producto'][0]["codigo"], prod['producto'][0]["cantidad"]):
            print(f"Error al actualizar stock para {prod['producto'][0]["nombre"]}")
    
    # Guardar factura en archivo
    
    with open(ARCHIVO_FACTURAS, "a") as f:
        for prod in productos:
            f.write(f"Fecha: {prod['fecha']}|Cliente: {prod['cliente']}|")
            for producto in prod['producto']:
                f.write(f"Codigo: {producto['codigo']}|Producto: {producto['nombre']}|Cantidad: {producto['cantidad']}|Total: {total}"+"\n")

    
    print("\nFactura generada y guardada exitosamente.")

def obtener_codigo():
    """
    Obtiene el siguiente código disponible para una nueva venta.
    
    Returns:
        int: Código único para la nueva venta
    """
    try:
        # Cuenta las líneas existentes y suma 1 para el nuevo código
        with open(ARCHIVO_FACTURAS, "r") as f:
            lineas = f.readlines()
            return len(lineas) + 1
    except FileNotFoundError:
        # Si el archivo no existe, comienza con código 1
        return 1


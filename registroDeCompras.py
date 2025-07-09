# ------------ registro_compras.py ------------
import os
from datetime import datetime

ARCHIVO_INVENTARIO = "inventario.txt"
ARCHIVO_PROVEEDORES = "proveedores.txt"
ARCHIVO_COMPRAS = "compras.txt"

def validar_fecha(fecha_str):
    try:
        datetime.strptime(fecha_str, "%Y-%m")
        return True
    except ValueError:
        return False

def registrar_compra(usuario_actual):
    print("\nREGISTRO DE COMPRA DE ARTÍCULOS")
    
    # Validar código de artículo (existente o nuevo)
    while True:
        codigo = input("Código del artículo (10 caracteres alfanuméricos): ").strip()
        if len(codigo) != 10 or not codigo.isalnum():
            print("El código debe tener exactamente 10 caracteres alfanuméricos.")
            continue
        
        # Verificar si el artículo existe
        articulo_existente = None
        if os.path.exists(ARCHIVO_INVENTARIO):
            with open(ARCHIVO_INVENTARIO, "r") as f:
                for linea in f:
                    datos = linea.strip().split("|")
                    if datos[0] == codigo:
                        articulo_existente = datos
                        break
        
        break
    
    # Validar nombre del proveedor (no vacío, hasta 50 caracteres)
    while True:
        proveedor = input("Nombre del proveedor (hasta 50 caracteres): ").strip()
        if not proveedor or len(proveedor) > 50:
            print("El proveedor no puede estar vacío y debe tener máximo 50 caracteres.")
        else:
            # Registrar proveedor si no existe
            if os.path.exists(ARCHIVO_PROVEEDORES):
                with open(ARCHIVO_PROVEEDORES, "r") as f:
                    if proveedor not in [linea.strip() for linea in f]:
                        with open(ARCHIVO_PROVEEDORES, "a") as f:
                            f.write(f"{proveedor}\n")
            else:
                with open(ARCHIVO_PROVEEDORES, "w") as f:
                    f.write(f"{proveedor}\n")
            break
    
    # Validar cantidad comprada (entero mayor a 0)
    while True:
        try:
            cantidad = int(input("Cantidad comprada (mayor a 0): "))
            if cantidad <= 0:
                print("La cantidad debe ser mayor a 0.")
            else:
                break
        except ValueError:
            print("Ingrese un número entero válido.")
    
    # Validar precio de compra (decimal mayor a 0)
    while True:
        try:
            precio = float(input("Precio unitario de compra (mayor a 0): "))
            if precio <= 0:
                print("El precio debe ser mayor a 0.")
            else:
                break
        except ValueError:
            print("Ingrese un valor numérico válido.")
    
    # Calcular total
    total = cantidad * precio
    
    # Fecha de compra (automática)
    fecha_compra = datetime.now().strftime("%Y-%m")
    
    # Actualizar inventario o registrar nuevo artículo
    if articulo_existente:
        # Actualizar stock
        nuevo_stock = int(articulo_existente[4]) + cantidad
        articulo_existente[4] = str(nuevo_stock)
        
        # Leer todos los artículos
        articulos = []
        with open(ARCHIVO_INVENTARIO, "r") as f:
            articulos = [linea.strip().split("|") for linea in f]
        
        # Actualizar el artículo específico
        for art in articulos:
            if art[0] == codigo:
                art[4] = str(nuevo_stock)
                break
        
        # Guardar cambios
        with open(ARCHIVO_INVENTARIO, "w") as f:
            for art in articulos:
                f.write("|".join(art) + "\n")
    else:
        # Registrar nuevo artículo
        print("\nEl artículo no existe en el inventario. Complete los datos para registrarlo:")
        
        # Validar nombre del artículo (no vacío, hasta 50 caracteres)
        while True:
            nombre = input("Nombre del artículo (hasta 50 caracteres): ").strip()
            if not nombre or len(nombre) > 50:
                print("El nombre no puede estar vacío y debe tener máximo 50 caracteres.")
            else:
                break
        
        # Validar categoría (no vacío, hasta 30 caracteres)
        while True:
            categoria = input("Categoría (hasta 30 caracteres): ").strip()
            if not categoria or len(categoria) > 30:
                print("La categoría no puede estar vacía y debe tener máximo 30 caracteres.")
            else:
                break
        
        # Fecha de vencimiento (opcional)
        fecha_vencimiento = ""
        while True:
            fecha_input = input("Fecha de vencimiento (AAAA-MM, opcional - dejar vacío): ").strip()
            if not fecha_input:
                break
            if validar_fecha(fecha_input):
                fecha_vencimiento = fecha_input
                break
            else:
                print("Formato de fecha incorrecto. Use AAAA-MM.")
        
        # Guardar nuevo artículo
        with open(ARCHIVO_INVENTARIO, "a") as f:
            f.write(f"{codigo}|{nombre}|{categoria}|{precio}|{cantidad}|{fecha_vencimiento}|{proveedor}\n")
    
    # Registrar la compra en el historial
    with open(ARCHIVO_COMPRAS, "a") as f:
        f.write(f"{codigo}|{proveedor}|{cantidad}|{precio}|{total}|{fecha_compra}|{usuario_actual['usuario']}\n")
    
    # Mostrar resumen
    print("\nCompra registrada exitosamente:")
    print(f"- Código de artículo: {codigo}")
    print(f"- Proveedor: {proveedor}")
    print(f"- Cantidad comprada: {cantidad}")
    print(f"- Precio unitario: S/ {precio:.2f}")
    print(f"- Total de compra: S/ {total:.2f}")
    print(f"- Fecha: {fecha_compra}")
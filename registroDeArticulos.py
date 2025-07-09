# ------------ registro_articulos.py ------------
import os
from datetime import datetime

ARCHIVO_INVENTARIO = "inventario.txt"

def validar_fecha(fecha_str):
    try:
        datetime.strptime(fecha_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def registrar_articulo():
    print("\nREGISTRO DE NUEVO ARTÍCULO")
    
    # Validar código del artículo (único, alfanumérico, 10 caracteres)
    while True:
        codigo = input("Código del artículo (10 caracteres alfanuméricos): ").strip()
        if len(codigo) != 10 or not codigo.isalnum():
            print("El código debe tener exactamente 10 caracteres alfanuméricos.")
            continue
        
        # Verificar si el código ya existe
        if os.path.exists(ARCHIVO_INVENTARIO):
            with open(ARCHIVO_INVENTARIO, "r") as f:
                for linea in f:
                    if linea.startswith(codigo):
                        print("Este código de artículo ya existe.")
                        break
                else:
                    break
        else:
            break
    
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
    
    # Validar precio (decimal mayor a 0)
    while True:
        try:
            precio = float(input("Precio por unidad (mayor a 0): "))
            if precio <= 0:
                print("El precio debe ser mayor a 0.")
            else:
                break
        except ValueError:
            print("Ingrese un valor numérico válido.")
    
    # Validar cantidad en stock (entero mayor o igual a 0)
    while True:
        try:
            cantidad = int(input("Cantidad en stock (mayor o igual a 0): "))
            if cantidad < 0:
                print("La cantidad no puede ser negativa.")
            else:
                break
        except ValueError:
            print("Ingrese un número entero válido.")
    
    # Fecha de vencimiento (opcional, formato dd/mm/aaaa)
    fecha_vencimiento = ""
    while True:
        fecha_input = input("Fecha de vencimiento (dd/mm/aaaa, opcional - dejar vacío): ").strip()
        if not fecha_input:
            break
        if validar_fecha(fecha_input):
            fecha_vencimiento = fecha_input
            break
        else:
            print("Formato de fecha incorrecto. Use dd/mm/aaaa.")
    
    # Proveedor (opcional, hasta 50 caracteres)
    proveedor = input("Proveedor (opcional - hasta 50 caracteres): ").strip()[:50]

    # Guardar en el archivo
    with open(ARCHIVO_INVENTARIO, "a") as f:
        f.write(f"{codigo}|{nombre}|{categoria}|{precio}|{cantidad}|{fecha_vencimiento}|{proveedor}"+"\n")
    
    
    # Mostrar resumen
    print("\nArtículo registrado exitosamente:")
    print(f"- Código: {codigo}")
    print(f"- Nombre: {nombre}")
    print(f"- Categoría: {categoria}")
    print(f"- Precio por unidad: {precio}")
    print(f"- Cantidad en stock: {cantidad}")
    print(f"- Fecha de vencimiento: {fecha_vencimiento if fecha_vencimiento else 'N/A'}")
    print(f"- Proveedor: {proveedor if proveedor else 'N/A'}")




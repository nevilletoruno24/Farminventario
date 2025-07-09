# ------------ bajas_inventario.py ------------
import os
from datetime import datetime

ARCHIVO_INVENTARIO = "inventario.txt"
ARCHIVO_BAJAS = "bajas.txt"

def registrar_baja(usuario_actual):
    print("\nREGISTRO DE BAJA DE INVENTARIO")
    
    if not os.path.exists(ARCHIVO_INVENTARIO):
        print("No hay artículos registrados en el inventario.")
        return
    
    # Mostrar artículos disponibles
    print("\nArtículos en inventario:")
    with open(ARCHIVO_INVENTARIO, "r") as f:
        for linea in f:
            datos = linea.strip().split("|")
            print(f"{datos[0]} - {datos[1]} (Stock: {datos[4]})")
    
    # Solicitar código del artículo
    while True:
        codigo = input("\nIngrese el código del artículo a dar de baja: ").strip()
        
        # Buscar artículo
        articulo = None
        articulos = []
        with open(ARCHIVO_INVENTARIO, "r") as f:
            for linea in f:
                datos = linea.strip().split("|")
                if datos[0] == codigo:
                    articulo = datos
                articulos.append(datos)
        
        if not articulo:
            print("Código de artículo no encontrado. Intente nuevamente.")
            continue
        
        break
    
    # Validar motivo de baja (no vacío, hasta 100 caracteres)
    while True:
        motivo = input("Motivo de la baja (pérdida/daño, hasta 100 caracteres): ").strip()
        if not motivo or len(motivo) > 100:
            print("El motivo no puede estar vacío y debe tener máximo 100 caracteres.")
        else:
            break
    
    # Validar cantidad a dar de baja (entero mayor a 0 y <= stock actual)
    stock_actual = int(articulo[4])
    while True:
        try:
            cantidad = int(input(f"Cantidad a dar de baja (stock actual: {stock_actual}): "))
            if cantidad <= 0:
                print("La cantidad debe ser mayor a 0.")
            elif cantidad > stock_actual:
                print(f"No puede dar de baja más de lo que existe en stock. Stock actual: {stock_actual}")
            else:
                break
        except ValueError:
            print("Ingrese un número entero válido.")
    
    # Fecha de baja (automática)
    fecha_baja = datetime.now().strftime("%Y-%m-%d")
    
    # Actualizar stock en inventario
    nuevo_stock = stock_actual - cantidad
    articulo[4] = str(nuevo_stock)
    
    # Guardar cambios en inventario
    with open(ARCHIVO_INVENTARIO, "w") as f:
        for art in articulos:
            f.write("|".join(art) + "\n")
    
    # Registrar la baja en el historial
    with open(ARCHIVO_BAJAS, "a") as f:
        f.write(f"{codigo}|{articulo[1]}|{cantidad}|{motivo}|{fecha_baja}|{usuario_actual['usuario']}\n")
    
    # Mostrar confirmación
    print("\nBaja registrada exitosamente:")
    print(f"- Código: {codigo}")
    print(f"- Nombre: {articulo[1]}")
    print(f"- Motivo: {motivo}")
    print(f"- Cantidad: {cantidad}")
    print(f"- Stock restante: {nuevo_stock}")
    print(f"- Fecha: {fecha_baja}")
    print(f"- Responsable: {usuario_actual['usuario']}")
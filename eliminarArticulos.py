# ------------ eliminar_articulos.py ------------
import os
from datetime import datetime

ARCHIVO_INVENTARIO = "inventario.txt"
ARCHIVO_HISTORIAL = "historial_eliminaciones.txt"

def eliminar_articulo():
    print("\nELIMINACIÓN DE ARTÍCULO")
    
    if not os.path.exists(ARCHIVO_INVENTARIO):
        print("No hay artículos registrados en el inventario.")
        return
    
    # Mostrar artículos disponibles
    print("\nArtículos en inventario:")
    with open(ARCHIVO_INVENTARIO, "r") as f:
        for linea in f:
            datos = linea.strip().split("|")
            print(f"{datos[0]} - {datos[1]} (Stock: {datos[4]})")
    
    # Solicitar código del artículo a eliminar
    while True:
        codigo = input("\nIngrese el código del artículo a eliminar: ").strip()
        
        # Verificar si el artículo existe
        articulos = []
        encontrado = False
        articulo_eliminado = None
        
        with open(ARCHIVO_INVENTARIO, "r") as f:
            for linea in f:
                datos = linea.strip().split("|")
                if datos[0] == codigo:
                    encontrado = True
                    articulo_eliminado = datos
                else:
                    articulos.append(linea)
        
        if not encontrado:
            print("Código de artículo no encontrado. Intente nuevamente.")
            continue
        
        break
    
    # Solicitar motivo de eliminación (opcional)
    motivo = input("Motivo de eliminación (opcional): ").strip()[:50]
    
    # Obtener usuario (simulado)
    usuario = "admin"  # En un sistema real, esto vendría de la autenticación
    
    # Obtener fecha actual
    fecha_eliminacion = datetime.now().strftime("%d/%m/%Y")
    
    # Guardar en historial
    with open(ARCHIVO_HISTORIAL, "a") as f:
        f.write(f"{codigo}|{articulo_eliminado[1]}|{usuario}|{fecha_eliminacion}|{motivo}\n")
    
    # Actualizar archivo de inventario (eliminando el artículo)
    with open(ARCHIVO_INVENTARIO, "w") as f:
        f.writelines(articulos)
    
    # Mostrar confirmación
    print("\nProducto eliminado exitosamente:")
    print(f"- Código: {codigo}")
    print(f"- Nombre: {articulo_eliminado[1]}")
    print(f"- Usuario que realizó la acción: {usuario}")
    print(f"- Fecha de eliminación: {fecha_eliminacion}")
    if motivo:
        print(f"- Motivo de eliminación: {motivo}")
# ------------ interfaz_grafica.py ------------
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from autenticacion import iniciar_sesion, verificar_permiso
from registroDeArticulos import registrar_articulo
from reporteInventario import menu_reportes
from registroDeCompras import registrar_compra
from bajasInventario import registrar_baja
from devoluciones import registrar_devolucion
from eliminarArticulos import eliminar_articulo
from ventas import generar_factura
from autenticacion import menu_usuarios
import sys

class SistemaInventarioGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Inventario")
        self.root.geometry("800x600")
        
        # Variables de estado
        self.usuario_actual = None
        
        # Mostrar pantalla de inicio de sesión
        self.mostrar_login()

    def mostrar_login(self):
        """Muestra la pantalla de inicio de sesión"""
        self.limpiar_pantalla()
        
        # Marco para el formulario de login
        login_frame = ttk.Frame(self.root, padding="20")
        login_frame.pack(expand=True)
        
        # Título
        ttk.Label(login_frame, text="INICIO DE SESIÓN", font=('Helvetica', 16)).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Campos de entrada
        ttk.Label(login_frame, text="Usuario:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.usuario_entry = ttk.Entry(login_frame)
        self.usuario_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(login_frame, text="Contraseña:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.password_entry = ttk.Entry(login_frame, show="*")
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Botón de inicio de sesión
        ttk.Button(login_frame, text="Iniciar Sesión", command=self.iniciar_sesion).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Centrar el frame
        login_frame.place(relx=0.5, rely=0.5, anchor="center")

    def iniciar_sesion(self):
        """Maneja el proceso de inicio de sesión"""
        usuario = self.usuario_entry.get()
        password = self.password_entry.get()
        
        # Simulamos el input para la autenticación por consola
        import sys
        from io import StringIO
        
        # Redirigir stdin para simular entrada
        old_stdin = sys.stdin
        sys.stdin = StringIO(f"{usuario}\n{password}\n")
        
        try:
            self.usuario_actual = iniciar_sesion()
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar sesión: {str(e)}")
        finally:
            # Restaurar stdin
            sys.stdin = old_stdin
        
        if self.usuario_actual:
            self.mostrar_menu_principal()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def mostrar_menu_principal(self):
        """Muestra el menú principal según los permisos del usuario"""
        self.limpiar_pantalla()
        
        # Marco principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Título
        ttk.Label(main_frame, 
                 text=f"SISTEMA DE INVENTARIO\nUsuario: {self.usuario_actual['nombre']} ({self.usuario_actual['rol']})", 
                 font=('Helvetica', 14), 
                 justify="center").pack(pady=10)
        
        # Marco para los botones
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(pady=20)
        
        # Crear botones según permisos
        row, col = 0, 0
        max_cols = 2
        
        if verificar_permiso(self.usuario_actual, 'registrar') or verificar_permiso(self.usuario_actual, 'modificar'):
            ttk.Button(buttons_frame, text="Gestión de Artículos", 
                      command=self.gestion_articulos).grid(row=row, column=col, padx=10, pady=10, sticky="ew")
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        if verificar_permiso(self.usuario_actual, 'reportes'):
            ttk.Button(buttons_frame, text="Reportes", 
                      command=self.mostrar_reportes).grid(row=row, column=col, padx=10, pady=10, sticky="ew")
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        if verificar_permiso(self.usuario_actual, 'compras'):
            ttk.Button(buttons_frame, text="Gestión de Compras", 
                      command=self.gestion_compras).grid(row=row, column=col, padx=10, pady=10, sticky="ew")
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        if verificar_permiso(self.usuario_actual, 'bajas'):
            ttk.Button(buttons_frame, text="Gestión de Bajas", 
                      command=self.gestion_bajas).grid(row=row, column=col, padx=10, pady=10, sticky="ew")
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        if verificar_permiso(self.usuario_actual, 'devoluciones'):
            ttk.Button(buttons_frame, text="Gestión de Devoluciones", 
                      command=self.gestion_devoluciones).grid(row=row, column=col, padx=10, pady=10, sticky="ew")
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        if verificar_permiso(self.usuario_actual, 'eliminar_articulos'):
            ttk.Button(buttons_frame, text="Eliminar Artículos", 
                      command=self.eliminar_articulos).grid(row=row, column=col, padx=10, pady=10, sticky="ew")
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        if verificar_permiso(self.usuario_actual, 'ventas'):
            ttk.Button(buttons_frame, text="Facturación", 
                      command=self.facturacion).grid(row=row, column=col, padx=10, pady=10, sticky="ew")
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        if self.usuario_actual['rol'] == 'admin':
            ttk.Button(buttons_frame, text="Gestión de Usuarios", 
                      command=self.gestion_usuarios).grid(row=row, column=col, padx=10, pady=10, sticky="ew")
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        # Botón de salida
        ttk.Button(buttons_frame, text="Salir", 
                  command=self.root.quit).grid(row=row, column=col, padx=10, pady=10, sticky="ew")

    def gestion_articulos(self):
        """Maneja la gestión de artículos"""
        try:
            registrar_articulo()
            messagebox.showinfo("Éxito", "Artículo registrado/modificado exitosamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al gestionar artículo: {str(e)}")

    def mostrar_reportes(self):
        """Muestra la interfaz de reportes"""
        # Crear una nueva ventana para los reportes
        reportes_window = tk.Toplevel(self.root)
        reportes_window.title("Reportes")
        reportes_window.geometry("600x400")
        
        # Marco principal
        main_frame = ttk.Frame(reportes_window, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Título
        ttk.Label(main_frame, text="MENÚ DE REPORTES", font=('Helvetica', 14)).pack(pady=10)
        
        # Botones de reportes
        ttk.Button(main_frame, text="Reporte de inventario actual", 
                  command=self.generar_reporte_inventario).pack(fill="x", pady=5)
        ttk.Button(main_frame, text="Reporte de artículos dados de baja", 
                  command=self.generar_reporte_bajas).pack(fill="x", pady=5)
        ttk.Button(main_frame, text="Reporte de artículos eliminados", 
                  command=self.generar_reporte_eliminaciones).pack(fill="x", pady=5)
        ttk.Button(main_frame, text="Reporte de facturas emitidas", 
                  command=self.generar_reporte_facturas).pack(fill="x", pady=5)
        ttk.Button(main_frame, text="Reporte de devoluciones", 
                  command=self.generar_reporte_devoluciones).pack(fill="x", pady=5)
        ttk.Button(main_frame, text="Reporte de compras", 
                  command=self.generar_reporte_compras).pack(fill="x", pady=5)
        ttk.Button(main_frame, text="Reporte general consolidado", 
                  command=self.generar_reporte_general).pack(fill="x", pady=5)
        ttk.Button(main_frame, text="Cerrar", 
                  command=reportes_window.destroy).pack(fill="x", pady=10)

    def generar_reporte_inventario(self):
        """Muestra el reporte de inventario en una nueva ventana"""
        self.mostrar_reporte_en_ventana("Reporte de Inventario", self.obtener_contenido_reporte("inventario"))

    def generar_reporte_bajas(self):
        """Muestra el reporte de bajas en una nueva ventana"""
        self.mostrar_reporte_en_ventana("Reporte de Bajas", self.obtener_contenido_reporte("bajas"))

    def generar_reporte_eliminaciones(self):
        """Muestra el reporte de eliminaciones en una nueva ventana"""
        self.mostrar_reporte_en_ventana("Reporte de Eliminaciones", self.obtener_contenido_reporte("eliminaciones"))

    def generar_reporte_facturas(self):
        """Muestra el reporte de facturas en una nueva ventana"""
        self.mostrar_reporte_en_ventana("Reporte de Facturas", self.obtener_contenido_reporte("facturas"))

    def generar_reporte_devoluciones(self):
        """Muestra el reporte de devoluciones en una nueva ventana"""
        self.mostrar_reporte_en_ventana("Reporte de Devoluciones", self.obtener_contenido_reporte("devoluciones"))

    def generar_reporte_compras(self):
        """Muestra el reporte de compras en una nueva ventana"""
        self.mostrar_reporte_en_ventana("Reporte de Compras", self.obtener_contenido_reporte("compras"))

    def generar_reporte_general(self):
        """Muestra el reporte general en una nueva ventana"""
        self.mostrar_reporte_en_ventana("Reporte General", self.obtener_contenido_reporte("general"))

    def obtener_contenido_reporte(self, tipo_reporte):
        """Obtiene el contenido del reporte especificado"""
        from io import StringIO
        import sys
        
        # Redirigir stdout para capturar la salida
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            if tipo_reporte == "inventario":
                from reporteInventario import generar_reporte_inventario
                generar_reporte_inventario()
            elif tipo_reporte == "bajas":
                from reporteInventario import generar_reporte_bajas
                generar_reporte_bajas()
            elif tipo_reporte == "eliminaciones":
                from reporteInventario import generar_reporte_eliminaciones
                generar_reporte_eliminaciones()
            elif tipo_reporte == "facturas":
                from reporteInventario import generar_reporte_facturas
                generar_reporte_facturas()
            elif tipo_reporte == "devoluciones":
                from reporteInventario import generar_reporte_devoluciones
                generar_reporte_devoluciones()
            elif tipo_reporte == "compras":
                from reporteInventario import generar_reporte_compras
                generar_reporte_compras()
            elif tipo_reporte == "general":
                from reporteInventario import generar_reporte_general
                generar_reporte_general()
            
            # Obtener la salida capturada
            contenido = sys.stdout.getvalue()
            return contenido
        except Exception as e:
            return f"Error al generar el reporte: {str(e)}"
        finally:
            # Restaurar stdout
            sys.stdout = old_stdout

    def mostrar_reporte_en_ventana(self, titulo, contenido):
        """Muestra el contenido del reporte en una nueva ventana"""
        report_window = tk.Toplevel(self.root)
        report_window.title(titulo)
        report_window.geometry("800x600")
        
        # Marco principal con scrollbar
        main_frame = ttk.Frame(report_window)
        main_frame.pack(fill="both", expand=True)
        
        # Text widget con scrollbar
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")
        
        report_text = tk.Text(text_frame, wrap="word", yscrollcommand=scrollbar.set)
        report_text.pack(fill="both", expand=True)
        
        scrollbar.config(command=report_text.yview)
        
        # Insertar contenido
        report_text.insert("1.0", contenido)
        report_text.config(state="disabled")
        
        # Botón para cerrar
        ttk.Button(main_frame, text="Cerrar", command=report_window.destroy).pack(pady=10)

    def gestion_compras(self):
        """Maneja la gestión de compras"""
        try:
            registrar_compra(self.usuario_actual)
            messagebox.showinfo("Éxito", "Compra registrada exitosamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar compra: {str(e)}")

    def gestion_bajas(self):
        """Maneja la gestión de bajas"""
        try:
            registrar_baja(self.usuario_actual)
            messagebox.showinfo("Éxito", "Baja registrada exitosamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar baja: {str(e)}")

    def gestion_devoluciones(self):
        """Maneja la gestión de devoluciones"""
        try:
            registrar_devolucion(self.usuario_actual)
            messagebox.showinfo("Éxito", "Devolución registrada exitosamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar devolución: {str(e)}")

    def eliminar_articulos(self):
        """Maneja la eliminación de artículos"""
        try:
            eliminar_articulo()
            messagebox.showinfo("Éxito", "Artículo eliminado exitosamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar artículo: {str(e)}")

    def facturacion(self):
        """Maneja la facturación"""
        try:
            generar_factura()
            messagebox.showinfo("Éxito", "Factura generada exitosamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar factura: {str(e)}")

    def gestion_usuarios(self):
        """Maneja la gestión de usuarios"""
        try:
            # Crear una nueva ventana para la gestión de usuarios
            usuarios_window = tk.Toplevel(self.root)
            usuarios_window.title("Gestión de Usuarios")
            usuarios_window.geometry("600x400")
            
            # Marco principal
            main_frame = ttk.Frame(usuarios_window, padding="20")
            main_frame.pack(fill="both", expand=True)
            
            # Título
            ttk.Label(main_frame, text="GESTIÓN DE USUARIOS", font=('Helvetica', 14)).pack(pady=10)
            
            # Botones de gestión de usuarios
            ttk.Button(main_frame, text="Registrar nuevo usuario", 
                      command=self.registrar_usuario).pack(fill="x", pady=5)
            ttk.Button(main_frame, text="Modificar permisos de usuario", 
                      command=self.modificar_permisos).pack(fill="x", pady=5)
            ttk.Button(main_frame, text="Cambiar estado de usuario", 
                      command=self.cambiar_estado_usuario).pack(fill="x", pady=5)
            ttk.Button(main_frame, text="Restablecer contraseña", 
                      command=self.restablecer_contrasena).pack(fill="x", pady=5)
            ttk.Button(main_frame, text="Cerrar", 
                      command=usuarios_window.destroy).pack(fill="x", pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"Error al acceder a gestión de usuarios: {str(e)}")

    def registrar_usuario(self):
        """Maneja el registro de nuevos usuarios"""
        try:
            from autenticacion import registrar_usuario
            registrar_usuario()
            messagebox.showinfo("Éxito", "Usuario registrado exitosamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar usuario: {str(e)}")

    def modificar_permisos(self):
        """Maneja la modificación de permisos"""
        try:
            from autenticacion import modificar_permisos
            modificar_permisos()
            messagebox.showinfo("Éxito", "Permisos modificados exitosamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al modificar permisos: {str(e)}")

    def cambiar_estado_usuario(self):
        """Maneja el cambio de estado de usuarios"""
        try:
            from autenticacion import cambiar_estado_usuario
            cambiar_estado_usuario()
            messagebox.showinfo("Éxito", "Estado de usuario modificado exitosamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cambiar estado de usuario: {str(e)}")

    def restablecer_contrasena(self):
        """Maneja el restablecimiento de contraseñas"""
        try:
            from autenticacion import restablecer_contrasena
            restablecer_contrasena()
            messagebox.showinfo("Éxito", "Contraseña restablecida exitosamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al restablecer contraseña: {str(e)}")

    def limpiar_pantalla(self):
        """Limpia todos los widgets de la pantalla"""
        for widget in self.root.winfo_children():
            widget.destroy()

def main():
    root = tk.Tk()
    app = SistemaInventarioGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
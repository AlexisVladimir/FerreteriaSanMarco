# src/views/ventas_view.py
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from src.controllers.ventas_controller import VentasController
from src.controllers.devolucion_controller import DevolucionController

class VentasView:
    def __init__(self, parent):
        # Controladores
        self.controller = VentasController()
        self.devolucion_controller = DevolucionController()

        # Frame principal de la vista de ventas
        self.frame = ttk.Frame(parent)
        self.frame.pack(expand=True, fill="both")

        # Notebook con dos pestañas: Ventas y Devoluciones
        self.sub_notebook = ttk.Notebook(self.frame, bootstyle="primary")
        self.sub_notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Pestaña Ventas
        self.ventas_frame = ttk.Frame(self.sub_notebook)
        self.sub_notebook.add(self.ventas_frame, text="Ventas")
        self.current_sale_items = []
        self.build_ventas_ui()

        # Pestaña Devoluciones
        self.devoluciones_frame = ttk.Frame(self.sub_notebook)
        self.sub_notebook.add(self.devoluciones_frame, text="Devoluciones")
        self.build_devoluciones_ui()

    # --- Pestaña Ventas ---
    def build_ventas_ui(self):
        input_frame = ttk.Frame(self.ventas_frame, padding=10)
        input_frame.pack(fill="x")
        ttk.Label(input_frame, text="ID Cliente:").grid(row=0, column=0, sticky="w", pady=5)
        self.id_cliente_entry = ttk.Entry(input_frame)
        self.id_cliente_entry.grid(row=0, column=1, sticky="ew", pady=5)

        ttk.Label(input_frame, text="ID Producto:").grid(row=1, column=0, sticky="w", pady=5)
        self.id_producto_entry = ttk.Entry(input_frame)
        self.id_producto_entry.grid(row=1, column=1, sticky="ew", pady=5)

        ttk.Label(input_frame, text="Cantidad:").grid(row=2, column=0, sticky="w", pady=5)
        self.cantidad_entry = ttk.Entry(input_frame)
        self.cantidad_entry.grid(row=2, column=1, sticky="ew", pady=5)

        input_frame.columnconfigure(1, weight=1)

        button_frame = ttk.Frame(self.ventas_frame, padding=10)
        button_frame.pack(fill="x")
        ttk.Button(button_frame, text="Agregar Producto",
                   command=self.agregar_producto, bootstyle="success").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Finalizar Venta",
                   command=self.finalizar_venta, bootstyle="primary").pack(side="right", padx=5)

        self.sale_table = ttk.Treeview(self.ventas_frame, columns=("ID Producto", "Cantidad"), show="headings")
        self.sale_table.heading("ID Producto", text="ID Producto")
        self.sale_table.heading("Cantidad", text="Cantidad")
        self.sale_table.pack(fill="both", expand=True, padx=10, pady=10)

    def agregar_producto(self):
        id_producto = self.id_producto_entry.get().strip()
        try:
            cantidad = int(self.cantidad_entry.get())
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor que 0")
        except ValueError:
            Messagebox.show_error("La cantidad debe ser un número entero mayor que 0.", "Error")
            return

        if not id_producto:
            Messagebox.show_error("Debe ingresar un ID de producto.", "Error")
            return

        self.current_sale_items.append({"id_producto": id_producto, "cantidad": cantidad})
        self.actualizar_tabla_ventas()

        self.id_producto_entry.delete(0, ttk.END)
        self.cantidad_entry.delete(0, ttk.END)

    def actualizar_tabla_ventas(self):
        for item in self.sale_table.get_children():
            self.sale_table.delete(item)
        for sale_item in self.current_sale_items:
            self.sale_table.insert("", ttk.END, values=(sale_item["id_producto"], sale_item["cantidad"]))

    def finalizar_venta(self):
        id_cliente = self.id_cliente_entry.get().strip()
        if not id_cliente:
            Messagebox.show_error("Debe ingresar un ID de cliente.", "Error")
            return
        if not self.current_sale_items:
            Messagebox.show_error("No hay productos en la venta.", "Error")
            return

        try:
            # Se asume que el empleado se fija de alguna forma; aquí se usa "1" como ejemplo
            ticket = self.controller.registrar_venta(id_cliente, "1", self.current_sale_items)
            Messagebox.show_info(
                f"Venta finalizada. Ticket ID: {ticket['id_ticket']}\nPDF generado en: {ticket['pdf_path']}",
                "Éxito"
            )
            self.id_cliente_entry.delete(0, ttk.END)
            self.current_sale_items.clear()
            self.actualizar_tabla_ventas()
        except Exception as e:
            error_message = f"Error al finalizar la venta: {str(e)}"
            print(f"Error capturado en finalizar_venta: {error_message}")
            Messagebox.show_error(error_message, "Error")

    # --- Pestaña Devoluciones ---
    def build_devoluciones_ui(self):
        devol_frame = ttk.Frame(self.devoluciones_frame, padding=10)
        devol_frame.pack(fill="x")

        ttk.Label(devol_frame, text="ID Ticket:").grid(row=0, column=0, sticky="w", pady=5)
        self.devol_ticket_entry = ttk.Entry(devol_frame)
        self.devol_ticket_entry.grid(row=0, column=1, pady=5, sticky="ew")

        ttk.Label(devol_frame, text="ID Producto:").grid(row=1, column=0, sticky="w", pady=5)
        self.devol_producto_entry = ttk.Entry(devol_frame)
        self.devol_producto_entry.grid(row=1, column=1, pady=5, sticky="ew")

        ttk.Label(devol_frame, text="Cantidad:").grid(row=2, column=0, sticky="w", pady=5)
        self.devol_cantidad_entry = ttk.Entry(devol_frame)
        self.devol_cantidad_entry.grid(row=2, column=1, pady=5, sticky="ew")

        ttk.Label(devol_frame, text="Motivo:").grid(row=3, column=0, sticky="w", pady=5)
        self.devol_motivo_entry = ttk.Entry(devol_frame)
        self.devol_motivo_entry.grid(row=3, column=1, pady=5, sticky="ew")

        devol_frame.columnconfigure(1, weight=1)

        ttk.Button(devol_frame, text="Registrar Devolución",
                   command=self.registrar_devolucion, bootstyle="info").grid(row=4, column=1, pady=10, sticky="e")

    def registrar_devolucion(self):
        id_ticket = self.devol_ticket_entry.get().strip()
        id_producto = self.devol_producto_entry.get().strip()
        try:
            cantidad = int(self.devol_cantidad_entry.get())
        except ValueError:
            Messagebox.show_error("La cantidad debe ser un número entero.", "Error")
            return
        motivo = self.devol_motivo_entry.get().strip()

        if not (id_ticket and id_producto and cantidad > 0):
            Messagebox.show_error("Todos los campos son obligatorios y la cantidad debe ser mayor que 0.", "Error")
            return

        devolucion = self.devolucion_controller.agregar_devolucion(id_ticket, id_producto, cantidad, motivo)
        if devolucion:
            Messagebox.show_info("Devolución registrada exitosamente.", "Éxito")
            self.devol_ticket_entry.delete(0, ttk.END)
            self.devol_producto_entry.delete(0, ttk.END)
            self.devol_cantidad_entry.delete(0, ttk.END)
            self.devol_motivo_entry.delete(0, ttk.END)
        else:
            Messagebox.show_error("Error al registrar la devolución.", "Error")

    def close(self):
        self.controller.close()
        self.devolucion_controller.close()

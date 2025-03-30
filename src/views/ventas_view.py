# src/views/ventas_view.py
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from src.controllers.ventas_controller import VentasController

class VentasView:
    def __init__(self, parent):
        self.controller = VentasController()
        self.frame = ttk.Frame(parent)
        self.current_sale_items = []
        self.build_ui()
        self.frame.pack(expand=True, fill="both")

    def build_ui(self):
        input_frame = ttk.Frame(self.frame, padding=10)
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

        button_frame = ttk.Frame(self.frame, padding=10)
        button_frame.pack(fill="x")
        ttk.Button(button_frame, text="Agregar Producto",
                   command=self.agregar_producto, bootstyle="success").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Finalizar Venta",
                   command=self.finalizar_venta, bootstyle="primary").pack(side="right", padx=5)

        self.sale_table = ttk.Treeview(self.frame, columns=("ID Producto", "Cantidad"), show="headings")
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
        self.actualizar_tabla()

        self.id_producto_entry.delete(0, ttk.END)
        self.cantidad_entry.delete(0, ttk.END)

    def actualizar_tabla(self):
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
            ticket = self.controller.registrar_venta(id_cliente, "empleado_dummy", self.current_sale_items)
            Messagebox.show_info(
                f"Venta finalizada. Ticket ID: {ticket['id_ticket']}\nPDF generado en: {ticket['pdf_path']}",
                "Éxito"
            )

            self.id_cliente_entry.delete(0, ttk.END)
            self.current_sale_items.clear()
            self.actualizar_tabla()
        except Exception as e:
            Messagebox.show_error(f"Error al finalizar la venta: {str(e)}", "Error")
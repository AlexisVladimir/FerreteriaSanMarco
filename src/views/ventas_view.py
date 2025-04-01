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

        # Nuevo frame para método de pago
        payment_frame = ttk.Frame(self.ventas_frame, padding=10)
        payment_frame.pack(fill="x")
        ttk.Label(payment_frame, text="Método de pago:").grid(row=0, column=0, sticky="w", pady=5)
        self.payment_method_var = ttk.StringVar()
        self.payment_method_combobox = ttk.Combobox(payment_frame, textvariable=self.payment_method_var, state="readonly")
        self.payment_method_combobox['values'] = ["Efectivo", "Tarjeta"]
        self.payment_method_combobox.current(0)
        self.payment_method_combobox.grid(row=0, column=1, sticky="ew", pady=5)
        ttk.Label(payment_frame, text="Monto entregado (si es efectivo):").grid(row=1, column=0, sticky="w", pady=5)
        self.efectivo_entry = ttk.Entry(payment_frame)
        self.efectivo_entry.grid(row=1, column=1, sticky="ew", pady=5)
        payment_frame.columnconfigure(1, weight=1)

        button_frame = ttk.Frame(self.ventas_frame, padding=10)
        button_frame.pack(fill="x")
        ttk.Button(button_frame, text="Agregar Producto", command=self.agregar_producto, bootstyle="success").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Eliminar Producto", command=self.eliminar_producto, bootstyle="danger").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Finalizar Venta", command=self.finalizar_venta, bootstyle="primary").pack(side="right", padx=5)

        # Actualizamos las columnas del Treeview para mostrar la información completa del producto
        self.sale_table = ttk.Treeview(self.ventas_frame, columns=("ID Producto", "Nombre", "Descripción", "Precio", "Cantidad", "Subtotal"), show="headings")
        self.sale_table.heading("ID Producto", text="ID Producto")
        self.sale_table.heading("Nombre", text="Nombre")
        self.sale_table.heading("Descripción", text="Descripción")
        self.sale_table.heading("Precio", text="Precio")
        self.sale_table.heading("Cantidad", text="Cantidad")
        self.sale_table.heading("Subtotal", text="Subtotal")
        self.sale_table.pack(fill="both", expand=True, padx=10, pady=10)

        # Label para mostrar el total a pagar
        self.total_label = ttk.Label(self.ventas_frame, text="Total a pagar: $0.00", font=("Helvetica", 14))
        self.total_label.pack(pady=10)

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

        prod_info = self.controller.obtener_producto_info(id_producto)
        if not prod_info:
            Messagebox.show_error(f"Producto con ID {id_producto} no encontrado.", "Error")
            return

        if prod_info["stock"] < cantidad:
            Messagebox.show_error(f"No hay suficiente stock para el producto {prod_info['nombre']}. Stock actual: {prod_info['stock']}", "Error")
            return

        self.current_sale_items.append({
            "id_producto": id_producto,
            "nombre": prod_info["nombre"],
            "descripcion": prod_info["descripcion"],
            "precio": prod_info["precio"],
            "cantidad": cantidad
        })
        self.actualizar_tabla_ventas()

        self.id_producto_entry.delete(0, ttk.END)
        self.cantidad_entry.delete(0, ttk.END)

    def eliminar_producto(self):
        selected = self.sale_table.selection()
        if not selected:
            Messagebox.show_error("Seleccione un producto para eliminar.", "Error")
            return
        index = int(selected[0])
        del self.current_sale_items[index]
        self.actualizar_tabla_ventas()

    def actualizar_tabla_ventas(self):
        # Limpiar el Treeview
        for item in self.sale_table.get_children():
            self.sale_table.delete(item)
        total = 0

        # Insertar productos en el Treeview con los nuevos campos
        for index, item in enumerate(self.current_sale_items):
            subtotal = item["cantidad"] * item["precio"]
            total += subtotal*1.16
            self.sale_table.insert("", "end", iid=str(index),
                                   values=(item["id_producto"], item["nombre"], item["descripcion"], f"${item['precio']:.2f}",
                                           item["cantidad"], f"${subtotal:.2f}"))
        totaltotal = total * 1.16
        self.total_label.config(text=f"Total a pagar: ${total:.2f}")

    def finalizar_venta(self):
        id_cliente = self.id_cliente_entry.get().strip()
        if not id_cliente:
            Messagebox.show_error("Debe ingresar un ID de cliente.", "Error")
            return
        if not self.current_sale_items:
            Messagebox.show_error("No hay productos en la venta.", "Error")
            return

        payment_method = self.payment_method_var.get()
        efectivo_amount = None
        if payment_method == "Efectivo":
            try:
                efectivo_amount = float(self.efectivo_entry.get().strip())
            except ValueError:
                Messagebox.show_error("El monto entregado debe ser un número.", "Error")
                return

        try:
            ticket = self.controller.registrar_venta(id_cliente, "1", self.current_sale_items, payment_method, efectivo_amount)
            Messagebox.show_info(f"Venta finalizada. Ticket ID: {ticket['id_ticket']}\nPDF generado en: {ticket['pdf_path']}", "Éxito")
            self.id_cliente_entry.delete(0, ttk.END)
            self.current_sale_items.clear()
            self.actualizar_tabla_ventas()
        except Exception as e:
            error_message = f"Error al finalizar la venta: {str(e)}"
            print(f"Error capturado en finalizar_venta: {error_message}")
            Messagebox.show_error(error_message, "Error")

    # --- Pestaña Devoluciones (sin cambios) ---
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
        ttk.Button(devol_frame, text="Registrar Devolución", command=self.registrar_devolucion, bootstyle="info").grid(row=4, column=1, pady=10, sticky="e")

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

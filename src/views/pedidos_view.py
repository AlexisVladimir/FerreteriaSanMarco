import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from src.controllers.pedidos_controller import registrar_pedido

class PedidosView:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.build_ui()
        self.cargar_pedidos()

    def build_ui(self):
        input_frame = ttk.Frame(self.frame, padding=10)
        input_frame.pack(fill="x")
        ttk.Label(input_frame, text="ID Proveedor:").grid(row=0, column=0, sticky="w", pady=5)
        self.id_proveedor_entry = ttk.Entry(input_frame)
        self.id_proveedor_entry.grid(row=0, column=1, sticky="ew", pady=5)
        input_frame.columnconfigure(1, weight=1)

        button_frame = ttk.Frame(self.frame, padding=10)
        button_frame.pack(fill="x")
        ttk.Button(button_frame, text="Registrar Pedido",
                   command=self.registrar_pedido, bootstyle="success").pack(side="left", padx=5)

        self.pedidos_table = ttk.Treeview(self.frame,
            columns=("ID Pedido", "ID Proveedor", "Fecha Solicitud", "Estado"), show="headings")
        for col in ("ID Pedido", "ID Proveedor", "Fecha Solicitud", "Estado"):
            self.pedidos_table.heading(col, text=col)
        self.pedidos_table.pack(fill="both", expand=True, padx=10, pady=10)

    def registrar_pedido(self):
        id_proveedor = self.id_proveedor_entry.get().strip()
        if not id_proveedor:
            Messagebox.show_error("Debe ingresar el ID del proveedor.", "Error")
            return
        pedido_id = registrar_pedido(id_proveedor)
        Messagebox.show_info(f"Pedido registrado. ID Pedido: {pedido_id}", "Éxito")
        self.id_proveedor_entry.delete(0, ttk.END)
        self.cargar_pedidos()

    def cargar_pedidos(self):
        for item in self.pedidos_table.get_children():
            self.pedidos_table.delete(item)
        dummy_data = [
            (1, "prov1", "2023-03-29 12:00:00", "pendiente"),
            (2, "prov2", "2023-03-29 12:05:00", "recibido")
        ]
        for row in dummy_data:
            self.pedidos_table.insert("", ttk.END, values=row)
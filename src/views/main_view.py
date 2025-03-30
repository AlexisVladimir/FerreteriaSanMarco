import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from src.views.inventario_view import InventarioView
from src.views.ventas_view import VentasView
from src.views.pedidos_view import PedidosView
from src.views.reportes_view import ReportesView


class MainView:
    def __init__(self, root):
        self.root = root
        self.root.title("Ferretería San Marcos - Sistema de Gestión")
        self.root.geometry("1000x700")
        self.style = ttk.Style(theme='flatly')

        self.notebook = ttk.Notebook(self.root, bootstyle="primary")
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        self.add_tab("Principal", "Bienvenido al Sistema de Gestión de Ferretería San Marcos")
        self.notebook.add(VentasView(self.notebook).frame, text="Ventas")
        self.notebook.add(InventarioView(self.notebook).frame, text="Inventario")
        self.notebook.add(PedidosView(self.notebook).frame, text="Pedidos")
        self.notebook.add(ReportesView(self.notebook).frame, text="Reportes")

    def add_tab(self, title, message):
        frame = ttk.Frame(self.notebook)
        label = ttk.Label(frame, text=message, font=("Helvetica", 16))
        label.pack(pady=20)
        self.notebook.add(frame, text=title)


if __name__ == "__main__":
    root = ttk.Window(themename='flatly')
    app = MainView(root)
    root.mainloop()
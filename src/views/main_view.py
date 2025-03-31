import ttkbootstrap as ttk
from PIL import Image, ImageTk
from ttkbootstrap.constants import *
from src.views.inventario_view import InventarioView
from src.views.ventas_view import VentasView
from src.views.pedidos_view import PedidosView
from src.views.reportes_view import ReportesView
from src.views.administracion_view import AdministracionView
from src.views.turnos_view import TurnosView
from tkinter import PhotoImage


class MainView:
    def __init__(self, root):
        self.root = root
        self.root.title("Ferretería San Marcos - Sistema de Gestión")
        self.root.geometry("1000x700")
        self.style = ttk.Style(theme='flatly')

        self.style.configure("Black.TFrame", background="black")
        self.style.configure("White.TLabel", background="black", foreground="white", font=("Helvetica", 16))
        self.style.configure("Black.TLabel", background="black")

        self.notebook = ttk.Notebook(self.root, bootstyle="primary")
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        self.add_tab("Principal", "Bienvenido al Sistema de Gestión de Ferretería San Marcos")
        self.notebook.add(VentasView(self.notebook).frame, text="Ventas")
        self.notebook.add(TurnosView(self.notebook).frame, text="Turno")
        self.notebook.add(InventarioView(self.notebook).frame, text="Inventario")
        self.notebook.add(PedidosView(self.notebook).frame, text="Pedidos")
        self.notebook.add(ReportesView(self.notebook).frame, text="Reportes")
        self.notebook.add(AdministracionView(self.notebook).frame, text="Administracion")

        print("Creando InventarioView desde MainView")  # Debug
        self.inventario_view = InventarioView(self.root)


    def add_tab(self, title, message):
        if title == "Principal":
            frame = ttk.Frame(self.notebook, style="Black.TFrame")
            original_logo = PhotoImage(file="resources/logo_F.png")
            self.logo_image = original_logo
            image_label = ttk.Label(frame, image=self.logo_image, style="Black.TLabel")
            image_label.pack(pady=10)
            label = ttk.Label(frame, text=message, style="White.TLabel")
            label.pack(pady=20)
            self.notebook.add(frame, text=title)
        else:
            frame = ttk.Frame(self.notebook)
            label = ttk.Label(frame, text=message, font=("Helvetica", 16))
            label.pack(pady=20)
            self.notebook.add(frame, text=title)


if __name__ == "__main__":
    root = ttk.Window(themename='flatly')
    app = MainView(root)
    root.mainloop()
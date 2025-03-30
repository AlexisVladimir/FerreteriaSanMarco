import ttkbootstrap as tkb
from ttkbootstrap.constants import *
from tkinter import ttk, messagebox
from src.controllers.inventario_controller import InventarioController

class InventarioView:
    def __init__(self, parent):
        self.controller = InventarioController()
        self.frame = tkb.Frame(parent)
        self.setup_inventario_tab()
        self.frame.pack(expand=True, fill="both")

    def setup_inventario_tab(self):
        # Notebook para subsecciones dentro de Inventario
        notebook = ttk.Notebook(self.frame)

        # Subsección 1: Añadir Producto
        agregar_tab = ttk.Frame(notebook)
        notebook.add(agregar_tab, text="Añadir Producto")
        self.setup_agregar_tab(agregar_tab)

        # Subsección 2: Buscar Productos
        buscar_tab = ttk.Frame(notebook)
        notebook.add(buscar_tab, text="Buscar Productos")
        self.setup_buscar_tab(buscar_tab)

        # Subsección 3: Buscar por Estantería
        estanteria_tab = ttk.Frame(notebook)
        notebook.add(estanteria_tab, text="Buscar por Estantería")
        self.setup_estanteria_tab(estanteria_tab)

        # Subsección 4: Compatibilidad de Vehículos
        compatibilidad_tab = ttk.Frame(notebook)
        notebook.add(compatibilidad_tab, text="Compatibilidad Vehículos")
        self.setup_compatibilidad_tab(compatibilidad_tab)

        notebook.pack(expand=True, fill="both", padx=10, pady=10)

    def setup_agregar_tab(self, tab):
        form_frame = tkb.Frame(tab)
        form_frame.pack(pady=10, padx=10, fill="x")

        fields = [
            ("Nombre:", "nombre_entry"),
            ("Descripción:", "descripcion_entry"),
            ("Categoría (ID):", "categoria_entry"),
            ("Cantidad Inicial:", "cantidad_entry"),
            ("Precio Unitario:", "precio_entry"),
            ("Ubicación (ID):", "ubicacion_entry"),
            ("Proveedor (ID):", "proveedor_entry"),
            ("Fecha de Ingreso (YYYY-MM-DD):", "fecha_entry")
        ]

        for label_text, attr_name in fields:
            field_frame = tkb.Frame(form_frame)
            field_frame.pack(fill="x")
            tkb.Label(field_frame, text=label_text).pack(side="left")
            entry = tkb.Entry(field_frame)
            entry.pack(side="left", fill="x", expand=True, padx=5)
            setattr(self, attr_name, entry)

        tkb.Button(form_frame, text="Agregar Producto", bootstyle=SUCCESS, command=self.agregar_producto).pack(pady=10)

    def agregar_producto(self):
        try:
            nombre = self.nombre_entry.get()
            descripcion = self.descripcion_entry.get()
            categoria = int(self.categoria_entry.get())
            cantidad = int(self.cantidad_entry.get())
            precio = float(self.precio_entry.get())
            ubicacion = int(self.ubicacion_entry.get())
            proveedor = int(self.proveedor_entry.get())
            fecha = self.fecha_entry.get()

            if self.controller.agregar_producto(nombre, descripcion, categoria, cantidad, precio, ubicacion, proveedor, fecha):
                messagebox.showinfo("Éxito", "Producto agregado correctamente")
                # Limpiar campos
                for entry in [self.nombre_entry, self.descripcion_entry, self.categoria_entry, self.cantidad_entry,
                              self.precio_entry, self.ubicacion_entry, self.proveedor_entry, self.fecha_entry]:
                    entry.delete(0, "end")
            else:
                messagebox.showerror("Error", "No se pudo agregar el producto")
        except ValueError as e:
            messagebox.showerror("Error", "Por favor, ingrese valores válidos (números para categoría, cantidad, precio, ubicación, proveedor)")

    def setup_buscar_tab(self, tab):
        search_frame = tkb.Frame(tab)
        search_frame.pack(pady=10, padx=10, fill="x")

        tkb.Label(search_frame, text="Buscar por:").pack(side="left")
        self.buscar_entry = tkb.Entry(search_frame)
        self.buscar_entry.pack(side="left", fill="x", expand=True, padx=5)

        filter_frame = tkb.Frame(search_frame)
        filter_frame.pack(fill="x", pady=5)
        self.filtro_var = tkb.StringVar(value="Nombre")
        tkb.Radiobutton(filter_frame, text="Nombre", variable=self.filtro_var, value="Nombre", bootstyle="primary").pack(side="left", padx=5)
        tkb.Radiobutton(filter_frame, text="Categoría", variable=self.filtro_var, value="ID_Subcategoria", bootstyle="primary").pack(side="left", padx=5)
        tkb.Radiobutton(filter_frame, text="Proveedor", variable=self.filtro_var, value="ID_Proveedor", bootstyle="primary").pack(side="left", padx=5)
        tkb.Radiobutton(filter_frame, text="Ubicación", variable=self.filtro_var, value="ID_Ubicacion", bootstyle="primary").pack(side="left", padx=5)

        tkb.Button(search_frame, text="Buscar", bootstyle=INFO, command=self.buscar_productos).pack(side="left", padx=5)

        columns = ("ID", "Nombre", "Categoría", "Precio", "Stock", "Ubicación")
        self.tree = ttk.Treeview(tab, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

    def buscar_productos(self):
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        filtro = self.filtro_var.get()
        valor = self.buscar_entry.get()
        resultados = self.controller.buscar_productos(filtro, valor)

        for resultado in resultados:
            self.tree.insert("", "end", values=resultado)

    def setup_estanteria_tab(self, tab):
        estanteria_frame = tkb.Frame(tab)
        estanteria_frame.pack(pady=10, padx=10, fill="x")

        tkb.Label(estanteria_frame, text="Ubicación (ID):").pack(side="left")
        self.estanteria_entry = tkb.Entry(estanteria_frame)
        self.estanteria_entry.pack(side="left", fill="x", expand=True, padx=5)

        tkb.Button(estanteria_frame, text="Buscar", bootstyle=INFO, command=self.buscar_por_estanteria).pack(side="left", padx=5)

        columns = ("ID", "Nombre", "Categoría", "Stock", "Ubicación")
        self.estanteria_tree = ttk.Treeview(tab, columns=columns, show="headings")
        for col in columns:
            self.estanteria_tree.heading(col, text=col)
            self.estanteria_tree.column(col, width=100)
        self.estanteria_tree.pack(expand=True, fill="both", padx=10, pady=10)

    def buscar_por_estanteria(self):
        try:
            ubicacion = int(self.estanteria_entry.get())
            # Limpiar tabla
            for item in self.estanteria_tree.get_children():
                self.estanteria_tree.delete(item)

            resultados = self.controller.buscar_por_estanteria(ubicacion)
            for resultado in resultados:
                self.estanteria_tree.insert("", "end", values=resultado)
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un ID de ubicación válido (número)")

    def setup_compatibilidad_tab(self, tab):
        compat_frame = tkb.Frame(tab)
        compat_frame.pack(pady=10, padx=10, fill="x")

        fields = [
            ("Marca:", "marca_entry"),
            ("Modelo:", "modelo_entry"),
            ("Año:", "anio_entry")
        ]

        for label_text, attr_name in fields:
            field_frame = tkb.Frame(compat_frame)
            field_frame.pack(fill="x")
            tkb.Label(field_frame, text=label_text).pack(side="left")
            entry = tkb.Entry(field_frame)
            entry.pack(side="left", fill="x", expand=True, padx=5)
            setattr(self, attr_name, entry)

        tkb.Button(compat_frame, text="Buscar Birlos Compatibles", bootstyle=INFO, command=self.buscar_birlos_compatibles).pack(pady=5)

        columns = ("ID Birlo", "Medida", "Tipo Rosca", "Compatibilidad")
        self.compat_tree = ttk.Treeview(tab, columns=columns, show="headings")
        for col in columns:
            self.compat_tree.heading(col, text=col)
            self.compat_tree.column(col, width=100)
        self.compat_tree.pack(expand=True, fill="both", padx=10, pady=10)

    def buscar_birlos_compatibles(self):
        try:
            marca = self.marca_entry.get()
            modelo = self.modelo_entry.get()
            anio = int(self.anio_entry.get())

            # Limpiar tabla
            for item in self.compat_tree.get_children():
                self.compat_tree.delete(item)

            resultados = self.controller.buscar_birlos_compatibles(marca, modelo, anio)
            for resultado in resultados:
                self.compat_tree.insert("", "end", values=resultado)
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un año válido (número)")
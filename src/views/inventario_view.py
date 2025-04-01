# src/views/inventario_view.py
import ttkbootstrap as tkb
from ttkbootstrap.constants import *
from tkinter import ttk, messagebox
from src.controllers.inventario_controller import InventarioController

class InventarioView:
    def __init__(self, parent):
        print("Inicializando InventarioView")  # Debug
        self.controller = InventarioController()
        self.frame = tkb.Frame(parent)
        self.setup_inventario_tab()
        self.frame.pack(expand=True, fill="both")
        self.selected_product_id = None  # Para almacenar el ID del producto seleccionado
        self.subcategoria_ids = []  # Almacenará los IDs de subcategorías
        self.ubicacion_ids = []


    def setup_inventario_tab(self):
        notebook = ttk.Notebook(self.frame)

        # Pestaña de Gestión de Productos (CRUD completo)
        gestion_tab = ttk.Frame(notebook)
        notebook.add(gestion_tab, text="Gestión de Productos")
        self.setup_gestion_tab(gestion_tab)

        # Otras pestañas (búsquedas)
        buscar_tab = ttk.Frame(notebook)
        notebook.add(buscar_tab, text="Buscar Productos")
        self.setup_buscar_tab(buscar_tab)

        estanteria_tab = ttk.Frame(notebook)
        notebook.add(estanteria_tab, text="Buscar por Estantería")
        self.setup_estanteria_tab(estanteria_tab)

        compatibilidad_tab = ttk.Frame(notebook)
        notebook.add(compatibilidad_tab, text="Compatibilidad Vehículos")
        self.setup_compatibilidad_tab(compatibilidad_tab)

        notebook.pack(expand=True, fill="both", padx=10, pady=10)

    def setup_gestion_tab(self, tab):
        """Configura la pestaña de gestión de productos con Combobox para ubicaciones y subcategorías"""
        main_frame = tkb.Frame(tab)
        main_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Frame del formulario
        form_frame = tkb.LabelFrame(main_frame, text="Formulario de Producto", bootstyle="info")
        form_frame.pack(fill="x", pady=5)

        # Campo ID (solo lectura)
        field_frame = tkb.Frame(form_frame)
        field_frame.pack(fill="x", pady=2, padx=5)
        tkb.Label(field_frame, text="ID Producto:", width=15).pack(side="left")
        self.id_entry = tkb.Entry(field_frame)  # Editable por defecto
        self.id_entry.pack(side="left", fill="x", expand=True, padx=5)

        # Campos del formulario
        fields = [
            ("Nombre*:", "nombre_entry"),
            ("Descripción:", "descripcion_entry"),
            ("Cantidad*:", "cantidad_entry"),
            ("Precio Unitario*:", "precio_entry")
        ]
        for label_text, attr_name in fields:
            field_frame = tkb.Frame(form_frame)
            field_frame.pack(fill="x", pady=2, padx=5)
            tkb.Label(field_frame, text=label_text, width=15).pack(side="left")
            entry = tkb.Entry(field_frame)
            entry.pack(side="left", fill="x", expand=True, padx=5)
            setattr(self, attr_name, entry)

        # Combobox para Subcategoría
        field_frame = tkb.Frame(form_frame)
        field_frame.pack(fill="x", pady=2, padx=5)
        tkb.Label(field_frame, text="Subcategoría*:", width=15).pack(side="left")
        self.subcategoria_cb = ttk.Combobox(field_frame, state="readonly")
        self.subcategoria_cb.pack(side="left", fill="x", expand=True, padx=5)
        print("Llamando a load_subcategorias desde setup_gestion_tab")  # Debug
        self.load_subcategorias()  # Cargar subcategorías al iniciar

        # Combobox para Ubicación
        field_frame = tkb.Frame(form_frame)
        field_frame.pack(fill="x", pady=2, padx=5)
        tkb.Label(field_frame, text="Ubicación*:", width=15).pack(side="left")
        self.ubicacion_cb = ttk.Combobox(field_frame, state="readonly")
        self.ubicacion_cb.pack(side="left", fill="x", expand=True, padx=5)
        print("Llamando a load_ubicaciones desde setup_gestion_tab")  # Debug
        self.load_ubicaciones()  # Cargar ubicaciones al iniciar

        # Frame de botones
        btn_frame = tkb.Frame(form_frame)
        btn_frame.pack(fill="x", pady=10)
        tkb.Button(btn_frame, text="Agregar", bootstyle=SUCCESS, command=self.agregar_producto).pack(side="left",
                                                                                                     padx=5)
        self.btn_actualizar = tkb.Button(btn_frame, text="Actualizar", bootstyle=WARNING,
                                         command=self.actualizar_producto, state="disabled")
        self.btn_actualizar.pack(side="left", padx=5)
        self.btn_eliminar = tkb.Button(btn_frame, text="Eliminar", bootstyle=DANGER, command=self.eliminar_producto,
                                       state="disabled")
        self.btn_eliminar.pack(side="left", padx=5)
        tkb.Button(btn_frame, text="Limpiar", bootstyle=SECONDARY, command=self.limpiar_formulario).pack(side="right",
                                                                                                         padx=5)

        # Frame de la tabla
        table_frame = tkb.LabelFrame(main_frame, text="Lista de Productos", bootstyle="info")
        table_frame.pack(fill="both", expand=True, pady=5)

        # Configuración de la tabla
        columns = ("ID", "Nombre", "Descripción", "Subcategoría", "ID_Subcategoria", "Stock", "Precio", "Ubicación",
                   "ID_Ubicacion")
        self.product_table = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse",
                                          bootstyle="light")
        col_widths = [50, 150, 200, 100, 0, 60, 80, 100, 0]  # ID_Subcategoria y ID_Ubicacion ocultos (ancho 0)
        for idx, col in enumerate(columns):
            self.product_table.heading(col, text=col, anchor="center")
            self.product_table.column(col, width=col_widths[idx], anchor="center", stretch=False)

        # Scrollbars
        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.product_table.yview)
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=self.product_table.xview)
        self.product_table.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        # Diseño
        self.product_table.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # Evento de selección
        self.product_table.bind("<<TreeviewSelect>>", self.on_product_select)

        # Cargar datos iniciales
        print("Cargando productos desde setup_gestion_tab")  # Debug
        self.load_products()

    def load_subcategorias(self):
        """Carga las subcategorías en el Combobox"""
        print("Cargando subcategorías...")  # Debug
        subcategorias = self.controller.get_subcategorias()
        print(f"Subcategorías cargadas: {subcategorias}")
        if not subcategorias:
            print("No se encontraron subcategorías")
            self.subcategoria_ids = []
            self.subcategoria_cb["values"] = []
            messagebox.showerror("Error",
                                 "No se encontraron subcategorías en la base de datos. Por favor, agregue subcategorías antes de continuar.")
            raise RuntimeError("No se encontraron subcategorías en la base de datos")
        # Guardamos los IDs en una lista aparte
        self.subcategoria_ids = [subcat["id"] for subcat in subcategorias]
        # Mostramos los nombres en el Combobox
        self.subcategoria_cb["values"] = [subcat["nombre"] for subcat in subcategorias]
        print(f"IDs de subcategorías después de cargar: {self.subcategoria_ids}")  # Debug adicional

    def load_ubicaciones(self):
        """Carga las ubicaciones en el Combobox"""
        print("Cargando ubicaciones...")  # Debug
        ubicaciones = self.controller.get_ubicaciones()
        print(f"Ubicaciones cargadas: {ubicaciones}")
        if not ubicaciones:
            print("No se encontraron ubicaciones")
            self.ubicacion_ids = []
            self.ubicacion_cb["values"] = []
            messagebox.showerror("Error",
                                 "No se encontraron ubicaciones en la base de datos. Por favor, agregue ubicaciones antes de continuar.")
            raise RuntimeError("No se encontraron ubicaciones en la base de datos")
        # Guardamos los IDs en una lista aparte
        self.ubicacion_ids = [ubic["id"] for ubic in ubicaciones]
        # Mostramos las descripciones en el Combobox
        self.ubicacion_cb["values"] = [ubic["descripcion"] for ubic in ubicaciones]
        print(f"IDs de ubicaciones después de cargar: {self.ubicacion_ids}")  # Debug adicional

    def on_product_select(self, event):
        """Maneja la selección de un producto en la tabla"""
        try:
            selected = self.product_table.selection()
            if not selected:  # Si no hay selección, salir
                return

            item = self.product_table.item(selected[0])
            values = item.get('values', [])

            if not values or len(values) < 9:  # Validar que hay suficientes columnas
                print("Error: Datos del producto incompletos")
                return

            # Guardar el ID del producto seleccionado
            self.selected_product_id = values[0]
            print(f"Producto seleccionado - ID: {self.selected_product_id}")  # Debug

            # Depuración adicional: Mostrar el estado de las listas
            print(f"Estado de self.subcategoria_ids en on_product_select: {self.subcategoria_ids}")
            print(f"Estado de self.ubicacion_ids en on_product_select: {self.ubicacion_ids}")

            # Si las listas están vacías, intentar recargarlas
            if not self.subcategoria_ids:
                print("self.subcategoria_ids está vacía, intentando recargar...")
                self.load_subcategorias()
                if not self.subcategoria_ids:  # Verificar nuevamente después de recargar
                    messagebox.showerror("Error",
                                         "No hay subcategorías disponibles. Por favor, reinicie la aplicación.")
                    return

            if not self.ubicacion_ids:
                print("self.ubicacion_ids está vacía, intentando recargar...")
                self.load_ubicaciones()
                if not self.ubicacion_ids:  # Verificar nuevamente después de recargar
                    messagebox.showerror("Error", "No hay ubicaciones disponibles. Por favor, reinicie la aplicación.")
                    return

            # Actualizar campos del formulario
            self.id_entry.config(state="normal")
            self.id_entry.delete(0, "end")
            self.id_entry.insert(0, str(values[0]))
            self.id_entry.config(state="readonly")

            self.nombre_entry.delete(0, "end")
            self.nombre_entry.insert(0, values[1])

            self.descripcion_entry.delete(0, "end")
            self.descripcion_entry.insert(0, values[2] if values[2] else "")

            # Manejar la subcategoría (Combobox)
            if values[4]:  # ID_Subcategoria (columna oculta)
                try:
                    subcategoria_id = int(values[4])
                    print(
                        f"ID Subcategoría del producto: {subcategoria_id}, Subcategorías disponibles: {self.subcategoria_ids}")  # Debug
                    if subcategoria_id in self.subcategoria_ids:
                        idx = self.subcategoria_ids.index(subcategoria_id)
                        self.subcategoria_cb.current(idx)
                    else:
                        self.subcategoria_cb.set("")
                        messagebox.showwarning("Advertencia",
                                               f"La subcategoría con ID {subcategoria_id} no está disponible")
                except ValueError:
                    self.subcategoria_cb.set("")

            self.cantidad_entry.delete(0, "end")
            self.cantidad_entry.insert(0, values[5])

            self.precio_entry.delete(0, "end")
            precio = str(values[6]).replace("$", "").strip() if isinstance(values[6], str) else values[6]
            self.precio_entry.insert(0, precio)

            # Manejar la ubicación (Combobox) - Solo actualizar si está vacío
            if values[8] and not self.ubicacion_cb.get():  # ID_Ubicacion (columna oculta)
                try:
                    ubicacion_id = int(values[8])
                    print(
                        f"ID Ubicación del producto: {ubicacion_id}, Ubicaciones disponibles: {self.ubicacion_ids}")  # Debug
                    if ubicacion_id in self.ubicacion_ids:
                        idx = self.ubicacion_ids.index(ubicacion_id)
                        self.ubicacion_cb.current(idx)
                    else:
                        self.ubicacion_cb.set("")
                        messagebox.showwarning("Advertencia", f"La ubicación con ID {ubicacion_id} no está disponible")
                except ValueError:
                    self.ubicacion_cb.set("")

            # Habilitar botones de edición
            self.btn_actualizar.config(state="normal")
            self.btn_eliminar.config(state="normal")

        except Exception as e:
            print(f"Error en on_product_select: {str(e)}")
            messagebox.showerror("Error", f"No se pudo cargar el producto: {str(e)}")

    def limpiar_formulario(self):
        """Limpia el formulario y habilita el campo ID para nuevos registros"""
        for entry in [self.id_entry, self.nombre_entry, self.descripcion_entry,
                      self.cantidad_entry, self.precio_entry]:
            entry.delete(0, "end")
            entry.config(state="normal")  # Asegurar que el ID sea editable al limpiar

        self.subcategoria_cb.set("")  # Limpiar Combobox de subcategoría
        self.ubicacion_cb.set("")  # Limpiar Combobox de ubicación
        self.selected_product_id = None
        self.btn_actualizar.config(state="disabled")
        self.btn_eliminar.config(state="disabled")

    def load_products(self):
        # Limpiar tabla
        for item in self.product_table.get_children():
            self.product_table.delete(item)

        # Obtener productos del controlador
        products = self.controller.get_all_products()
        print(f"Productos cargados: {products}")  # Debug

        if not products:
            print("No se encontraron productos")
            return

        # Insertar productos en la tabla
        for product in products:
            self.product_table.insert("", "end", values=(
                product["id_producto"],
                product["nombre"],
                product.get("descripcion", ""),
                product.get("subcategoria", ""),  # Nombre de la subcategoría
                product.get("id_subcategoria", ""),  # ID de la subcategoría (oculto)
                product.get("stock", 0),
                f"${product.get('precio_unitario', 0):.2f}",
                product.get("ubicacion", ""),  # Descripción de la ubicación
                product.get("id_ubicacion", "")  # ID de la ubicación (oculto)
            ))

    def agregar_producto(self):
        """Agrega un nuevo producto al inventario"""
        # Validar campos obligatorios
        required_fields = [
            (self.nombre_entry, "Nombre"),
            (self.subcategoria_cb, "Subcategoría"),
            (self.cantidad_entry, "Cantidad"),
            (self.precio_entry, "Precio"),
            (self.ubicacion_cb, "Ubicación")
        ]
        for field, name in required_fields:
            if isinstance(field, ttk.Combobox):
                if field.current() == -1:
                    messagebox.showerror("Error", f"Seleccione una {name} válida")
                    return
            elif not field.get().strip():
                messagebox.showerror("Error", f"El campo {name} es obligatorio")
                return

        try:
            # Depuración: Mostrar el estado de las listas
            print(f"Estado de self.subcategoria_ids en agregar_producto: {self.subcategoria_ids}")
            print(f"Estado de self.ubicacion_ids en agregar_producto: {self.ubicacion_ids}")

            # Si las listas están vacías, intentar recargarlas
            if not self.subcategoria_ids:
                print("self.subcategoria_ids está vacía, intentando recargar...")
                self.load_subcategorias()
                if not self.subcategoria_ids:
                    messagebox.showerror("Error",
                                         "No hay subcategorías disponibles. Por favor, reinicie la aplicación.")
                    return

            if not self.ubicacion_ids:
                print("self.ubicacion_ids está vacía, intentando recargar...")
                self.load_ubicaciones()
                if not self.ubicacion_ids:
                    messagebox.showerror("Error", "No hay ubicaciones disponibles. Por favor, reinicie la aplicación.")
                    return

            # Obtener el ID de ubicación desde el Combobox
            ubicacion_idx = self.ubicacion_cb.current()
            if ubicacion_idx == -1:
                messagebox.showerror("Error", "Seleccione una ubicación válida")
                return
            print(f"Índice de ubicación seleccionado: {ubicacion_idx}, Ubicaciones disponibles: {self.ubicacion_ids}")
            if ubicacion_idx >= len(self.ubicacion_ids):
                messagebox.showerror("Error",
                                     f"Índice de ubicación {ubicacion_idx} fuera de rango. Ubicaciones disponibles: {self.ubicacion_ids}")
                return
            ubicacion_id = self.ubicacion_ids[ubicacion_idx]

            # Obtener el ID de subcategoría desde el Combobox
            subcategoria_idx = self.subcategoria_cb.current()
            if subcategoria_idx == -1:
                messagebox.showerror("Error", "Seleccione una subcategoría válida")
                return
            print(
                f"Índice de subcategoría seleccionado: {subcategoria_idx}, Subcategorías disponibles: {self.subcategoria_ids}")
            if subcategoria_idx >= len(self.subcategoria_ids):
                messagebox.showerror("Error",
                                     f"Índice de subcategoría {subcategoria_idx} fuera de rango. Subcategorías disponibles: {self.subcategoria_ids}")
                return
            subcategoria_id = self.subcategoria_ids[subcategoria_idx]

            # Obtener valores del formulario
            nombre = self.nombre_entry.get().strip()
            descripcion = self.descripcion_entry.get().strip() or None
            cantidad = int(self.cantidad_entry.get())
            precio = float(self.precio_entry.get())

            # Llamar al controlador para agregar el producto
            success, message = self.controller.agregar_producto(
                nombre=nombre,
                descripcion=descripcion,
                categoria=subcategoria_id,
                cantidad=cantidad,
                precio=precio,
                ubicacion=ubicacion_id,
                fecha=None
            )

            if success:
                messagebox.showinfo("Éxito", message)
                self.limpiar_formulario()
                self.load_products()
            else:
                messagebox.showerror("Error", message)

        except ValueError as e:
            messagebox.showerror("Error", f"Valores numéricos inválidos: {str(e)}")
        except Exception as e:
            print(f"Error al agregar producto: {str(e)}")
            messagebox.showerror("Error", f"Error al agregar: {str(e)}")

    def actualizar_producto(self):
        """Actualiza un producto existente usando el ID de ubicación del Combobox"""
        if not self.selected_product_id:
            messagebox.showerror("Error", "No hay producto seleccionado")
            return

        # Validar campos obligatorios
        required_fields = [
            (self.nombre_entry, "Nombre"),
            (self.subcategoria_cb, "Subcategoría"),
            (self.cantidad_entry, "Cantidad"),
            (self.precio_entry, "Precio"),
            (self.ubicacion_cb, "Ubicación")  # Validar Combobox
        ]
        for field, name in required_fields:
            if isinstance(field, ttk.Combobox):
                if field.current() == -1:
                    messagebox.showerror("Error", f"Seleccione una {name} válida")
                    return
            elif not field.get().strip():
                messagebox.showerror("Error", f"El campo {name} es obligatorio")
                return

        try:
            # Validar que las listas de IDs no estén vacías
            if not self.subcategoria_ids:
                messagebox.showerror("Error", "No hay subcategorías disponibles para seleccionar")
                return
            if not self.ubicacion_ids:
                messagebox.showerror("Error", "No hay ubicaciones disponibles para seleccionar")
                return

            # Obtener el ID de ubicación desde el Combobox
            ubicacion_idx = self.ubicacion_cb.current()
            if ubicacion_idx == -1:
                messagebox.showerror("Error", "Seleccione una ubicación válida")
                return
            print(
                f"Índice de ubicación seleccionado: {ubicacion_idx}, Ubicaciones disponibles: {self.ubicacion_ids}")  # Debug
            if ubicacion_idx >= len(self.ubicacion_ids):
                messagebox.showerror("Error",
                                     f"Índice de ubicación {ubicacion_idx} fuera de rango. Ubicaciones disponibles: {self.ubicacion_ids}")
                return
            ubicacion_id = self.ubicacion_ids[ubicacion_idx]

            # Obtener el ID de subcategoría desde el Combobox
            subcategoria_idx = self.subcategoria_cb.current()
            if subcategoria_idx == -1:
                messagebox.showerror("Error", "Seleccione una subcategoría válida")
                return
            print(
                f"Índice de subcategoría seleccionado: {subcategoria_idx}, Subcategorías disponibles: {self.subcategoria_ids}")  # Debug
            if subcategoria_idx >= len(self.subcategoria_ids):
                messagebox.showerror("Error",
                                     f"Índice de subcategoría {subcategoria_idx} fuera de rango. Subcategorías disponibles: {self.subcategoria_ids}")
                return
            subcategoria_id = self.subcategoria_ids[subcategoria_idx]

            # Validar valores numéricos
            nombre = self.nombre_entry.get().strip()
            descripcion = self.descripcion_entry.get().strip() or None
            cantidad = int(self.cantidad_entry.get())
            precio = float(self.precio_entry.get())

            # Llamar al controlador
            success, message = self.controller.actualizar_producto(
                producto_id=self.selected_product_id,
                nombre=nombre,
                descripcion=descripcion,
                categoria=subcategoria_id,
                cantidad=cantidad,
                precio=precio,
                ubicacion=ubicacion_id,  # Usa el ID, no la descripción
                fecha=None
            )

            if success:
                messagebox.showinfo("Éxito", message)
                self.limpiar_formulario()
                self.load_products()
            else:
                messagebox.showerror("Error", message)

        except ValueError as e:
            messagebox.showerror("Error", f"Valores numéricos inválidos: {str(e)}")
        except Exception as e:
            print(f"Error al actualizar producto: {str(e)}")
            messagebox.showerror("Error", f"Error al actualizar: {str(e)}")

    def eliminar_producto(self):
        """Elimina un producto existente"""
        if not self.selected_product_id:
            messagebox.showerror("Error", "No hay producto seleccionado")
            return

        confirmacion = messagebox.askyesno(
            "Confirmar",
            f"¿Eliminar el producto ID {self.selected_product_id}?"
        )

        if confirmacion:
            try:
                success, message = self.controller.eliminar_producto(self.selected_product_id)
                if success:
                    messagebox.showinfo("Éxito", message)
                    self.limpiar_formulario()
                    self.load_products()
                else:
                    messagebox.showerror("Error", message)
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar: {str(e)}")

    def setup_buscar_tab(self, tab):
        # Frame principal
        main_frame = tkb.Frame(tab)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame de búsqueda
        search_frame = tkb.LabelFrame(main_frame, text="Buscar Productos", bootstyle="info")
        search_frame.pack(fill="x", pady=5)

        # Campo de búsqueda
        search_field = tkb.Frame(search_frame)
        search_field.pack(fill="x", pady=5, padx=5)
        tkb.Label(search_field, text="Buscar:", width=8).pack(side="left")
        self.buscar_entry = tkb.Entry(search_field)
        self.buscar_entry.pack(side="left", fill="x", expand=True, padx=5)

        # Filtros de búsqueda
        filter_frame = tkb.Frame(search_frame)
        filter_frame.pack(fill="x", pady=5, padx=5)
        tkb.Label(filter_frame, text="Filtrar por:", width=8).pack(side="left")

        self.filtro_var = tkb.StringVar(value="Nombre")
        filters = [
            ("Nombre", "Nombre"),
            ("Subcategoría", "ID_Subcategoria"),
            ("Ubicación", "ID_Ubicacion")
        ]

        for text, value in filters:
            tkb.Radiobutton(
                filter_frame,
                text=text,
                variable=self.filtro_var,
                value=value,
                bootstyle="primary-toolbutton"
            ).pack(side="left", padx=5)

        # Botón de búsqueda
        btn_frame = tkb.Frame(search_frame)
        btn_frame.pack(fill="x", pady=5)
        tkb.Button(
            btn_frame,
            text="Buscar",
            bootstyle=INFO,
            command=self.buscar_productos
        ).pack(side="left", padx=5)

        # Frame para la tabla de resultados
        table_frame = tkb.LabelFrame(main_frame, text="Resultados", bootstyle="info")
        table_frame.pack(fill="both", expand=True, pady=5)

        # Configuración de la tabla
        columns = ("ID", "Nombre", "Subcategoría", "Stock", "Precio", "Ubicación")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        # Configurar columnas
        col_widths = [50, 150, 100, 60, 80, 100]
        for idx, col in enumerate(columns):
            self.tree.heading(col, text=col, anchor="center")
            self.tree.column(col, width=col_widths[idx], anchor="center", stretch=False)

        # Scrollbars
        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        # Diseño de la tabla y scrollbars
        self.tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")

        # Configurar el grid para expansión
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

    def buscar_productos(self):
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Obtener criterios de búsqueda
        filtro = self.filtro_var.get()
        valor = self.buscar_entry.get().strip()

        if not valor:
            messagebox.showwarning("Advertencia", "Por favor ingrese un valor para buscar")
            return

        # Realizar búsqueda
        resultados = self.controller.buscar_productos(filtro, valor)

        if not resultados:
            messagebox.showinfo("Información", "No se encontraron productos con los criterios especificados")
            return

        # Mostrar resultados
        for producto in resultados:
            self.tree.insert("", "end", values=(
                producto.get("id", ""),
                producto.get("nombre", ""),
                producto.get("subcategoria", "Sin subcategoría"),  # Usar get con valor por defecto
                producto.get("stock", 0),
                f"${producto.get('precio', 0):.2f}",
                producto.get("ubicacion", "Sin ubicación")
            ))

    def setup_estanteria_tab(self, tab):
        # Frame principal
        main_frame = tkb.Frame(tab)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame de búsqueda
        search_frame = tkb.LabelFrame(main_frame, text="Buscar por Ubicación", bootstyle="info")
        search_frame.pack(fill="x", pady=5)

        # Campo de búsqueda
        search_field = tkb.Frame(search_frame)
        search_field.pack(fill="x", pady=5, padx=5)
        tkb.Label(search_field, text="Ubicación (ID):", width=12).pack(side="left")
        self.estanteria_entry = tkb.Entry(search_field)
        self.estanteria_entry.pack(side="left", fill="x", expand=True, padx=5)

        # Botón de búsqueda
        btn_frame = tkb.Frame(search_frame)
        btn_frame.pack(fill="x", pady=5)
        tkb.Button(
            btn_frame,
            text="Buscar",
            bootstyle=INFO,
            command=self.buscar_por_estanteria
        ).pack(side="left", padx=5)

        # Frame para la tabla de resultados
        table_frame = tkb.LabelFrame(main_frame, text="Productos en Ubicación", bootstyle="info")
        table_frame.pack(fill="both", expand=True, pady=5)

        # Configuración de la tabla
        columns = ("ID", "Nombre", "Subcategoría", "Stock", "Ubicación")
        self.estanteria_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        # Configurar columnas
        col_widths = [50, 150, 100, 60, 100]
        for idx, col in enumerate(columns):
            self.estanteria_tree.heading(col, text=col, anchor="center")
            self.estanteria_tree.column(col, width=col_widths[idx], anchor="center", stretch=False)

        # Scrollbars
        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.estanteria_tree.yview)
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=self.estanteria_tree.xview)
        self.estanteria_tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        # Diseño de la tabla y scrollbars
        self.estanteria_tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")

        # Configurar el grid para expansión
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

    def buscar_por_estanteria(self):
        try:
            ubicacion = self.estanteria_entry.get().strip()

            if not ubicacion:
                messagebox.showwarning("Advertencia", "Por favor ingrese un ID de ubicación")
                return

            # Limpiar tabla
            for item in self.estanteria_tree.get_children():
                self.estanteria_tree.delete(item)

            resultados = self.controller.buscar_por_estanteria(ubicacion)

            if not resultados:
                messagebox.showinfo("Información", "No se encontraron productos en esta ubicación")
                return

            for producto in resultados:
                self.estanteria_tree.insert("", "end", values=(
                    producto.get("id", ""),
                    producto.get("nombre", ""),
                    producto.get("subcategoria", "Sin subcategoría"),  # Usar get con valor por defecto
                    producto.get("stock", 0),
                    producto.get("ubicacion", "Sin ubicación")
                ))
        except ValueError:
            messagebox.showerror("Error", "El ID de ubicación debe ser un número")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")

    def setup_compatibilidad_tab(self, tab):
        # Frame principal
        main_frame = tkb.Frame(tab)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame de búsqueda
        search_frame = tkb.LabelFrame(main_frame, text="Compatibilidad con Vehículos", bootstyle="info")
        search_frame.pack(fill="x", pady=5)

        # Campos de búsqueda
        fields = [
            ("Marca*:", "marca_entry"),
            ("Modelo*:", "modelo_entry"),
            ("Año*:", "ano_entry")
        ]

        for label_text, attr_name in fields:
            field_frame = tkb.Frame(search_frame)
            field_frame.pack(fill="x", pady=2, padx=5)
            tkb.Label(field_frame, text=label_text, width=10).pack(side="left")
            entry = tkb.Entry(field_frame)
            entry.pack(side="left", fill="x", expand=True, padx=5)
            setattr(self, attr_name, entry)

        # Botón de búsqueda
        btn_frame = tkb.Frame(search_frame)
        btn_frame.pack(fill="x", pady=5)
        tkb.Button(
            btn_frame,
            text="Buscar Birlos Compatibles",
            bootstyle=INFO,
            command=self.buscar_birlos_compatibles
        ).pack(side="left", padx=5)

        # Frame para la tabla de resultados
        table_frame = tkb.LabelFrame(main_frame, text="Birlos Compatibles", bootstyle="info")
        table_frame.pack(fill="both", expand=True, pady=5)

        # Configuración de la tabla
        columns = ("ID", "Nombre", "Medida", "Tipo Rosca", "Compatibilidad")
        self.compat_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        # Configurar columnas
        col_widths = [50, 150, 80, 100, 100]
        for idx, col in enumerate(columns):
            self.compat_tree.heading(col, text=col, anchor="center")
            self.compat_tree.column(col, width=col_widths[idx], anchor="center", stretch=False)

        # Scrollbars
        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.compat_tree.yview)
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=self.compat_tree.xview)
        self.compat_tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        # Diseño de la tabla y scrollbars
        self.compat_tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")

        # Configurar el grid para expansión
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

    def buscar_birlos_compatibles(self):
        # Limpiar tabla
        for item in self.compat_tree.get_children():
            self.compat_tree.delete(item)

        # Obtener criterios de búsqueda
        marca = self.marca_entry.get().strip()
        modelo = self.modelo_entry.get().strip()
        anio = self.ano_entry.get().strip()

        # Validar campos
        if not marca or not modelo or not anio:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
            return

        try:
            # Realizar búsqueda
            resultados = self.controller.buscar_birlos_compatibles(marca, modelo, int(anio))

            if not resultados:
                messagebox.showinfo("Información", "No se encontraron birlos compatibles")
                return

            # Mostrar resultados
            for birlo in resultados:
                self.compat_tree.insert("", "end", values=(
                    birlo["id"],
                    birlo["nombre"],
                    birlo["medida"],
                    birlo["tipo_rosca"],
                    birlo["compatibilidad"]
                ))
        except ValueError:
            messagebox.showerror("Error", "El año debe ser un número válido")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")
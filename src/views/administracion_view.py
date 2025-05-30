# src/views/administracion_view.py
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from src.controllers.clientes_controller import ClientesController
from src.controllers.empleados_controller import EmpleadosController
from src.controllers.proveedores_controller import ProveedoresController
from src.controllers.turnos_controller import TurnosController

class AdministracionView:
    def __init__(self, notebook):
        # Crear un frame contenedor que se añadirá al notebook principal
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Administración")

        # Crear un canvas y un scrollbar para que el contenido sea scrollable
        self.canvas = ttk.Canvas(self.frame)
        self.vscrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vscrollbar.set)
        self.vscrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Crear un frame interno que contendrá todo el contenido de administración
        self.inner_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Crear sub-notebook dentro del frame interno
        self.admin_notebook = ttk.Notebook(self.inner_frame, bootstyle="secondary")
        self.admin_notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Instanciar controladores
        self.clientes_controller = ClientesController()
        self.empleados_controller = EmpleadosController()
        self.proveedores_controller = ProveedoresController()
        self.turnos_controller = TurnosController()

        # Crear pestañas
        self._create_clientes_tab()
        self._create_empleados_tab()
        self._create_proveedores_tab()

    # ================= Pestaña Clientes =================
    def _create_clientes_tab(self):
        self.clientes_frame = ttk.Frame(self.admin_notebook)
        self.admin_notebook.add(self.clientes_frame, text="Clientes")

        form_frame = ttk.Frame(self.clientes_frame, padding=10)
        form_frame.pack(fill="x")

        ttk.Label(form_frame, text="ID Cliente:").grid(row=0, column=0, sticky="w", pady=5)
        self.cliente_id_entry = ttk.Entry(form_frame)
        self.cliente_id_entry.grid(row=0, column=1, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Nombre:").grid(row=1, column=0, sticky="w", pady=5)
        self.cliente_nombre_entry = ttk.Entry(form_frame)
        self.cliente_nombre_entry.grid(row=1, column=1, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Contacto:").grid(row=2, column=0, sticky="w", pady=5)
        self.cliente_contacto_entry = ttk.Entry(form_frame)
        self.cliente_contacto_entry.grid(row=2, column=1, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Dirección:").grid(row=3, column=0, sticky="w", pady=5)
        self.cliente_direccion_entry = ttk.Entry(form_frame)
        self.cliente_direccion_entry.grid(row=3, column=1, pady=5, sticky="ew")

        form_frame.columnconfigure(1, weight=1)

        button_frame = ttk.Frame(self.clientes_frame, padding=10)
        button_frame.pack(fill="x")
        ttk.Button(button_frame, text="Agregar Cliente", command=self.agregar_cliente, bootstyle="success").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Editar Cliente", command=self.editar_cliente, bootstyle="warning").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Eliminar Cliente", command=self.eliminar_cliente, bootstyle="danger").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Consultar Historial de Compras", command=self.consultar_historial_compras, bootstyle="info").pack(side="left", padx=5)

        table_frame = ttk.Frame(self.clientes_frame, padding=10)
        table_frame.pack(fill="both", expand=True)
        self.clientes_table = ttk.Treeview(table_frame, columns=("ID", "Nombre", "Contacto", "Dirección"), show="headings")
        for col in ("ID", "Nombre", "Contacto", "Dirección"):
            self.clientes_table.heading(col, text=col)
        self.clientes_table.pack(fill="both", expand=True)
        self.clientes_table.bind("<Double-1>", self.cargar_datos_cliente)

        # Nuevo frame para el historial de compras
        self.historial_clientes_frame = ttk.Frame(self.clientes_frame, padding=10)
        self.historial_clientes_frame.pack(fill="both", expand=True)
        ttk.Label(self.historial_clientes_frame, text="Historial de Compras", font=("Helvetica", 14)).pack(pady=5)
        self.historial_clientes_table = ttk.Treeview(self.historial_clientes_frame, columns=("Ticket ID", "Fecha", "Total"), show="headings")
        for col in ("Ticket ID", "Fecha", "Total"):
            self.historial_clientes_table.heading(col, text=col)
        self.historial_clientes_table.pack(fill="both", expand=True)

        self.actualizar_tabla_clientes()

    def agregar_cliente(self):
        nombre = self.cliente_nombre_entry.get()
        contacto = self.cliente_contacto_entry.get()
        direccion = self.cliente_direccion_entry.get()
        if not (nombre and direccion):
            Messagebox.show_error("Nombre y Dirección son obligatorios.", "Error")
            return
        cliente = self.clientes_controller.agregar_cliente(nombre, contacto, direccion)
        if cliente:
            Messagebox.show_info(f"Cliente {cliente.nombre} agregado.", "Éxito")
            self.actualizar_tabla_clientes()
            self.limpiar_campos_cliente()
        else:
            Messagebox.show_error("Error al agregar cliente.", "Error")

    def editar_cliente(self):
        id_cliente = self.cliente_id_entry.get()
        nombre = self.cliente_nombre_entry.get()
        contacto = self.cliente_contacto_entry.get()
        direccion = self.cliente_direccion_entry.get()
        if self.clientes_controller.editar_cliente(id_cliente, nombre, contacto, direccion):
            Messagebox.show_info("Cliente actualizado.", "Éxito")
            self.actualizar_tabla_clientes()
            self.limpiar_campos_cliente()
        else:
            Messagebox.show_error("Error al actualizar cliente.", "Error")

    def eliminar_cliente(self):
        selected = self.clientes_table.selection()
        if not selected:
            Messagebox.show_error("Seleccione un cliente para eliminar.", "Error")
            return
        id_cliente = self.clientes_table.item(selected[0], "values")[0]
        if self.clientes_controller.eliminar_cliente(id_cliente):
            Messagebox.show_info("Cliente eliminado.", "Éxito")
            self.actualizar_tabla_clientes()
            self.limpiar_campos_cliente()
        else:
            Messagebox.show_error("Error al eliminar cliente.", "Error")

    def cargar_datos_cliente(self, event):
        selected = self.clientes_table.focus()
        if selected:
            values = self.clientes_table.item(selected, "values")
            self.cliente_id_entry.delete(0, ttk.END)
            self.cliente_id_entry.insert(0, values[0])
            self.cliente_nombre_entry.delete(0, ttk.END)
            self.cliente_nombre_entry.insert(0, values[1])
            self.cliente_contacto_entry.delete(0, ttk.END)
            self.cliente_contacto_entry.insert(0, values[2])
            self.cliente_direccion_entry.delete(0, ttk.END)
            self.cliente_direccion_entry.insert(0, values[3])

    def actualizar_tabla_clientes(self):
        for row in self.clientes_table.get_children():
            self.clientes_table.delete(row)
        clientes = self.clientes_controller.obtener_clientes()
        for cliente in clientes:
            self.clientes_table.insert("", "end", values=(cliente.id_cliente, cliente.nombre, cliente.contacto, cliente.direccion))

    def limpiar_campos_cliente(self):
        self.cliente_id_entry.delete(0, ttk.END)
        self.cliente_nombre_entry.delete(0, ttk.END)
        self.cliente_contacto_entry.delete(0, ttk.END)
        self.cliente_direccion_entry.delete(0, ttk.END)

    def consultar_historial_compras(self):
        id_cliente = self.cliente_id_entry.get().strip()
        if not id_cliente:
            Messagebox.show_error("Ingrese un ID de cliente para consultar el historial.", "Error")
            return
        historial = self.clientes_controller.obtener_historial_compras(id_cliente)
        for row in self.historial_clientes_table.get_children():
            self.historial_clientes_table.delete(row)
        for item in historial:
            self.historial_clientes_table.insert("", "end", values=(item["id_ticket"], item["fecha_hora"], f"${item['total']:.2f}"))

# ================= Pestaña Empleados =================
    def _create_empleados_tab(self):
        self.empleados_frame = ttk.Frame(self.admin_notebook)
        self.admin_notebook.add(self.empleados_frame, text="Empleados")

        # Formulario para gestionar empleados
        form_frame = ttk.Frame(self.empleados_frame, padding=10)
        form_frame.pack(fill="x")

        ttk.Label(form_frame, text="ID Empleado:").grid(row=0, column=0, sticky="w", pady=5)
        self.empleado_id_entry = ttk.Entry(form_frame)
        self.empleado_id_entry.grid(row=0, column=1, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Nombre Completo:").grid(row=1, column=0, sticky="w", pady=5)
        self.empleado_nombre_completo_entry = ttk.Entry(form_frame)
        self.empleado_nombre_completo_entry.grid(row=1, column=1, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Cargo:").grid(row=2, column=0, sticky="w", pady=5)
        self.empleado_cargo_entry = ttk.Entry(form_frame)
        self.empleado_cargo_entry.grid(row=2, column=1, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Teléfono:").grid(row=3, column=0, sticky="w", pady=5)
        self.empleado_telefono_entry = ttk.Entry(form_frame)
        self.empleado_telefono_entry.grid(row=3, column=1, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Correo:").grid(row=4, column=0, sticky="w", pady=5)
        self.empleado_correo_entry = ttk.Entry(form_frame)
        self.empleado_correo_entry.grid(row=4, column=1, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Contraseña:").grid(row=5, column=0, sticky="w", pady=5)
        self.empleado_contrasena_entry = ttk.Entry(form_frame, show="*")
        self.empleado_contrasena_entry.grid(row=5, column=1, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Fecha Ingreso:").grid(row=6, column=0, sticky="w", pady=5)
        self.empleado_fecha_entry = ttk.Entry(form_frame)
        self.empleado_fecha_entry.grid(row=6, column=1, pady=5, sticky="ew")

        form_frame.columnconfigure(1, weight=1)

        button_frame = ttk.Frame(self.empleados_frame, padding=10)
        button_frame.pack(fill="x")
        ttk.Button(button_frame, text="Agregar Empleado", command=self.agregar_empleado, bootstyle="success").pack(
            side="left", padx=5)
        ttk.Button(button_frame, text="Editar Empleado", command=self.editar_empleado, bootstyle="warning").pack(
            side="left", padx=5)
        ttk.Button(button_frame, text="Eliminar Empleado", command=self.eliminar_empleado, bootstyle="danger").pack(
            side="left", padx=5)
        ttk.Button(button_frame, text="Consultar Historial de Ventas", command=self.consultar_historial_ventas,
                   bootstyle="info").pack(side="left", padx=5)
        # Nuevo botón para consultar historial de turnos
        ttk.Button(button_frame, text="Consultar Historial de Turnos", command=self.consultar_historial_turnos,
                   bootstyle="info").pack(side="left", padx=5)

        table_frame = ttk.Frame(self.empleados_frame, padding=10)
        table_frame.pack(fill="both", expand=True)
        self.empleados_table = ttk.Treeview(table_frame, columns=(
        "ID", "Nombre Completo", "Cargo", "Teléfono", "Correo", "Fecha Ingreso"), show="headings")
        for col in ("ID", "Nombre Completo", "Cargo", "Teléfono", "Correo", "Fecha Ingreso"):
            self.empleados_table.heading(col, text=col)
        self.empleados_table.pack(fill="both", expand=True)
        self.empleados_table.bind("<Double-1>", self.cargar_datos_empleado)

        # Nuevo frame para historial de ventas
        self.historial_empleados_frame = ttk.Frame(self.empleados_frame, padding=10)
        self.historial_empleados_frame.pack(fill="both", expand=True)
        ttk.Label(self.historial_empleados_frame, text="Historial de Ventas", font=("Helvetica", 14)).pack(pady=5)
        self.historial_empleados_table = ttk.Treeview(self.historial_empleados_frame,
                                                      columns=("Ticket ID", "Fecha", "Total"), show="headings")
        for col in ("Ticket ID", "Fecha", "Total"):
            self.historial_empleados_table.heading(col, text=col)
        self.historial_empleados_table.pack(fill="both", expand=True)

        # Nuevo frame para historial de turnos
        self.turnos_empleados_frame = ttk.Frame(self.empleados_frame, padding=10)
        self.turnos_empleados_frame.pack(fill="both", expand=True)
        ttk.Label(self.turnos_empleados_frame, text="Historial de Turnos", font=("Helvetica", 14)).pack(pady=5)
        self.turnos_empleados_table = ttk.Treeview(self.turnos_empleados_frame,
                                                   columns=(
                                                   "ID Empleado", "Nombre", "Fecha", "Hora Entrada", "Hora Salida"),
                                                   show="headings")
        for col in ("ID Empleado", "Nombre", "Fecha", "Hora Entrada", "Hora Salida"):
            self.turnos_empleados_table.heading(col, text=col)
        self.turnos_empleados_table.pack(fill="both", expand=True)

        self.actualizar_tabla_empleados()

    def agregar_empleado(self):
        nombre_completo = self.empleado_nombre_completo_entry.get()
        cargo = self.empleado_cargo_entry.get()
        telefono = self.empleado_telefono_entry.get()
        correo = self.empleado_correo_entry.get()
        contrasena = self.empleado_contrasena_entry.get()
        fecha_ingreso = self.empleado_fecha_entry.get()
        if not nombre_completo or not contrasena:
            Messagebox.show_error("Los campos Nombre Completo y Contraseña son obligatorios.", "Error")
            return
        empleado = self.empleados_controller.agregar_empleado(nombre_completo, cargo, telefono, correo, fecha_ingreso,
                                                              contrasena)
        if empleado:
            Messagebox.show_info(f"Empleado {empleado.nombre_completo} agregado.", "Éxito")
            self.actualizar_tabla_empleados()
            self.limpiar_campos_empleado()
        else:
            Messagebox.show_error("Error al agregar empleado.", "Error")

    def editar_empleado(self):
        id_empleado = self.empleado_id_entry.get()
        nombre_completo = self.empleado_nombre_completo_entry.get()
        cargo = self.empleado_cargo_entry.get()
        telefono = self.empleado_telefono_entry.get()
        correo = self.empleado_correo_entry.get()
        contrasena = self.empleado_contrasena_entry.get()
        fecha_ingreso = self.empleado_fecha_entry.get()
        if self.empleados_controller.editar_empleado(id_empleado, nombre_completo, cargo, telefono, correo,
                                                     fecha_ingreso, contrasena if contrasena.strip() else None):
            Messagebox.show_info("Empleado actualizado.", "Éxito")
            self.actualizar_tabla_empleados()
            self.limpiar_campos_empleado()
        else:
            Messagebox.show_error("Error al actualizar empleado.", "Error")

    def eliminar_empleado(self):
        selected = self.empleados_table.selection()
        if not selected:
            Messagebox.show_error("Seleccione un empleado para eliminar.", "Error")
            return
        id_empleado = self.empleados_table.item(selected[0], "values")[0]
        if self.empleados_controller.eliminar_empleado(id_empleado):
            Messagebox.show_info("Empleado eliminado.", "Éxito")
            self.actualizar_tabla_empleados()
            self.limpiar_campos_empleado()
        else:
            Messagebox.show_error("Error al eliminar empleado.", "Error")

    def cargar_datos_empleado(self, event):
        selected = self.empleados_table.focus()
        if selected:
            values = self.empleados_table.item(selected, "values")
            self.empleado_id_entry.delete(0, ttk.END)
            self.empleado_id_entry.insert(0, values[0])
            self.empleado_nombre_completo_entry.delete(0, ttk.END)
            self.empleado_nombre_completo_entry.insert(0, values[1])
            self.empleado_cargo_entry.delete(0, ttk.END)
            self.empleado_cargo_entry.insert(0, values[2])
            self.empleado_telefono_entry.delete(0, ttk.END)
            self.empleado_telefono_entry.insert(0, values[3])
            self.empleado_correo_entry.delete(0, ttk.END)
            self.empleado_correo_entry.insert(0, values[4])
            self.empleado_fecha_entry.delete(0, ttk.END)
            self.empleado_fecha_entry.insert(0, values[5])
            self.empleado_contrasena_entry.delete(0, ttk.END)

    def consultar_historial_ventas(self):
        id_empleado = self.empleado_id_entry.get().strip()
        if not id_empleado:
            Messagebox.show_error("Ingrese un ID de empleado para consultar el historial de ventas.", "Error")
            return
        historial = self.empleados_controller.obtener_historial_ventas(id_empleado)
        for row in self.historial_empleados_table.get_children():
            self.historial_empleados_table.delete(row)
        for item in historial:
            self.historial_empleados_table.insert("", "end", values=(
            item["id_ticket"], item["fecha_hora"], f"${item['total']:.2f}"))

    def consultar_historial_turnos(self):
        id_empleado = self.empleado_id_entry.get().strip()
        if not id_empleado:
            Messagebox.show_error("Ingrese un ID de empleado para consultar el historial de turnos.", "Error")
            return
        # Usar el controlador de turnos para obtener el historial
        historial = self.turnos_controller.obtener_turnos(id_empleado)
        for row in self.turnos_empleados_table.get_children():
            self.turnos_empleados_table.delete(row)
        for item in historial:
            self.turnos_empleados_table.insert("", "end",
                                               values=(item["id_empleado"], item["nombre"],
                                                       item["fecha"], item["hora_entrada"], item["hora_salida"]))

    def actualizar_tabla_empleados(self):
        for row in self.empleados_table.get_children():
            self.empleados_table.delete(row)
        empleados = self.empleados_controller.obtener_empleados()
        for emp in empleados:
            self.empleados_table.insert("", "end", values=(
            emp.id_empleado, emp.nombre_completo, emp.cargo, emp.telefono, emp.correo, emp.fecha_ingreso))

    def limpiar_campos_empleado(self):
        self.empleado_id_entry.delete(0, ttk.END)
        self.empleado_nombre_completo_entry.delete(0, ttk.END)
        self.empleado_cargo_entry.delete(0, ttk.END)
        self.empleado_telefono_entry.delete(0, ttk.END)
        self.empleado_correo_entry.delete(0, ttk.END)
        self.empleado_fecha_entry.delete(0, ttk.END)
        self.empleado_contrasena_entry.delete(0, ttk.END)

# ================= Pestaña Proveedores (no se modificó) =================
    def _create_proveedores_tab(self):
        self.proveedores_frame = ttk.Frame(self.admin_notebook)
        self.admin_notebook.add(self.proveedores_frame, text="Proveedores")

        form_frame = ttk.Frame(self.proveedores_frame, padding=10)
        form_frame.pack(fill="x")

        ttk.Label(form_frame, text="ID Proveedor:").grid(row=0, column=0, sticky="w", pady=5)
        self.proveedor_id_entry = ttk.Entry(form_frame)
        self.proveedor_id_entry.grid(row=0, column=1, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Nombre:").grid(row=1, column=0, sticky="w", pady=5)
        self.proveedor_nombre_entry = ttk.Entry(form_frame)
        self.proveedor_nombre_entry.grid(row=1, column=1, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Contacto:").grid(row=2, column=0, sticky="w", pady=5)
        self.proveedor_contacto_entry = ttk.Entry(form_frame)
        self.proveedor_contacto_entry.grid(row=2, column=1, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Teléfono:").grid(row=3, column=0, sticky="w", pady=5)
        self.proveedor_telefono_entry = ttk.Entry(form_frame)
        self.proveedor_telefono_entry.grid(row=3, column=1, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Email:").grid(row=4, column=0, sticky="w", pady=5)
        self.proveedor_email_entry = ttk.Entry(form_frame)
        self.proveedor_email_entry.grid(row=4, column=1, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Dirección:").grid(row=5, column=0, sticky="w", pady=5)
        self.proveedor_direccion_entry = ttk.Entry(form_frame)
        self.proveedor_direccion_entry.grid(row=5, column=1, pady=5, sticky="ew")

        form_frame.columnconfigure(1, weight=1)

        button_frame = ttk.Frame(self.proveedores_frame, padding=10)
        button_frame.pack(fill="x")
        ttk.Button(button_frame, text="Agregar Proveedor", command=self.agregar_proveedor, bootstyle="success").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Editar Proveedor", command=self.editar_proveedor, bootstyle="warning").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Eliminar Proveedor", command=self.eliminar_proveedor, bootstyle="danger").pack(side="left", padx=5)

        table_frame = ttk.Frame(self.proveedores_frame, padding=10)
        table_frame.pack(fill="both", expand=True)
        self.proveedores_table = ttk.Treeview(table_frame, columns=("ID", "Nombre", "Contacto", "Teléfono", "Email", "Dirección"), show="headings")
        for col in ("ID", "Nombre", "Contacto", "Teléfono", "Email", "Dirección"):
            self.proveedores_table.heading(col, text=col)
        self.proveedores_table.pack(fill="both", expand=True)
        self.proveedores_table.bind("<Double-1>", self.cargar_datos_proveedor)

        self.actualizar_tabla_proveedores()

    def agregar_proveedor(self):
        nombre = self.proveedor_nombre_entry.get()
        contacto = self.proveedor_contacto_entry.get()
        telefono = self.proveedor_telefono_entry.get()
        email = self.proveedor_email_entry.get()
        direccion = self.proveedor_direccion_entry.get()
        if not (nombre and direccion):
            Messagebox.show_error("Nombre y Dirección son obligatorios.", "Error")
            return
        proveedor = self.proveedores_controller.agregar_proveedor(nombre, contacto, telefono, email, direccion)
        if proveedor:
            Messagebox.show_info(f"Proveedor {proveedor.nombre} agregado.", "Éxito")
            self.actualizar_tabla_proveedores()
            self.limpiar_campos_proveedor()
        else:
            Messagebox.show_error("Error al agregar proveedor.", "Error")

    def editar_proveedor(self):
        id_proveedor = self.proveedor_id_entry.get()
        nombre = self.proveedor_nombre_entry.get()
        contacto = self.proveedor_contacto_entry.get()
        telefono = self.proveedor_telefono_entry.get()
        email = self.proveedor_email_entry.get()
        direccion = self.proveedor_direccion_entry.get()
        if self.proveedores_controller.editar_proveedor(id_proveedor, nombre, contacto, telefono, email, direccion):
            Messagebox.show_info("Proveedor actualizado.", "Éxito")
            self.actualizar_tabla_proveedores()
            self.limpiar_campos_proveedor()
        else:
            Messagebox.show_error("Error al actualizar proveedor.", "Error")

    def eliminar_proveedor(self):
        selected = self.proveedores_table.selection()
        if not selected:
            Messagebox.show_error("Seleccione un proveedor para eliminar.", "Error")
            return
        id_proveedor = self.proveedores_table.item(selected[0], "values")[0]
        if self.proveedores_controller.eliminar_proveedor(id_proveedor):
            Messagebox.show_info("Proveedor eliminado.", "Éxito")
            self.actualizar_tabla_proveedores()
            self.limpiar_campos_proveedor()
        else:
            Messagebox.show_error("Error al eliminar proveedor.", "Error")

    def cargar_datos_proveedor(self, event):
        selected = self.proveedores_table.focus()
        if selected:
            values = self.proveedores_table.item(selected, "values")
            self.proveedor_id_entry.delete(0, ttk.END)
            self.proveedor_id_entry.insert(0, values[0])
            self.proveedor_nombre_entry.delete(0, ttk.END)
            self.proveedor_nombre_entry.insert(0, values[1])
            self.proveedor_contacto_entry.delete(0, ttk.END)
            self.proveedor_contacto_entry.insert(0, values[2])
            self.proveedor_telefono_entry.delete(0, ttk.END)
            self.proveedor_telefono_entry.insert(0, values[3])
            self.proveedor_email_entry.delete(0, ttk.END)
            self.proveedor_email_entry.insert(0, values[4])
            self.proveedor_direccion_entry.delete(0, ttk.END)
            self.proveedor_direccion_entry.insert(0, values[5])

    def actualizar_tabla_proveedores(self):
        for row in self.proveedores_table.get_children():
            self.proveedores_table.delete(row)
        proveedores = self.proveedores_controller.obtener_proveedores()
        for prov in proveedores:
            self.proveedores_table.insert("", "end", values=(prov.id_proveedor, prov.nombre, prov.contacto, prov.telefono, prov.email, prov.direccion))

    def limpiar_campos_proveedor(self):
        self.proveedor_id_entry.delete(0, ttk.END)
        self.proveedor_nombre_entry.delete(0, ttk.END)
        self.proveedor_contacto_entry.delete(0, ttk.END)
        self.proveedor_telefono_entry.delete(0, ttk.END)
        self.proveedor_email_entry.delete(0, ttk.END)
        self.proveedor_direccion_entry.delete(0, ttk.END)

#esto es para cerrar pestanas

    def close(self):
        self.clientes_controller.close()
        self.empleados_controller.close()
        self.proveedores_controller.close()

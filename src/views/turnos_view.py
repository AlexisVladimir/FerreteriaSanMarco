# src/views/turnos_view.py
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from datetime import datetime
from src.controllers.turnos_controller import TurnosController

class TurnosView:
    def __init__(self, parent):
        self.controller = TurnosController()
        self.frame = ttk.Frame(parent)
        self.frame.pack(expand=True, fill="both")
        self.build_ui()
        self.update_clock()

    def build_ui(self):
        # Reloj en tiempo real
        self.clock_label = ttk.Label(self.frame, text="", font=("Helvetica", 16))
        self.clock_label.pack(pady=10)

        # Campo para ID del empleado
        form_frame = ttk.Frame(self.frame, padding=10)
        form_frame.pack(fill="x")
        ttk.Label(form_frame, text="ID Empleado:").grid(row=0, column=0, sticky="w", pady=5)
        self.id_empleado_entry = ttk.Entry(form_frame)
        self.id_empleado_entry.grid(row=0, column=1, sticky="ew", pady=5)
        form_frame.columnconfigure(1, weight=1)

        # Botones para iniciar y finalizar turno
        button_frame = ttk.Frame(self.frame, padding=10)
        button_frame.pack(fill="x")
        ttk.Button(button_frame, text="Iniciar Turno", command=self.iniciar_turno, bootstyle="success").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Finalizar Turno", command=self.finalizar_turno, bootstyle="danger").pack(side="left", padx=5)

    def update_clock(self):
        now = datetime.now().strftime("%H:%M:%S")
        self.clock_label.config(text=now)
        self.clock_label.after(1000, self.update_clock)

    def iniciar_turno(self):
        id_empleado = self.id_empleado_entry.get().strip()
        if not id_empleado:
            Messagebox.show_error("Ingrese el ID del empleado.", "Error")
            return
        try:
            result = self.controller.iniciar_turno(id_empleado)
            Messagebox.show_info(f"Turno iniciado a las {result['hora_entrada']} del {result['fecha']}.", "Éxito")
        except Exception as e:
            Messagebox.show_error(str(e), "Error")

    def finalizar_turno(self):
        id_empleado = self.id_empleado_entry.get().strip()
        if not id_empleado:
            Messagebox.show_error("Ingrese el ID del empleado.", "Error")
            return
        try:
            result = self.controller.finalizar_turno(id_empleado)
            Messagebox.show_info(f"Turno finalizado a las {result['hora_salida']} del {result['fecha']}.", "Éxito")
        except Exception as e:
            Messagebox.show_error(str(e), "Error")

    def close(self):
        self.controller.close()

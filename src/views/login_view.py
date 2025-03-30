# src/views/login_view.py
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from src.controllers.login_controller import LoginController

class LoginView:
    def __init__(self, parent, on_success=None):
        self.controller = LoginController()
        self.on_success = on_success
        self.frame = ttk.Frame(parent)
        self.build_ui()
        self.frame.pack(expand=True, fill="both")

    def build_ui(self):
        ttk.Label(self.frame, text="Iniciar Sesión", font=("Helvetica", 16)).pack(pady=20)

        form_frame = ttk.Frame(self.frame, padding=10)
        form_frame.pack(fill="x")

        ttk.Label(form_frame, text="Correo:").grid(row=0, column=0, sticky="w", pady=5)
        self.correo_entry = ttk.Entry(form_frame)
        self.correo_entry.grid(row=0, column=1, sticky="ew", pady=5)

        ttk.Label(form_frame, text="Contraseña:").grid(row=1, column=0, sticky="w", pady=5)
        self.contrasena_entry = ttk.Entry(form_frame, show="*")
        self.contrasena_entry.grid(row=1, column=1, sticky="ew", pady=5)

        form_frame.columnconfigure(1, weight=1)

        ttk.Button(self.frame, text="Iniciar Sesión", command=self.login, bootstyle="primary").pack(pady=10)

    def login(self):
        correo = self.correo_entry.get().strip()
        contrasena = self.contrasena_entry.get().strip()
        if not correo or not contrasena:
            Messagebox.show_error("Debe ingresar correo y contraseña.", "Error")
            return

        user = self.controller.login(correo, contrasena)
        if user:
            Messagebox.show_info(f"Bienvenido, {user['nombre_completo']}!", "Éxito")
            if self.on_success:
                self.on_success(user)
        else:
            Messagebox.show_error("Correo o contraseña incorrectos.", "Error")

    def close(self):
        self.controller.close()

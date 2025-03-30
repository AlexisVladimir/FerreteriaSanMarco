# src/controllers/login_controller.py
import bcrypt
from src.utils.db_helper import DatabaseHelper

class LoginController:
    def __init__(self):
        self.db = DatabaseHelper()

    def login(self, correo, contrasena_input):
        query = "SELECT ID_Empleado, Nombre_Completo, Cargo, Contrasena, ID_Rol FROM Empleado WHERE Correo = %s"
        result = self.db.fetch_query(query, (correo,))
        if result:
            id_empleado, nombre_completo, cargo, contrasena_hash, id_rol = result[0]
            # Verifica la contraseña usando bcrypt
            if bcrypt.checkpw(contrasena_input.encode('utf-8'), contrasena_hash.encode('utf-8')):
                return {
                    "id_empleado": id_empleado,
                    "nombre_completo": nombre_completo,
                    "cargo": cargo,
                    "id_rol": id_rol
                }
        return None

    def close(self):
        self.db.close()

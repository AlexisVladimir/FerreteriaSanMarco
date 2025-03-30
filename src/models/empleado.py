# src/models/empleado.py
class Empleado:
    def __init__(self, id_empleado, nombre_completo, cargo, telefono, correo, fecha_ingreso, contrasena):
        self.id_empleado = id_empleado
        self.nombre_completo = nombre_completo
        self.cargo = cargo
        self.telefono = telefono
        self.correo = correo
        self.fecha_ingreso = fecha_ingreso
        self.contrasena = contrasena

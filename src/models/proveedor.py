# src/models/proveedor.py
class Proveedor:
    def __init__(self, id_proveedor, nombre, contacto, telefono, email, direccion, sitio_web, notas):
        self.id_proveedor = id_proveedor
        self.nombre = nombre
        self.contacto = contacto
        self.telefono = telefono
        self.email = email
        self.direccion = direccion
        self.sitio_web = sitio_web
        self.notas = notas

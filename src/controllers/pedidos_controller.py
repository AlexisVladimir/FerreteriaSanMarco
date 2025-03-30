# Dentro de src/controllers/pedidos_controller.py
from datetime import datetime
from src.utils.db_helper import DatabaseHelper

class PedidosController:
    def __init__(self):
        self.db = DatabaseHelper()

    def registrar_pedido(self, id_proveedor, pedido_items):
        try:
            pedido_query = """
                INSERT INTO Pedido_Proveedor (ID_Proveedor, Fecha_Solicitud, Estado)
                VALUES (%s, %s, %s)
            """
            fecha_solicitud = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            estado = "pendiente"
            pedido_params = (id_proveedor, fecha_solicitud, estado)
            self.db.execute_query(pedido_query, pedido_params)
            pedido_id_query = "SELECT LAST_INSERT_ID()"
            pedido_id_result = self.db.fetch_query(pedido_id_query)
            id_pedido = pedido_id_result[0][0]
            for item in pedido_items:
                id_producto = item["id_producto"]
                cantidad = item["cantidad"]
                precio_compra = item.get("precio_compra", 0.0)
                detalle_query = """
                    INSERT INTO Detalle_Pedido (ID_Pedido, ID_Producto, Cantidad, Precio_Compra)
                    VALUES (%s, %s, %s, %s)
                """
                detalle_params = (id_pedido, id_producto, cantidad, precio_compra)
                self.db.execute_query(detalle_query, detalle_params)
            return {"id_pedido": id_pedido, "estado": estado, "fecha_solicitud": fecha_solicitud}
        except Exception as e:
            raise Exception(f"Error al registrar el pedido: {str(e)}")

    def close(self):
        self.db.close()

# Función de nivel módulo que usa la clase
def registrar_pedido(id_proveedor, pedido_items):
    controller = PedidosController()
    resultado = controller.registrar_pedido(id_proveedor, pedido_items)
    controller.close()
    return resultado

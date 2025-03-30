# src/controllers/ventas_controller.py
from datetime import datetime
from src.utils.db_helper import DatabaseHelper
from src.utils.report_generator import ReportGenerator

class VentasController:
    def __init__(self):
        self.db = DatabaseHelper()
        self.report_generator = ReportGenerator()

    def registrar_venta(self, id_cliente, id_empleado, sale_items):
        try:
            print(f"Iniciando registro de venta: ID_Cliente={id_cliente}, ID_Empleado={id_empleado}, Items={sale_items}")

            # Validar que el cliente y el empleado existan
            cliente_query = "SELECT ID_Cliente FROM Cliente WHERE ID_Cliente = %s"
            cliente_result = self.db.fetch_query(cliente_query, (id_cliente,))
            if not cliente_result:
                raise Exception(f"El cliente con ID {id_cliente} no existe.")
            print(f"Cliente {id_cliente} validado.")

            empleado_query = "SELECT ID_Empleado FROM Empleado WHERE ID_Empleado = %s"
            empleado_result = self.db.fetch_query(empleado_query, (id_empleado,))
            if not empleado_result:
                raise Exception(f"El empleado con ID {id_empleado} no existe.")
            print(f"Empleado {id_empleado} validado.")

            # Calcular el total
            total = sum(item["cantidad"] * 10.0 for item in sale_items)
            print(f"Total calculado: {total}")

            # Iniciar una transacción
            self.db.connection.start_transaction()
            print("Transacción iniciada.")

            # Insertar el ticket
            ticket_query = """
                INSERT INTO Ticket (Fecha_Hora, ID_Empleado, ID_Cliente, Total)
                VALUES (%s, %s, %s, %s)
            """
            fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ticket_params = (fecha_hora, id_empleado, id_cliente, total)
            self.db.execute_query(ticket_query, ticket_params)
            print("Ticket insertado.")

            # Obtener el ID del ticket
            ticket_id_query = "SELECT LAST_INSERT_ID()"
            ticket_id_result = self.db.fetch_query(ticket_id_query)
            id_ticket = ticket_id_result[0][0]
            print(f"Ticket insertado con ID: {id_ticket}")

            # Insertar los detalles del ticket
            for item in sale_items:
                id_producto = item["id_producto"]
                cantidad = item["cantidad"]
                precio_unitario = 10.0
                subtotal = cantidad * precio_unitario

                # Validar que el producto exista y tenga suficiente stock
                producto_query = "SELECT Stock FROM Producto WHERE ID_Producto = %s"
                producto_result = self.db.fetch_query(producto_query, (id_producto,))
                if not producto_result:
                    raise Exception(f"El producto con ID {id_producto} no existe.")
                stock_actual = producto_result[0][0]
                print(f"Producto {id_producto} encontrado con stock: {stock_actual}")
                if stock_actual < cantidad:
                    raise Exception(f"No hay suficiente stock para el producto con ID {id_producto}. Stock actual: {stock_actual}")

                detalle_query = """
                    INSERT INTO Detalle_Ticket (ID_Ticket, ID_Producto, Cantidad, Precio_Unitario, Subtotal)
                    VALUES (%s, %s, %s, %s, %s)
                """
                detalle_params = (id_ticket, id_producto, cantidad, precio_unitario, subtotal)
                self.db.execute_query(detalle_query, detalle_params)
                print(f"Detalle insertado para producto {id_producto}")

                # Actualizar el stock
                stock_query = "UPDATE Producto SET Stock = Stock - %s WHERE ID_Producto = %s"
                stock_params = (cantidad, id_producto)
                self.db.execute_query(stock_query, stock_params)
                print(f"Stock actualizado para producto {id_producto}")

            # Generar el PDF del ticket
            ticket_data = {
                "id_ticket": id_ticket,
                "fecha_hora": fecha_hora,
                "id_empleado": id_empleado,
                "id_cliente": id_cliente,
                "total": total
            }
            pdf_path = self.report_generator.generate_ticket_pdf(ticket_data, sale_items)
            print(f"Ticket PDF generado en: {pdf_path}")

            # Confirmar la transacción
            self.db.connection.commit()
            print("Transacción confirmada.")

            return {"id_ticket": id_ticket, "total": total, "pdf_path": pdf_path}
        except Exception as e:
            # Revertir la transacción en caso de error
            self.db.connection.rollback()
            print(f"Transacción revertida debido a un error: {str(e)}")
            # Asegurarnos de que el mensaje de error sea claro
            error_message = f"Error al registrar la venta: {str(e)}"
            raise Exception(error_message)

    def close(self):
        self.db.close()
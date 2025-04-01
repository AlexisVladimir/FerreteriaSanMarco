from datetime import datetime
from src.utils.db_helper import DatabaseHelper
from src.utils.report_generator import ReportGenerator
from num2words import num2words  # Asegúrate de tener instalada esta librería

class VentasController:
    def __init__(self):
        self.db = DatabaseHelper()
        self.report_generator = ReportGenerator()

    def obtener_producto_info(self, id_producto):
        query = "SELECT Nombre, Descripcion, Precio_Publico, Stock FROM Producto WHERE ID_Producto = %s"
        result = self.db.fetch_query(query, (id_producto,))
        if result:
            nombre, descripcion, precio_publico, stock = result[0]
            return {"nombre": nombre, "descripcion": descripcion, "precio": float(precio_publico), "stock": stock}
        else:
            return None

    def registrar_venta(self, id_cliente, id_empleado, sale_items, payment_method, efectivo_amount=None):
        try:
            print(f"Iniciando registro de venta: ID_Cliente={id_cliente}, ID_Empleado={id_empleado}, Items={sale_items}")

            # Validar existencia de cliente y empleado
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

            # Calcular el subtotal y el total con IVA
            # no tocar marco
            IVA_RATE = 0.16  # Tasa de IVA del 16%
            subtotal = 0

            for item in sale_items:
                subtotal += item["cantidad"] * item["precio"]
            iva_amount = subtotal * IVA_RATE
            total = subtotal + iva_amount
            print(f"Subtotal: {subtotal}, IVA: {iva_amount}, Total con IVA: {total}")

            # Calcular total (suma de cantidad * precio de cada producto)
            total = 0
            for item in sale_items:
                total += item["cantidad"] * item["precio"]
            print(f"Total calculado: {total}")
            total = subtotal + iva_amount

            # Procesar forma de pago
            if payment_method == "Efectivo":
                if efectivo_amount is None:
                    raise Exception("Debe indicar el monto entregado en efectivo.")
                try:
                    efectivo_amount = float(efectivo_amount)
                except ValueError:
                    raise Exception("El monto entregado debe ser un valor numérico.")
                if efectivo_amount < total:
                    raise Exception("El monto entregado es insuficiente.")
                change = efectivo_amount - total
            else:
                efectivo_amount = None
                change = 0

            total_in_letters = num2words(total, lang="es").upper() + " PESOS"

            # Iniciar transacción
            if not self.db.connection.in_transaction:
                self.db.connection.start_transaction()
            print("Transacción iniciada.")

            # Insertar ticket
            ticket_query = """
                        INSERT INTO Ticket (Fecha_Hora, ID_Empleado, ID_Cliente, Total)
                        VALUES (%s, %s, %s, %s)
                    """
            fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ticket_params = (fecha_hora, id_empleado, id_cliente, total)
            self.db.execute_query(ticket_query, ticket_params)
            print("Ticket insertado.")

            ticket_id_query = "SELECT LAST_INSERT_ID()"
            ticket_id_result = self.db.fetch_query(ticket_id_query)
            id_ticket = ticket_id_result[0][0]
            print(f"Ticket insertado con ID: {id_ticket}")

            # Insertar detalle de cada producto y actualizar stock
            for item in sale_items:
                id_producto = item["id_producto"]
                cantidad = item["cantidad"]
                precio_unitario = item["precio"]
                subtotal_item = cantidad * precio_unitario

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
                detalle_params = (id_ticket, id_producto, cantidad, precio_unitario, subtotal_item)
                self.db.execute_query(detalle_query, detalle_params)
                print(f"Detalle insertado para producto {id_producto}")

                stock_query = "UPDATE Producto SET Stock = Stock - %s WHERE ID_Producto = %s"
                stock_params = (cantidad, id_producto)
                self.db.execute_query(stock_query, stock_params)
                print(f"Stock actualizado para producto {id_producto}")

            # Armar datos para el ticket
            ticket_data = {
                "id_ticket": id_ticket,
                "fecha_hora": fecha_hora,
                "id_empleado": id_empleado,
                "id_cliente": id_cliente,
                "total": total,  # Total ya incluye IVA
                "subtotal": subtotal,  # Agregamos el subtotal para mostrarlo en el PDF
                "iva_amount": iva_amount, # Si se aplica IVA, agrégalo aquí
                "payment_method": payment_method,
                "efectivo_amount": efectivo_amount,
                "change": change,
                "total_in_letters": total_in_letters
            }
            pdf_path = self.report_generator.generate_ticket_pdf(ticket_data, sale_items)
            print(f"Ticket PDF generado en: {pdf_path}")

            self.db.connection.commit()
            print("Transacción confirmada.")

            return {"id_ticket": id_ticket, "total": total, "pdf_path": pdf_path}
        except Exception as e:
            self.db.connection.rollback()
            print(f"Transacción revertida debido a un error: {str(e)}")
            raise Exception(f"Error al registrar la venta: {str(e)}")

    def close(self):
        self.db.close()

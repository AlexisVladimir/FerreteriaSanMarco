# src/utils/report_generator.py
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from datetime import datetime
import os

class ReportGenerator:
    def __init__(self, output_dir="reports"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_ticket_pdf(self, ticket_data, sale_items, filename=None):
        """
        ticket_data debe incluir:
         - id_ticket, fecha_hora, id_empleado, id_cliente, subtotal, iva_amount, total,
           payment_method, efectivo_amount, change, total_in_letters
        sale_items: lista de diccionarios con claves:
         - id_producto, nombre, descripcion, precio, cantidad
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ticket_{ticket_data['id_ticket']}_{timestamp}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        c = canvas.Canvas(filepath, pagesize=letter)
        width, height = letter

        # Título del ticket
        c.setFont("Helvetica-Bold", 16)
        c.drawString(1 * inch, height - 1 * inch, "Ferretería San Marco - Ticket de Venta")

        # Información general del ticket
        c.setFont("Helvetica", 12)
        y_position = height - 1.5 * inch
        c.drawString(1 * inch, y_position, f"Ticket ID: {ticket_data['id_ticket']}")
        y_position -= 0.3 * inch
        c.drawString(1 * inch, y_position, f"Fecha y Hora: {ticket_data['fecha_hora']}")
        y_position -= 0.3 * inch
        c.drawString(1 * inch, y_position, f"Cliente ID: {ticket_data['id_cliente']}")
        y_position -= 0.3 * inch
        c.drawString(1 * inch, y_position, f"Empleado ID: {ticket_data['id_empleado']}")
        y_position -= 0.5 * inch

        # Encabezado de la tabla de productos
        c.setFont("Helvetica-Bold", 12)
        c.drawString(1 * inch, y_position, "Productos:")
        y_position -= 0.3 * inch
        c.drawString(1 * inch, y_position, "ID")
        c.drawString(2 * inch, y_position, "Nombre")
        c.drawString(4 * inch, y_position, "Cantidad")
        c.drawString(5 * inch, y_position, "C/P")
        c.drawString(6 * inch, y_position, "Subtotal")
        y_position -= 0.1 * inch
        c.line(1 * inch, y_position, 7 * inch, y_position)
        y_position -= 0.3 * inch

        # Lista de productos
        c.setFont("Helvetica", 12)
        for item in sale_items:
            id_producto = item["id_producto"]
            nombre = item.get("nombre", "Desconocido")
            cantidad = item["cantidad"]
            precio_unitario = item["precio"]
            item_subtotal = cantidad * precio_unitario
            c.drawString(1 * inch, y_position, str(id_producto))
            c.drawString(2 * inch, y_position, nombre[:20])
            c.drawString(4 * inch, y_position, str(cantidad))
            c.drawString(5 * inch, y_position, f"${precio_unitario:.2f}")
            c.drawString(6 * inch, y_position, f"${item_subtotal:.2f}")
            y_position -= 0.3 * inch
            if y_position < 2 * inch:
                c.showPage()
                y_position = height - 1 * inch
                c.setFont("Helvetica-Bold", 12)
                c.drawString(1 * inch, y_position, "Productos (continuación):")
                y_position -= 0.3 * inch
                c.drawString(1 * inch, y_position, "ID")
                c.drawString(2 * inch, y_position, "Nombre")
                c.drawString(4 * inch, y_position, "Cantidad")
                c.drawString(5 * inch, y_position, "Precio Unitario")
                c.drawString(6 * inch, y_position, "Subtotal")
                y_position -= 0.1 * inch
                c.line(1 * inch, y_position, 7 * inch, y_position)
                y_position -= 0.3 * inch
                c.setFont("Helvetica", 12)

        # Mostrar subtotal, IVA y total
        y_position -= 0.3 * inch
        c.setFont("Helvetica-Bold", 12)
        c.drawString(1 * inch, y_position, f"Subtotal (sin IVA): ${ticket_data['subtotal']:.2f}")
        y_position -= 0.3 * inch
        c.drawString(1 * inch, y_position, f"IVA (16.0%): ${ticket_data['iva_amount']:.2f}")
        y_position -= 0.3 * inch
        c.drawString(1 * inch, y_position, f"Total a Pagar (con IVA): ${ticket_data['total']:.2f}")
        y_position -= 0.5 * inch

        # Mostrar información de pago
        c.setFont("Helvetica-Bold", 12)
        c.drawString(1 * inch, y_position, f"Método de Pago: {ticket_data['payment_method']}")
        y_position -= 0.3 * inch
        if ticket_data["payment_method"] == "Efectivo":
            c.drawString(1 * inch, y_position, f"Monto Entregado: ${ticket_data['efectivo_amount']:.2f}")
            y_position -= 0.3 * inch
            c.drawString(1 * inch, y_position, f"Cambio: ${ticket_data['change']:.2f}")
            y_position -= 0.3 * inch
        c.drawString(1 * inch, y_position, f"Total en Letras: {ticket_data['total_in_letters']}")
        y_position -= 0.5 * inch

        # Pie de página
        c.setFont("Helvetica", 10)
        c.drawString(1 * inch, 1 * inch, "Gracias por su compra en Ferretería San Marco")
        c.drawString(1 * inch, 0.7 * inch, "Fecha de generación: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        c.showPage()
        c.save()
        return filepath

    def generate_sales_report(self, sales_data, filename=None):
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"sales_report_{timestamp}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        c = canvas.Canvas(filepath, pagesize=letter)
        width, height = letter
        c.setFont("Helvetica-Bold", 16)
        c.drawString(1 * inch, height - 1 * inch, "Ferretería San Marco - Reporte de Ventas")
        c.setFont("Helvetica-Bold", 12)
        y_position = height - 1.5 * inch
        c.drawString(1 * inch, y_position, "ID Ticket")
        c.drawString(2 * inch, y_position, "Fecha y Hora")
        c.drawString(3.5 * inch, y_position, "Cliente ID")
        c.drawString(4.5 * inch, y_position, "Total")
        y_position -= 0.1 * inch
        c.line(1 * inch, y_position, 6 * inch, y_position)
        y_position -= 0.3 * inch
        c.setFont("Helvetica", 12)
        for sale in sales_data:
            c.drawString(1 * inch, y_position, str(sale[0]))
            c.drawString(2 * inch, y_position, str(sale[1]))
            c.drawString(3.5 * inch, y_position, str(sale[3]))
            c.drawString(4.5 * inch, y_position, f"${sale[4]:.2f}")
            y_position -= 0.3 * inch
            if y_position < 1 * inch:
                c.showPage()
                y_position = height - 1 * inch
                c.setFont("Helvetica-Bold", 12)
                c.drawString(1 * inch, y_position, "ID Ticket")
                c.drawString(2 * inch, y_position, "Fecha y Hora")
                c.drawString(3.5 * inch, y_position, "Cliente ID")
                c.drawString(4.5 * inch, y_position, "Total")
                y_position -= 0.1 * inch
                c.line(1 * inch, y_position, 6 * inch, y_position)
                y_position -= 0.3 * inch
                c.setFont("Helvetica", 12)
        c.setFont("Helvetica", 10)
        c.drawString(1 * inch, 0.7 * inch, "Reporte generado el: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        c.showPage()
        c.save()
        return filepath

    def generate_inventory_report(self, inventory_data, filename=None):
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"inventory_report_{timestamp}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        c = canvas.Canvas(filepath, pagesize=letter)
        width, height = letter
        c.setFont("Helvetica-Bold", 16)
        c.drawString(1 * inch, height - 1 * inch, "Ferretería San Marco - Reporte de Inventario")
        c.setFont("Helvetica-Bold", 12)
        y_position = height - 1.5 * inch
        c.drawString(1 * inch, y_position, "ID Producto")
        c.drawString(2.5 * inch, y_position, "Nombre")
        c.drawString(4.5 * inch, y_position, "Stock")
        y_position -= 0.1 * inch
        c.line(1 * inch, y_position, 6 * inch, y_position)
        y_position -= 0.3 * inch
        c.setFont("Helvetica", 12)
        for item in inventory_data:
            c.drawString(1 * inch, y_position, str(item["id_producto"]))
            c.drawString(2.5 * inch, y_position, item["nombre"])
            c.drawString(4.5 * inch, y_position, str(item["stock"]))
            y_position -= 0.3 * inch
            if y_position < 1 * inch:
                c.showPage()
                y_position = height - 1 * inch
                c.setFont("Helvetica-Bold", 12)
                c.drawString(1 * inch, y_position, "ID Producto")
                c.drawString(2.5 * inch, y_position, "Nombre")
                c.drawString(4.5 * inch, y_position, "Stock")
                y_position -= 0.1 * inch
                c.line(1 * inch, y_position, 6 * inch, y_position)
                y_position -= 0.3 * inch
                c.setFont("Helvetica", 12)
        c.setFont("Helvetica", 10)
        c.drawString(1 * inch, 0.7 * inch, "Reporte generado el: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        c.showPage()
        c.save()
        return filepath

    def generate_devoluciones_report(self, devoluciones_data, filename=None):
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"devoluciones_report_{timestamp}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        c = canvas.Canvas(filepath, pagesize=letter)
        width, height = letter
        c.setFont("Helvetica-Bold", 16)
        c.drawString(1 * inch, height - 1 * inch, "Ferretería San Marco - Reporte de Devoluciones")
        c.setFont("Helvetica-Bold", 12)
        y_position = height - 1.5 * inch
        c.drawString(1 * inch, y_position, "ID Devolución")
        c.drawString(2 * inch, y_position, "ID Ticket")
        c.drawString(3 * inch, y_position, "ID Producto")
        c.drawString(4 * inch, y_position, "Cantidad")
        c.drawString(5 * inch, y_position, "Motivo")
        c.drawString(6 * inch, y_position, "Fecha")
        y_position -= 0.1 * inch
        c.line(1 * inch, y_position, 7 * inch, y_position)
        y_position -= 0.3 * inch
        c.setFont("Helvetica", 12)
        for devol in devoluciones_data:
            id_devolucion, id_ticket, id_producto, cantidad, motivo, fecha = devol
            c.drawString(1 * inch, y_position, str(id_devolucion))
            c.drawString(2 * inch, y_position, str(id_ticket))
            c.drawString(3 * inch, y_position, str(id_producto))
            c.drawString(4 * inch, y_position, str(cantidad))
            c.drawString(5 * inch, y_position, motivo if motivo else "")
            c.drawString(6 * inch, y_position, str(fecha))
            y_position -= 0.3 * inch
            if y_position < 1 * inch:
                c.showPage()
                y_position = height - 1 * inch
                c.setFont("Helvetica-Bold", 12)
                c.drawString(1 * inch, y_position, "ID Devolución")
                c.drawString(2 * inch, y_position, "ID Ticket")
                c.drawString(3 * inch, y_position, "ID Producto")
                c.drawString(4 * inch, y_position, "Cantidad")
                c.drawString(5 * inch, y_position, "Motivo")
                c.drawString(6 * inch, y_position, "Fecha")
                y_position -= 0.1 * inch
                c.line(1 * inch, y_position, 7 * inch, y_position)
                y_position -= 0.3 * inch
                c.setFont("Helvetica", 12)
        c.setFont("Helvetica", 10)
        c.drawString(1 * inch, 0.7 * inch, "Reporte generado el: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        c.showPage()
        c.save()
        return filepath

    def generate_low_stock_report(self, low_stock_data, filename=None):
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"low_stock_report_{timestamp}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        c = canvas.Canvas(filepath, pagesize=letter)
        width, height = letter
        c.setFont("Helvetica-Bold", 16)
        c.drawString(1 * inch, height - 1 * inch, "Ferretería San Marco - Reporte de Bajo Stock")
        c.setFont("Helvetica-Bold", 12)
        y_position = height - 1.5 * inch
        c.drawString(1 * inch, y_position, "ID Producto")
        c.drawString(2.5 * inch, y_position, "Nombre")
        c.drawString(5 * inch, y_position, "Stock")
        y_position -= 0.1 * inch
        c.line(1 * inch, y_position, 6 * inch, y_position)
        y_position -= 0.3 * inch
        c.setFont("Helvetica", 12)
        for item in low_stock_data:
            c.drawString(1 * inch, y_position, str(item["id_producto"]))
            c.drawString(2.5 * inch, y_position, item["nombre"])
            c.drawString(5 * inch, y_position, str(item["stock"]))
            y_position -= 0.3 * inch
            if y_position < 1 * inch:
                c.showPage()
                y_position = height - 1 * inch
                c.setFont("Helvetica-Bold", 12)
                c.drawString(1 * inch, y_position, "ID Producto")
                c.drawString(2.5 * inch, y_position, "Nombre")
                c.drawString(5 * inch, y_position, "Stock")
                y_position -= 0.1 * inch
                c.line(1 * inch, y_position, 6 * inch, y_position)
                y_position -= 0.3 * inch
                c.setFont("Helvetica", 12)
        c.setFont("Helvetica", 10)
        c.drawString(1 * inch, 0.7 * inch, "Reporte generado el: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        c.showPage()
        c.save()
        return filepath

    def generate_rentability_report(self, rentability_data, filename=None):
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"rentability_report_{timestamp}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        c = canvas.Canvas(filepath, pagesize=letter)
        width, height = letter
        c.setFont("Helvetica-Bold", 16)
        c.drawString(1 * inch, height - 1 * inch, "Ferretería San Marco - Reporte de Rentabilidad por Producto")
        c.setFont("Helvetica-Bold", 12)
        y_position = height - 1.5 * inch
        c.drawString(1 * inch, y_position, "ID Producto")
        c.drawString(2 * inch, y_position, "Nombre")
        c.drawString(4 * inch, y_position, "Precio Compra")
        c.drawString(5 * inch, y_position, "Precio Venta")
        c.drawString(6 * inch, y_position, "Ganancia")
        y_position -= 0.1 * inch
        c.line(1 * inch, y_position, 7 * inch, y_position)
        y_position -= 0.3 * inch
        c.setFont("Helvetica", 12)
        for item in rentability_data:
            c.drawString(1 * inch, y_position, str(item["id_producto"]))
            c.drawString(2 * inch, y_position, item["nombre"])
            c.drawString(4 * inch, y_position, f"${item['precio_compra']:.2f}")
            c.drawString(5 * inch, y_position, f"${item['precio_publico']:.2f}")
            c.drawString(6 * inch, y_position, f"${item['ganancia']:.2f}")
            y_position -= 0.3 * inch
            if y_position < 1 * inch:
                c.showPage()
                y_position = height - 1 * inch
                c.setFont("Helvetica-Bold", 12)
                c.drawString(1 * inch, y_position, "ID Producto")
                c.drawString(2 * inch, y_position, "Nombre")
                c.drawString(4 * inch, y_position, "Precio Compra")
                c.drawString(5 * inch, y_position, "Precio Venta")
                c.drawString(6 * inch, y_position, "Ganancia")
                y_position -= 0.1 * inch
                c.line(1 * inch, y_position, 7 * inch, y_position)
                y_position -= 0.3 * inch
                c.setFont("Helvetica", 12)
        c.setFont("Helvetica", 10)
        c.drawString(1 * inch, 0.7 * inch, "Reporte generado el: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        c.showPage()
        c.save()
        return filepath

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
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ticket_{ticket_data['id_ticket']}_{timestamp}.pdf"

        filepath = os.path.join(self.output_dir, filename)
        c = canvas.Canvas(filepath, pagesize=letter)
        width, height = letter

        c.setFont("Helvetica-Bold", 16)
        c.drawString(1 * inch, height - 1 * inch, "Ferretería San Marco - Ticket de Venta")

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

        c.setFont("Helvetica-Bold", 12)
        c.drawString(1 * inch, y_position, "Productos:")
        y_position -= 0.3 * inch
        c.drawString(1 * inch, y_position, "ID Producto")
        c.drawString(3 * inch, y_position, "Cantidad")
        c.drawString(4.5 * inch, y_position, "Precio Unitario")
        c.drawString(6 * inch, y_position, "Subtotal")
        y_position -= 0.1 * inch
        c.line(1 * inch, y_position, 7 * inch, y_position)
        y_position -= 0.3 * inch

        c.setFont("Helvetica", 12)
        for item in sale_items:
            id_producto = item["id_producto"]
            cantidad = item["cantidad"]
            precio_unitario = 10.0  # Precio fijo por simplicidad
            subtotal = cantidad * precio_unitario

            c.drawString(1 * inch, y_position, str(id_producto))
            c.drawString(3 * inch, y_position, str(cantidad))
            c.drawString(4.5 * inch, y_position, f"${precio_unitario:.2f}")
            c.drawString(6 * inch, y_position, f"${subtotal:.2f}")
            y_position -= 0.3 * inch

        y_position -= 0.3 * inch
        c.setFont("Helvetica-Bold", 12)
        c.drawString(1 * inch, y_position, f"Total: ${ticket_data['total']:.2f}")

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
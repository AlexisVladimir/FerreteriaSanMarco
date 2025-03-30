#que pedo porque tengo 2
#talvez lo guardaste por si acaso no jalaba uno
# no voy a mover nada de este es un
# src/views/reportes_view.py
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from src.controllers.reportes_controller import ReportesController
from src.utils.report_generator import ReportGenerator

class ReportesView:
    def __init__(self, parent):
        self.controller = ReportesController()
        self.report_generator = ReportGenerator()
        self.frame = ttk.Frame(parent)
        self.build_ui()
        self.frame.pack(expand=True, fill="both")

    def build_ui(self):
        # Título
        ttk.Label(self.frame, text="Módulo de Reportes", font=("Helvetica", 16)).pack(pady=20)

        # Botones para generar reportes
        ttk.Button(self.frame, text="Generar Reporte de Ventas", bootstyle=INFO, command=self.generate_sales_report).pack(pady=10)
        ttk.Button(self.frame, text="Generar Reporte de Inventario", bootstyle=INFO, command=self.generate_inventory_report).pack(pady=10)
        ttk.Button(self.frame, text="Generar Reporte de Devoluciones", bootstyle=INFO, command=self.generate_devoluciones_report).pack(pady=10)

        # Área para mostrar resultados
        self.result_label = ttk.Label(self.frame, text="", font=("Helvetica", 12))
        self.result_label.pack(pady=20)

    def generate_sales_report(self):
        try:
            sales_data = self.controller.get_sales_data()
            if not sales_data:
                Messagebox.show_info("No hay ventas registradas.", "Información")
                return

            pdf_path = self.report_generator.generate_sales_report(sales_data)
            self.result_label.config(text=f"Reporte de ventas generado en: {pdf_path}")
        except Exception as e:
            Messagebox.show_error(f"Error al generar el reporte de ventas: {str(e)}", "Error")

    def generate_inventory_report(self):
        try:
            inventory_data = self.controller.get_inventory_data()
            if not inventory_data:
                Messagebox.show_info("No hay productos en el inventario.", "Información")
                return

            pdf_path = self.report_generator.generate_inventory_report(inventory_data)
            self.result_label.config(text=f"Reporte de inventario generado en: {pdf_path}")
        except Exception as e:
            Messagebox.show_error(f"Error al generar el reporte de inventario: {str(e)}", "Error")

    def generate_devoluciones_report(self):
        try:
            devoluciones_data = self.controller.get_devoluciones_data()
            if not devoluciones_data:
                Messagebox.show_info("No hay devoluciones registradas.", "Información")
                return

            pdf_path = self.report_generator.generate_devoluciones_report(devoluciones_data)
            self.result_label.config(text=f"Reporte de devoluciones generado en: {pdf_path}")
        except Exception as e:
            Messagebox.show_error(f"Error al generar el reporte de devoluciones: {str(e)}", "Error")

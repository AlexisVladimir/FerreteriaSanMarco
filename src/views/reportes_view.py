# src/views/reportes_view.py
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from src.controllers.reportes_controller import ReportesController
from src.utils.report_generator import ReportGenerator
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

class ReportesView:
    def __init__(self, parent):
        self.controller = ReportesController()
        self.report_generator = ReportGenerator()
        self.frame = ttk.Frame(parent)
        self.current_canvas = None  # Para manejar el gráfico actual
        self.build_ui()
        self.frame.pack(expand=True, fill="both")

    def build_ui(self):
        # Frame superior para los botones de reportes
        top_frame = ttk.Frame(self.frame)
        top_frame.pack(side=TOP, fill=X, padx=10, pady=10)

        # Título
        ttk.Label(top_frame, text="Módulo de Reportes", font=("Helvetica", 16)).pack(pady=10)

        # Botones para generar reportes PDF
        ttk.Button(top_frame, text="Generar Reporte de Ventas", bootstyle=INFO, command=self.generate_sales_report).pack(side=LEFT, padx=5)
        ttk.Button(top_frame, text="Generar Reporte de Inventario", bootstyle=INFO, command=self.generate_inventory_report).pack(side=LEFT, padx=5)
        ttk.Button(top_frame, text="Generar Reporte de Devoluciones", bootstyle=INFO, command=self.generate_devoluciones_report).pack(side=LEFT, padx=5)
        ttk.Button(top_frame, text="Generar Reporte de Bajo Stock", bootstyle=INFO, command=self.generate_low_stock_report).pack(side=LEFT, padx=5)
        ttk.Button(top_frame, text="Generar Reporte de Rentabilidad", bootstyle=INFO, command=self.generate_rentability_report).pack(side=LEFT, padx=5)
        # Botón para mostrar gráfico de ganancias
        ttk.Button(top_frame, text="Mostrar Gráfico de Ganancias", bootstyle=INFO, command=self.show_profit_pie).pack(side=LEFT, padx=5)

        # Frame central para los gráficos
        center_frame = ttk.Frame(self.frame)
        center_frame.pack(expand=True, fill=BOTH, padx=10, pady=10)

        # Frame para los botones de selección de gráficos (otros gráficos existentes)
        graph_buttons_frame = ttk.Frame(center_frame)
        graph_buttons_frame.pack(fill=X, pady=5)
        ttk.Button(graph_buttons_frame, text="Días con Más Ventas", bootstyle=PRIMARY, command=self.show_sales_by_day).pack(side=LEFT, padx=5)
        ttk.Button(graph_buttons_frame, text="Índices de Ganancia", bootstyle=PRIMARY, command=self.show_profit_index).pack(side=LEFT, padx=5)
        ttk.Button(graph_buttons_frame, text="Productos Más Vendidos", bootstyle=PRIMARY, command=self.show_top_products).pack(side=LEFT, padx=5)

        # Frame para el gráfico
        self.graph_frame = ttk.Frame(center_frame)
        self.graph_frame.pack(expand=True, fill=BOTH)

        # Área para mostrar resultados (en la parte inferior)
        self.result_label = ttk.Label(self.frame, text="", font=("Helvetica", 12))
        self.result_label.pack(pady=20)

    def clear_graph(self):
        if self.current_canvas:
            self.current_canvas.get_tk_widget().destroy()
            self.current_canvas = None
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

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

    def generate_low_stock_report(self):
        try:
            low_stock_data = self.controller.get_low_stock_products()
            if not low_stock_data:
                Messagebox.show_info("No hay productos con bajo stock.", "Información")
                return
            pdf_path = self.report_generator.generate_low_stock_report(low_stock_data)
            self.result_label.config(text=f"Reporte de bajo stock generado en: {pdf_path}")
        except Exception as e:
            Messagebox.show_error(f"Error al generar el reporte de bajo stock: {str(e)}", "Error")

    def generate_rentability_report(self):
        try:
            rentability_data = self.controller.get_rentability_by_product()
            if not rentability_data:
                Messagebox.show_info("No hay datos de rentabilidad para mostrar.", "Información")
                return
            pdf_path = self.report_generator.generate_rentability_report(rentability_data)
            self.result_label.config(text=f"Reporte de rentabilidad generado en: {pdf_path}")
        except Exception as e:
            Messagebox.show_error(f"Error al generar el reporte de rentabilidad: {str(e)}", "Error")

    def show_profit_pie(self):
        try:
            profit_data = self.controller.get_profit_data()
            revenue = profit_data["revenue"]
            devolutions = profit_data["devolutions"]
            net_profit = profit_data["net_profit"]
            if revenue == 0:
                Messagebox.show_info("No hay ingresos para calcular ganancias.", "Información")
                return
            labels = ["Devoluciones", "Ganancias Netas"]
            sizes = [devolutions, net_profit]
            self.clear_graph()
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.set_title("Comparación: Ganancias Netas vs. Devoluciones")
            plt.tight_layout()
            self.current_canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            self.current_canvas.draw()
            self.current_canvas.get_tk_widget().pack(expand=True, fill=BOTH)
        except Exception as e:
            Messagebox.show_error(f"Error al generar el gráfico de ganancias: {str(e)}", "Error")

    def show_sales_by_day(self):
        try:
            sales_data = self.controller.get_sales_by_day()
            if not sales_data:
                Messagebox.show_info("No hay datos de ventas para mostrar.", "Información")
                return
            self.clear_graph()
            dates = [str(data['fecha']) for data in sales_data]
            totals = [data['total'] for data in sales_data]
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.plot(dates, totals, marker='o', color='blue')
            ax.set_title("Ventas por Día")
            ax.set_xlabel("Fecha")
            ax.set_ylabel("Total de Ventas ($)")
            plt.xticks(rotation=45)
            plt.tight_layout()
            self.current_canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            self.current_canvas.draw()
            self.current_canvas.get_tk_widget().pack(expand=True, fill=BOTH)
        except Exception as e:
            Messagebox.show_error(f"Error al generar el gráfico de ventas por día: {str(e)}", "Error")

    def show_profit_index(self):
        try:
            profit_data = self.controller.get_profit_data()
            if not profit_data:
                Messagebox.show_info("No hay datos de ganancia para mostrar.", "Información")
                return
            self.clear_graph()
            labels = ["Ingresos", "Devoluciones", "Ganancia Neta"]
            values = [profit_data["revenue"], profit_data["devolutions"], profit_data["net_profit"]]
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.bar(labels, values, color=["green", "red", "blue"])
            ax.set_title("Índices de Ganancia")
            ax.set_ylabel("Monto ($)")
            plt.tight_layout()
            self.current_canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            self.current_canvas.draw()
            self.current_canvas.get_tk_widget().pack(expand=True, fill=BOTH)
        except Exception as e:
            Messagebox.show_error(f"Error al generar el gráfico de índices de ganancia: {str(e)}", "Error")

    def show_top_products(self):
        try:
            top_products = self.controller.get_top_products()
            if not top_products:
                Messagebox.show_info("No hay datos de productos vendidos para mostrar.", "Información")
                return
            self.clear_graph()
            products = [data['nombre'] for data in top_products]
            quantities = [data['cantidad'] for data in top_products]
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.pie(quantities, labels=products, autopct='%1.1f%%', startangle=90)
            ax.set_title("Productos Más Vendidos")
            plt.tight_layout()
            self.current_canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            self.current_canvas.draw()
            self.current_canvas.get_tk_widget().pack(expand=True, fill=BOTH)
        except Exception as e:
            Messagebox.show_error(f"Error al generar el gráfico de productos más vendidos: {str(e)}", "Error")

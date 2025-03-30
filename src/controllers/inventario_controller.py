# src/controllers/inventario_controller.py
from src.utils.db_helper import DatabaseHelper
from datetime import datetime


class InventarioController:
    def __init__(self):
        self.db = DatabaseHelper()

    # ==============================
    # OPERACIONES CRUD BÁSICAS
    # ==============================

    def get_all_products(self):
        """Obtener todos los productos con información relacionada"""
        query = """
            SELECT 
                p.ID_Producto, 
                p.Nombre, 
                p.Descripcion, 
                IFNULL(s.Nombre, 'Sin Subcategoría') AS Subcategoria,
                IFNULL(c.Nombre, 'Sin Categoría') AS Categoria, 
                p.Stock, 
                p.Precio_Publico, 
                IFNULL(u.Descripcion, 'Sin Ubicación') AS Ubicacion,
                IFNULL(pr.Nombre, 'Sin Proveedor') AS Proveedor,
                IFNULL(p.Fecha_Ingreso, 'Sin Fecha') AS Fecha_Ingreso
            FROM Producto p
            LEFT JOIN Subcategoria s ON p.ID_Subcategoria = s.ID_Subcategoria
            LEFT JOIN Categoria c ON s.ID_Categoria = c.ID_Categoria
            LEFT JOIN Ubicacion u ON p.ID_Ubicacion = u.ID_Ubicacion
            LEFT JOIN Producto_Proveedor pp ON p.ID_Producto = pp.ID_Producto
            LEFT JOIN Proveedor pr ON pp.ID_Proveedor = pr.ID_Proveedor
            ORDER BY p.ID_Producto
        """
        try:
            products = self.db.fetch_query(query)
            return [{
                "id_producto": item[0],
                "nombre": item[1],
                "descripcion": item[2] if item[2] else "Sin descripción",
                "subcategoria": item[3],
                "categoria": item[4],
                "stock": item[5],
                "precio_unitario": float(item[6]) if item[6] else 0.0,
                "ubicacion": item[7],
                "proveedor": item[8] if item[8] else "Sin proveedor",
                "fecha_ingreso": item[9].strftime('%Y-%m-%d') if isinstance(item[9], datetime) else item[9]
            } for item in products]
        except Exception as e:
            print(f"Error al obtener productos: {str(e)}")
            return []

    def agregar_producto(self, nombre, descripcion, categoria, cantidad, precio, ubicacion, fecha):
        """Agregar un nuevo producto al inventario"""
        if not nombre or not cantidad or not precio:
            return False, "Nombre, cantidad y precio son campos obligatorios"

        try:
            query = """
                INSERT INTO Producto (
                    Nombre, 
                    Descripcion, 
                    ID_Subcategoria, 
                    Stock, 
                    Precio_Unitario, 
                    ID_Ubicacion, 
                    Fecha_Ingreso
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                nombre.strip(),
                descripcion.strip() if descripcion else None,
                int(categoria) if categoria else None,
                int(cantidad),
                float(precio),
                int(ubicacion) if ubicacion else None,
                fecha if fecha else None
            )
            self.db.execute_query(query, params)
            return True, "Producto agregado correctamente"
        except ValueError:
            return False, "Por favor ingrese valores numéricos válidos para cantidad, precio y ubicación"
        except Exception as e:
            print(f"Error al agregar producto: {str(e)}")
            return False, f"Error al agregar producto: {str(e)}"

    def actualizar_producto(self, producto_id, nombre, descripcion, categoria, cantidad, precio, ubicacion, fecha):
        """Actualizar un producto existente"""
        try:
            query = """
                UPDATE Producto 
                SET 
                    Nombre = %s,
                    Descripcion = %s,
                    ID_Subcategoria = %s,
                    Stock = %s,
                    Precio_Unitario = %s,
                    ID_Ubicacion = %s,
                    Fecha_Ingreso = %s
                WHERE ID_Producto = %s
            """
            params = (
                nombre.strip(),
                descripcion.strip() if descripcion else None,
                int(categoria) if categoria else None,
                int(cantidad),
                float(precio),
                int(ubicacion) if ubicacion else None,
                fecha if fecha else None,
                int(producto_id)
            )
            self.db.execute_query(query, params)
            return True, "Producto actualizado correctamente"
        except ValueError:
            return False, "Por favor ingrese valores numéricos válidos"
        except Exception as e:
            print(f"Error al actualizar producto: {str(e)}")
            return False, f"Error al actualizar producto: {str(e)}"

    def eliminar_producto(self, producto_id):
        """Eliminar un producto del inventario"""
        try:
            # Verificar si el producto existe
            if not self._producto_existe(producto_id):
                return False, "El producto no existe"

            # Verificar relaciones con otras tablas
            tablas_relacionadas = self._verificar_relaciones_producto(producto_id)
            if tablas_relacionadas:
                return False, f"No se puede eliminar, el producto tiene registros relacionados en: {', '.join(tablas_relacionadas)}"

            # Si no hay problemas, proceder con la eliminación
            query = "DELETE FROM Producto WHERE ID_Producto = %s"
            self.db.execute_query(query, (producto_id,))
            return True, "Producto eliminado correctamente"
        except Exception as e:
            print(f"Error al eliminar producto: {str(e)}")
            return False, f"Error al eliminar producto: {str(e)}"

    # ==============================
    # FUNCIONES DE BÚSQUEDA
    # ==============================

    def buscar_productos(self, filtro, valor):
        """Buscar productos según criterio especificado"""
        if not valor:
            return []

        query = """
            SELECT 
                p.ID_Producto, 
                p.Nombre, 
                IFNULL(s.Nombre, 'Sin Subcategoría') AS Subcategoria,
                p.Precio_Unitario, 
                p.Stock, 
                IFNULL(u.Descripcion, 'Sin Ubicación') AS Ubicacion
            FROM Producto p
            LEFT JOIN Subcategoria s ON p.ID_Subcategoria = s.ID_Subcategoria
            LEFT JOIN Ubicacion u ON p.ID_Ubicacion = u.ID_Ubicacion
            LEFT JOIN Producto_Proveedor pp ON p.ID_Producto = pp.ID_Producto
            WHERE {condicion}
        """

        conditions = {
            "Nombre": "p.Nombre LIKE %s",
            "ID_Subcategoria": "p.ID_Subcategoria = %s",
            "ID_Proveedor": "pp.ID_Proveedor = %s",
            "ID_Ubicacion": "p.ID_Ubicacion = %s"
        }

        if filtro not in conditions:
            return []

        condicion = conditions[filtro]
        valor = f"%{valor}%" if filtro == "Nombre" else valor

        try:
            query = query.format(condicion=condicion)
            results = self.db.fetch_query(query, (valor,))
            return [{
                "id": item[0],
                "nombre": item[1],
                "subcategoria": item[2],
                "precio": float(item[3]) if item[3] else 0.0,
                "stock": item[4],
                "ubicacion": item[5]
            } for item in results]
        except Exception as e:
            print(f"Error al buscar productos: {str(e)}")
            return []

    def buscar_por_estanteria(self, ubicacion):
        """Buscar productos por ubicación específica"""
        if not ubicacion:
            return []

        query = """
            SELECT 
                p.ID_Producto, 
                p.Nombre, 
                IFNULL(c.Nombre, 'Sin Categoría') AS Categoria,
                p.Stock, 
                IFNULL(u.Descripcion, 'Sin Ubicación') AS Ubicacion
            FROM Producto p
            LEFT JOIN Subcategoria s ON p.ID_Subcategoria = s.ID_Subcategoria
            LEFT JOIN Categoria c ON s.ID_Categoria = c.ID_Categoria
            LEFT JOIN Ubicacion u ON p.ID_Ubicacion = u.ID_Ubicacion
            WHERE p.ID_Ubicacion = %s
            ORDER BY p.Nombre
        """
        try:
            results = self.db.fetch_query(query, (int(ubicacion),))
            return [{
                "id": item[0],
                "nombre": item[1],
                "categoria": item[2],
                "stock": item[3],
                "ubicacion": item[4]
            } for item in results]
        except Exception as e:
            print(f"Error al buscar por estantería: {str(e)}")
            return []

    def buscar_birlos_compatibles(self, marca, modelo, anio):
        """Buscar birlos compatibles con un vehículo específico"""
        if not marca or not modelo or not anio:
            return []

        try:
            query = """
                SELECT 
                    p.ID_Producto, 
                    p.Nombre, 
                    b.Medida, 
                    b.Tipo_Rosca, 
                    'Compatible' AS Compatibilidad
                FROM Producto p
                JOIN Birlo b ON p.ID_Producto = b.ID_Producto
                JOIN Vehiculo v ON b.ID_Birlo = v.ID_Birlo
                WHERE v.Marca = %s AND v.Modelo = %s AND v.Año = %s
                ORDER BY p.Nombre
            """
            results = self.db.fetch_query(query, (marca.strip(), modelo.strip(), int(anio)))
            return [{
                "id": item[0],
                "nombre": item[1],
                "medida": item[2],
                "tipo_rosca": item[3],
                "compatibilidad": item[4]
            } for item in results]
        except ValueError:
            return []
        except Exception as e:
            print(f"Error al buscar birlos compatibles: {str(e)}")
            return []

    # ==============================
    # FUNCIONES PRIVADAS DE APOYO
    # ==============================

    def _producto_existe(self, producto_id):
        """Verificar si un producto existe en la base de datos"""
        query = "SELECT COUNT(*) FROM Producto WHERE ID_Producto = %s"
        result = self.db.fetch_query(query, (producto_id,))
        return result and result[0][0] > 0

    def _verificar_relaciones_producto(self, producto_id):
        """Verificar si el producto tiene registros relacionados en otras tablas"""
        relaciones = [
            ("Producto_Proveedor", "ID_Producto"),
            ("Tornillo", "ID_Producto"),
            ("Pija", "ID_Producto"),
            ("Tuerca", "ID_Producto"),
            ("Birlo", "ID_Producto"),
            ("Seguro", "ID_Producto"),
            ("Clip_Push", "ID_Producto"),
            ("Movimiento", "ID_Producto"),
            ("Detalle_Pedido_Proveedor", "ID_Producto"),
            ("Detalle_Ticket", "ID_Producto"),
            ("Devolucion", "ID_Producto")
        ]

        tablas_con_relaciones = []
        for tabla, columna in relaciones:
            query = f"SELECT COUNT(*) FROM {tabla} WHERE {columna} = %s"
            result = self.db.fetch_query(query, (producto_id,))
            if result and result[0][0] > 0:
                tablas_con_relaciones.append(tabla)

        return tablas_con_relaciones

    def close(self):
        """Cerrar conexión a la base de datos"""
        self.db.close()
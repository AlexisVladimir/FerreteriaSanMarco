# src/controllers/turnos_controller.py
from datetime import datetime, date
from src.utils.db_helper import DatabaseHelper

class TurnosController:
    def __init__(self):
        self.db = DatabaseHelper()

    def iniciar_turno(self, id_empleado):
        today = date.today().strftime("%Y-%m-%d")
        query_check = """
            SELECT ID_Turno FROM Turno
            WHERE ID_Empleado = %s AND Fecha = %s AND Hora_Salida = '00:00:00'
        """
        result = self.db.fetch_query(query_check, (id_empleado, today))
        if result:
            raise Exception("El turno ya ha sido iniciado para hoy.")
        hora_entrada = datetime.now().strftime("%H:%M:%S")
        query_insert = """
            INSERT INTO Turno (Hora_Entrada, Hora_Salida, Fecha, ID_Empleado)
            VALUES (%s, %s, %s, %s)
        """
        params = (hora_entrada, "00:00:00", today, id_empleado)
        if self.db.execute_query(query_insert, params):
            return {"hora_entrada": hora_entrada, "fecha": today}
        else:
            raise Exception("Error al iniciar el turno.")

    def finalizar_turno(self, id_empleado):
        today = date.today().strftime("%Y-%m-%d")
        hora_salida = datetime.now().strftime("%H:%M:%S")
        query_update = """
            UPDATE Turno
            SET Hora_Salida = %s
            WHERE ID_Empleado = %s AND Fecha = %s AND Hora_Salida = '00:00:00'
        """
        if self.db.execute_query(query_update, (hora_salida, id_empleado, today)):
            return {"hora_salida": hora_salida, "fecha": today}
        else:
            raise Exception("No se encontró un turno iniciado para finalizar.")

    def obtener_turnos(self, id_empleado):
        # Se hace JOIN con Empleado para obtener también el nombre
        query = """
            SELECT T.Fecha, T.Hora_Entrada, T.Hora_Salida, E.ID_Empleado, E.Nombre_Completo
            FROM Turno T
            JOIN Empleado E ON T.ID_Empleado = E.ID_Empleado
            WHERE T.ID_Empleado = %s
            ORDER BY T.Fecha DESC
        """
        data = self.db.fetch_query(query, (id_empleado,))
        return [{"fecha": row[0],
                 "hora_entrada": row[1],
                 "hora_salida": row[2],
                 "id_empleado": row[3],
                 "nombre": row[4]} for row in data]

    def close(self):
        self.db.close()

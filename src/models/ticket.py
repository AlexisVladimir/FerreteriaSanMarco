class Ticket:
    def __init__(self, id_ticket, fecha_hora, id_empleado, id_cliente, total):
        self.id_ticket = id_ticket
        self.fecha_hora = fecha_hora
        self.id_empleado = id_empleado
        self.id_cliente = id_cliente
        self.total = total
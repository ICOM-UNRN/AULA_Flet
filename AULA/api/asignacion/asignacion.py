import psycopg2


class Asignacion():
    def __init__(self, conn: psycopg2.connect):
        self.conn: psycopg2.connect = conn
        self.cursor = self.conn.cursor()

    def get_asignaciones(self):
        self.cursor.execute('SELECT * FROM asignacion')
        colums = [descr.name for descr in self.cursor.description]
        rows = [row for row in self.cursor.fetchall()]
        data = {
            "columns": colums,
            "rows": rows
        }
        return data

    def get_asignacion(self, aula):
        result = self.cursor.callproc("get_asignacion", [aula])
        self.conn.commit()
        return result

    def get_materias_eventos_asignados(self, carrera, edificio, aula):
        if carrera == "":
            carrera = None
        if edificio == "":
            edificio = None
        if aula == "":
            aula = None
        self.cursor.callproc("get_materias_eventos_asignados", [carrera, edificio, aula])
        self.conn.commit()
        colums = [descr.name for descr in self.cursor.description]
        rows = [row for row in self.cursor.fetchall()]
        data = {
            "columns": colums,
            "rows": rows
        }
        return data

    def insert_asignacion(self, aula, dia, comienzo, fin, materia=None, evento=None):
        if evento == "":
            evento = None
        if materia == "":
            materia = None
        result = self.cursor.callproc(
            "insert_asignacion", [aula, dia, comienzo, fin, materia, evento])
        self.conn.commit()
        return result

    def update_asignacion(self, id, aula=None, materia=None, evento=None, dia=None, comienzo=None, fin=None):
        if evento == "":
            evento = None
        if materia == "":
            materia = None
        result = self.cursor.callproc(
            "update_asignacion", [id, aula, materia, evento, dia, comienzo, fin])
        self.conn.commit()
        if (result != 0):
            return False
        return True

    def delete_asignacion(self, id):
        result = self.cursor.callproc("delete_asignacion", [id])
        self.conn.commit()
        if (result != 0):
            return False
        return True

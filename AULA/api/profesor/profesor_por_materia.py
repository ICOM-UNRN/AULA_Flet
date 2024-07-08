import psycopg2
import os

class Profesor_por_materia():
    def __init__(self, conn : psycopg2.connect):
        self.conn : psycopg2.connect = conn
        self.cursor = self.conn.cursor()

    def get_profesores_por_materia(self):
        self.cursor.execute('SELECT * FROM profesor_por_materia')
        colums = [descr.name for descr in self.cursor.description]
        rows = [row for row in self.cursor.fetchall()]
        data = {
            "columns" : colums,
            "rows" : rows
        }
        return data

    def get_profesor_por_materia(self, materia : int):
        result = self.cursor.callproc("get_profesor_por_materia", [materia])
        self.conn.commit()
        return result

    def insert_profesor_por_materia(self, materia : int, profesor : int, cant_alumnos : int, tipo_clase : str, activo : bool):
        self.cursor.callproc("insert_profesor_por_materia", [materia, profesor, cant_alumnos, tipo_clase, activo])
        self.conn.commit()
        return True
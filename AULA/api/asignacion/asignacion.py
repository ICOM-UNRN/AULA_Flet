import psycopg2
import os

class Asignacion():
    def __init__(self, conn : psycopg2.connect):
        self.conn : psycopg2.connect = conn
        self.cursor = self.conn.cursor()

    def get_asignaciones(self):
        self.cursor.execute('SELECT * FROM asignacion')
        colums = [descr.name for descr in self.cursor.description]
        rows = [row for row in self.cursor.fetchall()]
        data = {
            "columns" : colums,
            "rows" : rows
        }
        return data

    def get_asignacion(self, aula):
        result = self.cursor.callproc("get_asignacion", [aula])
        self.conn.commit()
        return result

    def insert_asignacion(self, aula, dia, comienzo, fin, materia, evento):
        self.cursor.callproc("insert_asignacion", [aula, dia, comienzo, fin, materia, evento])
        self.conn.commit()
        return True
    
    def update_asignacion(self, aula, dia, comienzo, fin, materia, evento):
        result = self.cursor.callproc("update_asignacion", [aula, dia, comienzo, fin, materia, evento])
        self.conn.commit()
        if(result != 0):
            return False
        return True

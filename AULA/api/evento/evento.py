import psycopg2
import os

class Evento():
    def __init__(self, conn : psycopg2.connect):
        self.conn : psycopg2.connect = conn
        self.cursor = self.conn.cursor()

    def get_eventos(self):
        self.cursor.execute('SELECT * FROM evento')
        colums = [descr.name for descr in self.cursor.description]
        rows = [row for row in self.cursor.fetchall()]
        data = {
            "columns" : colums,
            "rows" : rows
        }
        return data

    def get_evento(self, nombre):
        result = self.cursor.callproc("get_evento", [nombre])
        self.conn.commit()
        return result

    def insert_evento(self, nombre, descripcion : str, comienzo, fin):
        self.cursor.callproc("insert_evento", [nombre, descripcion, comienzo, fin])
        self.conn.commit()
        return True
import psycopg2
import os

class Edificio():
    def __init__(self, conn : psycopg2.connect):
        self.conn : psycopg2.connect = conn
        self.cursor = self.conn.cursor()

    def get_edificios(self):
        self.cursor.execute('SELECT * FROM edificio')
        colums = [descr.name for descr in self.cursor.description]
        rows = [row for row in self.cursor.fetchall()]
        data = {
            "columns" : colums,
            "rows" : rows
        }
        return data

    def get_edificio(self, nombre):
        result = self.cursor.callproc("get_edificio", [nombre])
        self.conn.commit()
        return result

    def insert_edificio(self, nombre, direccion, altura):
        self.cursor.callproc("insert_edificio", [nombre, direccion, altura])
        self.conn.commit()
        return True
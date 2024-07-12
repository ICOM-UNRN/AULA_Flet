import psycopg2
import os

class Aula():
    def __init__(self, conn : psycopg2.connect):
        self.conn : psycopg2.connect = conn
        self.cursor = self.conn.cursor()

    def get_aulas(self):
        self.cursor.execute('SELECT * FROM aula')
        colums = [descr.name for descr in self.cursor.description]
        rows = [row for row in self.cursor.fetchall()]
        data = {
            "columns" : colums,
            "rows" : rows
        }
        return data

    def get_aula(self, nombre):
        result = self.cursor.callproc("get_aula", [nombre])
        self.conn.commit()
        return result

    def insert_aula(self, edificio, nombre):
        result = self.cursor.callproc("insert_aula", [edificio, nombre])
        self.conn.commit()
        return result
    
    def update_aula(self, id, nombre = None, edificio = None):
        result = self.cursor.callproc("update_aula", [id, nombre, edificio])
        self.conn.commit()
        if(result != 0):
            return False
        return True

    def delete_aula(self, id):
        result = self.cursor.callproc("delete_aula", [id])
        self.conn.commit()
        if(result != 0):
            return False
        return True
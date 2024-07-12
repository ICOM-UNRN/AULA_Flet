import psycopg2
import os

class Recurso_por_aula():
    def __init__(self, conn : psycopg2.connect):
        self.conn : psycopg2.connect = conn
        self.cursor = self.conn.cursor()

    def get_recursos_por_aula(self):
        self.cursor.execute('SELECT * FROM recurso_por_aula')
        colums = [descr.name for descr in self.cursor.description]
        rows = [row for row in self.cursor.fetchall()]
        data = {
            "columns" : colums,
            "rows" : rows
        }
        return data

    def get_recurso_por_aula(self, id_aula : int):
        result = self.cursor.callproc("get_recurso_por_aula", [id_aula])
        self.conn.commit()
        return result

    def insert_recurso_por_aula(self, id_aula : int, id_recurso : int, cantidad : int):
        result = self.cursor.callproc("insert_recurso_por_aula", [id_aula, id_recurso, cantidad])
        self.conn.commit()
        return result
    
    def update_recurso_por_aula(self, id_aula, id_recurso, cantidad = None):
        result = self.cursor.callproc("update_recurso_por_aula", [id_aula, id_recurso, cantidad])
        self.conn.commit()
        if(result != 0):
            return False
        return True

    def delete_recurso_por_aula(self, id_aula, id_recurso):
        result = self.cursor.callproc("delete_recurso_por_aula", [id_aula, id_recurso])
        self.conn.commit()
        if(result != 0):
            return False
        return True
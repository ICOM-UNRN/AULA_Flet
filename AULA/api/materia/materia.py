import psycopg2
import os

class Materia():
    def __init__(self, conn : psycopg2.connect):
        self.conn = conn
        self.cursor = self.conn.cursor()
    
    def get_materias(self):
        self.cursor.execute('SELECT * FROM materia')
        colums = [descr.name for descr in self.cursor.description]
        rows = [row for row in self.cursor.fetchall()]
        data = {
            "columns" : colums,
            "rows" : rows
        }
        return data

    def get_materia(self, codigo_guarani):
        result = self.cursor.callproc("get_materia", [codigo_guarani])
        return result

    def insert_materia(self, codigo_guarani : str, carrera : str, nombre : str, anio : str, cuatrimestre : str, taxonomia : str, horas_semanales : str, comisiones : str ):
        self.cursor.callproc("insert_materia", [codigo_guarani, carrera, nombre, anio, cuatrimestre, taxonomia, horas_semanales, comisiones])
        self.conn.commit()
        return True
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
    
    def get_carreras(self):
        self.cursor.execute('select distinct carrera from materia;')
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
        result = self.cursor.callproc("insert_materia", [codigo_guarani, carrera, nombre, anio, cuatrimestre, taxonomia, horas_semanales, comisiones])
        self.conn.commit()
        return result
    
    def update_materia(self, id, codigo_guarani = None, carrera = None, nombre = None, anio = None, cuatrimestre = None, taxonomia = None, horas_semanales = None, comisiones = None):
        result = self.cursor.callproc("update_materia", [id, codigo_guarani, carrera, nombre, anio, cuatrimestre, taxonomia, horas_semanales, comisiones])
        self.conn.commit()
        if(result != 0):
            return False
        return True

    def delete_materia(self, id):
        result = self.cursor.callproc("delete_materia", [id])
        self.conn.commit()
        if(result != 0):
            return False
        return True
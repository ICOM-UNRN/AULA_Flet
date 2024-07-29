import psycopg2
import os

class Profesor():
    def __init__(self, conn : psycopg2.connect):
        self.conn : psycopg2.connect = conn
        self.cursor = self.conn.cursor()

    def get_profesores(self):
        self.cursor.execute('SELECT * FROM profesor')
        colums = [descr.name for descr in self.cursor.description]
        rows = [row for row in self.cursor.fetchall()]
        data = {
            "columns" : colums,
            "rows" : rows
        }
        return data

    def get_profesor(self, id : int = None, dni : int = None, nombre : str = None, apellido : str = None, condicion : str = None, categoria : str = None, dedicacion : str = None, periodo_a_cargo : str = None, horarios_disponibles : str = None):
        self.cursor.callproc("get_profesor", [id, dni, nombre, apellido, condicion, categoria, dedicacion, periodo_a_cargo, horarios_disponibles])
        self.conn.commit()
        colums = [descr.name for descr in self.cursor.description]
        rows = [row for row in self.cursor.fetchall()]
        data = {
            "columns" : colums,
            "rows" : rows
        }
        return data

    def insert_profesor(self, dni : int, nombre : str, apellido : str, condicion : str, categoria : str, dedicacion : str, periodo_a_cargo : str, horarios_disponibles : str):
        result = self.cursor.callproc("insert_profesor", [dni, nombre, apellido, condicion, categoria, dedicacion, periodo_a_cargo, horarios_disponibles])
        self.conn.commit()
        return result

    def update_profesor(self, id, documento = None, nombre = None, apellido = None, condicion = None, categoria = None, dedicacion = None, periodo_a_cargo = None, horarios_disponibles = None):
        result = self.cursor.callproc("update_profesor", [id, documento, nombre, apellido, condicion, categoria, dedicacion, periodo_a_cargo, horarios_disponibles])
        self.conn.commit()
        if(result != 0):
            return False
        return True

    def delete_profesor(self, id):
        result = self.cursor.callproc("delete_profesor", [id])
        self.conn.commit()
        if(result != 0):
            return False
        return True

if __name__ == "__main__":
    db_host = os.getenv("POSTGRES_HOST")
    db_pass = os.getenv("POSTGRES_PASSWORD")
    db_name = os.getenv("POSTGRES_DATABASE")
    db_user = os.getenv("POSTGRES_USER")
    conn = psycopg2.connect(dbname=db_name,
        user=db_user,
        password=db_pass,
        host=db_host,
        port=5432)
    profesor = Profesor(conn)
    result = profesor.get_profesor(nombre='Paola')
    print(result)
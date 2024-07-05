import psycopg2
import os

class Profesor():
    def __init__(self, conn : psycopg2.connect):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def get_profesores(self):
        result = self.cursor.callproc("public.get_profesores")
        self.conn.commit()
        return result

    def get_profesor(self, dni : int):
        result = self.cursor.callproc("public.get_profesor", [dni])
        self.conn.commit()
        return result

    def insert_profesor(self, dni : int, nombre : str, apellido : str, condicion : str, categoria : str, dedicacion : str, periodo_a_cargo : str):
        self.cursor.callproc("public.insert_profesor", [dni, nombre, apellido, condicion, categoria, dedicacion, periodo_a_cargo])
        self.conn.commit()
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
    result = profesor.get_profesor(dni= 12345678)
    print(result)
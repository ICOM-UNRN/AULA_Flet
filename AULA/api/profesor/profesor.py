import psycopg2
import os
from zope.interface import document


class Profesor():
    def __init__(self, conn: psycopg2.connect):
        self.conn: psycopg2.connect = conn
        self.cursor = self.conn.cursor()

    def get_profesores(self):
        try:
            self.cursor.execute('SELECT * FROM profesor')
            columns = [descr.name for descr in self.cursor.description]
            rows = [row for row in self.cursor.fetchall()]
            data = {
                "columns": columns,
                "rows": rows
            }
            return data
        except Exception as e:
            print(f"Error al obtener profesores: {e}")
            return None

    def get_profesor(self, id: int = None, dni: int = None, nombre: str = None, apellido: str = None, condicion: str = None, categoria: str = None, dedicacion: str = None, periodo_a_cargo: str = None, horarios_disponibles: str = None):
        try:
            self.cursor.callproc("get_profesor", [
                                 id, dni, nombre, apellido, condicion, categoria, dedicacion, periodo_a_cargo, horarios_disponibles])
            self.conn.commit()
            columns = [descr.name for descr in self.cursor.description]
            rows = [row for row in self.cursor.fetchall()]
            data = {
                "columns": columns,
                "rows": rows
            }
            return data
        except Exception as e:
            print(f"Error al obtener profesor: {e}")
            return None

    def insert_profesor(self, dni: int, nombre: str, apellido: str, condicion: str, categoria: str, dedicacion: str, periodo_a_cargo: str, horarios_disponibles: str):
        try:
            result = self.cursor.callproc("insert_profesor", [
                                          dni, nombre, apellido, condicion, categoria, dedicacion, periodo_a_cargo, horarios_disponibles])
            self.conn.commit()
            return result
        except Exception as e:
            print(f"Error al insertar profesor: {e}")
            return None

    def update_profesor(self, id, documento=None, nombre=None, apellido=None, condicion=None, categoria=None, dedicacion=None, periodo_a_cargo=None, horarios_disponibles=None):
        try:
            result = self.cursor.callproc("update_profesor", [
                                          id, documento, nombre, apellido, condicion, categoria, dedicacion, periodo_a_cargo, horarios_disponibles])
            self.conn.commit()
            if result != 0:
                return False
            return True
        except Exception as e:
            print(f"Error al actualizar profesor: {e}")
            return False

    def delete_profesor(self, id):
        try:
            result = self.cursor.callproc("delete_profesor", [id])
            self.conn.commit()
            if result != 0:
                return False
            return True
        except Exception as e:
            print(f"Error al eliminar profesor: {e}")
            return False

    def insert_or_update_profesor(self, documento, apellido, nombre, condicion, categoria, dedicacion, horarios_disponibles):
        try:
            self.cursor.execute('''
                INSERT INTO profesor (documento, apellido, nombre, condicion, categoria, dedicacion, horarios_disponibles)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (documento) DO UPDATE
                SET apellido = EXCLUDED.apellido,
                    nombre = EXCLUDED.nombre,
                    condicion = EXCLUDED.condicion,
                    categoria = EXCLUDED.categoria,
                    dedicacion = EXCLUDED.dedicacion,
                    horarios_disponibles = EXCLUDED.horarios_disponibles
            ''', (documento, apellido, nombre, condicion, categoria, dedicacion, horarios_disponibles))
            self.conn.commit()
        except Exception as e:
            print(f"Error al insertar o actualizar profesor: {e}")


if __name__ == "__main__":
    db_host = os.getenv("POSTGRES_HOST")
    db_pass = os.getenv("POSTGRES_PASSWORD")
    db_name = os.getenv("POSTGRES_DATABASE")
    db_user = os.getenv("POSTGRES_USER")

    try:
        conn = psycopg2.connect(
            dbname=db_name, user=db_user, password=db_pass, host=db_host, port=5432)
        profesor = Profesor(conn)
        result = profesor.get_profesor(nombre='Paola')
        print(result)
    except Exception as e:
        print(f"Error al conectar con la base de datos: {e}")
    finally:
        if conn:
            conn.close()

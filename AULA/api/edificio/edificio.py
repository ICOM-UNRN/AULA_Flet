import psycopg2
import os


class Edificio():
    def __init__(self, conn: psycopg2.connect):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def get_edificios(self):
        try:
            self.cursor.execute('SELECT * FROM edificio')
            columns = [descr.name for descr in self.cursor.description]
            rows = [row for row in self.cursor.fetchall()]
            data = {
                "columns": columns,
                "rows": rows
            }
            return data
        except Exception as e:
            print(f"Error al obtener edificios: {e}")
            return None

    def get_edificio(self, nombre):
        try:
            self.cursor.callproc("get_edificio", [nombre])
            result = self.cursor.fetchall()
            self.conn.commit()
            return result
        except Exception as e:
            print(f"Error al obtener edificio: {e}")
            return None

    def insert_edificio(self, nombre, direccion, altura):
        try:
            self.cursor.callproc("insert_edificio", [
                                 nombre, direccion, altura])
            self.conn.commit()
        except Exception as e:
            print(f"Error al insertar edificio: {e}")
            self.conn.rollback()

    def update_edificio(self, id, nombre=None, direccion=None, altura=None):
        try:
            self.cursor.callproc("update_edificio", [
                                 id, nombre, direccion, altura])
            self.conn.commit()
            # Verificar si se realizó alguna actualización
            if self.cursor.rowcount == 0:
                return False
            return True
        except Exception as e:
            print(f"Error al actualizar edificio: {e}")
            self.conn.rollback()
            return False

    def delete_edificio(self, id):
        try:
            self.cursor.callproc("delete_edificio", [id])
            self.conn.commit()
            # Verificar si se realizó alguna eliminación
            if self.cursor.rowcount == 0:
                return False
            return True
        except Exception as e:
            print(f"Error al eliminar edificio: {e}")
            self.conn.rollback()
            return False

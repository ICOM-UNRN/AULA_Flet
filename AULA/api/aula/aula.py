import psycopg2
import os


class Aula():
    def __init__(self, conn: psycopg2.connect):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def get_aulas(self):
        try:
            self.cursor.execute('SELECT * FROM aula')
            columns = [descr.name for descr in self.cursor.description]
            rows = [row for row in self.cursor.fetchall()]
            data = {
                "columns": columns,
                "rows": rows
            }
            return data
        except Exception as e:
            print(f"Error al obtener aulas: {e}")
            return None

    def get_aula(self, nombre):
        try:
            self.cursor.callproc("get_aula", [nombre])
            result = self.cursor.fetchall()
            self.conn.commit()
            return result
        except Exception as e:
            print(f"Error al obtener aula: {e}")
            return None

    def insert_aula(self, edificio, nombre):
        try:
            self.cursor.callproc("insert_aula", [edificio, nombre])
            self.conn.commit()
        except Exception as e:
            print(f"Error al insertar aula: {e}")
            self.conn.rollback()

    def update_aula(self, id, nombre=None, edificio=None):
        try:
            self.cursor.callproc("update_aula", [id, nombre, edificio])
            self.conn.commit()
            # Verificar si se realizó alguna actualización
            if self.cursor.rowcount == 0:
                return False
            return True
        except Exception as e:
            print(f"Error al actualizar aula: {e}")
            self.conn.rollback()
            return False

    def delete_aula(self, id):
        try:
            self.cursor.callproc("delete_aula", [id])
            self.conn.commit()
            # Verificar si se realizó alguna eliminación
            if self.cursor.rowcount == 0:
                return False
            return True
        except Exception as e:
            print(f"Error al eliminar aula: {e}")
            self.conn.rollback()
            return False

import os
import psycopg2


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
            self.cursor.callproc("get_profesor",
                                [id, dni, nombre, apellido, condicion, categoria, dedicacion, periodo_a_cargo, horarios_disponibles])
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
            self.cursor.execute('''
                INSERT INTO profesor (dni, nombre, apellido, condicion, categoria, dedicacion, periodo_a_cargo, horarios_disponibles)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (dni, nombre, apellido, condicion, categoria, dedicacion, periodo_a_cargo, horarios_disponibles))
            self.conn.commit()
        except Exception as e:
            print(f"Error al insertar profesor: {e}")
            self.conn.rollback()  # Rollback en caso de error

    def update_profesor(self, id, documento=None, nombre=None, apellido=None, condicion=None, categoria=None, dedicacion=None, periodo_a_cargo=None, horarios_disponibles=None):
        try:
            self.cursor.execute('''
                UPDATE profesor
                SET documento = COALESCE(%s, documento),
                    nombre = COALESCE(%s, nombre),
                    apellido = COALESCE(%s, apellido),
                    condicion = COALESCE(%s, condicion),
                    categoria = COALESCE(%s, categoria),
                    dedicacion = COALESCE(%s, dedicacion),
                    periodo_a_cargo = COALESCE(%s, periodo_a_cargo),
                    horarios_disponibles = COALESCE(%s, horarios_disponibles)
                WHERE id = %s
            ''', (documento, nombre, apellido, condicion, categoria, dedicacion, periodo_a_cargo, horarios_disponibles, id))
            self.conn.commit()
            return self.cursor.rowcount > 0  # Retorna True si se actualizó alguna fila
        except Exception as e:
            print(f"Error al actualizar profesor: {e}")
            self.conn.rollback()  # Rollback en caso de error
            return False

    def delete_profesor(self, id):
        try:
            self.cursor.execute("DELETE FROM profesor WHERE id = %s", [id])
            self.conn.commit()
            return self.cursor.rowcount > 0  # Retorna True si se eliminó alguna fila
        except Exception as e:
            print(f"Error al eliminar profesor: {e}")
            self.conn.rollback()  # Rollback en caso de error
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
            self.conn.rollback()  # Rollback en caso de error


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

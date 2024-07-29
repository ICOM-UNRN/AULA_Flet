import psycopg2
import os


class Materia():
    def __init__(self, conn: psycopg2.connect):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def get_materias(self):
        try:
            self.cursor.execute('SELECT * FROM materia')
            columns = [descr.name for descr in self.cursor.description]
            rows = [row for row in self.cursor.fetchall()]
            data = {
                "columns": columns,
                "rows": rows
            }
            return data
        except Exception as e:
            print(f"Error al obtener materias: {e}")
            return None

    def get_carreras(self):
        try:
            self.cursor.execute('SELECT DISTINCT carrera FROM materia')
            columns = [descr.name for descr in self.cursor.description]
            rows = [row for row in self.cursor.fetchall()]
            data = {
                "columns": columns,
                "rows": rows
            }
            return data
        except Exception as e:
            print(f"Error al obtener carreras: {e}")
            return None

    def get_materia(self, codigo_guarani):
        try:
            self.cursor.callproc("get_materia", [codigo_guarani])
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print(f"Error al obtener materia: {e}")
            return None

    def insert_materia(self, codigo_guarani: str, carrera: str, nombre: str, anio: str, cuatrimestre: str, taxonomia: str, horas_semanales: str, alumnos_esperados: int, comisiones: str):
        try:
            result = self.cursor.callproc("insert_materia", [
                                          codigo_guarani, carrera, nombre, anio, cuatrimestre, taxonomia, horas_semanales, alumnos_esperados, comisiones])
            self.conn.commit()
            return result
        except Exception as e:
            print(f"Error al insertar materia: {e}")
            return None

    def update_materia(self, codigo_guarani: str, carrera: str, nombre: str, anio: str, cuatrimestre: str, taxonomia: str, horas_semanales: str, alumnos_esperados: int, comisiones: str):
        try:
            result = self.cursor.callproc("update_materia", [
                                          id, codigo_guarani, carrera, nombre, anio, cuatrimestre, taxonomia, horas_semanales, alumnos_esperados, comisiones])
            self.conn.commit()
            if result != 0:
                return False
            return True
        except Exception as e:
            print(f"Error al actualizar materia: {e}")
            return False

    def delete_materia(self, id):
        try:
            result = self.cursor.callproc("delete_materia", [id])
            self.conn.commit()
            if result != 0:
                return False
            return True
        except Exception as e:
            print(f"Error al eliminar materia: {e}")
            return False

    def insert_or_update_materia(self, codigo_guarani: str, carrera: str, nombre: str, anio: str, cuatrimestre: str, taxonomia: str, horas_semanales: str, alumnos_esperados: int, comisiones: str):
        try:
            self.cursor.execute('''
                INSERT INTO materia (codigo_guarani, carrera, nombre, anio, cuatrimestre, taxonomia, horas_semanales, alumnos_esperados, comisiones)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (codigo_guarani) DO UPDATE
                SET carrera = EXCLUDED.carrera,
                    nombre = EXCLUDED.nombre,
                    anio = EXCLUDED.anio,
                    cuatrimestre = EXCLUDED.cuatrimestre,
                    taxonomia = EXCLUDED.taxonomia,
                    horas_semanales = EXCLUDED.horas_semanales,
                    alumnos_esperados = EXCLUDED.alumnos_esperados,
                    comisiones = EXCLUDED.comisiones
            ''', (codigo_guarani, carrera, nombre, anio, cuatrimestre, taxonomia, horas_semanales, alumnos_esperados, comisiones))
            self.conn.commit()
        except Exception as e:
            print(f"Error al insertar o actualizar materia: {e}")


if __name__ == "__main__":
    db_host = os.getenv("POSTGRES_HOST")
    db_pass = os.getenv("POSTGRES_PASSWORD")
    db_name = os.getenv("POSTGRES_DATABASE")
    db_user = os.getenv("POSTGRES_USER")

    try:
        conn = psycopg2.connect(
            dbname=db_name, user=db_user, password=db_pass, host=db_host, port=5432)
        materia = Materia(conn)
        result = materia.get_materias()
        print(result)
    except Exception as e:
        print(f"Error al conectar con la base de datos: {e}")
    finally:
        if conn:
            conn.close()

import psycopg2


class Profesor_por_materia():
    def __init__(self, conn: psycopg2.connect):
        self.conn: psycopg2.connect = conn
        self.cursor = self.conn.cursor()

    def get_profesores_por_materia(self):
        try:
            self.cursor.execute('SELECT * FROM profesor_por_materia')
            columns = [descr.name for descr in self.cursor.description]
            rows = [row for row in self.cursor.fetchall()]
            data = {
                "columns": columns,
                "rows": rows
            }
            return data
        except psycopg2.Error as e:
            print(f"Error al obtener profesores por materia: {e}")
            return None

    def get_profesor_por_materia(self, materia: int):
        try:
            result = self.cursor.callproc(
                "get_profesor_por_materia", [materia])
            self.conn.commit()
            return result
        except psycopg2.Error as e:
            print(f"Error al obtener profesor por materia: {e}")
            return None

    def insert_profesor_por_materia(self, materia: int, profesor: int, cant_alumnos: int, tipo_clase: str, activo: bool):
        try:
            result = self.cursor.callproc("insert_profesor_por_materia", [
                                          materia, profesor, cant_alumnos, tipo_clase, activo])
            self.conn.commit()
            return result
        except psycopg2.Error as e:
            print(f"Error al insertar profesor por materia: {e}")
            return None

    def update_profesor_por_materia(self, id_materia, id_profesor, alumnos_esperados=None, tipo_clase=None, archivo=None):
        try:
            result = self.cursor.callproc("update_profesor_por_materia", [
                                          id_materia, id_profesor, alumnos_esperados, tipo_clase, archivo])
            self.conn.commit()
            if result != 0:
                return False
            return True
        except psycopg2.Error as e:
            print(f"Error al actualizar profesor por materia: {e}")
            return False

    def delete_profesor_por_materia(self, id_materia, id_profesor):
        try:
            result = self.cursor.callproc("delete_profesor_por_materia", [
                                          id_materia, id_profesor])
            self.conn.commit()
            if result != 0:
                return False
            return True
        except psycopg2.Error as e:
            print(f"Error al eliminar profesor por materia: {e}")
            return False

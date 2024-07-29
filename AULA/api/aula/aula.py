import psycopg2


class Aula():
    def __init__(self, conn: psycopg2.connect):
        self.conn: psycopg2.connect = conn
        self.cursor = self.conn.cursor()

    def get_aulas(self):
        self.cursor.execute('SELECT * FROM aula')
        columns = [descr.name for descr in self.cursor.description]
        rows = [row for row in self.cursor.fetchall()]
        data = {
            "columns": columns,
            "rows": rows
        }
        return data

    def get_aula(self, nombre):
        result = self.cursor.callproc("get_aula", [nombre])
        self.conn.commit()
        return result

    def insert_aula(self, nombre, capacidad_maxima, edificio, disponibilidad=None):
        # Asegúrate de que la cantidad y tipo de parámetros coincidan con la definición de la función en la base de datos
        if disponibilidad is None:
            self.cursor.callproc(
                "insert_aula", [nombre, capacidad_maxima, edificio])
        else:
            self.cursor.callproc(
                "insert_aula", [nombre, capacidad_maxima, edificio, disponibilidad])
        self.conn.commit()

    def update_aula(self, id, nombre=None, edificio=None, capacidad=None):
        try:
            self.cursor.callproc(
                "update_aula", [id, nombre, edificio, capacidad])
            self.conn.commit()
        except Exception as e:
            print(f"Error al actualizar aula: {e}")
            self.conn.rollback()

    def delete_aula(self, id):
        try:
            self.cursor.callproc("delete_aula", [id])
            self.conn.commit()
        except Exception as e:
            print(f"Error al eliminar aula: {e}")
            self.conn.rollback()

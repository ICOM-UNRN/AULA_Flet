import psycopg2

class Recurso():
    def __init__(self, conn : psycopg2.connect):
        self.conn = conn
        self.cursor = self.conn.cursor()
    
    def get_recursos(self):
        self.cursor.execute('SELECT * FROM recurso')
        colums = [descr.name for descr in self.cursor.description]
        rows = [row for row in self.cursor.fetchall()]
        data = {
            "columns" : colums,
            "rows" : rows
        }
        return data

    def get_recurso(self, id_recurso):
        result = self.cursor.callproc("get_recurso", [id_recurso])
        return result

    def insert_recurso(self, nombre : str, descripcion : str):
        result = self.cursor.callproc("insert_recurso", [nombre, descripcion])
        self.conn.commit()
        return result
    
    def update_recurso(self, id, nombre = None, descripcion = None):
        result = self.cursor.callproc("update_recurso", [id, nombre, descripcion])
        self.conn.commit()
        if(result != 0):
            return False
        return True

    def delete_recurso(self, id):
        result = self.cursor.callproc("delete_recurso", [id])
        self.conn.commit()
        if(result != 0):
            return False
        return True
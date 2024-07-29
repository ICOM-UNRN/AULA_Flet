import psycopg2
from api.aula.aula import Aula
from api.edificio.edificio import Edificio


def main():
    # Configura la conexión a la base de datos
    conn = psycopg2.connect(
        dbname="verceldb",
        user="default",
        password="vseaL4xSbR3Q",
        host="ep-super-mouse-a4hq4rqf-pooler.us-east-1.aws.neon.tech",
        port="5432"
    )

    try:
        # Crear instancias de las clases
        aula_db = Aula(conn)
        edificio_db = Edificio(conn)

        # Verificar si el edificio "Anasagasti II" existe
        edificio_nombre = "Anasagasti II"
        edificios = edificio_db.get_edificios()['rows']
        edificios_nombres = [edificio[1] for edificio in edificios]

        if edificio_nombre not in edificios_nombres:
            # Insertar el edificio si no existe
            edificio_db.insert_edificio(
                edificio_nombre, "Direccion ejemplo", 5)

        # Obtener el id del edificio "Anasagasti II"
        edificios = edificio_db.get_edificios()['rows']
        edificio_id = next(
            edificio[0] for edificio in edificios if edificio[1] == edificio_nombre)

        # Insertar aulas
        aulas = [
            {"nombre": f"Aula {i+1}", "capacidad_maxima": 30,
                "edificio": edificio_id,  # Usar el ID del edificio
                "disponibilidad": '{"lunes": ["08-10", "10-12"], "martes": ["08-10"]}'}
            for i in range(7)
        ]

        for aula in aulas:
            aula_db.insert_aula(
                aula["nombre"], aula["capacidad_maxima"], aula["edificio"], aula["disponibilidad"])

        print("Aulas y edificios inicializados exitosamente.")

    except Exception as e:
        print(f"Error en la inicialización: {e}")

    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    main()

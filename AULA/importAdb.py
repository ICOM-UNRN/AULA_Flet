import json
import sys
import psycopg2
from api.materia.materia import Materia
from api.profesor.profesor import Profesor
from api.profesor.profesor_por_materia import Profesor_por_materia
from catador.app.src.catador2 import main as main_catador

sys.stdout.reconfigure(encoding='ISO-8859-1')
# Conexión a la base de datos


def connect_db():
    try:
        conn = psycopg2.connect(
            dbname="verceldb",
            user="default",
            password="vseaL4xSbR3Q",
            host="ep-super-mouse-a4hq4rqf-pooler.us-east-1.aws.neon.tech",
            port="5432"
        )
        return conn
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None


def importar_profesores(profesor_db, archivo_profesores):
    try:
        with open(archivo_profesores, 'r', encoding='utf-8') as file:
            profesores = json.load(file)
            for profesor in profesores:
                profesor_db.insert_or_update_profesor(
                    profesor['dni'],
                    profesor['apellido'],
                    profesor['nombre'],
                    profesor['condicion'],
                    profesor['categoria'],
                    profesor['dedicacion'],
                    profesor['horarios_disponibles']
                )
        print("Importación de profesores completada.")
    except Exception as e:
        print(f"Error al importar profesores: {e}")


def importar_materias(materia_db, archivo_materias):
    try:
        with open(archivo_materias, 'r', encoding='utf-8') as file:
            materias = json.load(file)
            for materia in materias:
                cuatrimestre = int(materia['cuatrimestre'][13:])

                materia_db.insert_or_update_materia(
                    materia['codigo_guarani'],
                    materia['carrera'],
                    materia['nombre'],
                    materia['anio'],
                    cuatrimestre,
                    materia['taxonomia'],
                    materia['horas_semanales'],
                    materia['alumnos_esperados'],
                    materia['comisiones']
                )
        print("Importación de materias completada.")
    except Exception as e:
        print(f"Error al importar materias: {e}")


def importar_profesor_por_materia(profesor_por_materia_db, archivo_profesor_por_materia, materia_db, profesor_db):
    try:
        with open(archivo_profesor_por_materia, 'r', encoding='utf-8') as file:
            asignaciones = json.load(file)

            # Obtener todos los IDs de materias y profesores
            materias = materia_db.get_materias()['rows']
            profesores = profesor_db.get_profesores()['rows']

            materia_id_map = {materia[1]: materia[0]
                              for materia in materias}  # {codigo_guarani: id}
            profesor_id_map = {profesor[1]: profesor[0]
                               for profesor in profesores}  # {dni: id}

            for asignacion in asignaciones:
                materia_codigo_guarani = asignacion['materia']
                profesor_dni = asignacion['profesor']

                materia_id = materia_id_map.get(materia_codigo_guarani)
                profesor_id = profesor_id_map.get(profesor_dni)

                if materia_id is None:
                    print(f"Materia con código {
                          materia_codigo_guarani} no encontrada.")
                    continue

                if profesor_id is None:
                    print(f"Profesor con DNI {profesor_dni} no encontrado.")
                    continue

                # Convertir 'activo' a booleano si es necesario
                activo = asignacion['activo']
                if isinstance(activo, str):
                    activo = activo.lower() in ['true', '1']

                profesor_por_materia_db.insert_profesor_por_materia(
                    materia_id,
                    profesor_id,
                    # Asegurarse de que sea un entero
                    int(asignacion['cant_alumnos']),
                    asignacion['tipo_clase'],
                    activo
                )

        print("Importación de asignaciones profesor por materia completada.")
    except Exception as e:
        print(f"Error al importar asignaciones profesor por materia: {e}")


def main(path : str):
    conn = connect_db()
    if conn is None:
        return

    profesor_db = Profesor(conn)
    materia_db = Materia(conn)
    profesor_por_materia_db = Profesor_por_materia(conn)
    nombre_archivo = path
    main_catador(nombre_archivo)
    archivo_profesores = 'archivos_generados/profesores.json'
    archivo_materias = 'archivos_generados/materias.json'
    archivo_profesor_por_materia = 'archivos_generados/profesor_por_materia.json'

    importar_profesores(profesor_db, archivo_profesores)
    importar_materias(materia_db, archivo_materias)
    importar_profesor_por_materia(
        profesor_por_materia_db, archivo_profesor_por_materia, materia_db, profesor_db
    )

    conn.close()
    print("Se terminaron de importar los datos.")

if __name__ == "__main__":
    main()

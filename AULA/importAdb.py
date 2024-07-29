import json
import os
from api.materia.materia import Materia
from api.profesor.profesor import Profesor
import psycopg2
import re

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
                # # Remover todo texto que no sea un número de cuatrimestre
                # cuatrimestre = re.sub(r'\D', '', materia['cuatrimestre'])
                # # Convertir cuatrimestre a entero
                # cuatrimestre = int(cuatrimestre) if cuatrimestre else 0
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


def main():
    conn = connect_db()
    if conn is None:
        return

    profesor_db = Profesor(conn)
    materia_db = Materia(conn)

    archivo_profesores = 'AULA/archivos_generados/profesores.json'
    archivo_materias = 'AULA/archivos_generados/materias.json'

    importar_profesores(profesor_db, archivo_profesores)
    importar_materias(materia_db, archivo_materias)

    conn.close()


if __name__ == "__main__":
    main()

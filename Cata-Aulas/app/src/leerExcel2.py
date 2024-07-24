import pandas as pd
import csv
import json


def leer_excel(nombre_archivo):
    try:
        # Leer el archivo Excel
        df = pd.read_excel(nombre_archivo)

        # Diccionarios para almacenar datos procesados
        carreras_data = {}
        profesores_data = {}
        materias_data = {}
        materias_set = set()  # Conjunto para evitar duplicados de materias

        # Procesar cada fila del DataFrame
        for index, row in df.iterrows():
            codigo_guarani = row['Código Guaraní']
            nombre_materia = row['Materia']
            año = row['Año']
            cuatrimestre = row['Cuatrimestre']
            taxonomia = row['Taxonomía']
            horas_semanales = row['Horas Semanales']
            alumnos_esperados = row['Alumnos Esperados']
            comisiones = row['Comisiones']
            tipo_clase = row['Tipo de clase']
            horas_frente_curso = row['Horas frente al curso']
            carrera = row['Carrera']

            dni_profesor = row['DNI Docente']
            apellido_profesor = row['Apellido Docente']
            nombre_profesor = row['Nombre Docente']
            condicion_profesor = row['Condición']
            categoria_profesor = row['Categoría']
            dedicacion_profesor = row['Dedicación']
            horarios_disponibles = row['Horarios Disponibles']

            # Procesar datos para carreras
            if carrera not in carreras_data:
                carreras_data[carrera] = []
            carreras_data[carrera].append(codigo_guarani)

            # Procesar datos para profesores
            if dni_profesor not in profesores_data:
                profesores_data[dni_profesor] = {
                    "dni": dni_profesor,
                    "apellido": apellido_profesor,
                    "nombre": nombre_profesor,
                    "condicion": condicion_profesor,
                    "categoria": categoria_profesor,
                    "dedicacion": dedicacion_profesor,
                    "horarios_disponibles": horarios_disponibles,
                    "materias": set()  # Utilizamos un conjunto para evitar duplicados
                }
            # Agregar materia a la lista de materias del profesor si no está ya presente
            profesores_data[dni_profesor]["materias"].add(nombre_materia)

            # Procesar datos para materias, evitando duplicados
            materia_key = (codigo_guarani, nombre_materia, año, cuatrimestre)
            if materia_key not in materias_set:
                materia_data = {
                    "codigo_guarani": codigo_guarani,
                    "nombre": nombre_materia,
                    "carrera": carrera,
                    "año": año,
                    "cuatrimestre": cuatrimestre,
                    "taxonomia": taxonomia,
                    "horas_semanales": horas_semanales,
                    "alumnos_esperados": alumnos_esperados,
                    "comisiones": comisiones,
                    "tipo_clase": tipo_clase,
                    "horas_frente_curso": horas_frente_curso,
                    "profesores": []  # Lista para almacenar profesores de la materia
                }
                materias_data[materia_key] = materia_data
                materias_set.add(materia_key)
            # Agregar profesor a la lista de profesores de la materia (nombre, apellido y categoría)
            materias_data[materia_key]["profesores"].append({
                "categoria": categoria_profesor,
                "nombre": nombre_profesor,
                "apellido": apellido_profesor
            })

        # Convertir diccionarios a listas
        carreras_list = [{"carrera": k, "codigo_guarani": v}
                         for k, v in carreras_data.items()]
        profesores_list = [
            {
                "dni": profesor["dni"],
                "apellido": profesor["apellido"],
                "nombre": profesor["nombre"],
                "condicion": profesor["condicion"],
                "categoria": profesor["categoria"],
                "dedicacion": profesor["dedicacion"],
                "horarios_disponibles": profesor["horarios_disponibles"],
                # Convertir el conjunto de materias a lista
                "materias": list(profesor["materias"])
            }
            for profesor in profesores_data.values()
        ]
        materias_list = list(materias_data.values())

        # Guardar datos en archivos CSV y JSON
        save_data_to_csv("carrera.csv", carreras_list)
        save_data_to_json("carrera.json", carreras_list)
        save_data_to_csv("profesores.csv", profesores_list)
        save_data_to_json("profesores.json", profesores_list)
        save_data_to_csv("materias.csv", materias_list)
        save_data_to_json("materias.json", materias_list)

    except pd.errors.EmptyDataError:
        print("El archivo Excel está vacío.")
    except FileNotFoundError:
        print(f"No se encontró el archivo: {nombre_archivo}")
    except Exception as e:
        print(f"Error al procesar el archivo Excel: {e}")


def save_data_to_csv(filename, data):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = list(data[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def save_data_to_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=4)


if __name__ == "__main__":
    leer_excel(r'etc\dist2cuadH.xlsx')

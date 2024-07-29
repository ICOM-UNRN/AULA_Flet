import os
import psycopg2
from api.materia.materia import Materia
from api.profesor.profesor import Profesor
from api.aula.aula import Aula
from api.edificio.edificio import Edificio
from api.asignacion.asignacion import Asignacion
from api.profesor.profesor_por_materia import Profesor_por_materia
from collections import defaultdict
import csv
import json


def main():
    conn = psycopg2.connect(
        dbname="verceldb",
        user="default",
        password="vseaL4xSbR3Q",
        host="ep-super-mouse-a4hq4rqf-pooler.us-east-1.aws.neon.tech",
        port="5432"
    )

    materia_db = Materia(conn)
    profesor_db = Profesor(conn)
    aula_db = Aula(conn)
    edificio_db = Edificio(conn)
    asignacion_db = Asignacion(conn)
    profesor_por_materia_db = Profesor_por_materia(conn)

    profesores2 = []
    materias2 = []
    try:
        aulas = aula_db.get_aulas()['rows']
        materias = materia_db.get_materias()
        profesores = profesor_db.get_profesores()['rows']

        # Obtener la relación entre profesores y materias
        profesores_por_materia = profesor_por_materia_db.get_profesores_por_materia()
        if not profesores_por_materia:
            print("No se pudieron obtener los profesores por materia.")
            return

        # Imprimir datos obtenidos para depuración
        print("Datos obtenidos de 'get_profesores_por_materia':")
        print(profesores_por_materia)

        # Procesar materias
        if isinstance(materias, dict) and 'columns' in materias and 'rows' in materias:
            columnas_materias = materias['columns']
            columnas_profesores_por_materia = profesores_por_materia['columns']
            for materia in materias['rows']:
                materia_dict = dict(zip(columnas_materias, materia))
                materia_id = materia_dict.get('id')
                # Acceder a profesores por materia
                profesores_materia = [
                    p[columnas_profesores_por_materia.index('id_profesor')]
                    for p in profesores_por_materia['rows']
                    if p[columnas_profesores_por_materia.index('id_materia')] == materia_id
                ]
                materia_dict['profesores'] = profesores_materia
                materias2.append(materia_dict)
            materias = materias2
        else:
            print(f"Advertencia: Formato inesperado de materias: {
                  type(materias)}")
            return  # Detener ejecución si el formato es incorrecto

        # Depuración: Mostrar el tipo de datos de las materias
        depurar_materias(materias)
        verificar_datos_materias(materias)

        columnas_profesores = profesor_db.get_profesores()['columns']
        for profesor in profesores:
            profesores2.append(
                {key: value for key, value in zip(columnas_profesores, profesor)})
        profesores = profesores2

        columnas_aulas = aula_db.get_aulas()['columns']
        aulas = [dict(zip(columnas_aulas, aula)) for aula in aulas]

        horarios_disponibles_profesores = organizar_horarios_profesores(
            profesores)
        horarios_disponibles_aulas = organizar_horarios_aulas(aulas)

        materias_reordenadas = reordenar_materias_por_alumnos(materias)

        sugerencias_helper = asignacion_helper(
            materias_reordenadas, horarios_disponibles_profesores, horarios_disponibles_aulas, 'Anasagasti II'
        )

        # escribir_sugerencias(sugerencias_helper, 'Sugerencias.csv')
        print("Asignación automática completada. Las sugerencias se han guardado en 'Sugerencias.csv'.")

        # Guardar asignaciones en la base de datos
        guardar_asignaciones_db(sugerencias_helper, asignacion_db)
        print("Asignaciones guardadas en la base de datos.")

    except Exception as e:
        print(f"Error en la ejecución: {e}")

    finally:
        if conn:
            conn.close()


def depurar_materias(materias):
    for materia in materias:
        print(f"Tipo de materia: {type(materia)}")
        if isinstance(materia, dict):
            print(f"Claves en el diccionario de materia: {
                  list(materia.keys())}")
        else:
            print(f"Advertencia: Se esperaba un diccionario, pero se obtuvo {
                  type(materia)}")


def organizar_horarios_profesores(profesores):
    if not isinstance(profesores, list):
        raise TypeError("Se esperaba una lista de profesores.")
    for profesor in profesores:
        if not isinstance(profesor, dict):
            raise TypeError(
                "Cada elemento en la lista debe ser un diccionario.")
        if 'horarios_disponibles' not in profesor:
            raise KeyError(
                "Cada diccionario de profesor debe tener la clave 'horarios_disponibles'.")

    horarios_disponibles = defaultdict(lambda: defaultdict(list))
    for profesor in profesores:
        if 'horarios_disponibles' not in profesor:
            print(
                f"Falta 'horarios_disponibles' en los datos del profesor: {profesor}")
            continue

        profesor_horarios = defaultdict(list)
        str_copia_horarios_disponibles = profesor['horarios_disponibles']
        try:
            for bloque_dia_horas in str_copia_horarios_disponibles.split(';'):
                dia_horas = bloque_dia_horas.strip().split(',')
                dia = dia_horas[0].strip()
                for horas_rango in dia_horas[1:]:
                    horas = horas_rango.strip().split('-')
                    if len(horas) == 2:
                        hora_inicio = int(horas[0].strip())
                        hora_fin = int(horas[1].strip())
                        profesor_horarios[dia].append(
                            f"{hora_inicio}-{hora_fin}")
        except Exception as e:
            print(f"Error al procesar horarios del profesor {
                  profesor['nombre']}: {e}")

        nombre_completo = f"{profesor['nombre']} {profesor['apellido']}"
        horarios_disponibles[nombre_completo] = profesor_horarios
    return horarios_disponibles


def organizar_horarios_aulas(aulas):
    horarios_disponibles_aulas = defaultdict(lambda: defaultdict(list))
    if isinstance(aulas, dict) and 'columns' in aulas and 'rows' in aulas:
        columnas_aulas = aulas['columns']
        for aula in aulas['rows']:
            aula_dict = dict(zip(columnas_aulas, aula))
            aula_nombre = aula_dict.get('nombre')
            aula_disponibilidad = aula_dict.get('disponibilidad', '{}')
            try:
                disponibilidad_aula = json.loads(aula_disponibilidad)
                for dia, disponibilidad_horaria in disponibilidad_aula.items():
                    for rango in disponibilidad_horaria:
                        horarios_disponibles_aulas[aula_nombre][dia].append(
                            rango)
            except json.JSONDecodeError:
                print(f"Error al decodificar JSON en disponibilidad para aula {
                      aula_nombre}")
    else:
        print("Error: El formato de datos de aulas es incorrecto.")
    return horarios_disponibles_aulas


def separar_horas(horas_disponibles):
    rangos_separados = []
    for hora_rango in horas_disponibles:
        hora_inicio, hora_fin = hora_rango.split('-')
        rangos_separados.append((int(hora_inicio), int(hora_fin)))
    return rangos_separados


def separar_profesores(profesores):
    if isinstance(profesores, list):
        # Convertir a cadenas y eliminar espacios en blanco
        return [str(prof).strip() for prof in profesores]
    else:
        print("Error: 'profesores' debe ser una lista.")
        return []


def verificar_disponibilidad(profesor_nombre, horarios_profesores, horarios_aulas):
    aula_con_disponibilidad = []
    if profesor_nombre not in horarios_profesores:
        return aula_con_disponibilidad
    for dia, horas_disponibles in horarios_profesores[profesor_nombre].items():
        horas_separadas = separar_horas(horas_disponibles)
        for hora_inicio, hora_fin in horas_separadas:
            for aula, aulas_disponibles in horarios_aulas.items():
                if dia in aulas_disponibles:
                    horas_aula = [int(horas.split('-')[0])
                                  for horas in aulas_disponibles[dia]]
                    if hora_inicio in horas_aula and hora_fin in horas_aula:
                        aula_con_disponibilidad.append({
                            "Aula": aula,
                            "Dia": dia,
                            "Hora Inicio": hora_inicio,
                            "Hora Fin": hora_fin
                        })
    return aula_con_disponibilidad


def reordenar_materias_por_alumnos(materias):
    try:
        materias_reordenadas = sorted(materias, key=lambda materia: materia.get(
            'alumnos_esperados', 0), reverse=True)
    except Exception as e:
        print(f"Error al reordenar materias por número de alumnos: {e}")
        materias_reordenadas = materias

    return materias_reordenadas


def asignacion_helper(materias, horarios_profesores, horarios_aulas, edificio_predefinido):
    sugerencias = []
    for materia in materias:
        profesores_separados = separar_profesores(materia.get(
            'profesores', []))  # Usa un valor por defecto vacío
        if not profesores_separados:
            print(f"Advertencia: La clave 'profesores' está vacía o no está presente en el diccionario de materia: {
                  materia}")

        for profesor_nombre in profesores_separados:
            aulas_con_disponibilidad = verificar_disponibilidad(
                profesor_nombre, horarios_profesores, horarios_aulas)
            if aulas_con_disponibilidad:
                for aula in aulas_con_disponibilidad:
                    aula_nombre = aula['Aula']
                    aula_edificio = next(
                        (a['edificio'] for a in aulas if a['nombre'] == aula_nombre), None)
                    if aula_edificio == edificio_predefinido:
                        sugerencias.append({
                            'Carrera': materia['carrera'],
                            'Codigo Guarani': materia['codigo_guarani'],
                            'Materia': materia['nombre'],
                            'Profesor': profesor_nombre,
                            'Edificio': aula_edificio,
                            'Aula': aula['Aula'],
                            'Dia': aula['Dia'],
                            'Hora inicio': aula['Hora Inicio'],
                            'Hora fin': aula['Hora Fin']
                        })
                        break
            else:
                print(f"    {profesor_nombre} | No hay aulas disponibles")
    return sugerencias


def verificar_datos_materias(materias):
    for materia in materias:
        if 'profesores' not in materia:
            print(f"Advertencia: La clave 'profesores' no está presente en el diccionario de materia: {
                  materia}")
        else:
            print(f"Datos de materia con 'profesores': {
                  materia['profesores']}")


def escribir_sugerencias(sugerencias, archivo):
    with open(archivo, 'w', newline='', encoding='ISO-8859-1') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Carrera', 'Codigo Guarani', 'Materia', 'Edificio',
                        'Profesor', 'Aula', 'Dia', 'Hora inicio', 'Hora fin'])
        for sugerencia in sugerencias:
            writer.writerow([
                sugerencia.get('Carrera', ''),
                sugerencia.get('Codigo Guarani', ''),
                sugerencia.get('Materia', ''),
                sugerencia.get('Edificio', ''),
                sugerencia.get('Profesor', ''),
                sugerencia.get('Aula', ''),
                sugerencia.get('Dia', ''),
                sugerencia.get('Hora inicio', ''),
                sugerencia.get('Hora fin', '')
            ])


def guardar_asignaciones_db(sugerencias, asignacion_db):
    for sugerencia in sugerencias:
        aula = sugerencia['Aula']
        dia = sugerencia['Dia']
        comienzo = sugerencia['Hora inicio']
        fin = sugerencia['Hora fin']
        materia = sugerencia['Materia']
        evento = None  # Ajusta según tu lógica

        # Insertar asignación en la base de datos
        asignacion_db.insert_asignacion(
            aula, dia, comienzo, fin, materia, evento)


if __name__ == "__main__":
    main()

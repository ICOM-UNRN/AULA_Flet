import json
import csv
import unicodedata
from collections import defaultdict
from arrow import get
import psycopg2
from api.materia.materia import Materia
from api.profesor.profesor import Profesor
from api.aula.aula import Aula
from api.edificio.edificio import Edificio
from api.asignacion.asignacion import Asignacion
from api.profesor.profesor_por_materia import Profesor_por_materia


def conectar_base_datos():
    return psycopg2.connect(
        dbname="verceldb",
        user="default",
        password="vseaL4xSbR3Q",
        host="ep-super-mouse-a4hq4rqf-pooler.us-east-1.aws.neon.tech",
        port="5432"
    )


def main():
    conn = None
    try:
        conn = conectar_base_datos()

        materia_db = Materia(conn)
        profesor_db = Profesor(conn)
        aula_db = Aula(conn)
        edificio_db = Edificio(conn)
        asignacion_db = Asignacion(conn)
        profesor_por_materia_db = Profesor_por_materia(conn)

        profesores2 = []
        materias2 = []
        aulas2 = []

        # Obtener datos
        aulas = aula_db.get_aulas()['rows']
        materias = materia_db.get_materias()
        profesores = profesor_db.get_profesores()['rows']
        profesores_por_materia = profesor_por_materia_db.get_profesores_por_materia()
        asignaciones = asignacion_db.get_asignaciones()

        if not profesores_por_materia:
            print("No se pudieron obtener los profesores por materia.")
            return

        # Procesar materias
        if isinstance(materias, dict) and 'columns' in materias and 'rows' in materias:
            columnas_materias = materias['columns']
            columnas_profesores_por_materia = profesores_por_materia['columns']
            profesores_materia = []
            for materia in materias['rows']:
                materia_dict = dict(zip(columnas_materias, materia))
                materia_id = materia_dict.get('id')
                # Acceder a profesores por materia
                for p in profesores_por_materia['rows']:
                    if p[columnas_profesores_por_materia.index('id_materia')] == materia_id:
                        profesor_en_db = profesor_db.get_profesor(
                            id=p[columnas_profesores_por_materia.index('id_profesor')])
                        profesor_en_db_columns = profesor_en_db["columns"]
                        nombre_profesor = profesor_en_db['rows'][0][profesor_en_db_columns.index(
                            'nombre')] + ' ' + profesor_en_db['rows'][0][profesor_en_db_columns.index('apellido')]
                        profesores_materia.append(nombre_profesor)
                materia_dict['profesores'] = profesores_materia.copy()
                materias2.append(materia_dict)
                profesores_materia.clear()
            materias = materias2
        else:
            print(f"Advertencia: Formato inesperado de materias: {
                  type(materias)}")
            return

        # Convertir los datos de profesores y aulas a diccionarios
        columnas_profesores = profesor_db.get_profesores()['columns']
        for profesor in profesores:
            profesores2.append(
                {key: value for key, value in zip(columnas_profesores, profesor)})
        profesores = profesores2

        columnas_aulas = aula_db.get_aulas()['columns']
        aulas = convertir_datos_aulas(aula_db.get_aulas()['rows'])

        horarios_disponibles_profesores = organizar_horarios_profesores(
            profesores)
        horarios_disponibles_aulas = organizar_horarios_aulas(
            aulas, asignaciones)

        for aula in horarios_disponibles_aulas:
            print(aula, horarios_disponibles_aulas[aula])
        materias_reordenadas = reordenar_materias_por_alumnos(materias)

        sugerencias_helper, fallos_asignacion = asignacion_helper(
            materias_reordenadas, horarios_disponibles_profesores, horarios_disponibles_aulas, 'Anasagasti II'
        )

        escribir_sugerencias(sugerencias_helper,
                             fallos_asignacion, 'Sugerencias.csv')
        print("Asignación automática completada. Las sugerencias y los fallos se han guardado en 'Sugerencias.csv'.")

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


def normalizar_nombre(nombre):
    """Normaliza el nombre eliminando acentos y caracteres especiales."""
    nombre_normalizado = unicodedata.normalize(
        'NFKD', nombre).encode('ASCII', 'ignore').decode('ASCII')
    return nombre_normalizado


def organizar_horarios_profesores(profesores):
    """Organiza los horarios disponibles de los profesores en un formato adecuado."""
    if not isinstance(profesores, list):
        raise TypeError("Se esperaba una lista de profesores.")

    horarios_disponibles = defaultdict(lambda: defaultdict(list))

    for profesor in profesores:
        if not isinstance(profesor, dict):
            raise TypeError(
                "Cada elemento en la lista debe ser un diccionario.")
        if 'horarios_disponibles' not in profesor:
            raise KeyError(
                "Cada diccionario de profesor debe tener la clave 'horarios_disponibles'.")

        profesor_horarios = defaultdict(list)
        str_copia_horarios_disponibles = profesor['horarios_disponibles']

        try:
            for bloque_dia_horas in str_copia_horarios_disponibles.split(';'):
                dia_horas = bloque_dia_horas.strip().split(',')
                dia = dia_horas[0].strip()
                for horas_rango in dia_horas[1:]:
                    horas = horas_rango.strip().split('-')
                    if len(horas) == 2:
                        try:
                            hora_inicio = int(horas[0].strip())
                            hora_fin = int(horas[1].strip())
                            profesor_horarios[dia].append(
                                f"{hora_inicio}-{hora_fin}")
                        except ValueError:
                            print(f"Formato de horas incorrecto: {
                                  horas_rango}")
        except Exception as e:
            print(f"Error al procesar horarios del profesor {
                  profesor['nombre']}: {e}")

        nombre_completo = f"{profesor['nombre']} {profesor['apellido']}"
        # print(f"Horarios para el profesor {
        #       nombre_completo}: {profesor_horarios}")
        horarios_disponibles[nombre_completo] = profesor_horarios

    return horarios_disponibles


def organizar_horarios_aulas(aulas, asignaciones):
    horarios_disponibles_aulas = defaultdict(lambda: defaultdict(list))

    # Obtener la disponibilidad total inicial para cada aula
    for aula in aulas:
        aula_nombre = aula.get('nombre')
        capacidad = aula.get('capacidad', 0)

        # Asumir que la disponibilidad total es de 8 AM a 8 PM (ejemplo, ajusta según necesidad)
        horarios_disponibles_aulas[aula_nombre] = {
            'LUN': ['08-23'],
            'MAR': ['08-23'],
            'MIE': ['08-23'],
            'JUE': ['08-23'],
            'VIE': ['08-23'],
        }

    # Restar las asignaciones ya hechas
    if isinstance(asignaciones, dict) and 'rows' in asignaciones:
        for asignacion in asignaciones['rows']:
            aula_id = asignacion[1]
            dia = asignacion[4]
            hora_inicio = asignacion[5]
            hora_fin = asignacion[6]

            # Buscar el nombre del aula a partir del id
            aula_nombre = next((a['nombre']
                               for a in aulas if a['id_aula'] == aula_id), None)
            if aula_nombre and dia in horarios_disponibles_aulas:
                for i, rango in enumerate(horarios_disponibles_aulas[aula_nombre][dia]):
                    rango_inicio, rango_fin = map(int, rango.split('-'))
                    if hora_inicio >= rango_inicio and hora_fin <= rango_fin:
                        # Eliminar el rango ocupado
                        horarios_disponibles_aulas[aula_nombre][dia].pop(i)
                        break

    return horarios_disponibles_aulas


def convertir_datos_aulas(data):
    columnas = ['id_aula', 'id_edificio', 'nombre',
                'capacidad']  # Ajusta según tus datos reales
    return [dict(zip(columnas, fila)) for fila in data]


def separar_horas(horas_disponibles):
    """Convierte un rango de horas como '8-12' en una tupla de enteros (8, 12)."""
    rangos_separados = []
    for hora_rango in horas_disponibles:
        hora_inicio, hora_fin = hora_rango.split('-')
        rangos_separados.append((int(hora_inicio), int(hora_fin)))
    return rangos_separados


def separar_profesores(profesores):
    if isinstance(profesores, list):
        # Aquí puedes realizar cualquier procesamiento adicional necesario en la lista de profesores
        return profesores
    else:
        print(f"Advertencia: Se esperaba una lista de profesores, pero se obtuvo {
              type(profesores)}")
        return []


def asignacion_helper(materias, horarios_disponibles_profesores, horarios_disponibles_aulas, nombre_edificio):
    asignaciones_realizadas = []
    fallos_asignacion = []

    for materia in materias:
        materia_id = materia.get('id')
        profesores = materia.get('profesores', [])
        alumnos_esperados = materia.get('alumnos_esperados', 0)

        for profesor in profesores:
            horarios_profesor = horarios_disponibles_profesores.get(
                profesor, {})
            for dia, rangos in horarios_profesor.items():
                for rango in rangos:
                    hora_inicio, hora_fin = map(int, rango.split('-'))
                    for aula_nombre, disponibilidad in horarios_disponibles_aulas.items():
                        if dia in disponibilidad:
                            for aula_rango in disponibilidad[dia]:
                                aula_inicio, aula_fin = map(
                                    int, aula_rango.split('-'))
                                if aula_inicio <= hora_inicio and aula_fin >= hora_fin:
                                    asignaciones_realizadas.append([
                                        materia.get('carrera'),
                                        materia.get('codigo_guarani'),
                                        materia.get('nombre'),
                                        materia_id,
                                        profesor,
                                        aula_nombre,
                                        aula.get('id_aula'),
                                        dia,
                                        hora_inicio,
                                        hora_fin
                                    ])
                                    # Marcar el aula como ocupada
                                    disponibilidad[dia].remove(aula_rango)
                                    break
                            else:
                                continue
                            break
                    else:
                        continue
                    break
                else:
                    continue
                break
            else:
                fallos_asignacion.append([
                    materia.get('codigo_guarani'),
                    materia.get('nombre'),
                    profesor,
                    'No se pudo asignar aula',
                    dia,
                    hora_inicio,
                    hora_fin
                ])

    return asignaciones_realizadas, fallos_asignacion


def reordenar_materias_por_alumnos(materias):
    # Implementa la lógica para reordenar materias según el número de alumnos esperados
    return sorted(materias, key=lambda x: x.get('alumnos_esperados', 0), reverse=True)


def escribir_sugerencias(asignaciones_realizadas, fallos_asignacion, nombre_archivo):
    with open(nombre_archivo, 'w', newline='') as archivo_csv:
        writer = csv.writer(archivo_csv)
        writer.writerow(['Carrera', 'Código Guarani', 'Materia', 'Profesor',
                        'Aula', 'Día', 'Hora Inicio', 'Hora Fin', 'Estado'])

        for asignacion in asignaciones_realizadas:
            writer.writerow(asignacion + ['Asignación realizada'])

        for fallo in fallos_asignacion:
            writer.writerow(fallo + ['Fallo en asignación'])


def guardar_asignaciones_db(sugerencias, asignacion_db):
    for sugerencia in sugerencias:
        # Asegúrate de que la sugerencia tenga la longitud correcta antes de acceder a los índices
        if len(sugerencia) < 8:
            print(f"Advertencia: Datos de asignación incompletos: {
                  sugerencia}")
            continue

        # Asegúrate de que los índices se correspondan con la estructura de tu sugerencia
        # Asumiendo que la columna 'Aula' está en la posición 4
        aula = sugerencia[4]
        # Asumiendo que la columna 'Materia' está en la posición 2
        materia = sugerencia[2]
        # Asumiendo que la columna 'Día' está en la posición 5
        dia = sugerencia[5]
        # Asumiendo que la columna 'Hora Inicio' está en la posición 6
        hora_inicio = sugerencia[6]
        # Asumiendo que la columna 'Hora Fin' está en la posición 7
        hora_fin = sugerencia[7]

        # Inserta en la base de datos usando la función insert_asignacion
        asignacion_db.insert_asignacion(
            aula, dia, hora_inicio, hora_fin, materia
        )


if __name__ == "__main__":
    main()

import json
import csv
import unicodedata
from collections import defaultdict
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
                        profesor_en_db = profesor_db.get_profesor(id=p[columnas_profesores_por_materia.index('id_profesor')])
                        profesor_en_db_columns = profesor_en_db["columns"]
                        nombre_profesor = profesor_en_db['rows'][0][profesor_en_db_columns.index('nombre')]
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
        horarios_disponibles_aulas = organizar_horarios_aulas(aulas)

        materias_reordenadas = reordenar_materias_por_alumnos(materias)

        sugerencias_helper = asignacion_helper(
            materias_reordenadas, horarios_disponibles_profesores, horarios_disponibles_aulas, 'Anasagasti II'
        )

        escribir_sugerencias(sugerencias_helper, 'Sugerencias.csv')
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
        print(f"Horarios para el profesor {
              nombre_completo}: {profesor_horarios}")
        horarios_disponibles[nombre_completo] = profesor_horarios

    return horarios_disponibles


def organizar_horarios_aulas(aulas):
    horarios_disponibles_aulas = defaultdict(lambda: defaultdict(list))

    # Verificar si el formato de los datos de aulas es correcto
    if isinstance(aulas, list) and all(isinstance(aula, dict) for aula in aulas):
        for aula in aulas:
            aula_nombre = aula.get('nombre')
            aula_disponibilidad = aula.get('disponibilidad', '{}')

            try:
                disponibilidad_aula = json.loads(aula_disponibilidad)
                for dia, disponibilidad_horaria in disponibilidad_aula.items():
                    for rango in disponibilidad_horaria:
                        horarios_disponibles_aulas[aula_nombre][dia].append(
                            rango)
            except json.JSONDecodeError:
                print(f"Error al decodificar JSON en disponibilidad para aula {
                      aula_nombre}: {aula_disponibilidad}")
    else:
        print("Error: El formato de datos de aulas es incorrecto.")

    return horarios_disponibles_aulas


def convertir_datos_aulas(data):
    # Asumiendo que data es una lista de tuplas o listas
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
        # Convertir a cadenas y eliminar espacios en blanco
        return [str(prof).strip() for prof in profesores]
    else:
        print("Error: 'profesores' debe ser una lista.")
        return []


def verificar_disponibilidad(profesor_nombre, horarios_profesores, horarios_aulas):
    aula_con_disponibilidad = []

    profesor_nombre_normalizado = normalizar_nombre(profesor_nombre)

    if profesor_nombre_normalizado not in [normalizar_nombre(n) for n in horarios_profesores.keys()]:
        print(f"Advertencia: El profesor {
              profesor_nombre} no tiene horarios disponibles.")
        return aula_con_disponibilidad

    horarios_profesor = horarios_profesores[profesor_nombre]
    print(f"Horarios del profesor {profesor_nombre}: {horarios_profesor}")

    for dia, horas_disponibles in horarios_profesor.items():
        horas_separadas = separar_horas(horas_disponibles)
        print(f"Verificando disponibilidad para el día {dia} y horas {
              horas_separadas} del profesor {profesor_nombre}.")
        for hora_inicio, hora_fin in horas_separadas:
            for aula, aulas_disponibles in horarios_aulas.items():
                if dia in aulas_disponibles:
                    for rango_aula in aulas_disponibles[dia]:
                        hora_inicio_aula, hora_fin_aula = map(
                            int, rango_aula.split('-'))
                        if hora_inicio >= hora_inicio_aula and hora_fin <= hora_fin_aula:
                            aula_con_disponibilidad.append({
                                "Aula": aula,
                                "Dia": dia,
                                "Hora Inicio": hora_inicio,
                                "Hora Fin": hora_fin
                            })
                            print(f"Encontrada disponibilidad para el aula {
                                  aula} en el día {dia} y hora {hora_inicio}-{hora_fin}.")
                            break
    return aula_con_disponibilidad


def reordenar_materias_por_alumnos(materias):
    """
    Reordena la lista de materias por el número de alumnos esperados en orden descendente.
    """
    try:
        if not isinstance(materias, list):
            raise TypeError("El parámetro 'materias' debe ser una lista.")

        # Verificar que cada elemento en la lista es un diccionario
        for materia in materias:
            if not isinstance(materia, dict):
                raise TypeError(
                    "Cada elemento en la lista de materias debe ser un diccionario.")

        materias_reordenadas = sorted(materias, key=lambda materia: int(
            materia.get('alumnos_esperados', 0)), reverse=True)
        return materias_reordenadas

    except Exception as e:
        print(f"Error al reordenar materias por número de alumnos: {e}")
        return materias


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
                        (a['id_edificio'] for a in aulas if a['nombre'] == aula_nombre), None)
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

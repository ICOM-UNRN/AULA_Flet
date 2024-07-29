import psycopg2
from api.materia.materia import Materia
from api.profesor.profesor import Profesor
from api.aula.aula import Aula
from api.edificio.edificio import Edificio
from collections import defaultdict
import csv


def main():
    try:
        # Configura la conexión a la base de datos
        conn = psycopg2.connect(
            dbname="verceldb",
            user="default",
            password="vseaL4xSbR3Q",
            host="ep-super-mouse-a4hq4rqf-pooler.us-east-1.aws.neon.tech",
            port="5432"
        )

        # Crear instancias de las clases
        materia_db = Materia(conn)
        profesor_db = Profesor(conn)
        aula_db = Aula(conn)
        edificio_db = Edificio(conn)

        # Obtener los datos necesarios
        aulas = aula_db.get_aulas()['rows']
        materias = materia_db.get_materias()['rows']
        profesores = profesor_db.get_profesores()['rows']

        # Convertir tuplas a diccionarios usando los nombres de las columnas
        columnas_profesores = profesor_db.get_profesores()['columns']
        profesores = [dict(zip(columnas_profesores, profesor))
                      for profesor in profesores]

        columnas_aulas = aula_db.get_aulas()['columns']
        aulas = [dict(zip(columnas_aulas, aula)) for aula in aulas]

        columnas_materias = materia_db.get_materias()['columns']
        materias = [dict(zip(columnas_materias, materia))
                    for materia in materias]

        # Organizar horarios
        horarios_disponibles_profesores = organizar_horarios_profesores(
            profesores)
        horarios_disponibles_aulas = organizar_horarios_aulas(aulas)

        # Reordenar materias por alumnos esperados
        materias_reordenadas = reordenar_materias_por_alumnos(materias)

        # Asignar materias a aulas
        sugerencias_helper = asignacion_helper(
            materias_reordenadas, horarios_disponibles_profesores, horarios_disponibles_aulas, 'Anasagasti II'
        )

        # Escribir sugerencias en un archivo
        escribir_sugerencias(sugerencias_helper, 'Sugerencias.csv')
        print("Asignación automática completada. Las sugerencias se han guardado en 'Sugerencias.csv'.")

    except Exception as e:
        print(f"Error en la conexión o ejecución: {e}")
    finally:
        if conn:
            conn.close()


def reordenar_materias_por_alumnos(materias):
    return sorted(materias, key=lambda x: x.get('alumnos_esperados', 0) or 0, reverse=True)


def organizar_horarios_profesores(profesores):
    horarios_disponibles = defaultdict(lambda: defaultdict(list))
    for profesor in profesores:
        profesor_horarios = defaultdict(list)
        str_copia_horarios_disponibles = profesor.get(
            'horarios_disponibles', '')
        if str_copia_horarios_disponibles:
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
        nombre_completo = f"{profesor.get('nombre', '')} {
            profesor.get('apellido', '')}"
        horarios_disponibles[nombre_completo] = profesor_horarios
    return horarios_disponibles


def organizar_horarios_aulas(aulas):
    horarios_disponibles_aulas = defaultdict(lambda: defaultdict(list))
    for aula in aulas:
        disponibilidad_aula = aula.get('disponibilidad', {})
        if isinstance(disponibilidad_aula, dict):
            for dia, disponibilidad_horaria in disponibilidad_aula.items():
                if isinstance(disponibilidad_horaria, list):
                    for hora, disponible in enumerate(disponibilidad_horaria, start=8):
                        if disponible:
                            horarios_disponibles_aulas[aula['nombre']][dia].append(f"{
                                                                                   hora}")
    return horarios_disponibles_aulas


def separar_horas(horas_disponibles):
    rangos_separados = []
    for hora_rango in horas_disponibles:
        hora_inicio, hora_fin = hora_rango.split('-')
        rangos_separados.append((int(hora_inicio), int(hora_fin)))
    return rangos_separados


def separar_profesores(profesores):
    return [prof.strip() for prof in profesores.split(',')]


def verificar_disponibilidad(profesor_nombre, horarios_profesores, horarios_aulas):
    aula_con_disponibilidad = []
    if profesor_nombre not in horarios_profesores:
        return aula_con_disponibilidad
    for dia, horas_disponibles in horarios_profesores[profesor_nombre].items():
        horas_separadas = separar_horas(horas_disponibles)
        for hora_inicio, hora_fin in horas_separadas:
            for aula, aulas_disponibles in horarios_aulas.items():
                if dia in aulas_disponibles:
                    horas_aula = [int(horas)
                                  for horas in aulas_disponibles[dia]]
                    if hora_inicio in horas_aula and hora_fin in horas_aula:
                        aula_con_disponibilidad.append({
                            "Aula:": aula, "Dia:": dia, "Hora Inicio:": hora_inicio, "Hora Fin:": hora_fin
                        })
    return aula_con_disponibilidad


def asignacion_helper(materias, horarios_profesores, horarios_aulas, edificio_predefinido):
    sugerencias = []
    for materia in materias:
        profesores_separados = separar_profesores(
            materia.get('profesores', ''))
        for profesor_nombre in profesores_separados:
            aulas_con_disponibilidad = verificar_disponibilidad(
                profesor_nombre, horarios_profesores, horarios_aulas)
            if aulas_con_disponibilidad:
                for aula in aulas_con_disponibilidad:
                    aula_nombre = aula['Aula:']
                    aula_edificio = next(
                        (a['edificio'] for a in aulas if a['nombre'] == aula_nombre), None)
                    if aula_edificio == edificio_predefinido:
                        sugerencias.append({
                            'Carrera': materia.get('carrera', ''),
                            'Codigo Guarani': materia.get('codigo_guarani', ''),
                            'Materia': materia.get('nombre', ''),
                            'Profesor': profesor_nombre,
                            'Edificio': aula_edificio,
                            'Aula': aula['Aula:'],
                            'Dia': aula['Dia:'],
                            'Hora inicio': aula['Hora Inicio:'],
                            'Hora fin': aula['Hora Fin:']
                        })
                        break  # Salir del loop de aulas, pasar al siguiente profesor
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


if __name__ == "__main__":
    main()

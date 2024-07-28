import csv
import ast
import sys
from collections import defaultdict

# Configurar la salida estándar a UTF-8
sys.stdout.reconfigure(encoding='ISO-8859-1')


def leer_aulas(archivo):
    aulas = []
    try:
        with open(archivo, newline='', encoding='ISO-8859-1') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Saltar encabezado
            for row in reader:
                if len(row) >= 4:
                    try:
                        capacidad = int(row[1]) if row[1].isdigit() else 0
                        disponibilidad = ast.literal_eval(
                            row[3]) if row[3] else []
                        aulas.append({
                            'nombre': row[0],
                            'capacidad': capacidad,
                            'edificio': row[2],
                            'disponibilidad': disponibilidad
                        })
                    except (ValueError, SyntaxError):
                        print(f"Error: Valor inválido en la fila {
                              row} del archivo {archivo}")
                else:
                    print(f"Error: Fila con menos de 4 columnas en {archivo}")
    except FileNotFoundError:
        print(f"Error: Archivo {archivo} no encontrado")
    except csv.Error as e:
        print(f"Error: Error al leer el archivo {archivo}: {e}")
    return aulas


def leer_materias(archivo):
    materias = []
    try:
        with open(archivo, newline='', encoding='ISO-8859-1') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Saltar encabezado
            for row in reader:
                if len(row) >= 12:  # Ajustado para asegurar que todas las columnas requeridas estén presentes
                    # Convertir lista de diccionarios a un string con nombres de profesores
                    profesores = row[11]
                    try:
                        profesores_lista = ast.literal_eval(profesores)
                        if isinstance(profesores_lista, list):
                            profesores = ', '.join(
                                f"{prof['nombre']} {prof['apellido']}" for prof in profesores_lista)
                    except (ValueError, SyntaxError):
                        pass
                    materias.append({
                        'codigo_guarani': row[0],
                        'nombre': row[1],
                        'carrera': row[2],
                        'anio': row[3],
                        'cuatrimestre': row[4],
                        'profesores': profesores,
                        'alumnos_esperados': int(row[7]) if row[7].isdigit() else 0,
                        'horas_frente_curso': int(row[10]) if row[10].isdigit() else 0,
                        'comisiones': row[8]
                    })
                else:
                    print(f"Error: Fila con menos de 12 columnas en {archivo}")
    except FileNotFoundError:
        print(f"Error: Archivo {archivo} no encontrado")
    except csv.Error as e:
        print(f"Error: Error al leer el archivo {archivo}: {e}")
    return materias


def leer_profesores(archivo):
    profesores = []
    try:
        with open(archivo, newline='', encoding='ISO-8859-1') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Saltar encabezado
            for row in reader:
                if len(row) >= 8:  # Ajustado para asegurar que todas las columnas requeridas estén presentes
                    profes_dict = {
                        'nombre': row[2],
                        'apellido': row[1],
                        'condicion': row[3],
                        'materias': row[7],
                        'horarios_disponibles': row[6],
                    }
                    profesores.append(profes_dict)
                else:
                    print(f"Error: Fila con menos de 8 columnas en {archivo}")
    except FileNotFoundError:
        print(f"Error: Archivo {archivo} no encontrado")
    except csv.Error as e:
        print(f"Error: Error al leer el archivo {archivo}: {e}")
    return profesores


def organizar_horarios_profesores(profesores):
    horarios_disponibles = defaultdict(lambda: defaultdict(list))

    for profesor in profesores:
        profesor_horarios = defaultdict(list)
        str_copia_horarios_disponibles = profesor['horarios_disponibles']

        for bloque_dia_horas in str_copia_horarios_disponibles.split(';'):
            dia_horas = bloque_dia_horas.strip().split(',')  # Separar por comas
            dia = dia_horas[0].strip()  # Obtener el día

            for horas_rango in dia_horas[1:]:
                horas = horas_rango.strip().split('-')
                if len(horas) == 2:
                    hora_inicio = int(horas[0].strip())
                    hora_fin = int(horas[1].strip())
                    profesor_horarios[dia].append(f"{hora_inicio}-{hora_fin}")

        nombre_completo = f"{profesor['nombre']} {profesor['apellido']}"
        horarios_disponibles[nombre_completo] = profesor_horarios

    return horarios_disponibles


def organizar_horarios_aulas(aulas):
    horarios_disponibles_aulas = defaultdict(lambda: defaultdict(list))

    for aula in aulas:
        disponibilidad_aula = aula['disponibilidad']

        for dia, disponibilidad_horaria in disponibilidad_aula.items():
            for hora, disponible in enumerate(disponibilidad_horaria, start=8):
                if disponible:
                    horarios_disponibles_aulas[aula['nombre']][dia].append(
                        # f"{hora}-{hora + 1}")
                        f"{hora}")

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
        # print(f"No se encontraron horarios para el profesor {profesor_nombre}")
        return

    # print(f"Profesor: {profesor_nombre}")
    # print("Horario de profesores:")
    for dia, horas_disponibles in horarios_profesores[profesor_nombre].items():
        # print(f"Día: {dia}")
        horas_separadas = separar_horas(horas_disponibles)
        for hora_inicio, hora_fin in horas_separadas:
            # print(f"\t- Inicio: {hora_inicio}, Fin: {hora_fin}")

            for aula, aulas_disponibles in horarios_aulas.items():
                for dia, horas in aulas_disponibles.items():
                    horas_aula = [int(horas)
                                  for horas in aulas_disponibles[dia]]
                    # print(f"\t\t- Aulas disponibles: {horas_aula}")
                    if hora_inicio in horas_aula:
                        # print("Hora inicio", hora_inicio, "encontrada")
                        if hora_fin in horas_aula:
                            # print("Hora fin", hora_fin, "encontrada")
                            # print(hora_inicio, hora_fin)
                            # print(
                            #     f"\t\t- Dia: {dia}, Aula disponible: {aula}, Inicio: {hora_inicio}, Fin: {hora_fin}")
                            aula_con_disponibilidad.append({
                                "Aula:": aula, "Dia:": dia, "Hora Inicio:": hora_inicio, "Hora Fin:": hora_fin})
    return aula_con_disponibilidad


def asignar_materias_a_aulas(materias):
    sugestion = []
    for materia in materias:
        prosefores_separados = separar_profesores(materia['profesores'])
        # print(materia['nombre'], prosefores_separados)
        for profesor_nombre in prosefores_separados:
            aula_con_disponibilidad = verificar_disponibilidad(
                profesor_nombre, horarios_profesores, horarios_aulas)
            if aula_con_disponibilidad:
                # print(f"{materia['nombre']}:")
                for aula in aula_con_disponibilidad:
                    sugestion.append({
                        'Materia': materia['nombre'], 'Profesor': profesor_nombre, 'Aula': aula['Aula:'], 'Dia': aula['Dia:'], 'Hora inicio': aula['Hora Inicio:'], 'Hora fin': aula['Hora Fin:']})
                    # print(f"\tAula: {aula['Aula:']}, Dia: {aula['Dia:']}, Hora Inicio: {
                    #     aula['Hora Inicio:']}, Hora Fin: {aula['Hora Fin:']}")
            else:
                print(f"{materia['nombre']} | No hay aulas disponibles")
    return sugestion


def escribir_sugestiones(sugestiones, archivo):
    with open(archivo, 'w', newline='', encoding='ISO-8859-1') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Materia', 'Profesor', 'Aula',
                        'Dia', 'Hora inicio', 'Hora fin'])
        for sugestion in sugestiones:
            writer.writerow([sugestion['Materia'], sugestion['Profesor'],
                            sugestion['Aula'], sugestion['Dia'], sugestion['Hora inicio'], sugestion['Hora fin']])


def asignar_sugestiones_automatico(sugestiones, horarios_aulas):
    # Ordenar sugerencias por "alumnos esperados" en orden descendente
    sugerencias_ordenadas = sorted(sugestiones, key=lambda x: x.get(
        'alumnos_esperados', 0), reverse=True)
    print(sugerencias_ordenadas)

    # Crear copias de las aulas disponibles
    aulas_disponibles_copia = defaultdict(lambda: defaultdict(list))
    for aula, dias in horarios_aulas.items():
        for dia, horas in dias.items():
            aulas_disponibles_copia[aula][dia] = list(horas)

    asignadas = []
    no_asignadas = []

    for sugerencia in sugerencias_ordenadas:
        materia = sugerencia['Materia']
        profesor = sugerencia['Profesor']
        dia = sugerencia['Dia']
        hora_inicio = sugerencia['Hora inicio']
        hora_fin = sugerencia['Hora fin']

        aula_asignada = None

        for aula, dias in aulas_disponibles_copia.items():
            if dia in dias:
                horas_disponibles = dias[dia]
                if hora_inicio in horas_disponibles and hora_fin in horas_disponibles:
                    aula_asignada = aula
                    # Eliminar las horas ocupadas de la copia
                    aulas_disponibles_copia[aula][dia].remove(hora_inicio)
                    aulas_disponibles_copia[aula][dia].remove(hora_fin)
                    break

        if aula_asignada:
            asignadas.append({
                'Materia': materia,
                'Profesor': profesor,
                'Aula': aula_asignada,
                'Dia': dia,
                'Hora inicio': hora_inicio,
                'Hora fin': hora_fin
            })
        else:
            no_asignadas.append(sugerencia)

    return asignadas, no_asignadas


# Leer los archivos
aulas = leer_aulas('Aulas.csv')
materias = leer_materias('Materias.csv')
profesores = leer_profesores('Profesores.csv')

# Procesar horarios disponibles por día para cada profesor
horarios_profesores = organizar_horarios_profesores(profesores)

# Procesar o devolver los horarios organizados almacenados en horarios_disponibles_aulas
horarios_aulas = organizar_horarios_aulas(aulas)

# Imprime todo lo obtenido en el codigo

# Aulas
# for aula in horarios_aulas:
#     print(f"\nAula: {aula}")
#     for dia, horas in horarios_aulas[aula].items():
#         print(f"  {dia}: {', '.join(horas)}")

# Profesores
# for profesor in horarios_profesores:
#     print(f"\nProfesor: {profesor}")
#     for dia, horas in horarios_profesores[profesor].items():
#         print(f"  {dia}: {', '.join(horas)}")

# Materias
# for materia in materias:
#     print(f"\nMateria: {materia['nombre']}, Profesor: {materia['profesores']}")

# # Asignaciones
# print("Asignaciones realizadas:")
# for asignacion in asignaciones:
#     print(f"Materia: {asignacion['materia']}, Aula: {asignacion['aula']}, Día: {
#           asignacion['dia']}, Hora: {asignacion['hora']}, Profesor: {asignacion['profesor']}")

# # Imprimir horario del profesor específico
# profesor_nombre = "CATERINA LAMPERTI"
# if profesor_nombre in horarios_profesores:
#     print(f"Profesor: {profesor_nombre}")
#     print("Horario de profesores:")
#     for dia, horas_disponibles in horarios_profesores[profesor_nombre].items():
#         print(f"Día: {dia}")
#         for hora_rango in horas_disponibles:
#             print(f"\t- {hora_rango}")
# else:
#     print(f"No se encontraron horarios para el profesor {profesor_nombre}")

# # Imprimir horario de aulas
# print("\nHorario de aulas:")
# for aula, aulas_disponibles in horarios_aulas.items():
#     print(f"Aula: {aula}")
#     for dia, horas in aulas_disponibles.items():
#         print(f"\t{dia}: {', '.join(horas)}")

# disponibilidad_profe = verificar_disponibilidad(
#     "CATERINA LAMPERTI", horarios_profesores, horarios_aulas)
# print("Disponibilidad profe: ")
# for aula in disponibilidad_profe:
#     print(aula)

# test_asignar = asignar_materias_a_aulas(materias)
# for asignacion in test_asignar:
#     print(f"{asignacion['Materia']} | {asignacion['Profesor']} | {asignacion['Aula']} | {
#           asignacion['Dia']} | {asignacion['Hora inicio']} | {asignacion['Hora fin']}")

# escribir_sugestiones(asignar_materias_a_aulas(materias), 'sugerencias.csv')
# asignar_sugestiones_automatico(asignar_materias_a_aulas, horarios_aulas)

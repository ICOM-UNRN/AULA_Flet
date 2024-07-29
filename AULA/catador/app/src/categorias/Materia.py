# categorias/materia.py

class Materia:
    def __init__(self, codigo_guarani, nombre, año, cuatrimestre, taxonomia, horas_semanales, alumnos_esperados, comisiones, tipo_clase, horas_frente_curso, carrera, profesores):
        self.codigo_guarani = codigo_guarani
        self.carrera = carrera
        self.nombre = nombre
        self.año = año
        self.cuatrimestre = cuatrimestre
        self.taxonomia = taxonomia
        self.horas_semanales = horas_semanales
        self.alumnos_esperados = alumnos_esperados
        self.comisiones = comisiones
        self.tipo_clase = tipo_clase
        self.horas_frente_curso = horas_frente_curso
        self.profesores = profesores

    def __str__(self):
        profesores_str = ", ".join([f"{profesor['apellido']} {profesor['nombre']} ({
                                   profesor['categoria']})" for profesor in self.profesores])
        return f"Materia: {self.nombre} ({self.codigo_guarani}), Carrera: {self.carrera}, Año: {self.año}, Cuatrimestre: {self.cuatrimestre}, Profesores: {profesores_str}"

    def to_dict(self):
        return {
            "codigo_guarani": self.codigo_guarani,
            "nombre": self.nombre,
            "carrera": self.carrera,
            "año": self.año,
            "cuatrimestre": self.cuatrimestre,
            "taxonomia": self.taxonomia,
            "horas_semanales": self.horas_semanales,
            "alumnos_esperados": self.alumnos_esperados,
            "comisiones": self.comisiones,
            "tipo_clase": self.tipo_clase,
            "horas_frente_curso": self.horas_frente_curso,
            "profesores": self.profesores
        }

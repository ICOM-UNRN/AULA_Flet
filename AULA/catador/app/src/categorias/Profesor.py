# Profesor.py

class Profesor:
    def __init__(self, dni, apellido, nombre, condicion, categoria, dedicacion, materias, horarios_disponibles):
        self.dni = dni
        self.apellido = apellido
        self.nombre = nombre
        self.condicion = condicion
        self.categoria = categoria
        self.dedicacion = dedicacion
        self.materias = materias
        self.horarios_disponibles = horarios_disponibles

    def __str__(self):
        return f"Profesor: {self.apellido} {self.nombre} (DNI: {self.dni}), Horarios disponibles: {self.horarios_disponibles}"

    def to_dict(self):
        return {
            "dni": self.dni,
            "apellido": self.apellido,
            "nombre": self.nombre,
            "condicion": self.condicion,
            "categoria": self.categoria,
            "dedicacion": self.dedicacion,
            "materias": self.materias,
            "horarios_disponibles": self.horarios_disponibles
        }

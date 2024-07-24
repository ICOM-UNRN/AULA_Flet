class Carrera:
    def __init__(self, nombre, años, materias, edificio_preferido):
        self.nombre = nombre
        self.años = años
        self.materias = materias
        self.edificio_preferido = edificio_preferido

    def __str__(self):
        return f"Carrera: {self.nombre}, Duración: {self.años} años, Materias: {', '.join([materia.nombre for materia in self.materias])}, Edificio preferido: {self.edificio_preferido}"

    def agregar_materia(self, materia):
        self.materias.append(materia)

    def eliminar_materia(self, materia):
        if materia in self.materias:
            self.materias.remove(materia)
        else:
            print(f"La materia {
                  materia.nombre} no pertenece a la carrera {self.nombre}")

    def ver_materias(self):
        for materia in self.materias:
            print(f"- {materia}")

    def guardar_csv(self, filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(
                ["Nombre", "Años", "Materias", "Edificio preferido"])
            writer.writerow([self.nombre, self.años, ','.join(
                [materia.nombre for materia in self.materias]), self.edificio_preferido])

    def guardar_json(self, filename):
        data = {
            "nombre": self.nombre,
            "años": self.años,
            "materias": [materia.to_dict() for materia in self.materias],
            "edificio_preferido": self.edificio_preferido
        }
        with open(filename, 'w') as json_file:
            json.dump(data, json_file)

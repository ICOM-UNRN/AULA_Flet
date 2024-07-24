from categorias.Aula import Aula
import csv
import json


class Edificio:
    def __init__(self, nombre):
        self.nombre = nombre
        self.pisos = {}

    def agregar_piso(self, nombre_piso, numero_aulas, ocupancia_maxima):
        aulas = [Aula(f"{nombre_piso}-{i+1}", ocupancia_maxima, self.nombre)
                 # Pasar self.nombre como el argumento edificio
                 for i in range(numero_aulas)]
        self.pisos[nombre_piso] = aulas

    def mostrar_disponibilidad(self):
        for piso, aulas in self.pisos.items():
            print(f"Disponibilidad en el piso {piso}:")
            for aula in aulas:
                print(f"Aula {aula.nombre}:")
                for dia, horarios in aula.disponibilidad.items():
                    print(f"    {dia}: {horarios}")
                print()

    def guardar_aulas_csv(self, filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            for aulas in self.pisos.values():
                for aula in aulas:
                    aula.to_csv(writer)

    def guardar_aulas_json(self, filename):
        data = {"aulas": []}
        for aulas in self.pisos.values():
            for aula in aulas:
                data["aulas"].append(aula.to_json())
        with open(filename, 'w') as json_file:
            json.dump(data, json_file)

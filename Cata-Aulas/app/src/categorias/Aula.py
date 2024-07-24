import csv
import json


class Aula:
    def __init__(self, nombre, ocupancia_maxima, edificio):
        self.nombre = nombre
        self.ocupancia_maxima = ocupancia_maxima
        self.edificio = edificio
        self.disponibilidad = {
            'Lunes': [True] * 15,   # 8am - 10pm (22h)
            'Martes': [True] * 15,
            'Miércoles': [True] * 15,
            'Jueves': [True] * 15,
            'Viernes': [True] * 15
        }

    def reservar_horario(self, dia, hora):
        if self.disponibilidad[dia][hora - 8]:
            self.disponibilidad[dia][hora - 8] = False
            print(f"Horario reservado en {
                  self.nombre} el día {dia} a las {hora}:00")
        else:
            print(f"El horario en {self.nombre} el día {
                  dia} a las {hora}:00 ya está ocupado.")

    def liberar_horario(self, dia, hora):
        if not self.disponibilidad[dia][hora - 8]:
            self.disponibilidad[dia][hora - 8] = True
            print(f"Horario liberado en {
                  self.nombre} el día {dia} a las {hora}:00")
        else:
            print(f"El horario en {self.nombre} el día {
                  dia} a las {hora}:00 ya está disponible.")

    def to_csv(self, csv_writer):
        csv_writer.writerow(
            [self.nombre, self.ocupancia_maxima, self.edificio, self.disponibilidad])

    def to_json(self):
        return {
            "nombre": self.nombre,
            "ocupancia_maxima": self.ocupancia_maxima,
            "edificio": self.edificio,
            "disponibilidad": self.disponibilidad
        }

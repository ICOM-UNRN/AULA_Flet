import subprocess
from categorias.Edificio import Edificio
import os
import shutil


def mover_archivos_a_carpeta(carpeta_destino):
    # Crear la carpeta si no existe
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)
        print(f"Carpeta '{carpeta_destino}' creada.")
    else:
        print(f"Carpeta '{carpeta_destino}' ya existe.")

    # Obtener la lista de archivos en el directorio actual
    archivos = os.listdir('.')

    # Mover archivos CSV y JSON a la carpeta destino
    for archivo in archivos:
        if archivo.endswith('.csv') or archivo.endswith('.json'):
            ruta_origen = os.path.join('.', archivo)
            ruta_destino = os.path.join(carpeta_destino, archivo)
            shutil.move(ruta_origen, ruta_destino)
            print(f"Archivo '{archivo}' movido a '{carpeta_destino}'.")


def main():
    try:
        # Ejecutar leerExcel.py usando subprocess
        subprocess.run(["python", "app/src/leerExcel2.py"], check=True)

        # Crear el edificio
        edificio = Edificio("Anasagasti II")

        # Agregar pisos y aulas
        edificio.agregar_piso("Segundo Piso", 4, 30)
        edificio.agregar_piso("Tercer Piso", 4, 30)
        edificio.agregar_piso("PB", 2, 20)

        # Mostrar disponibilidad
        # edificio.mostrar_disponibilidad()

        # Guardar la información en CSV y JSON
        edificio.guardar_aulas_csv("aulas.csv")
        edificio.guardar_aulas_json("aulas.json")

        # Corre el programa de asignación de materias
        subprocess.run(["python", "app/src/asignacion6.py"], check=True)

        # Llamar a la función para mover los archivos
        mover_archivos_a_carpeta('archivos generados')

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

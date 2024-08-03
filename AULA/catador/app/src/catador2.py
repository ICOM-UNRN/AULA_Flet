from . import leerExcel2
import sys
import os

sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../../../..')))


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


def main(ruta_archivo):
    try:
        leerExcel2.leer_excel(ruta_archivo)

        # Llamar a la función para mover los archivos
        mover_archivos_a_carpeta('AULA/archivos_generados')

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # Cambia esto por la ruta real del archivo
    ruta_archivo = "ruta/al/archivo.xlsx"
    main(ruta_archivo)

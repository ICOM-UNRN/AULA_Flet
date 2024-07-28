import psycopg2
import sys
import subprocess
import os

# Datos de conexión a PostgreSQL
POSTGRES_HOST = "ep-super-mouse-a4hq4rqf-pooler.us-east-1.aws.neon.tech"
POSTGRES_PORT = 5432  # Suponiendo el puerto predeterminado
POSTGRES_USUARIO = "default"
POSTGRES_CONTRASEÑA = "vseaL4xSbR3Q"
BASE_DE_DATOS = "verceldb"

# Configurar la salida estándar a UTF-8
sys.stdout.reconfigure(encoding='UTF-8')

try:
    # Ejecutar main.py usando subprocess
    current_dir = os.path.dirname(os.path.abspath(__file__))
    main_script = os.path.join(current_dir, 'main.py')

    subprocess.run(["python", main_script], check=True)

    # Conectar a la base de datos PostgreSQL
    conexion = psycopg2.connect(host=POSTGRES_HOST, port=POSTGRES_PORT,
                                user=POSTGRES_USUARIO, password=POSTGRES_CONTRASEÑA, database=BASE_DE_DATOS)
    print("¡Conectado a la base de datos PostgreSQL!")

    from AULA.api.asignacion.asignacion import Asignacion

    asignacion = Asignacion(conexion)

    # Ejemplos de uso de la clase Asignacion
    # Obtener todas las asignaciones
    asignaciones = asignacion.get_asignaciones()
    print("Asignaciones:", asignaciones)

    # Insertar una nueva asignación (ejemplo)
    nueva_asignacion = asignacion.insert_asignacion(
        'Aula 101', 'Lunes', '08:00', '10:00', 'Matemáticas')
    print("Nueva asignación insertada:", nueva_asignacion)

    # Cerrar la conexión
    conexion.close()
    print("Conexión a PostgreSQL cerrada")

except (Exception, psycopg2.Error) as error:
    print("Error al conectar con PostgreSQL", error)

finally:
    if conexion:
        conexion.close()
        print("Conexión a PostgreSQL cerrada")

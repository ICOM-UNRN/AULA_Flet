import psycopg2
import sys
import subprocess
import os
from api.asignacion.asignacion import Asignacion
from api.materia.materia import Materia
from api.aula.aula import Aula
from api.edificio.edificio import Edificio
from api.profesor.profesor import Profesor

# Datos de conexión a PostgreSQL
POSTGRES_HOST = "ep-super-mouse-a4hq4rqf-pooler.us-east-1.aws.neon.tech"
POSTGRES_PORT = 5432  # Suponiendo el puerto predeterminado
POSTGRES_USUARIO = "default"
POSTGRES_CONTRASEÑA = "vseaL4xSbR3Q"
BASE_DE_DATOS = "verceldb"

# Conectar a la base de datos PostgreSQL
conexion = psycopg2.connect(host=POSTGRES_HOST, port=POSTGRES_PORT,
                            user=POSTGRES_USUARIO, password=POSTGRES_CONTRASEÑA, database=BASE_DE_DATOS)

# Configurar la salida estándar a UTF-8
sys.stdout.reconfigure(encoding='UTF-8')

try:
    # Ejecutar main.py usando subprocess
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # main_script = os.path.join(os.path.dirname(
    #     'AULA/catador/app/src/'), 'catador.py')

    # subprocess.run(["python", main_script], check=True)

    print("¡Conectado a la base de datos PostgreSQL!")

    # Conexion y obtencion de datos db
    asignacion = Asignacion(conexion)
    materia = Materia(conexion)
    profesor = Profesor(conexion)
    edificio = Edificio(conexion)
    aula = Aula(conexion)

    asignaciones = asignacion.get_asignaciones()
    materias = materia.get_materias()
    profesores = profesor.get_profesores()
    edificios = edificio.get_edificios()
    aulas = aula.get_aulas()

    print("Asignaciones:", asignaciones)
    # print("Materias:", materias)
    # print("Profesores:", profesores)
    print("Edificios:", edificios)
    print("Aulas:", aulas)

    # Cerrar la conexión
    conexion.close()
    print("Conexión a PostgreSQL cerrada")

except (Exception, psycopg2.Error) as error:
    print("Error al conectar con PostgreSQL", error)

finally:
    if conexion:
        conexion.close()
        print("Conexión a PostgreSQL cerrada")

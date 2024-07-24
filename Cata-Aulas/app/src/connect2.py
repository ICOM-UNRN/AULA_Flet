import psycopg2
import sys

POSTGRES_HOST = "ep-super-mouse-a4hq4rqf-pooler.us-east-1.aws.neon.tech"
POSTGRES_PORT = 5432  # Suponiendo el puerto predeterminado
POSTGRES_USUARIO = "default"
POSTGRES_CONTRASEÑA = "vseaL4xSbR3Q"
BASE_DE_DATOS = "verceldb"

# Configurar la salida estándar a UTF-8
sys.stdout.reconfigure(encoding='UTF-8')

try:
    conexion = psycopg2.connect(host=POSTGRES_HOST, port=POSTGRES_PORT,
                                user=POSTGRES_USUARIO, password=POSTGRES_CONTRASEÑA, database=BASE_DE_DATOS)
    print("¡Conectado a la base de datos PostgreSQL!")

    cursor = conexion.cursor()
    print("Cursor abierto")

    cursor.execute("SELECT version()")
    version = cursor.fetchone()
    print("Version de PostgreSQL:", version[0])

    cursor.close()
    print("Cursor cerrado")

    cursor = None
    print("Cursor reiniciado")


except (Exception, psycopg2.Error) as error:
    print("Error al conectar con PostgreSQL", error)

finally:
    if conexion:
        conexion.close()
        print("Conexión a PostgreSQL cerrada")

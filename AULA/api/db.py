"""
Archivo para realizar distintas acciones sobre
la conexion de la base de datos.

Por ejemplo: Conectarse o cerrar la conexion
"""
import os
import psycopg2
from dotenv import load_dotenv, dotenv_values 
# loading variables from .env file
load_dotenv() 

def connect_to_db():
    """
    Funcion para conectarse con la base de datos seteada
    en las variables de entorno.
    """
    db_host = os.getenv("POSTGRES_HOST")
    db_pass = os.getenv("POSTGRES_PASSWORD")
    db_name = os.getenv("POSTGRES_DATABASE")
    db_user = os.getenv("POSTGRES_USER")
    conn = psycopg2.connect(dbname=db_name,
        user=db_user,
        password=db_pass,
        host=db_host,
        port=5432
    )

    return conn

def close_connection(conn):
    """
    Funcion para cerrar la base de datos.
    
    Args:
        conn: Conexion de la base de datos. Objeto de la clase psycopg2
    """

    try:
        conn.close()
    except Exception as e:
        raise e

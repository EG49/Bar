import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "database": "bar_db",
    "user": "evans",
    "password": "Clave34*",
    "port": 5432
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT"),
            sslmode="prefer"
        )
        cursor = conn.cursor()
        cursor.execute('SET search_path TO "employee-evaluation-system", public;')
        conn.commit()
        cursor.close()
        return conn
    except Exception as e:
        print("Error de conexion:", e)
        return None

def setup_database():
    conn = get_connection()
    if not conn:
        print("No se pudo conectar a la base de datos.")
        return False
    try:
        cur = conn.cursor()
        cur.execute('CREATE SCHEMA IF NOT EXISTS "employee-evaluation-system";')
        cur.execute('SET search_path TO "employee-evaluation-system", public;')
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS areas (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) UNIQUE NOT NULL
            );
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS empleados (
                codigo VARCHAR(20) PRIMARY KEY,
                nombres VARCHAR(100) NOT NULL,
                apellidos VARCHAR(100) NOT NULL,
                correo VARCHAR(150) NOT NULL,
                telefono VARCHAR(20) NOT NULL,
                estado VARCHAR(20) NOT NULL CHECK (estado IN ('Activo', 'Inactivo')),
                fecha_ingreso DATE NOT NULL,
                area_id INTEGER REFERENCES areas(id) ON DELETE SET NULL
            );
        """)
        conn.commit()
        
        cur.execute("SELECT COUNT(*) FROM areas;")
        if cur.fetchone()[0] == 0:
            areas = [
                ("Atencion al Cliente",),
                ("Ventas",),
                ("Soporte Tecnico",),
                ("Calidad y Monitoreo",),
                ("Operaciones Financieras",)
            ]
            cur.executemany("INSERT INTO areas (nombre) VALUES (%s);", areas)
            conn.commit()
            print("Areas agregadas.")
            
        cur.close()
        conn.close()
        print("Base de datos lista.")
        return True
    except Exception as e:
        print("Error al armar la BD:", e)
        if conn:
            conn.rollback()
            conn.close()
        return False

if __name__ == "__main__":
    setup_database()
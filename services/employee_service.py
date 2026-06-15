from database.connection import get_connection

def obtener_areas():
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, nombre FROM areas ORDER BY nombre;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        print("Error al obtener areas:", e)
        return []

def crear_empleado(emp):
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO empleados (codigo, nombres, apellidos, correo, telefono, estado, fecha_ingreso, area_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """, (emp.codigo, emp.nombres, emp.apellidos, emp.correo, emp.telefono, emp.estado, emp.fecha_ingreso, emp.area_id))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print("Error al crear empleado:", e)
        conn.rollback()
        conn.close()
        return False

def obtener_empleados():
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT e.codigo, e.nombres, e.apellidos, e.correo, e.telefono, e.estado, e.fecha_ingreso, a.nombre, e.area_id
            FROM empleados e
            LEFT JOIN areas a ON e.area_id = a.id
            ORDER BY e.codigo;
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        print("Error al obtener empleados:", e)
        return []

def buscar_empleados(criterio):
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        query = """
            SELECT e.codigo, e.nombres, e.apellidos, e.correo, e.telefono, e.estado, e.fecha_ingreso, a.nombre, e.area_id
            FROM empleados e
            LEFT JOIN areas a ON e.area_id = a.id
            WHERE e.codigo ILIKE %s OR e.nombres ILIKE %s OR e.apellidos ILIKE %s OR a.nombre ILIKE %s
            ORDER BY e.codigo;
        """
        criterio_like = f"%{criterio}%"
        cur.execute(query, (criterio_like, criterio_like, criterio_like, criterio_like))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        print("Error al buscar empleados:", e)
        return []

def actualizar_empleado(emp):
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE empleados
            SET nombres = %s, apellidos = %s, correo = %s, telefono = %s, estado = %s, fecha_ingreso = %s, area_id = %s
            WHERE codigo = %s;
        """, (emp.nombres, emp.apellidos, emp.correo, emp.telefono, emp.estado, emp.fecha_ingreso, emp.area_id, emp.codigo))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print("Error al actualizar empleado:", e)
        conn.rollback()
        conn.close()
        return False

def eliminar_empleado(codigo):
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM empleados WHERE codigo = %s;", (codigo,))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print("Error al eliminar empleado:", e)
        conn.rollback()
        conn.close()
        return False

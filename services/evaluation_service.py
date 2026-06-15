from database.connection import get_connection

class EvaluationService:

    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def get_years(self):
        self.cursor.execute("""
            SELECT DISTINCT EXTRACT(YEAR FROM created_at)
            FROM evaluaciones
            WHERE created_at IS NOT NULL
            ORDER BY 1 DESC
        """)
        return [str(int(row[0])) for row in self.cursor.fetchall()]

    def get_employees_by_period(self, year, month):
        self.cursor.execute("""
            SELECT DISTINCT e.codigo, e.nombres, e.apellidos
            FROM evaluaciones ev
            INNER JOIN empleados e ON e.codigo = ev.codigo_empleado
            WHERE EXTRACT(YEAR FROM ev.created_at) = %s
            AND EXTRACT(MONTH FROM ev.created_at) = %s
            ORDER BY e.codigo
        """, (year, month))
        return self.cursor.fetchall()

    def get_employee_evaluations(self, codigo, year, month):
        self.cursor.execute("""
            SELECT e.created_at, hc.tipo_evaluacion, e.total_puntos
            FROM evaluaciones e
            INNER JOIN historial_cargas hc ON hc.id = e.id_historial_carga
            WHERE e.codigo_empleado = %s
            AND EXTRACT(YEAR FROM e.created_at) = %s
            AND EXTRACT(MONTH FROM e.created_at) = %s
            ORDER BY e.created_at ASC
        """, (codigo, year, month))
        return self.cursor.fetchall()

    def calculate_average(self, codigo, year, month):
        self.cursor.execute("""
            SELECT AVG(total_puntos)
            FROM evaluaciones
            WHERE codigo_empleado = %s
            AND EXTRACT(YEAR FROM created_at) = %s
            AND EXTRACT(MONTH FROM created_at) = %s
        """, (codigo, year, month))

        result = self.cursor.fetchone()

        if result and result[0]:
            return float(result[0])

        return 0

    def save_performance_evaluation(self, codigo, promedio, comentario, year, month):
        self.cursor.execute("""
            INSERT INTO evaluacion_desempeno
            (codigo_empleado, promedio_total, comentario, anio, mes)
            VALUES (%s, %s, %s, %s, %s)
        """, (codigo, promedio, comentario, year, month))

        self.conn.commit()

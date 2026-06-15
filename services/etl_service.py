import os
import pandas as pd

from datetime import datetime

from database.connection import get_connection


def process_excel(
    file_path,
    tipo_evaluacion
):

    # ==================================
    # LEER EXCEL
    # ==================================
    df = pd.read_excel(file_path)

    # ==================================
    # LIMPIAR COLUMNAS
    # ==================================
    df.columns = (
        df.columns
        .str.strip()
        .str.replace("\n", " ")
        .str.replace("  ", " ")
    )

    # ==================================
    # CONVERTIR NaN -> None
    # ==================================
    df = df.where(
        pd.notnull(df),
        None
    )

    # ==================================
    # DATOS ARCHIVO
    # ==================================
    file_name = os.path.basename(
        file_path
    )

    total_registros = len(df)

    # ==================================
    # CONEXIÓN BD
    # ==================================
    conn = get_connection()

    cursor = conn.cursor()

    try:

        # ==================================
        # FECHA ACTUAL LIMPIA
        # ==================================
        current_date = datetime.now().replace(
            microsecond=0
        )

        # ==================================
        # INSERTAR HISTORIAL
        # ==================================
        cursor.execute("""
            INSERT INTO historial_cargas (
                nombre_archivo,
                estado,
                registros_procesados,
                fecha_carga,
                tipo_evaluacion
            )
            VALUES (%s,%s,%s,%s,%s)
            RETURNING id
        """, (
            file_name,
            "Éxito",
            total_registros,
            current_date,
            tipo_evaluacion
        ))

        id_historial_carga = (
            cursor.fetchone()[0]
        )

        # ==================================
        # RECORRER FILAS EXCEL
        # ==================================
        for index, row in df.iterrows():

            # ==================================
            # CÓDIGO EMPLEADO
            # ==================================
            codigo_empleado = str(
                row["Codigo de Empleado"]
            ).strip()

            # ==================================
            # VALIDAR EMPLEADO
            # ==================================
            cursor.execute("""
                SELECT codigo
                FROM empleados
                WHERE codigo = %s
            """, (
                codigo_empleado,
            ))

            empleado = cursor.fetchone()

            # ==================================
            # EMPLEADO NO EXISTE
            # ==================================
            if not empleado:

                print(
                    f"Empleado no encontrado: "
                    f"{codigo_empleado}"
                )

                continue

            codigo_empleado = empleado[0]

            # ==================================
            # FECHAS
            # ==================================
            fecha_inicio = row[
                "Hora de inicio"
            ]

            fecha_fin = row[
                "Hora de finalización"
            ]

            fecha_publicacion = row[
                "Hora de publicación de la calificación"
            ]

            # ==================================
            # LIMPIAR FECHAS
            # ==================================
            if pd.isna(fecha_inicio):
                fecha_inicio = None

            if pd.isna(fecha_fin):
                fecha_fin = None

            if pd.isna(fecha_publicacion):
                fecha_publicacion = None

            # ==================================
            # OTROS CAMPOS
            # ==================================
            correo = row[
                "Correo electrónico"
            ]

            nombre = row[
                "Nombre"
            ]

            comentario_general = row[
                "Comentarios del cuestionario"
            ]

            total_puntos = row[
                "Total de puntos"
            ]

            if pd.isna(total_puntos):
                total_puntos = 0

            # ==================================
            # INSERTAR EVALUACIÓN
            # ==================================
            cursor.execute("""
                INSERT INTO evaluaciones (
                    id_historial_carga,
                    codigo_empleado,
                    fecha_inicio,
                    fecha_fin,
                    correo,
                    nombre_evaluado,
                    total_puntos,
                    comentario_general,
                    fecha_publicacion
                )
                VALUES (
                    %s,%s,%s,%s,%s,%s,%s,%s,%s
                )
                RETURNING id
            """, (
                id_historial_carga,
                codigo_empleado,
                fecha_inicio,
                fecha_fin,
                correo,
                nombre,
                total_puntos,
                comentario_general,
                fecha_publicacion
            ))

            evaluacion_id = (
                cursor.fetchone()[0]
            )

            # ==================================
            # INSERTAR RESPUESTAS
            # ==================================
            for i in range(1, 11):

                respuesta = row.get(
                    f"Pregunta{i}"
                )

                puntaje = row.get(
                    f"Puntos: Pregunta{i}"
                )

                comentario = row.get(
                    f"Comentarios: Pregunta{i}"
                )

                # ==================================
                # LIMPIAR NaN
                # ==================================
                if pd.isna(respuesta):
                    respuesta = None

                if pd.isna(puntaje):
                    puntaje = 0

                if pd.isna(comentario):
                    comentario = None

                # ==================================
                # INSERTAR RESPUESTA
                # ==================================
                cursor.execute("""
                    INSERT INTO respuestas_evaluacion (
                        evaluacion_id,
                        numero_pregunta,
                        respuesta,
                        puntaje,
                        comentario
                    )
                    VALUES (%s,%s,%s,%s,%s)
                """, (
                    evaluacion_id,
                    i,
                    respuesta,
                    puntaje,
                    comentario
                ))

        # ==================================
        # CONFIRMAR TRANSACCIÓN
        # ==================================
        conn.commit()

        print(
            "ETL completado correctamente"
        )

    except Exception as e:

        conn.rollback()

        print(
            "Error ETL:",
            e
        )

        raise e

    finally:

        cursor.close()

        conn.close()


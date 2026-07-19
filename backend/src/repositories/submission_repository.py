from db import get_connection


def create(student_id, task_id, answer):
    """Inserta una entrega. La tabla entregas tiene una restriccion
    UNIQUE(estudiante_id, tarea_id) que garantiza a nivel de base de datos
    que un estudiante no pueda entregar dos veces la misma tarea, incluso
    ante condiciones de carrera entre distintos nodos de la aplicacion."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO entregas (estudiante_id, tarea_id, respuesta, entregado_en) '
            'VALUES (%s, %s, %s, NOW())',
            (student_id, task_id, answer)
        )
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        return new_id
    finally:
        conn.close()


def find_by_student_and_task(student_id, task_id):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            'SELECT id, estudiante_id AS student_id, tarea_id AS task_id, '
            'respuesta AS answer, entregado_en AS submitted_at '
            'FROM entregas WHERE estudiante_id = %s AND tarea_id = %s LIMIT 1',
            (student_id, task_id)
        )
        row = cursor.fetchone()
        cursor.close()
        return row
    finally:
        conn.close()


def find_all_by_student(student_id):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            'SELECT e.id, e.tarea_id AS task_id, e.respuesta AS answer, '
            '       e.entregado_en AS submitted_at, '
            '       t.titulo AS task_title, t.codigo AS task_code '
            'FROM entregas e '
            'INNER JOIN tareas t ON t.id = e.tarea_id '
            'WHERE e.estudiante_id = %s '
            'ORDER BY e.entregado_en DESC',
            (student_id,)
        )
        rows = cursor.fetchall()
        cursor.close()
        return rows
    finally:
        conn.close()

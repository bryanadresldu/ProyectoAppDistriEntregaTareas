from db import get_connection


def find_all():
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            'SELECT id, titulo AS title, codigo AS code, '
            'descripcion AS description, fecha_limite AS deadline '
            'FROM tareas ORDER BY fecha_limite ASC'
        )
        rows = cursor.fetchall()
        cursor.close()
        return rows
    finally:
        conn.close()


def find_by_id(task_id):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            'SELECT id, titulo AS title, codigo AS code, '
            'descripcion AS description, fecha_limite AS deadline '
            'FROM tareas WHERE id = %s LIMIT 1',
            (task_id,)
        )
        row = cursor.fetchone()
        cursor.close()
        return row
    finally:
        conn.close()


def create(title, code, description, deadline, created_by):
    """Crea una tarea nueva. Solo debe invocarse desde el flujo de
    docente (ver services/task_service.py, protegido por
    @role_required('teacher'))."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO tareas (titulo, codigo, descripcion, fecha_limite, creado_por) '
            'VALUES (%s, %s, %s, %s, %s)',
            (title, code, description, deadline, created_by)
        )
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        return find_by_id(new_id)
    finally:
        conn.close()
